"""Intake and contest-scope contracts; research and image reading belong to the agent."""
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import urlparse

from contracts import require_schema

ROOT = Path(__file__).resolve().parents[1]
STAGES = ('identificacao', 'edital', 'retificacoes', 'banca', 'provas-alvo',
          'provas-relacionadas', 'fontes-conteudo', 'acervo')


def instruction_inventory(root=ROOT):
    root = Path(root)
    paths = {root/'AGENTS.md', root/'README.md'}
    for folder, pattern in [('.agents/skills', '*/SKILL.md'), ('docs', '*.md'),
                            ('templates', '*'), ('schemas', '*'), ('references', '*.md')]:
        paths.update(p for p in (root/folder).glob(pattern) if p.is_file())
    return [{'arquivo': p.relative_to(root).as_posix(), 'sha256': sha256(p.read_bytes()).hexdigest(),
             'lido_em': None} for p in sorted(paths)]


def initial_request(ident, text, kind, origin='texto', image=None):
    value = {'id': ident, 'tipo': kind, 'entrada': {'origem': origin, 'texto': text, 'imagem': image},
             'concurso': dict(orgao=None, cargo=None, especialidade=None, ano=None, banca=None),
             'edital': dict(url=None, versao=None, sha256=None, conferido_em=None,
                            retificacoes_verificadas=False),
             'escopo': dict(tipo='concurso', descricao='Todo o programa aplicável ao cargo; confirmar identidade.', selecao=[]),
             'programa': [], 'pesquisa': [dict(etapa=s, estado='pendente', relato='Pesquisar e registrar evidências.',
                                             evidencias=[]) for s in STAGES],
             'contexto': instruction_inventory(), 'lacunas': ['Identidade, edital e pesquisa ainda não conferidos.']}
    require_schema(value, 'pedido.schema.json', 'pedido')
    return value


