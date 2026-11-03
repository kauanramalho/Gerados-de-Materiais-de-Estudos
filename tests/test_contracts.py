import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from material import load_material

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / 'material'
        shutil.copytree(ROOT / 'materials/dataprev-sql', self.folder)

    def edit(self, file, mutate):
        p = self.folder / file
        value = json.loads(p.read_text())
        mutate(value)
        p.write_text(json.dumps(value))

    def test_chapters_wrong_type_is_a_located_validation_error(self):
        self.edit('material.json', lambda d: d.update(chapters='inválido'))
        with self.assertRaisesRegex(ValueError, r'material.json.chapters: tipo esperado'):
            load_material(self.folder / 'material.json')

    def test_impossible_source_date_is_rejected(self):
        self.edit('fontes.json', lambda d: d[0].update(checked_on='2026-02-30'))
        with self.assertRaisesRegex(ValueError, r'fontes.json\[0\].checked_on'):
            load_material(self.folder / 'material.json')

    def test_unknown_source_field_is_not_silently_ignored(self):
        self.edit('fontes.json', lambda d: d[0].update(segredo='fixture'))
        with self.assertRaisesRegex(ValueError, 'campos não permitidos: segredo'):
            load_material(self.folder / 'material.json')

    def test_invalid_question_container_has_clear_error(self):
        (self.folder / 'questoes.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'lista de questões'):
            load_material(self.folder / 'material.json')

    def test_incomplete_figure_metadata_blocks_the_build(self):
        self.edit('figuras.json', lambda d: d[0].update(alt=''))
        with self.assertRaisesRegex(ValueError, r'figuras.json\[0\].alt'):
            load_material(self.folder / 'material.json')

    def test_coverage_requires_an_explicit_limit(self):
        self.edit('cobertura.json', lambda d: d[0].pop('limits'))
        with self.assertRaisesRegex(ValueError, 'limits'):
            load_material(self.folder / 'material.json')

    def test_question_hash_must_match_declared_evidence(self):
        self.edit('questoes.json', lambda d: d[0]['fonte_original'].update(prova_sha256='a' * 64))
        with self.assertRaisesRegex(ValueError, 'hash de prova diverge'):
            load_material(self.folder / 'material.json')

    def test_embedded_credentials_are_rejected_in_source_url(self):
        self.edit('fontes.json', lambda d: d[0].update(url='https://:secret@example.org/x'))
        with self.assertRaisesRegex(ValueError, 'Fonte incompleta'):
            load_material(self.folder / 'material.json')

    def test_cli_returns_failure_without_traceback_for_invalid_nested_type(self):
        self.edit('questoes.json', lambda d: d[0].update(alternativas=[]))
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_material.py'),
                                 str(self.folder / 'material.json'), '--check'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('alternativas', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
