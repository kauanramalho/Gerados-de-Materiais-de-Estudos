import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from material import load_material, compose_material, local_path
from check_sql import check_cases
from contents import contents_entries
from integrity import validate_navigation

ROOT = Path(__file__).resolve().parents[1]


class MaterialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / 'material'
        shutil.copytree(ROOT / 'materials/dataprev-sql', self.folder)

    def edit(self, filename, mutate):
        path = self.folder / filename
        data = json.loads(path.read_text(encoding='utf-8'))
        mutate(data)
        path.write_text(json.dumps(data), encoding='utf-8')

    def test_manifest_connects_coverage_sources_and_questions(self):
        data = load_material(self.folder / 'material.json')
        self.assertEqual(len(data['questions']), 11)

    def test_input_cannot_read_outside_material_folder(self):
        external = self.folder.parent / 'private.txt'
        external.write_text('private')
        with self.assertRaises(ValueError):
            local_path(self.folder, '../private.txt')

    def test_real_item_requires_hash_of_source_evidence(self):
        self.edit('questoes.json', lambda questions: questions[0]['fonte_original'].pop('prova_sha256'))
        with self.assertRaisesRegex(ValueError, 'hash'):
            load_material(self.folder / 'material.json')

    def test_unknown_learning_objective_blocks_publication(self):
        self.edit('cobertura.json', lambda rows: rows[0]['objectives'].append('OBJ-INEXISTENTE'))
        with self.assertRaisesRegex(ValueError, 'inexistente'):
            load_material(self.folder / 'material.json')

    def test_external_or_undeclared_image_blocks_publication(self):
        path = self.folder / '01-modelagem.md'
        path.write_text(path.read_text(encoding='utf-8') + '\n![x](https://example.com/tracker.png)')
        with self.assertRaisesRegex(ValueError, 'Imagem'):
            load_material(self.folder / 'material.json')

    def test_link_only_item_does_not_reproduce_original(self):
        data = load_material(self.folder / 'material.json')
        data['questions'][0]['enunciado'] = 'ORIGINAL_QUE_NAO_PODE_SER_REPUBLICADO'
        data['questions'][0]['alternativas']['A'] = 'ALTERNATIVA_QUE_NAO_PODE_SER_REPUBLICADA'
        text = compose_material(data)
        self.assertNotIn('ORIGINAL_QUE_NAO_PODE', text)
        self.assertNotIn('ALTERNATIVA_QUE_NAO_PODE', text)
        self.assertIn('Gabarito oficial preliminar', text)

    def test_caderno_links_only_to_local_question_resolution_pairs(self):
        data = load_material(self.folder / 'material.json')
        text = compose_material(data, 'caderno')
        self.assertNotIn('](#integridade)', text)
        for q in data['questions']:
            self.assertIn(f'](#res-{q["id"].lower()})', text)
            self.assertIn(f'](#{q["id"].lower()})', text)

    def test_official_zip_is_download_link_without_fake_pdf_page_jump(self):
        data = load_material(self.folder / 'material.json')
        source = data['questions'][0]['fonte_original']
        source['prova_url'] = 'https://example.org/PROVAS.ZIP?download=1'
        text = compose_material(data, 'caderno')
        self.assertIn('[Baixar arquivo oficial de provas (ZIP)](https://example.org/PROVAS.ZIP?download=1)', text)
        self.assertNotIn('PROVAS.ZIP?download=1#page=', text)
        self.assertIn('Extraia o ZIP', text)

    def test_official_pdf_keeps_page_deep_link(self):
        data = load_material(self.folder / 'material.json')
        source = data['questions'][0]['fonte_original']
        source['prova_url'] = 'https://example.org/prova.pdf'
        source['pagina'] = '7'
        text = compose_material(data, 'caderno')
        self.assertIn('[Abrir questão na prova oficial](https://example.org/prova.pdf#page=7)', text)

    def test_question_ids_keep_destinations_without_filling_the_book_contents(self):
        data = load_material(self.folder / 'material.json')
        data['request'] = {
            'concurso': dict(orgao='Órgão de teste', cargo='Cargo', ano=2026, banca='Fixture'),
            'programa': [dict(id=obj, materia='Matéria de treino')
                         for obj in {q['objetivo'] for q in data['questions']}],
        }
        text = compose_material(data, 'caderno')
        html = subprocess.run(['pandoc', '--from=markdown-raw_html', '--to=html', '--standalone',
                               '--toc', '--toc-depth=2', '--number-sections'],
                              input=text, text=True, capture_output=True, check=True).stdout
        targets = {entry['target'] for entry in contents_entries(html)}
        self.assertIn('questoes-autorais-disciplina-1', targets)
        self.assertIn('gabarito-comentado', targets)
        for q in data['questions']:
            anchor = q['id'].lower()
            self.assertNotIn(anchor, targets)
            self.assertNotIn('res-' + anchor, targets)
        self.assertEqual(validate_navigation(html, data['questions']), [])

    def test_sql_counterexamples_and_constraints_pass(self):
        result = check_cases(self.folder / 'verificacoes.json')
        self.assertTrue(result['passed'])
        self.assertEqual(len(result['cases']), 13)

    def test_incorrect_sql_result_is_detected(self):
        self.edit('verificacoes.json', lambda data: data['cases'][0].update(expected=[]))
        self.assertFalse(check_cases(self.folder / 'verificacoes.json')['passed'])
