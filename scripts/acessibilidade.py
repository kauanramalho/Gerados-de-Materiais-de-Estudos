"""Measured HTML/PDF accessibility checks with explicit limits; not PDF/UA certification."""
import argparse,json,re,shutil,sys
from html import escape,unescape
from pathlib import Path
from contents import pdf_names


def svg_accessibility(html):
    """Pandoc preserves alt on inline SVG; expose it as a standard accessible name."""
    def replace(match):
        tag=match[0];label=re.search(r'\balt="([^"]+)"',tag)
        if not label or 'aria-hidden="true"' in tag or 'role="presentation"' in tag:
            return tag
        extra=''
        if not re.search(r'\brole=',tag):extra+=' role="img"'
        if not re.search(r'\baria-label(?:ledby)?=',tag):
            extra+=' aria-label="'+escape(unescape(label[1]),quote=True)+'"'
        return tag[:-1]+extra+'>'
    return re.sub(r'<svg\b[^>]*>',replace,html)


def contrast(rgb, background):
    def luminance(values):
        values=[v/255 for v in values]
        values=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in values]
        return .2126*values[0]+.7152*values[1]+.0722*values[2]
    a,b=sorted([luminance(rgb),luminance(background)])
    return (b+.05)/(a+.05)


def inspect(html_path,pdf_path):
    from playwright.sync_api import sync_playwright
    import pymupdf as fitz
    errors=[]
    with sync_playwright() as pw:
        executable=shutil.which('chromium') or shutil.which('google-chrome') or pw.chromium.executable_path
        browser=pw.chromium.launch(executable_path=executable,headless=True,args=['--no-sandbox'])
        try:
            page=browser.new_page(java_script_enabled=False)
            page.route('**/*',lambda route:route.abort())
            page.set_content(Path(html_path).read_text(encoding='utf-8'),wait_until='load',timeout=15000)
            dom=page.evaluate('''() => {
              const visible=e=>!!e.getClientRects().length && getComputedStyle(e).visibility!=="hidden";
              const rgb=s=>(s.match(/[\\d.]+/g)||[]).slice(0,3).map(Number);
              const text=[];
              for(const e of document.body.querySelectorAll('*')){
                if(!visible(e)||!Array.from(e.childNodes).some(n=>n.nodeType===3&&n.textContent.trim()))continue;
                const c=getComputedStyle(e);let p=e,b='';
                while(p){b=getComputedStyle(p).backgroundColor;if(b!=='rgba(0, 0, 0, 0)'&&b!=='transparent')break;p=p.parentElement;}
                text.push({label:e.textContent.trim().slice(0,90),foreground:rgb(c.color),background:rgb(b||'rgb(255,255,255)'),size:parseFloat(c.fontSize),bold:parseInt(c.fontWeight)>=700});
              }
              const links=Array.from(document.querySelectorAll('a[href]')).filter(visible);
              links.forEach((e,i)=>e.dataset.aeAuditIndex=i);
              return {lang:document.documentElement.lang,
                headings:Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).filter(visible).map(e=>({id:e.id,level:+e.tagName[1],text:e.textContent.trim()})),
                images:Array.from(document.querySelectorAll('img,svg')).filter(visible).map(e=>({alt:e.getAttribute('aria-label')||e.getAttribute('alt')||e.querySelector('title')?.textContent,role:e.getAttribute('role'),tag:e.tagName.toLowerCase()})),
                tables:Array.from(document.querySelectorAll('table')).filter(visible).map(e=>({headers:e.querySelectorAll('th').length,rows:e.rows.length})),
                math:Array.from(document.querySelectorAll('math')).filter(visible).map(e=>e.textContent.trim()),text,links:links.length};
            }''')
            if not dom['lang'].lower().startswith('pt'):
                errors.append('Idioma do documento não declarado como português')
            previous=0
            for h in dom['headings']:
                if previous and h['level']>previous+1:errors.append('Salto de título: '+h['text'])
                previous=h['level']
            if any(not str(i['alt'] or '').strip() and i['role']!='presentation' for i in dom['images']):
                errors.append('Imagem informativa sem descrição alternativa')
            if any(i['tag']=='svg' and i['role'] not in ('img','presentation') for i in dom['images']):
                errors.append('SVG sem papel semântico de imagem')
            if any(not t['headers'] for t in dom['tables']):errors.append('Tabela sem cabeçalho semântico')
            if any(not text for text in dom['math']):errors.append('MathML sem conteúdo textual')
            failures=[]
            for row in dom['text']:
                minimum=3 if row['size']>=24 or (row['bold'] and row['size']>=18.66) else 4.5
                ratio=contrast(row['foreground'],row['background'])
                if ratio+.01<minimum:failures.append({'text':row['label'],'ratio':round(ratio,2),'required':minimum})
            errors += ['Contraste insuficiente: '+r['text'] for r in failures]
            tabs=0
            for index in range(dom['links']):
                page.keyboard.press('Tab')
                focus=page.evaluate('''()=>{const e=document.activeElement,c=getComputedStyle(e);return {index:e.dataset.aeAuditIndex,outline:parseFloat(c.outlineWidth),style:c.outlineStyle};}''')
                if focus['index']!=str(index) or focus['outline']<2 or focus['style']=='none':
                    errors.append('Ordem de teclado/foco visível falhou no link '+str(index+1));break
                tabs+=1
        finally:browser.close()
    with fitz.open(pdf_path) as doc:
        catalog=doc.pdf_catalog()
        tagged=doc.xref_get_key(catalog,'StructTreeRoot')[0]!='null' and doc.xref_get_key(catalog,'MarkInfo')[0]!='null'
        if not tagged:errors.append('PDF sem árvore estrutural/marcação')
        names=pdf_names(doc);positions=[]
        for h in dom['headings']:
            if h['id'] in names:
                entry=names[h['id']];point=fitz.Point(entry['to'])*doc[entry['page']].transformation_matrix
                positions.append((entry['page'],point.y))
        ordered=all(a<=b for a,b in zip(positions,positions[1:]))
        if not ordered:errors.append('Ordem dos títulos do PDF diverge do HTML')
        bounds=[]
        for page_number,page in enumerate(doc):
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        if not (page.rect+(-1,-1,1,1)).contains(fitz.Rect(span['bbox'])):
                            bounds.append(page_number+1)
        if bounds:errors.append('Texto fora dos limites da página: '+str(sorted(set(bounds))))
    return dict(passed=not errors,errors=errors,html=dict(language=dom['lang'],images=len(dom['images']),tables=len(dom['tables']),
                mathml=len(dom['math']),text_contrasts=len(dom['text']),contrast_failures=failures,keyboard_links=tabs),
                pdf=dict(tagged=tagged,heading_order_checked=len(positions),heading_order=ordered,text_bounds_ok=not bounds),
                limits=['Não é certificação WCAG ou PDF/UA.','Leitor de tela real e interpretação semântica de fórmulas/tabelas exigem revisão assistiva.',
                        'Contraste medido para texto e fundo CSS dos documentos deste motor; imagens e fundos complexos exigem revisão visual.'])


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('html',type=Path);parser.add_argument('pdf',type=Path)
    parser.add_argument('--report',required=True,type=Path);args=parser.parse_args(argv)
    try:
        result=inspect(args.html,args.pdf);args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('Auditoria de acessibilidade: '+('aprovada com limites declarados'if result['passed']else'reprovada'));return 0 if result['passed']else 1
    except (ValueError,KeyError,OSError) as error:
        print('Falha na auditoria: '+str(error),file=sys.stderr);return 1


if __name__=='__main__':sys.exit(main())
