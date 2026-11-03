"""Book-style contents generated from Pandoc headings and final PDF destinations."""
from html import escape
from html.parser import HTMLParser
import re


class ContentsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth, self.current, self.entries = 0, None, []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'ul':
            self.depth += 1
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.current = {'target': attrs['href'][1:], 'depth': self.depth, 'text': ''}

    def handle_data(self, text):
        if self.current is not None:
            self.current['text'] += text

    def handle_endtag(self, tag):
        if tag == 'a' and self.current is not None:
            text = re.sub(r'\s+', ' ', self.current.pop('text')).strip()
            match = re.fullmatch(r'(\d+(?:\.\d+)*)\s+(.+)', text)
            if not match:
                raise ValueError(f'Título de sumário sem numeração: {text}')
            self.current.update(number=match[1], title=match[2])
            self.entries.append(self.current)
            self.current = None
        if tag == 'ul':
            self.depth -= 1


TOC = re.compile(r'<nav\b[^>]*\bid="TOC"[^>]*>.*?</nav>', re.S)


def contents_entries(html):
    match = TOC.search(html)
    if not match:
        raise ValueError('Sumário do Pandoc não encontrado')
    parser = ContentsParser()
    parser.feed(match[0])
    return parser.entries


def render_contents(html, entries, pages=None):
    pages = pages or {}
    groups = []
    for entry in entries:
        if entry['depth'] == 1:
            groups.append({'entry': entry, 'children': []})
        elif entry['depth'] == 2 and groups:
            groups[-1]['children'].append(entry)
        else:
            raise ValueError('Hierarquia de sumário inválida')

    def link(entry):
        target = escape(entry['target'], quote=True)
        page = str(pages.get(entry['target'], ''))
        return (f'<a class="toc-link" href="#{target}" id="toc-{target}">'
                f'<span class="toc-number">{escape(entry["number"])}</span>'
                f'<span class="toc-label">{escape(entry["title"])}</span>'
                '<span class="toc-leader" aria-hidden="true"></span>'
                f'<span class="toc-page">{page}</span></a>')

    rows = []
    for group in groups:
        children = ''.join(f'<li>{link(e)}</li>' for e in group['children'])
        nested = f'<ol class="toc-subsections">{children}</ol>' if children else ''
        rows.append(f'<li class="toc-chapter">{link(group["entry"])}{nested}</li>')
    nav = ('<nav id="TOC" role="doc-toc" aria-labelledby="toc-title">'
           '<h2 id="toc-title">Sumário</h2>'
           '<div class="toc-column-label" aria-hidden="true">Página</div>'
           '<ol class="toc-chapters">' + ''.join(rows) + '</ol></nav>')
    return TOC.sub(lambda _: nav, html, count=1)


def pdf_contents_pages(path, entries):
    import pymupdf as fitz
    with fitz.open(path) as document:
        destinations = document.resolve_names()
        pages = {}
        for entry in entries:
            target = entry['target']
            destination = destinations.get(target, {})
            page = destination.get('page', -1)
            if not 0 <= page < len(document):
                raise ValueError(f'Destino PDF ausente: {target}')
            pages[target] = page + 1
        return pages
