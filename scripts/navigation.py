"""Bind each visible HTML link to its clickable PDF area and intended destination."""
from hashlib import sha256
from html import escape, unescape
from html.parser import HTMLParser
import math
import re
import unicodedata
from urllib.parse import unquote
from contents import pdf_names

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
HELPERS = re.compile(r'<div hidden aria-hidden="true" data-ae-navigation-index="1">.*?</div>', re.S)


def compact(text):
    text = unicodedata.normalize('NFKC', text).replace('\u00ad', '').replace('\u200b', '')
    return ''.join(text.split())


class LinkModel(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.links, self.targets, self.ids, self.duplicates = [], [], {}, set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        ident = attrs.get('id')
        if ident:
            if ident in self.ids:
                self.duplicates.append(ident)
            self.ids.add(ident)
        hidden = ('hidden' in attrs or attrs.get('aria-hidden') == 'true'
                  or 'display:none' in attrs.get('style', '').replace(' ', '')
                  or any(n['hidden'] for n in self.stack))
        node = {'tag': tag, 'attrs': attrs, 'text': '', 'hidden': hidden}
        if tag not in VOID:
            self.stack.append(node)

    def handle_data(self, data):
        for node in self.stack:
            if node['tag'] == 'a' or node['attrs'].get('id'):
                node['text'] += data

    def handle_endtag(self, tag):
        index = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i]['tag'] == tag), None)
        if index is None:
            return
        nodes, self.stack = self.stack[index:], self.stack[:index]
        for node in reversed(nodes):
            attrs, text = node['attrs'], re.sub(r'\s+', ' ', node['text']).strip()
            ident = attrs.get('id')
            if ident and node['tag'] in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'caption', 'figcaption'):
                self.targets[ident] = text
            if node['tag'] == 'a' and attrs.get('href', '').startswith('#') and not node['hidden']:
                self.links.append({'source': ident, 'target': unquote(attrs['href'][1:]), 'label': text})


def instrument_html(html):
    """Add nonvisual source identities; hidden references make Chrome retain their PDF names."""
    html = HELPERS.sub('', html)
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    sequence = 0

    def identify(match):
        nonlocal sequence
        tag = match[0]
        if not re.search(r'\shref=[\'\"]#', tag) or re.search(r'\sid=', tag):
            return tag
        while True:
            sequence += 1
            ident = f'ae-link-{sequence:05d}'
            if ident not in ids:
                break
        ids.add(ident)
        return tag[:-1] + f' id="{ident}">'

    html = re.sub(r'<a\b[^>]*>', identify, html)
    model = LinkModel()
    model.feed(html)
    references = ''.join(f'<a style="display:none" href="#{escape(link["source"], quote=True)}" '
                         'aria-hidden="true"></a>' for link in model.links)
    index = '<div hidden aria-hidden="true" data-ae-navigation-index="1">' + references + '</div>'
    if '</body>' not in html:
        raise ValueError('HTML completo é obrigatório para preparar a navegação PDF')
    return html.replace('</body>', index + '\n</body>', 1)


def required_edges(entries, questions, include_theory=True, theory_label='Retomar a teoria'):
    edges = [{'source': 'toc-' + e['target'], 'target': e['target'], 'role': 'toc',
              'label': e['number'] + ' ' + e['title']} for e in entries]
    for q in questions:
        ident = q['id'].lower()
        edges += [{'source': f'nav-{ident}-answer', 'target': 'res-' + ident,
                   'role': 'answer', 'label': 'Ir ao gabarito comentado'},
                  {'source': f'nav-res-{ident}-back', 'target': ident,
                   'role': 'back', 'label': 'Voltar à questão'}]
        if include_theory:
            edges.append({'source': f'nav-res-{ident}-theory', 'target': q['theory'],
                          'role': 'theory', 'label': theory_label})
    return edges


