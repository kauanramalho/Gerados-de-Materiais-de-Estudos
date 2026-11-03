"""Material publishing: local content, provenance, navigation and reproducible evidence."""
from datetime import datetime, timezone
from hashlib import sha256
from html import escape
import json
import platform
from pathlib import Path
import re
import shutil
import statistics
import subprocess
from urllib.parse import urlparse

from contents import contents_entries, render_contents, pdf_contents_pages
from integrity import validate_questions, validate_navigation

ROOT = Path(__file__).resolve().parents[1]


def local_path(folder, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError('Referência local deve ser um caminho relativo não vazio')
    resolved = (folder / relative).resolve()
    if not resolved.is_relative_to(folder.resolve()) or not resolved.is_file():
        raise ValueError(f'Arquivo ausente ou fora da pasta do material: {relative}')
    return resolved


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def http_url(value):
    parsed = urlparse(str(value))
    return parsed.scheme == 'https' and bool(parsed.netloc) and not parsed.username


def load_material(path):
    path = Path(path).resolve()
    folder, config = path.parent, read_json(path)
    for field in ('id', 'title', 'version', 'scope', 'chapters', 'questions', 'sources', 'figures', 'coverage'):
        if field not in config or config[field] in ('', None):
            raise ValueError(f'Manifesto sem campo: {field}')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', config['id']):
        raise ValueError('ID do material deve usar letras minúsculas, números e hífen')
    data = {key: read_json(local_path(folder, config[key]))
            for key in ('questions', 'sources', 'figures', 'coverage')}
    if not isinstance(config['chapters'], list) or not config['chapters']:
        raise ValueError('O material deve ter ao menos um capítulo')
    if any(not isinstance(value, list) or any(not isinstance(row, dict) for row in value)
           for value in data.values()):
        raise ValueError('Questões, fontes, figuras e cobertura devem ser listas de registros')
    errors = validate_questions(data['questions'])
    if errors:
        raise ValueError('\n'.join(errors))
    source_ids = [s.get('id') for s in data['sources']]
    if len(set(source_ids)) != len(source_ids) or any(not x for x in source_ids):
        raise ValueError('Fontes sem ID ou com IDs duplicados')
    for source in data['sources']:
        if not all(source.get(k) for k in ('title', 'url', 'checked_on', 'locator', 'rights')) or not http_url(source['url']):
            raise ValueError(f'Fonte incompleta: {source.get("id")}')
    chapter_ids, anchors, inputs = set(), set(), [path]
    for chapter in config['chapters']:
        if chapter['id'] in chapter_ids or not chapter.get('objectives'):
            raise ValueError('Capítulo duplicado ou sem objetivos')
        chapter_ids.add(chapter['id'])
        text_path = local_path(folder, chapter['file'])
        text = text_path.read_text(encoding='utf-8')
        if re.search(r'^# ', text, re.M):
            raise ValueError('Conteúdo de capítulo deve começar no nível H2; o publicador cria o H1')
        anchors.update(re.findall(r'\{#([\w-]+)\}', text))
        inputs.append(text_path)
    anchors.update(chapter_ids)
    declared_figures = {figure['file'] for figure in data['figures']}
    for chapter in config['chapters']:
        text = local_path(folder, chapter['file']).read_text(encoding='utf-8')
        for alternative, target in re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text):
            if not alternative.strip() or target not in declared_figures:
                raise ValueError('Imagem sem descrição ou fora do manifesto de figuras')
            local_path(folder, target)
    figure_ids = set()
    for figure in data['figures']:
        if figure['id'] in figure_ids or not all(figure.get(k) for k in ('caption', 'alt', 'rights', 'source')):
            raise ValueError('Figura duplicada ou sem metadados editoriais')
        figure_ids.add(figure['id'])
        figure_path = local_path(folder, figure['file'])
        if figure_path.suffix.lower() not in ('.svg', '.png', '.jpg', '.jpeg'):
            raise ValueError('Formato de figura não suportado')
        if figure['source'] != 'original-projeto' and figure['source'] not in source_ids:
            raise ValueError('Figura aponta para fonte inexistente')
        chapter_texts = '\n'.join(local_path(folder, c['file']).read_text(encoding='utf-8') for c in config['chapters'])
        if figure['file'] not in chapter_texts:
            raise ValueError(f'Figura sem chamada no capítulo: {figure["id"]}')
        inputs.append(figure_path)
    question_ids = {q['id'] for q in data['questions']}
    for q in data['questions']:
        if not q.get('theory') or q['theory'] not in anchors:
            raise ValueError(f'{q["id"]}: remissão teórica ausente')
        if not set(q.get('source_ids', [])) <= set(source_ids):
            raise ValueError(f'{q["id"]}: fonte desconhecida')
        if q['origem'] in ('REAL', 'ADAPTADA'):
            original = q['fonte_original']
            if not all(http_url(original[k]) for k in ('prova_url', 'gabarito_url')):
                raise ValueError(f'{q["id"]}: URL de prova/gabarito inválida')
            if original['gabarito_status'] not in ('preliminar', 'definitivo', 'retificado', 'anulada'):
                raise ValueError(f'{q["id"]}: gabarito não confirmado para publicação')
            for field in ('prova_sha256', 'gabarito_sha256'):
                if not re.fullmatch(r'[a-f0-9]{64}', original.get(field, '')):
                    raise ValueError(f'{q["id"]}: falta hash da evidência: {field}')
            if q['direitos'] == 'reproducao-verificada' and not q.get('permission_evidence'):
                raise ValueError(f'{q["id"]}: falta evidência da permissão de reprodução')
        if q['origem'] == 'ADAPTADA' and not q.get('permission_evidence'):
            raise ValueError('Item adaptado exige evidência de permissão')
    objectives = {o for c in config['chapters'] for o in c['objectives']}
    if any(q['objetivo'] not in objectives for q in data['questions']):
        raise ValueError('Questão aponta para objetivo não ensinado')
    for row in data['coverage']:
        if not row.get('edital_item') or not row.get('status'):
            raise ValueError('Matriz sem item do edital/estado de cobertura')
        if not set(row.get('objectives', [])) <= objectives or not set(row.get('questions', [])) <= question_ids:
            raise ValueError('Matriz aponta para objetivo/questão inexistente')
    mapped = {o for row in data['coverage'] for o in row.get('objectives', [])}
    if objectives - mapped:
        raise ValueError('Existem objetivos sem rastreabilidade no edital')
    inputs += [local_path(folder, config[k]) for k in ('questions', 'sources', 'figures', 'coverage')]
    if config.get('profile'):
        inputs.append(local_path(folder, config['profile']))
    if config.get('practice_context'):
        inputs.append(local_path(folder, config['practice_context']))
    return {'config': config, 'folder': folder, 'inputs': inputs, **data}


