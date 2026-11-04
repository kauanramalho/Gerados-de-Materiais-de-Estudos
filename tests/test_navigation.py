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
from navigation import instrument_html, link_plan, required_edges, audit_pdf_links, finalize_pdf_destinations
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
    <a href="https://example.org/reference">Referência externa</a>
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
        bad = re.sub(r'(<span class="toc-page"[^>]*>)2(</span>)', r'\g<1>9\2', rendered, count=1)
        self.assertNotEqual(bad, rendered)
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
                    page.pdf(path=str(cls.pdf), format='A4', prefer_css_page_size=True, tagged=True, outline=True)
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
        self.assertEqual(len(result['toc_rows']), len(self.entries))
        self.assertTrue(all(row['parts'] == 3 and row['full_row_clickable'] for row in result['toc_rows']))

    def test_large_page_numbers_stay_on_one_line_in_the_production_layout(self):
        from playwright.sync_api import sync_playwright
        css = (Path(__file__).resolve().parents[1] / 'styles/apostila.css').read_text()
        html, entries, _ = fixture()
        html = render_contents(html, entries, {e['target']: 12345 for e in entries})
        html = html.replace('</head>', '<style>' + css + '</style></head>')
        with sync_playwright() as pw:
            executable = shutil.which('chromium') or shutil.which('google-chrome') or pw.chromium.executable_path
            browser = pw.chromium.launch(executable_path=executable, headless=True, args=['--no-sandbox'])
            try:
                page = browser.new_page()
                page.emulate_media(media='print')
                page.set_content(html)
                results = page.locator('.toc-page').evaluate_all('''items => items.map(item => {
                    const range = document.createRange(); range.selectNodeContents(item);
                    const rectangles = Array.from(range.getClientRects());
                    const row = item.closest('a').getBoundingClientRect();
                    return {lines: rectangles.length, inside: rectangles.every(r => r.left >= row.left && r.right <= row.right + 1)};
                })''')
                self.assertEqual(len(results), len(entries))
                self.assertTrue(all(r['lines'] == 1 and r['inside'] for r in results), results)
            finally:
                browser.close()

    def test_toc_page_number_cannot_be_outside_the_click_area(self):
        path = self.root / 'toc-page-not-clickable.pdf'
        offset = self.fitz.Point(audit_pdf_links(self.pdf, self.plan)['coordinate_offset_pt'])
        with self.fitz.open(self.pdf) as doc:
            names = pdf_names(doc)
            page = doc[names['toc-theory-a']['page']]
            link = next(l for l in page.get_links() if l.get('nameddest') == 'theory-a')
            point = self.fitz.Point(names['toc-theory-a-page']['to']) * page.transformation_matrix + offset
            rect = self.fitz.Rect(link['from']);rect.x1 = point.x - 3
            bottom_left = self.fitz.Point(rect.x0, rect.y1) * ~page.transformation_matrix
            top_right = self.fitz.Point(rect.x1, rect.y0) * ~page.transformation_matrix
            doc.xref_set_key(link['xref'], 'Rect', f'[{bottom_left.x} {bottom_left.y} {top_right.x} {top_right.y}]')
            doc.save(path)
        result = audit_pdf_links(path, self.plan)
        self.assertFalse(result['passed'])
        self.assertTrue(any('Sumário sem área clicável contínua' in e for e in result['errors']), result['errors'])

    def test_toc_gap_is_clickable_even_when_all_three_text_parts_have_links(self):
        path = self.root / 'toc-leader-not-clickable.pdf'
        with self.fitz.open(self.pdf) as doc:
            names = pdf_names(doc);page = doc[names['toc-theory-a']['page']]
            link = next(l for l in page.get_links() if l.get('nameddest') == 'theory-a')
            rect = link['from'];dest = names['theory-a']
            point = self.fitz.Point(dest['to']) * doc[dest['page']].transformation_matrix
            page.delete_link(link)
            for area in [self.fitz.Rect(rect.x0, rect.y0, 220, rect.y1),
                         self.fitz.Rect(460, rect.y0, rect.x1, rect.y1)]:
                page.insert_link({'kind': self.fitz.LINK_GOTO, 'from': area, 'page': dest['page'], 'to': point})
            doc.save(path)
        result = audit_pdf_links(path, self.plan)
        self.assertFalse(result['passed'])
        self.assertTrue(any('Sumário sem área clicável contínua' in e for e in result['errors']), result['errors'])

    def test_normalization_keeps_appearance_tags_outlines_external_urls_and_unicode_routes(self):
        path = self.root / 'portable.pdf';shutil.copy2(self.pdf, path)
        with self.fitz.open(path) as doc:
            words = [p.get_text('words') for p in doc]
            streams = [[doc.xref_stream(x) for x in p.get_contents()] for p in doc]
            outlines = doc.get_toc()
            uris = [l['uri'] for p in doc for l in p.get_links() if l['kind'] == self.fitz.LINK_URI]
            self.assertEqual(doc.xref_get_key(doc.pdf_catalog(), 'StructTreeRoot')[0], 'xref')
        report = finalize_pdf_destinations(path, self.plan)
        self.assertGreaterEqual(report['rewritten_links'], len(self.plan['links']))
        audit = audit_pdf_links(path, self.plan, require_explicit=True)
        self.assertTrue(audit['passed'], audit['errors'])
        self.assertEqual(audit['coordinate_offset_pt'], [0, 0])
        with self.fitz.open(path) as doc:
            self.assertEqual(words, [p.get_text('words') for p in doc])
            self.assertEqual(streams, [[doc.xref_stream(x) for x in p.get_contents()] for p in doc])
            self.assertEqual(outlines, doc.get_toc())
            self.assertEqual(uris, [l['uri'] for p in doc for l in p.get_links() if l['kind'] == self.fitz.LINK_URI])
            self.assertEqual(doc.xref_get_key(doc.pdf_catalog(), 'StructTreeRoot')[0], 'xref')
            self.assertIn('teoria-ação', pdf_names(doc))
            self.assertTrue(all(l['kind'] == self.fitz.LINK_GOTO and not l.get('nameddest')
                                for p in doc for l in p.get_links() if l['kind'] != self.fitz.LINK_URI))

    def test_normalization_is_idempotent(self):
        path = self.root / 'idempotent.pdf';shutil.copy2(self.pdf, path)
        finalize_pdf_destinations(path, self.plan);before = sha256(path.read_bytes()).hexdigest()
        report = finalize_pdf_destinations(path, self.plan)
        self.assertEqual(report['rewritten_links'], 0)
        self.assertEqual(before, sha256(path.read_bytes()).hexdigest())

    def test_normalization_does_not_repair_or_mask_a_wrong_route(self):
        path = self.mutate('nav-q-aut-001-answer', 'res-q-aut-002')
        before = sha256(path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'Navegação antes da normalização'):
            finalize_pdf_destinations(path, self.plan)
        self.assertEqual(before, sha256(path.read_bytes()).hexdigest())

    def test_new_export_contract_rejects_legacy_named_annotations(self):
        manifest = json.loads(self.manifest.read_text());manifest['version'] = 2
        path = self.root / 'explicit-required.json';path.write_text(json.dumps(manifest))
        result = inspect_pdf(self.pdf, path)
        self.assertFalse(result['navigation']['passed'])
        self.assertTrue(any('sem destino direto' in e for e in result['navigation']['errors']))

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