def link_plan(html, required, pages=None):
    model = LinkModel()
    model.feed(html)
    errors = [f'Âncora duplicada: {ident}' for ident in model.duplicates]
    by_source = {link['source']: link for link in model.links}
    for link in model.links:
        if not link['source']:
            errors.append('Link interno sem identidade de origem')
        if link['target'] not in model.ids:
            errors.append(f'Destino HTML ausente: {link["target"]}')
    for edge in required:
        actual = by_source.get(edge['source'])
        if not actual:
            errors.append(f'Link obrigatório ausente: {edge["source"]}')
            continue
        if actual['target'] != edge['target']:
            errors.append(f'Rota incorreta: {edge["source"]} → {actual["target"]}; esperado {edge["target"]}')
        label = edge['label']
        if edge['role'] == 'toc' and pages is not None:
            if edge['target'] not in pages:
                errors.append(f'Página do sumário ausente: {edge["target"]}')
            else:
                label += str(pages[edge['target']])
        if compact(actual['label']) != compact(label):
            errors.append(f'Rótulo ou página de sumário incorreto: {edge["source"]}')
        actual['role'] = edge['role']
    if errors:
        raise ValueError('\n'.join(errors))
    return {'version': 1, 'links': [{**link, 'role': link.get('role', 'reference')} for link in model.links],
            'targets': model.targets, 'toc_pages': pages or {}}


def _point(doc, name):
    import pymupdf as fitz
    page = name.get('page', -1)
    if not 0 <= page < len(doc) or not isinstance(name.get('to'), (tuple, list)):
        raise ValueError('Destino PDF sem página ou posição válida')
    point = fitz.Point(name['to']) * doc[page].transformation_matrix
    if not all(math.isfinite(x) for x in point):
        raise ValueError('Destino PDF com coordenada não finita')
    if not (-1 <= point.x <= doc[page].rect.width + 1 and -1 <= point.y <= doc[page].rect.height + 1):
        raise ValueError('Destino PDF com posição fora da página')
    return page, point