def compose_material(data, kind='apostila'):
    config, folder, questions = data['config'], data['folder'], data['questions']
    parts = ['# Como usar este material {#orientacoes}', config['scope'],
             f'**Versão {config["version"]} · Texto e questões autorais com assistência de IA.**',
             'Resolva os itens antes de abrir os comentários. Cada resolução oferece retorno à questão. '
             'As questões reais com direitos de reprodução não confirmados são oferecidas por link para a prova oficial.']
    if any(q.get('fonte_original', {}).get('gabarito_status') == 'preliminar' for q in questions):
        parts.append('> **Gabarito preliminar:** parte dos itens reais usa resposta oficial ainda preliminar. '
                     'Confira o status na página da banca antes de usar para pontuação definitiva.')
    if kind == 'apostila':
        for chapter in config['chapters']:
            parts += [f'# {chapter["title"]} {{#{chapter["id"]}}}',
                      local_path(folder, chapter['file']).read_text(encoding='utf-8')]
        if config.get('profile'):
            parts += ['# Evidência de prova e limites da amostra {#perfil-banca}',
                      local_path(folder, config['profile']).read_text(encoding='utf-8')]
    else:
        parts.append('Este caderno acompanha a apostila de mesmo título. As remissões à teoria são indicadas '
                     'pelo ID da seção da apostila; as questões e os comentários funcionam neste arquivo.')
        if config.get('practice_context'):
            parts += ['# Dados para resolver as questões {#dados-pratica}',
                      local_path(folder, config['practice_context']).read_text(encoding='utf-8')]
    for category, label, anchor in [('REAL', 'Questões reais: acesso à prova', 'questoes-reais'),
                                    ('ADAPTADA', 'Questões adaptadas', 'questoes-adaptadas'),
                                    ('AUTORAL', 'Questões autorais', 'questoes-autorais')]:
        selected = [q for q in questions if q['origem'] == category]
        if not selected:
            continue
        parts += [f'# {label} {{#{anchor}}}']
        for q in selected:
            qanchor = q['id'].lower()
            parts += ['::: {.question}', f'## {q["id"]} {{#{qanchor}}}']
            if category == 'AUTORAL':
                parts += [f'**Autoral · dificuldade {q["dificuldade"].replace("estimada-", "")} (estimativa editorial).**']
            if category != 'AUTORAL':
                source = q['fonte_original']
                parts += [f'**{category} · {source["banca"]} · {source["orgao"]} {source["ano"]} · '
                          f'{source["caderno"]}, questão {source["numero"]}, página {source["pagina"]}.**',
                          f'[Abrir questão na prova oficial]({source["prova_url"]}#page={source["pagina"]})',
                          'O texto e as alternativas originais devem ser lidos na prova. '
                          'O comentário desta apostila é produzido pelo projeto.']
            if q['direitos'] != 'somente-link':
                parts += [q['enunciado']]
                parts += [f'**{key}.** {value}' for key, value in q['alternativas'].items()]
            parts += [f'[Ir ao gabarito comentado](#res-{qanchor})', ':::']
    parts += ['# Gabarito comentado {#gabarito-comentado}']
    for q in questions:
        qanchor = q['id'].lower()
        parts += ['::: {.solution}', f'## Resolução {q["id"]} {{#res-{qanchor}}}']
        if q['origem'] == 'AUTORAL':
            parts += [f'**Resposta do projeto: {q["resposta"]}.**']
        else:
            source = q['fonte_original']
            parts += [f'**Gabarito oficial {source["gabarito_status"]}: {q["resposta"]}.** '
                      f'[Consultar gabarito]({source["gabarito_url"]}#page={source.get("gabarito_pagina",1)})']
        parts += [f'**{key}.** {value}' for key, value in q['comentarios'].items()]
        if q.get('reasoning'):
            parts += [q['reasoning']]
        if kind == 'apostila':
            parts += [f'[Retomar a teoria](#{q["theory"]}) · [Voltar à questão](#{qanchor})']
        else:
            parts += [f'Teoria na apostila: `{q["theory"]}`. [Voltar à questão](#{qanchor})']
        parts += [':::']
    parts += ['# Fontes e rastreabilidade {#fontes}',
              'A presença de uma fonte não equivale a permissão para reproduzi-la. '
              'Os esquemas são originais; os itens reais identificados como referência usam acesso externo.']
    parts += [f'- **[{s["id"]}]{{#fonte-{s["id"].lower()}}}** — [{s["title"]}]({s["url"]}). {s["locator"]}. '
              f'Conferido em {s["checked_on"]}. Uso: {s["rights"]}.' for s in data['sources']]
    table = ['| Item do edital | Objetivos | Estado e limites |', '|---|---|---|']
    table += [f'| {r["edital_item"]} | {", ".join(r["objectives"])} | '
              f'{r["status"]}: {r.get("limits", "recorte do capítulo")} |' for r in data['coverage']]
    parts += ['## Cobertura e lacunas', '\n'.join(table)]
    return '\n\n'.join(parts) + '\n'


