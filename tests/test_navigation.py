import copy
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from contents import render_contents, pdf_contents_pages, pdf_names
from navigation import instrument_html, link_plan, required_edges, audit_pdf_links
from external_links import check_url, check_external
from audit_links import inspect_pdf


def fixture():
    entries = [{'target': target, 'number': number, 'title': title, 'depth': depth}
               for target, number, title, depth in [
                   ('theory-a', '1', 'Teoria A', 1), ('teoria-ação', '2', 'Teoria B', 1),
                   ('questions', '3', 'Questões', 1), ('q-aut-001', '3.1', 'Q-AUT-001', 2),
                   ('q-aut-002', '3.2', 'Q-AUT-002', 2), ('comments', '4', 'Comentários', 1),
                   ('res-q-aut-001', '4.1', 'Resolução Q-AUT-001', 2),
                   ('res-q-aut-002', '4.2', 'Resolução Q-AUT-002', 2)]]
    questions = [{'id': 'Q-AUT-001', 'theory': 'theory-a'}, {'id': 'Q-AUT-002', 'theory': 'teoria-ação'}]
    html = '''<!doctype html><html><head><meta charset="utf-8"><style>
    @page{size:A4;margin:20mm}body{font:11.5pt Arial}section{break-before:page}
    h1{font-size:20pt}h2{font-size:15pt}.space{height:70px}.toc-link{display:flex;gap:10px}
    .toc-leader{flex:1}.toc-subsections{margin-bottom:12px}li{margin-bottom:8px}
    </style></head><body><nav id="TOC"></nav>
    <section><h1 id="theory-a">1 Teoria A</h1><p>Primeiro conceito.</p>
    <p style="width:150px"><span style="display:inline-block;width:100px"></span><a id="wrapped-reference" href="#teoria-ação">Fonte complementar</a></p>
    <div class="space"></div>
    <h1 id="teoria-ação">2 Teoria B</h1><p>Segundo conceito na mesma página.</p></section>
    <section><h1 id="questions">3 Questões</h1>
    <h2 id="q-aut-001">3.1 Q-AUT-001</h2><p>Primeira questão.</p>
    <a id="nav-q-aut-001-answer" href="#res-q-aut-001">Ir ao gabarito comentado</a>
    <div class="space"></div><h2 id="q-aut-002">3.2 Q-AUT-002</h2><p>Segunda questão.</p>
    <a id="nav-q-aut-002-answer" href="#res-q-aut-002">Ir ao gabarito comentado</a></section>
    <section><h1 id="comments">4 Comentários</h1>
    <h2 id="res-q-aut-001">4.1 Resolução Q-AUT-001</h2><p>Primeira solução.</p>
    <a id="nav-res-q-aut-001-theory" href="#theory-a">Retomar a teoria</a> ·
    <a id="nav-res-q-aut-001-back" href="#q-aut-001">Voltar à questão</a>
    <div class="space"></div><h2 id="res-q-aut-002">4.2 Resolução Q-AUT-002</h2><p>Segunda solução.</p>
    <a id="nav-res-q-aut-002-theory" href="#teoria-ação">Retomar a teoria</a> ·
    <a id="nav-res-q-aut-002-back" href="#q-aut-002">Voltar à questão</a></section></body></html>'''
    html = instrument_html(render_contents(html, entries))
    return html, entries, required_edges(entries, questions)


def redirect(html, source, target):
    pattern = rf'(<a\b[^>]*\bid="{re.escape(source)}"[^>]*\bhref=")[^"]*'
    html, count = re.subn(pattern, lambda m: m[1] + '#' + target, html)
    assert count == 1
    return html


class HTMLNavigationTests(unittest.TestCase):
    def setUp(self):
        self.html, self.entries, self.required = fixture()

    def test_all_required_routes_have_sources_and_targets(self):
        plan = link_plan(self.html, self.required)
        self.assertEqual(len(plan['links']), 15)

    def test_swapped_existing_answer_is_rejected(self):
        bad = redirect(self.html, 'nav-q-aut-001-answer', 'res-q-aut-002')
        with self.assertRaisesRegex(ValueError, 'Rota incorreta'):
            link_plan(bad, self.required)

    def test_wrong_return_and_theory_are_rejected(self):
        for source, target in [('nav-res-q-aut-001-back', 'q-aut-002'),
                               ('nav-res-q-aut-001-theory', 'teoria-ação')]:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'Rota incorreta'):
                link_plan(redirect(self.html, source, target), self.required)

    def test_missing_button_does_not_pass_because_the_toc_links_to_the_answer(self):
        bad = re.sub(r'<a id="nav-q-aut-001-answer".*?</a>', '', self.html)
        with self.assertRaisesRegex(ValueError, 'Link obrigatório ausente'):
            link_plan(bad, self.required)

    def test_stale_toc_page_is_rejected_even_when_target_exists(self):
        pages = {e['target']: 2 for e in self.entries}
        rendered = render_contents(self.html, self.entries, pages)
        bad = rendered.replace('<span class="toc-page">2</span>', '<span class="toc-page">9</span>', 1)
        with self.assertRaisesRegex(ValueError, 'página de sumário incorreto'):
            link_plan(bad, self.required, pages)

    def test_duplicate_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Âncora duplicada'):
            link_plan(self.html.replace('</body>', '<i id="q-aut-001"></i></body>'), self.required)

    def test_hidden_index_is_not_a_second_set_of_visible_links(self):
        second = instrument_html(self.html)
        self.assertEqual(second.count('data-ae-navigation-index="1"'), 1)
        self.assertEqual(len(link_plan(second, self.required)['links']), 15)

    def test_empty_pandoc_code_line_anchors_are_not_reader_buttons(self):
        code = '<pre><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a>SELECT 1;</span></pre>'
        html = instrument_html(self.html.replace('</body>', code + '</body>'))
        self.assertEqual(len(link_plan(html, self.required)['links']), 15)


class PDFNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import pymupdf as fitz
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise unittest.SkipTest('Dependências PDF ausentes; executar no job artifacts')
        cls.fitz = fitz
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.addClassCleanup(cls.temp.cleanup)
        html, cls.entries, cls.required = fixture()
        cls.pdf, cls.html = cls.root / 'fixture.pdf', cls.root / 'fixture.html'
        with sync_playwright() as pw:
            executable = shutil.which('chromium') or shutil.which('google-chrome') or pw.chromium.executable_path
            if not Path(executable).is_file():
                raise unittest.SkipTest('Chromium ausente; executar no job artifacts')
            browser = pw.chromium.launch(executable_path=executable, headless=True, args=['--no-sandbox'])
            try:
                page = browser.new_page(java_script_enabled=False)
                pages = {}
                for _ in range(4):
                    final = render_contents(html, cls.entries, pages)
                    page.set_content(final)
                    page.pdf(path=str(cls.pdf), format='A4', prefer_css_page_size=True)
                    actual = pdf_contents_pages(cls.pdf, cls.entries)
                    if actual == pages:
                        break
                    pages = actual
                else:
                    raise AssertionError('Fixture não estabilizou')
            finally:
                browser.close()
        cls.html.write_text(final)
        cls.plan = link_plan(final, cls.required, pages)
        cls.manifest = cls.root / 'fixture-navigation.json'
        cls.manifest.write_text(json.dumps({'plan': cls.plan, 'pdf_sha256': sha256(cls.pdf.read_bytes()).hexdigest(),
                                         'html_sha256': sha256(cls.html.read_bytes()).hexdigest(),
                                         'html_file': cls.html.name, 'audit': {'passed': True}}))
        audit = audit_pdf_links(cls.pdf, cls.plan)
        if not audit['passed']:
            raise AssertionError(audit['errors'])

    def mutate(self, source, target=None, remove=False, zero_area=False, drift=0):
        edge = next(e for e in self.plan['links'] if e['source'] == source)
        result = self.root / ('mutated-' + source + '.pdf')
        with self.fitz.open(self.pdf) as doc:
            names = pdf_names(doc)
            page = doc[names[source]['page']]
            matches = [l for l in page.get_links() if l.get('nameddest') == edge['target']]
            self.assertEqual(len(matches), 1)
            link = matches[0]
            if remove:
                page.delete_link(link)
            elif zero_area:
                doc.xref_set_key(link['xref'], 'Rect', '[0 0 0 0]')
            else:
                dest = names[target or edge['target']]
                x, y = dest['to']
                value = f'[{doc.page_xref(dest["page"])} 0 R /XYZ {x} {y-drift} 0]'
                doc.xref_set_key(link['xref'], 'Dest', value)
            doc.save(result, garbage=3)
        return result

    def test_real_click_areas_and_destinations_match_the_plan(self):
        result = audit_pdf_links(self.pdf, self.plan)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(len(result['checked']), 15)

    def test_wrapped_reference_checks_every_clickable_fragment(self):
        result = audit_pdf_links(self.pdf, self.plan)
        check = next(c for c in result['checked'] if c['source'] == 'wrapped-reference')
        self.assertGreaterEqual(len(check['click_rects']), 2)
        self.assertEqual(result['checked_click_areas'], result['internal_annotations'])

    def test_wrong_existing_toc_destination_is_rejected(self):
        result = audit_pdf_links(self.mutate('toc-theory-a', 'teoria-ação'), self.plan)
        self.assertFalse(result['passed'])
        self.assertTrue(any('Clique PDF incorreto' in e for e in result['errors']))

    def test_wrong_answer_and_return_on_same_page_are_rejected(self):
        for source, target in [('nav-q-aut-001-answer', 'res-q-aut-002'),
                               ('nav-res-q-aut-001-back', 'q-aut-002')]:
            with self.subTest(source=source):
                result = audit_pdf_links(self.mutate(source, target), self.plan)
                self.assertFalse(result['passed'])
                self.assertTrue(any('Clique PDF incorreto' in e for e in result['errors']))

    def test_vertical_destination_error_on_the_correct_page_is_rejected(self):
        self.assertFalse(audit_pdf_links(self.mutate('nav-q-aut-001-answer', drift=90), self.plan)['passed'])

    def test_missing_return_and_invisible_click_area_are_rejected(self):
        for option in [{'remove': True}, {'zero_area': True}]:
            with self.subTest(option=option):
                result = audit_pdf_links(self.mutate('nav-res-q-aut-001-back', **option), self.plan)
                self.assertFalse(result['passed'])
                self.assertTrue(any('área clicável' in e for e in result['errors']))

    def test_equivalent_direct_goto_is_accepted(self):
        result = audit_pdf_links(self.mutate('nav-q-aut-001-answer'), self.plan)
        self.assertTrue(result['passed'], result['errors'])

    def test_omitting_a_link_from_the_plan_does_not_hide_an_annotation(self):
        plan = copy.deepcopy(self.plan)
        plan['links'] = [e for e in plan['links'] if e['source'] != 'nav-res-q-aut-001-back']
        self.assertFalse(audit_pdf_links(self.pdf, plan)['passed'])

    def test_standalone_audit_rejects_a_changed_pdf_hash(self):
        with self.assertRaisesRegex(ValueError, 'hash do PDF'):
            inspect_pdf(self.mutate('nav-q-aut-001-answer', 'res-q-aut-002'), self.manifest)

    def test_standalone_audit_recomputes_instead_of_trusting_cached_success(self):
        pdf = self.mutate('nav-q-aut-001-answer', 'res-q-aut-002')
        manifest = json.loads(self.manifest.read_text())
        manifest['pdf_sha256'] = sha256(pdf.read_bytes()).hexdigest()
        changed = self.root / 'cached.json'
        changed.write_text(json.dumps(manifest))
        self.assertFalse(inspect_pdf(pdf, changed)['navigation']['passed'])

    def test_destination_must_contain_its_expected_heading(self):
        path = self.root / 'missing-heading.pdf'
        with self.fitz.open(self.pdf) as doc:
            page = doc[pdf_names(doc)['q-aut-001']['page']]
            for rect in page.search_for('Q-AUT-001'):
                page.add_redact_annot(rect)
            page.apply_redactions()
            doc.save(path, garbage=3)
        result = audit_pdf_links(path, self.plan)
        self.assertFalse(result['passed'])
        self.assertTrue(any('Destino não coincide' in e for e in result['errors']))

    def test_native_browser_clicks_cover_toc_fields_and_wrapped_links(self):
        from browser_links import check_html_clicks
        result = check_html_clicks(self.html, self.plan)
        self.assertTrue(result['passed'], result['errors'])
        self.assertGreater(result['clicks'], len(self.plan['links']))

    def test_browser_detects_a_swapped_route_independently_of_the_plan(self):
        from browser_links import check_html_clicks
        changed = self.root / 'wrong-route.html'
        changed.write_text(redirect(self.html.read_text(), 'nav-q-aut-001-answer', 'res-q-aut-002'))
        result = check_html_clicks(changed, self.plan)
        self.assertFalse(result['passed'])
        self.assertTrue(any('nav-q-aut-001-answer' in e for e in result['errors']))