def attachment_path(folder, relative):
    path = (folder/relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(folder.resolve()) or not path.is_file():
        raise ValueError('Imagem ausente ou fora da pasta do pedido')
    return path


def read_request(path):
    path = Path(path).resolve()
    value = json.loads(path.read_text(encoding='utf-8'))
    require_schema(value, 'pedido.schema.json', path.name)
    image = value['entrada']['imagem']
    if value['entrada']['origem'] != 'texto' and image is None:
        raise ValueError('Pedido por foto/print exige a imagem original')
    if not value['entrada']['texto'].strip() and image is None:
        raise ValueError('Pedido sem texto ou imagem')
    if image:
        original = attachment_path(path.parent, image['arquivo'])
        if sha256(original.read_bytes()).hexdigest() != image['sha256']:
            raise ValueError('Hash da imagem diverge do pedido')
    return value


def request_errors(value, inventory=None):
    errors = []
    require_schema(value, 'pedido.schema.json', 'pedido')
    contest, notice = value['concurso'], value['edital']
    for field in ('orgao', 'cargo', 'ano', 'banca'):
        if not str(contest[field] or '').strip():
            errors.append('Identidade do concurso não confirmada: ' + field)
    if (urlparse(notice['url'] or '').scheme != 'https' or not urlparse(notice['url'] or '').hostname
            or not notice['versao'] or not notice['sha256'] or not notice['conferido_em']):
        errors.append('Edital oficial sem URL HTTPS, versão, data ou hash')
    if not notice['retificacoes_verificadas']:
        errors.append('Retificações ainda não conferidas')
    image = value['entrada']['imagem']
    if image and (not image['conferida'] or not image['transcricao'].strip()):
        errors.append('Foto/print precisa de transcrição conferida visualmente pelo agente')
    current = inventory if inventory is not None else instruction_inventory()
    read = {r['arquivo']: r for r in value['contexto']}
    if len(read) != len(value['contexto']):
        errors.append('Registro de leitura duplicado')
    for expected in current:
        actual = read.get(expected['arquivo'], {})
        if actual.get('sha256') != expected['sha256'] or not actual.get('lido_em'):
            errors.append('Instrução não lida ou alterada: ' + expected['arquivo'])
    stages = {r['etapa']: r for r in value['pesquisa']}
    if len(stages) != len(value['pesquisa']):
        errors.append('Etapa de pesquisa duplicada')
    for name in STAGES:
        row = stages.get(name)
        if not row or row['estado'] == 'pendente':
            errors.append('Pesquisa pendente: ' + name)
            continue
        if name in ('identificacao', 'edital', 'banca', 'fontes-conteudo') and row['estado'] != 'verificado':
            errors.append('Pesquisa essencial não confirmada: ' + name)
        if name in ('retificacoes', 'provas-alvo', 'provas-relacionadas') and row['estado'] not in ('verificado', 'nao-localizado'):
            errors.append('Pesquisa precisa de consulta registrada: ' + name)
        if row['estado'] != 'nao-aplicavel' and not row['evidencias']:
            errors.append('Pesquisa sem evidência: ' + name)
        if name in ('identificacao', 'edital', 'retificacoes', 'banca') and not any(
                e['oficial'] and urlparse(e['referencia']).scheme == 'https' and urlparse(e['referencia']).hostname
                for e in row['evidencias']):
            errors.append('Pesquisa sem referência oficial HTTPS: ' + name)
        if row['estado'] in ('nao-localizado', 'nao-publicado') and not value['lacunas']:
            errors.append('Resultado não localizado precisa de limitação explícita: ' + name)
    ids = [item['id'] for item in value['programa']]
    selected = set(value['escopo']['selecao'])
    if len(ids) != len(set(ids)):
        errors.append('Item do programa duplicado')
    if not ids or not selected or not selected <= set(ids):
        errors.append('Programa/seleção ausente ou com item inexistente')
    if value['escopo']['tipo'] == 'concurso' and selected != set(ids):
        errors.append('Pedido de concurso completo não pode reduzir a seleção do programa')
    return errors


def scope_errors(data, kind, final=False):
    request = data.get('request')
    if request is None:
        return ['Entrega final de concurso exige pedido vinculado'] if final else []
    errors = request_errors(request) if final else []
    if request['tipo'] != kind:
        errors.append('Formato solicitado diverge do formato de saída')
    selected = set(request['escopo']['selecao'])
    rows = {}
    mapped_questions = set()
    permitted_objectives = set()
    for row in data['coverage']:
        ident = row.get('edital_id')
        if not ident and row['status'] in ('pre-requisito', 'complemento') and not row['questions']:
            permitted_objectives.update(row['objectives'])
            continue
        if not ident or ident not in selected:
            errors.append('Cobertura fora do escopo solicitado: ' + str(ident or row['edital_item']))
            continue
        if ident in rows:
            errors.append('Cobertura duplicada: ' + ident)
        rows[ident] = row
        permitted_objectives.update(row['objectives'])
        expected = next((item['texto'] for item in request['programa'] if item['id'] == ident), None)
        if row['edital_item'] != expected:
            errors.append('Texto da cobertura diverge do programa: ' + ident)
        mapped_questions.update(row['questions'])
        if final and (row['status'] != 'completo' or not row['objectives'] or not row['questions']):
            errors.append('Item ainda sem conteúdo/prática completos: ' + ident)
    if final:
        errors += ['Item solicitado omitido: ' + ident for ident in sorted(selected - set(rows))]
        if not data['config'].get('profile'):
            errors.append('Entrega de concurso exige perfil da banca e limites da amostra')
        notice = request['edital']
        if not any(s['url'] == notice['url'] and s.get('sha256') == notice['sha256'] for s in data['sources']):
            errors.append('Edital do pedido não corresponde às fontes/hash do material')
    for question in data['questions']:
        if question['id'] not in mapped_questions:
            errors.append('Questão fora da cobertura solicitada: ' + question['id'])
        elif not any(question['id'] in row['questions'] and question['objetivo'] in row['objectives'] for row in rows.values()):
            errors.append('Questão vinculada ao objetivo errado: ' + question['id'])
    for chapter in data['config']['chapters']:
        if set(chapter['objectives']) - permitted_objectives:
            errors.append('Capítulo com objetivo fora do escopo: ' + chapter['id'])
    return errors


def require_delivery(data, kind, final=False):
    errors = scope_errors(data, kind, final)
    if errors:
        raise ValueError('\n'.join(errors))
    request = data.get('request')
    return {'status': 'final-structural-check-passed' if final else 'draft-or-reference',
            'request_id': request['id'] if request else None,
            'scope': request['escopo'] if request else None,
            'limit': 'Metadados e cobertura estrutural; pesquisa real, fidelidade ao edital e didática exigem revisão do agente.'}
