"""Format contracts and deterministic scoring; no implied equivalence to an official exam."""
from collections import Counter
from copy import deepcopy
from decimal import Decimal
import math
from pathlib import Path
import re

from contracts import require_schema


def validate_simulation(data, plan):
    require_schema(plan, 'simulado.schema.json', 'simulado')
    questions = {q['id']: q for q in data['questions']}
    if len(plan['order']) != len(questions) or set(plan['order']) != set(questions):
        raise ValueError('Ordem do simulado deve incluir cada questão exatamente uma vez')
    matrix = {r['objective']: r['count'] for r in plan['matrix']}
    if len(matrix) != len(plan['matrix']) or matrix != dict(Counter(q['objetivo'] for q in questions.values())):
        raise ValueError('Matriz do simulado diverge da distribuição das questões')
    scoring = plan['scoring']
    if not set(plan['annulled_ids']) <= set(questions) or not set(scoring['weights']) <= set(questions):
        raise ValueError('Anulação/peso aponta para questão inexistente')
    values = [scoring[k] for k in ('correct', 'wrong', 'blank')] + list(scoring['weights'].values())
    if any(not math.isfinite(v) for v in values):
        raise ValueError('Pontuação precisa de números finitos')
    for question in questions.values():
        official = question.get('fonte_original', {})
        if official.get('gabarito_status') == 'anulada' and question['id'] not in plan['annulled_ids']:
            raise ValueError('Questão oficialmente anulada deve constar do plano de anulações')
    if plan['basis']['type'] == 'oficial':
        source = next((s for s in data['sources'] if s['id'] == plan['basis']['source_id']), None)
        if not source or not source.get('sha256'):
            raise ValueError('Regra oficial exige fonte identificada e hash da evidência')
        if any(q.get('fonte_original', {}).get('gabarito_status') == 'preliminar' for q in questions.values()):
            raise ValueError('Gabarito preliminar não permite pontuação oficial definitiva')
    return plan


def score_simulation(data, responses):
    plan = validate_simulation(data, data['simulation'])
    if not isinstance(responses, dict):
        raise ValueError('Respostas devem mapear ID de questão para alternativa ou vazio')
    questions = {q['id']: q for q in data['questions']}
    if not set(responses) <= set(questions):
        raise ValueError('Resposta aponta para questão inexistente')
    rules = plan['scoring']; total = Decimal(0); maximum = Decimal(0); rows = []
    for ident in plan['order']:
        q = questions[ident]; choice = responses.get(ident)
        if choice not in ('', None) and choice not in q['alternativas']:
            raise ValueError('Alternativa inválida: '+ident)
        weight = Decimal(str(rules['weights'].get(ident, 1)))
        correct = Decimal(str(rules['correct']))*weight
        annulled = ident in plan['annulled_ids']
        if annulled and rules['annulled'] == 'exclude':
            result, points = 'anulada-excluida', Decimal(0)
        else:
            maximum += correct
            if annulled:
                result, points = 'anulada-creditada', correct
            elif choice in ('', None):
                result, points = 'branco', Decimal(str(rules['blank']))*weight
            elif choice == q['resposta']:
                result, points = 'correta', correct
            else:
                result, points = 'incorreta', Decimal(str(rules['wrong']))*weight
        total += points
        rows.append(dict(id=ident, response=choice, result=result, points=float(points)))
    return dict(points=float(total), maximum=float(maximum), percent=float(100*total/maximum) if maximum else None,
                basis=plan['basis'], rows=rows, note='Resultado de treino conforme o plano; não prevê aprovação ou desempenho futuro.')


def prepare_format(data, kind):
    if kind in ('apostila', 'caderno'):
        return data
    if kind not in ('simulado', 'revisao'):
        raise ValueError('Formato não implementado: '+kind)
    result = {**data, 'config': deepcopy(data['config'])}
    suffix = ' — Simulado' if kind == 'simulado' else ' — Revisão ativa'
    if not result['config']['title'].endswith(suffix):
        result['config']['title'] += suffix
    if kind == 'simulado':
        if not data.get('simulation'):
            raise ValueError('Simulado exige plano no manifesto')
        validate_simulation(data, data['simulation'])
    else:
        plan = data.get('revision')
        if not plan:
            raise ValueError('Revisão exige plano no manifesto')
        require_schema(plan, 'revisao.schema.json', 'revisao')
        files = {row['id']: row['file'] for row in plan['chapters']}
        if len(files) != len(plan['chapters']) or set(files) != {c['id'] for c in data['config']['chapters']}:
            raise ValueError('Revisão deve mapear cada capítulo do material')
        anchors = set(files)
        for chapter in result['config']['chapters']:
            chapter['file'] = files[chapter['id']]
            path = (data['folder']/chapter['file']).resolve()
            if not path.is_relative_to(data['folder'].resolve()) or not path.is_file():
                raise ValueError('Capítulo de revisão ausente ou fora da pasta')
            text = path.read_text(encoding='utf-8')
            if re.search(r'^# ', text, re.M):
                raise ValueError('Revisão deve começar em H2')
            anchors.update(re.findall(r'\{#([\w-]+)\}', text))
        if any(q['theory'] not in anchors for q in data['questions']):
            raise ValueError('Revisão sem destino teórico de uma questão')
    return result