def audit_pdf_links(path, plan):
    import pymupdf as fitz
    errors, checks, claimed = [], [], set()
    with fitz.open(path) as doc:
        names = pdf_names(doc)
        links = [(i, link) for i, page in enumerate(doc) for link in page.get_links()
                 if link['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED)]
        # Chrome's named destinations omit the CSS print margin. Derive the translation
        # from a unique visible TOC label, independently of its target, rather than hardcode it.
        offset = None
        for edge in plan['links']:
            if edge['role'] != 'toc' or edge['source'] not in names:
                continue
            page, point = _point(doc, names[edge['source']])
            matches = [link for i, link in links if i == page
                       and compact(doc[i].get_textbox(link['from'])) == compact(edge['label'])]
            if len(matches) == 1:
                offset = fitz.Point(matches[0]['from'].x0 - point.x, matches[0]['from'].y0 - point.y)
                break
        if offset is None:
            return {'errors': ['Não foi possível localizar uma área clicável do sumário'], 'checked': [],
                    'internal_annotations': len(links), 'passed': False}

        def destination_matches(link, target):
            expected_page, expected_point = _point(doc, names[target])
            if link.get('page') != expected_page:
                return False
            if link.get('nameddest') and unquote(link['nameddest']) != target:
                return False
            point = fitz.Point(link.get('to', (-1, -1)))
            if link.get('nameddest'):
                point = point * doc[expected_page].transformation_matrix
            return abs(point - expected_point) <= 1

        positions = {}
        for edge in plan['links']:
            source, target = edge['source'], edge['target']
            if source not in names or target not in names:
                errors.append(f'Origem/destino PDF ausente: {source} → {target}')
                continue
            try:
                page, point = _point(doc, names[source])
                point += offset
                positions[source] = (page, point)
                candidates = [link for i, link in links if i == page
                              and (link['from'] + (-1, -1, 1, 1)).contains(point)]
                if not candidates:
                    # For a wrapped <a>, Chrome names the corner of its union box:
                    # the first line's y and the continuation's leftmost x. That
                    # corner can be blank, so require a matching prefix AND tail.
                    label = compact(edge['label'])
                    for i, candidate in links:
                        if i != page or abs(candidate['from'].y0 - point.y) > 2:
                            continue
                        prefix = compact(doc[page].get_textbox(candidate['from']))
                        if not prefix or not label.startswith(prefix) or prefix == label:
                            continue
                        tails = [tail for j, tail in links if j == page
                                 and 0 < tail['from'].y0 - point.y <= 72
                                 and abs(tail['from'].x0 - point.x) <= 2
                                 and compact(doc[j].get_textbox(tail['from'])) in label[len(prefix):]
                                 and compact(doc[j].get_textbox(tail['from']))
                                 and destination_matches(tail, target)]
                        if tails:
                            candidates.append(candidate)
                candidates.sort(key=lambda link: abs(link['from'].x0 - point.x) + abs(link['from'].y0 - point.y))
                if not candidates:
                    errors.append(f'Link sem área clicável: {source}')
                    continue
                link = candidates[0]
                visible = compact(doc[page].get_textbox(link['from']))
                intended = compact(edge['label'])
                if intended and (not visible or not (intended in visible or intended.startswith(visible))):
                    errors.append(f'Área clicável não corresponde ao rótulo: {source}')
                if not destination_matches(link, target):
                    errors.append(f'Clique PDF incorreto: {source} → {target}')
                claimed.add((page, link['xref']))
                checks.append({'source': source, 'target': target, 'role': edge['role'],
                               'source_page': page + 1, 'target_page': names[target]['page'] + 1,
                               'click_rect': list(link['from']), 'click_rects': [list(link['from'])]})
            except (ValueError, KeyError) as error:
                errors.append(f'{source}: {error}')

        # Wrapped inline links can have several annotations. Every remaining fragment
        # must retain the same intended destination and belong to the nearby source label.
        for page, link in links:
            if (page, link['xref']) in claimed:
                continue
            fragment = compact(doc[page].get_textbox(link['from']))
            matched = False
            for edge in plan['links']:
                if edge['source'] not in positions or edge['target'] not in names:
                    continue
                first_page, point = positions[edge['source']]
                if first_page == page and -1 <= link['from'].y0 - point.y <= 72:
                    if fragment and fragment in compact(edge['label']) and destination_matches(link, edge['target']):
                        matched = True
                        claimed.add((page, link['xref']))
                        for check in checks:
                            if check['source'] == edge['source']:
                                check['click_rects'].append(list(link['from']))
                                break
                        break
            if not matched:
                errors.append(f'Anotação interna sem correspondência: página {page + 1}, xref {link["xref"]}')

        # A named anchor must actually land near its intended visible heading/label.
        for target in {edge['target'] for edge in plan['links']}:
            if target not in names:
                continue
            expected_text = plan['targets'].get(target)
            try:
                page, point = _point(doc, names[target])
            except ValueError as error:
                errors.append(f'{target}: {error}')
                continue
            physical = point + offset
            if expected_text:
                lines = [line for block in doc[page].get_text('dict')['blocks'] for line in block.get('lines', [])]
                nearby = [line for line in lines if physical.y - 3 <= line['bbox'][1] <= physical.y + 80]
                beginnings = [i for i, line in enumerate(nearby) if line['bbox'][1] <= physical.y + 32]
                found = any(compact(expected_text) in compact(''.join(span['text'] for line in nearby[i:i+4]
                            for span in line['spans'])) for i in beginnings)
                if not found:
                    errors.append(f'Destino não coincide com o título/texto esperado: {target}')
        for target, number in plan.get('toc_pages', {}).items():
            if target not in names or names[target]['page'] + 1 != number:
                errors.append(f'Página do sumário diverge do PDF: {target}')
        return {'passed': not errors, 'errors': errors, 'checked': checks,
                'internal_annotations': len(links), 'coordinate_offset_pt': list(offset),
                'checked_click_areas': len(claimed),
                'pdf_sha256': sha256(path.read_bytes()).hexdigest()}


def navigation_manifest(html_path, pdf_path, required, pages):
    html = html_path.read_text(encoding='utf-8')
    plan = link_plan(html, required, pages)
    audit = audit_pdf_links(pdf_path, plan)
    return {'version': 1, 'html_file': html_path.name, 'pdf_file': pdf_path.name,
            'html_sha256': sha256(html_path.read_bytes()).hexdigest(),
            'pdf_sha256': sha256(pdf_path.read_bytes()).hexdigest(), 'plan': plan, 'audit': audit}
