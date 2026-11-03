"""Build the fixed editorial/navigation sample; not a general material generator."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
from integrity import validate_questions, validate_navigation
from contents import contents_entries, render_contents, pdf_contents_pages

ROOT = Path(__file__).resolve().parents[1]


def compose(questions):
    parts = [(ROOT / 'examples/redes/capitulo.md').read_text(encoding='utf-8'),
             '\n# Pratique {#pratica}\n\nTodas as questões abaixo são autorais, sem atribuição a uma banca.\n']
    for q in questions:
        anchor = q['id'].lower()
        parts.append(f"\n## {q['id']} {{#{anchor}}}\n\n**AUTORAL · {q['dificuldade'].replace('estimada-', '')} (estimativa editorial).**\n\n{q['enunciado']}\n")
        for key, value in q['alternativas'].items():
            parts.append(f'\n**{key}.** {value}\n')
        parts.append(f'\n[Ir ao gabarito comentado](#res-{anchor})\n')
    parts.append('\n# Gabarito comentado {#gabarito}\n')
    for q in questions:
        anchor = q['id'].lower()
        parts.append(f"\n## Resolução {q['id']} {{#res-{anchor}}}\n\n**Resposta: {q['resposta']}.**\n")
        for key, comment in q['comentarios'].items():
            parts.append(f'\n**{key}.** {comment}\n')
        parts.append(f'\n[Retomar o conceito](#cap-001) · [Voltar à questão](#{anchor})\n')
    parts.append('''
# Referências e controle {#referencias}

Texto e esquema originais produzidos com assistência de IA. Conferência técnica em 03/11/2026. A amostra demonstra estrutura e navegação; não representa um edital ou perfil de banca. Não há questões reais incorporadas.

Referências técnicas consultadas: [Juniper — Layer 2 Forwarding Tables](https://www.juniper.net/documentation/us/en/software/junos/multicast-l2/topics/topic-map/layer-2-forwarding-tables.html) e [Cisco — Configure MAC](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr2-fwd/cdp-lldp-mac-udld/cdp-lldp-mac-udld-configuration-guide/configure-mac.pdf). Nenhuma figura desses documentos foi reproduzida.

Versão editorial 0.1.0. As situações são simplificadas, com uma VLAN, aprendizagem dinâmica habilitada e portas em encaminhamento, sem filtros adicionais. Não generalizar para toda configuração de switch.
''')
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', action='store_true')
    args = parser.parse_args()
    if not shutil.which('pandoc'):
        parser.error('Pandoc não encontrado. Instale antes de gerar a amostra.')
    questions = json.loads((ROOT / 'examples/redes/questoes.json').read_text(encoding='utf-8'))
    errors = validate_questions(questions)
    if errors:
        raise SystemExit('\n'.join(errors))
    if any(q['origem'] != 'AUTORAL' for q in questions):
        raise SystemExit('Este demonstrador aceita apenas a amostra autoral. Itens reais exigem outro fluxo editorial.')
    build = ROOT / 'build'
    build.mkdir(exist_ok=True)
    source = build / 'amostra.md'
    source.write_text(compose(questions), encoding='utf-8')
    output = build / 'amostra.html'
    subprocess.run(['pandoc', str(source), '--standalone', '--toc', '--toc-depth=2',
                    '--embed-resources', '--resource-path=' + str(ROOT / 'examples/redes'),
                    '--css=' + str(ROOT / 'styles/apostila.css'),
                    '--metadata=title:Ateliê de Estudos — amostra editorial',
                    '--metadata=lang:pt-BR', '--number-sections',
                    '--metadata=toc-title:Sumário', '-o', str(output)], check=True)
    original_html = output.read_text(encoding='utf-8')
    entries = contents_entries(original_html)
    output.write_text(render_contents(original_html, entries), encoding='utf-8')
    errors = validate_navigation(output.read_text(encoding='utf-8'), questions)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'HTML gerado e navegação validada: {output}')
    if args.pdf:
        browser = shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
        if not browser:
            parser.error('Chromium/Chrome não encontrado; HTML gerado, PDF pendente.')
        pdf = build / 'amostra.pdf'
        try:
            from playwright.sync_api import sync_playwright, Error
            import pymupdf as fitz
        except ImportError:
            parser.error('Para PDF: instale requirements-pdf.txt. O HTML já foi gerado.')
        try:
            with sync_playwright() as playwright:
                # Static, self-contained sample: no file:// navigation or external requests.
                instance = playwright.chromium.launch(executable_path=browser, headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage'], timeout=30000)
                try:
                    page = instance.new_page()
                    page.route('**/*', lambda route: route.abort())
                    pages = {}
                    footer = ('<div style="font:9px Arial;color:#64727b;width:100%;margin:0 20mm;'
                              'display:flex;justify-content:space-between;border-top:1px solid #d6dde0;'
                              'padding-top:7px"><span>Ateliê de Estudos</span>'
                              '<span class="pageNumber"></span></div>')
                    for _ in range(3):
                        output.write_text(render_contents(original_html, entries, pages), encoding='utf-8')
                        page.set_content(output.read_text(encoding='utf-8'), wait_until='load', timeout=15000)
                        page.pdf(path=str(pdf), format='A4', print_background=True,
                                 prefer_css_page_size=True, display_header_footer=True,
                                 header_template='<span></span>', footer_template=footer)
                        resolved_pages = pdf_contents_pages(pdf, entries)
                        if pages == resolved_pages:
                            break
                        pages = resolved_pages
                    else:
                        raise SystemExit('Paginação do sumário não estabilizou; confira o PDF.')
                    (build / 'toc-pages.json').write_text(
                        json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
                finally:
                    instance.close()
        except Error:
            raise SystemExit('Falha do Chromium/Playwright. HTML preservado; exportação PDF pendente.')
        if not pdf.is_file() or pdf.stat().st_size < 1000:
            raise SystemExit('Falha ao exportar PDF; confira Chromium e o HTML gerado.')
        print(f'PDF gerado: {pdf}. {len(entries)} entradas do sumário com paginação conferida.')


if __name__ == '__main__':
    main()