def audit_pdf(pdf, entries, pages, questions):
    import fitz
    errors, internal, external, body_sizes = [], 0, 0, []
    with fitz.open(pdf) as document:
        destinations = document.resolve_names()
        for page in document:
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        if len(span['text']) > 80 and 'Mono' not in span['font']:
                            body_sizes.append(span['size'])
            for link in page.get_links():
                if link['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED):
                    internal += 1
                    if not 0 <= link.get('page', -1) < len(document):
                        errors.append('Link para página inexistente')
                    if link.get('nameddest') and link['nameddest'] not in destinations:
                        errors.append('Destino nomeado não resolvido')
                elif link['kind'] == fitz.LINK_URI:
                    external += 1
        for q in questions:
            for target in (q['id'].lower(), 'res-' + q['id'].lower()):
                if target not in destinations:
                    errors.append(f'Questão/resolução ausente do PDF: {target}')
        if pdf_contents_pages(pdf, entries) != pages:
            errors.append('Paginação do sumário diverge do PDF')
        median_body = round(statistics.median(body_sizes), 2) if body_sizes else None
        if median_body is not None and median_body < 10:
            errors.append('Texto longo foi reduzido abaixo do tamanho de leitura previsto')
        result = {'pages': len(document), 'internal_links': internal, 'external_links': external,
                  'toc_entries': len(entries), 'question_pairs': len(questions),
                  'long_text_median_pt': median_body, 'errors': errors}
    return result


def publish(data, output_folder, kind='apostila', pdf=False):
    config, folder = data['config'], data['folder']
    output = Path(output_folder).resolve()
    if output == folder or folder.is_relative_to(output):
        raise ValueError('Saída não pode sobrescrever a pasta de origem')
    output.mkdir(parents=True, exist_ok=True)
    if not shutil.which('pandoc'):
        raise ValueError('Pandoc não encontrado')
    source, html_path = output / f'{kind}.md', output / f'{kind}.html'
    source.write_text(compose_material(data, kind), encoding='utf-8')
    subprocess.run(['pandoc', str(source), '--from=markdown-raw_html', '--standalone', '--toc',
                    '--toc-depth=2', '--number-sections', '--embed-resources',
                    '--resource-path=' + str(folder), '--css=' + str(ROOT / 'styles/apostila.css'),
                    '--metadata=title:' + config['title'], '--metadata=lang:pt-BR',
                    '--metadata=toc-title:Sumário', '-o', str(html_path)], check=True)
    original = html_path.read_text(encoding='utf-8')
    entries = contents_entries(original)
    html_path.write_text(render_contents(original, entries), encoding='utf-8')
    errors = validate_navigation(html_path.read_text(encoding='utf-8'), data['questions'])
    if errors:
        raise ValueError('\n'.join(errors))
    report = {'material': config['id'], 'version': config['version'], 'kind': kind,
              'generated_at': datetime.now(timezone.utc).isoformat(),
              'questions': len(data['questions']), 'html_navigation': 'passed',
              'editorial_review': 'requires-recorded-review', 'files': {}, 'inputs': {}}
    report['toolchain'] = {'publisher_version': '0.2.0', 'python': platform.python_version(),
                          'pandoc': subprocess.check_output(['pandoc', '--version'], text=True).splitlines()[0],
                          'stylesheet_sha256': sha256((ROOT / 'styles/apostila.css').read_bytes()).hexdigest(),
                          'publisher_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
                          'contents_sha256': sha256((ROOT / 'scripts/contents.py').read_bytes()).hexdigest()}
    if pdf:
        try:
            import fitz
            from playwright.sync_api import sync_playwright
        except ImportError as error:
            raise ValueError('Instale requirements-pdf.txt para gerar PDF') from error
        executable = shutil.which('chromium') or shutil.which('google-chrome')
        if not executable:
            raise ValueError('Chromium/Chrome não encontrado')
        pdf_path = output / f'{kind}.pdf'
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=executable, headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage'], timeout=30000)
            try:
                page = browser.new_page(java_script_enabled=False)
                page.route('**/*', lambda route: route.abort())
                pages = {}
                for _ in range(4):
                    html_path.write_text(render_contents(original, entries, pages), encoding='utf-8')
                    page.set_content(html_path.read_text(encoding='utf-8'), wait_until='load', timeout=15000)
                    footer = ('<div style="font:9px Arial;color:#64727b;width:100%;margin:0 20mm;'
                              'display:flex;justify-content:space-between;border-top:1px solid #d6dde0;'
                              'padding-top:7px"><span>Ateliê de Estudos</span>'
                              '<span class="pageNumber"></span></div>')
                    page.pdf(path=str(pdf_path), format='A4', print_background=True,
                             prefer_css_page_size=True, display_header_footer=True,
                             header_template='<span></span>', footer_template=footer)
                    actual = pdf_contents_pages(pdf_path, entries)
                    if actual == pages:
                        break
                    pages = actual
                else:
                    raise ValueError('Paginação do sumário não estabilizou')
            finally:
                browser.close()
        report['pdf'] = audit_pdf(pdf_path, entries, pages, data['questions'])
        if report['pdf']['errors']:
            raise ValueError('\n'.join(report['pdf']['errors']))
        (output / f'{kind}-toc.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
    for path in data['inputs']:
        report['inputs'][str(path.relative_to(folder))] = sha256(path.read_bytes()).hexdigest()
    for key in ('md', 'html', 'pdf'):
        path = output / f'{kind}.{key}'
        if path.exists() and (key != 'pdf' or pdf):
            report['files'][path.name] = sha256(path.read_bytes()).hexdigest()
    (output / f'{kind}-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report
