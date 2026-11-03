"""Checks for question provenance and exported HTML navigation (stdlib only)."""
from html.parser import HTMLParser
import re


def validate_questions(questions):
    errors, seen = [], set()
    required_source = {'banca', 'orgao', 'cargo', 'ano', 'caderno', 'numero',
                       'pagina', 'prova_url', 'gabarito_url', 'gabarito_status', 'conferido_em'}
    for q in questions:
        qid = q.get('id', '')
        if not re.fullmatch(r'Q-(AUT|REAL|ADP)-[0-9]{3,}', qid):
            errors.append(f'ID inválido: {qid}')
        if qid in seen:
            errors.append(f'ID duplicado: {qid}')
        seen.add(qid)
        alternatives = q.get('alternativas', {})
        if len(alternatives) < 2 or any(not str(v).strip() for v in alternatives.values()):
            errors.append(f'{qid}: alternativas insuficientes')
        if q.get('resposta') not in alternatives:
            errors.append(f'{qid}: resposta fora das alternativas')
        if set(q.get('comentarios', {})) != set(alternatives) or any(
                not str(v).strip() for v in q.get('comentarios', {}).values()):
            errors.append(f'{qid}: comentário ausente ou excedente')
        for field in ('objetivo', 'enunciado', 'dificuldade', 'formato'):
            if not q.get(field):
                errors.append(f'{qid}: campo obrigatório ausente: {field}')
        origin = q.get('origem')
        expected_prefix = {'AUTORAL': 'Q-AUT-', 'REAL': 'Q-REAL-', 'ADAPTADA': 'Q-ADP-'}
        if origin not in expected_prefix or not qid.startswith(expected_prefix.get(origin, 'INVALID')):
            errors.append(f'{qid}: origem incompatível com ID')
        if origin in ('REAL', 'ADAPTADA'):
            source = q.get('fonte_original', {})
            if not required_source <= source.keys() or any(not source.get(k) for k in required_source):
                errors.append(f'{qid}: origem real incompleta')
            if q.get('direitos') not in ('reproducao-verificada', 'somente-link'):
                errors.append(f'{qid}: direitos de terceiro não verificados')
        if origin == 'ADAPTADA' and not q.get('adaptacoes'):
            errors.append(f'{qid}: adaptações não registradas')
        if origin == 'AUTORAL' and ('fonte_original' in q or q.get('direitos') != 'original-projeto'):
            errors.append(f'{qid}: autoria ou direitos inconsistentes')
    return errors


class Navigation(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.duplicates = set(), [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            target = attrs['id']
            if target in self.ids:
                self.duplicates.append(target)
            self.ids.add(target)
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.links.append(attrs['href'][1:])


def validate_navigation(html, questions=()):
    nav = Navigation()
    nav.feed(html)
    errors = [f'Âncora duplicada: {target}' for target in nav.duplicates]
    errors += [f'Destino ausente: {target}' for target in nav.links if target not in nav.ids]
    for q in questions:
        target = q['id'].lower()
        for anchor in (target, f'res-{target}'):
            if anchor not in nav.ids or anchor not in nav.links:
                errors.append(f'Par de navegação incompleto: {anchor}')
    return errors