class ExternalNavigationTests(unittest.TestCase):
    class Response:
        status = 200
        def __init__(self, body=b'%PDF-1.7 fixture'):
            self.body = body
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def geturl(self):
            return 'https://example.org/prova.pdf'
        def read(self, maximum):
            assert maximum == 1024
            return self.body

    def test_healthy_pdf_and_fragment_deduplication(self):
        with patch('external_links.urlopen', return_value=self.Response()) as fetch:
            result = check_external(['https://example.org/prova.pdf#page=1', 'https://example.org/prova.pdf#page=2'])
            self.assertTrue(result['passed'])
            self.assertEqual(result['count'], 1)
            self.assertEqual(fetch.call_count, 1)

    def test_html_error_page_is_not_accepted_as_pdf(self):
        with patch('external_links.urlopen', return_value=self.Response(b'<html>login</html>')):
            self.assertEqual(check_url('https://example.org/prova.pdf')['status'], 'unexpected-content')

    def test_access_block_and_missing_page_are_not_reported_as_success(self):
        for code, status in [(403, 'blocked'), (404, 'http-error')]:
            with self.subTest(code=code), patch('external_links.urlopen', side_effect=HTTPError('url', code, 'fixture', {}, None)):
                self.assertEqual(check_url('https://example.org/prova.pdf')['status'], status)

    def test_timeout_remains_unconfirmed(self):
        with patch('external_links.urlopen', side_effect=TimeoutError):
            self.assertFalse(check_external(['https://example.org/prova.pdf'])['passed'])

    def test_non_https_or_credential_url_is_rejected_without_request(self):
        with patch('external_links.urlopen') as fetch:
            self.assertEqual(check_url('http://example.org/prova.pdf')['status'], 'invalid')
            self.assertEqual(check_url('https://user:password@example.org/prova.pdf')['status'], 'invalid')
            fetch.assert_not_called()
