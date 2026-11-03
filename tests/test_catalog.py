import copy
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from catalog import import_material, search, history, export_catalog, question_key, validate_transition, connect

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / 'material'
        shutil.copytree(ROOT / 'materials/dataprev-sql', self.folder)
        self.manifest = self.folder / 'material.json'
        self.db = Path(self.temp.name) / 'acervo.sqlite'

    def edit(self, file, mutate):
        p = self.folder / file
        value = json.loads(p.read_text())
        mutate(value)
        p.write_text(json.dumps(value))

    def revision_fixture(self):
        # Synthetic revision, never a claim about the real FGV key.
        self.edit('material.json', lambda d: d.update(version='fixture-2'))
        def revise(questions):
            q = questions[0]
            q['resposta'] = 'A'
            q['fonte_original'].update(gabarito_status='retificado', gabarito_sha256='a' * 64,
                                      gabarito_url='https://example.org/fixture-key.pdf')
            q['source_ids'] = [k for k in q['source_ids'] if k != 'G26'] + ['GFIX']
        self.edit('questoes.json', revise)
        self.edit('fontes.json', lambda d: d.append({'id': 'GFIX', 'title': 'Fixture sintética',
                  'url': 'https://example.org/fixture-key.pdf', 'locator': 'fixture',
                  'checked_on': '2026-11-03', 'rights': 'somente-link', 'sha256': 'a' * 64}))

    def test_import_and_reimport_are_idempotent(self):
        self.assertEqual(import_material(self.db, self.manifest)['inserted'], 11)
        self.assertEqual(import_material(self.db, self.manifest)['reused'], 11)
        self.assertEqual(len(search(self.db)), 11)

    def test_same_questions_in_another_material_do_not_duplicate(self):
        import_material(self.db, self.manifest)
        self.edit('material.json', lambda d: d.update(id='outro-material'))
        result = import_material(self.db, self.manifest)
        self.assertEqual(result['inserted'], 0)
        self.assertEqual(result['reused'], 11)
        self.assertTrue(all(len(r['occurrences']) == 2 for r in search(self.db)))

    def test_bank_year_topic_filters_are_combined(self):
        import_material(self.db, self.manifest)
        rows = search(self.db, bank='fgv', year=2026, topic='integridade', origin='REAL', status='preliminar')
        self.assertTrue(rows)
        self.assertTrue(all(r['bank'] == 'FGV' and r['year'] == 2026 for r in rows))
        self.assertEqual(search(self.db, bank='FGV', year=1999), [])

    def test_authored_items_do_not_inherit_the_reference_bank(self):
        import_material(self.db, self.manifest)
        rows = search(self.db, origin='AUTORAL')
        self.assertEqual(len(rows), 8)
        self.assertTrue(all(r['bank'] is None for r in rows))
        self.assertEqual(search(self.db, bank='FGV', origin='AUTORAL'), [])

    def test_search_uses_literal_parameters(self):
        import_material(self.db, self.manifest)
        self.assertEqual(search(self.db, topic="' OR 1=1 --"), [])
        self.assertEqual(len(search(self.db)), 11)

    def test_link_only_exports_never_include_original_item_text(self):
        self.edit('questoes.json', lambda d: d[0].update(enunciado='PRIVATE_ORIGINAL_SENTINEL'))
        import_material(self.db, self.manifest)
        output = Path(self.temp.name) / 'catalog.json'
        export_catalog(self.db, output)
        self.assertNotIn('PRIVATE_ORIGINAL_SENTINEL', output.read_text())
        real = next(r for r in search(self.db) if r['origin'] == 'REAL')
        self.assertNotIn('enunciado', real['record'])
        self.assertNotIn('alternativas', real['record'])

    def test_changes_to_an_already_registered_edition_are_rejected(self):
        import_material(self.db, self.manifest)
        self.edit('material.json', lambda d: d.update(scope='Escopo alterado na mesma edição'))
        with self.assertRaisesRegex(ValueError, 'incremente version'):
            import_material(self.db, self.manifest)

    def test_revision_requires_explicit_reason_and_is_atomic(self):
        import_material(self.db, self.manifest)
        self.revision_fixture()
        self.edit('questoes.json', lambda d: d.append({**copy.deepcopy(d[3]),
                  'id': 'Q-AUT-999', 'enunciado': 'Item sintético inédito para testar transação.'}))
        self.edit('questoes.json', lambda d: d.insert(0, d.pop()))
        with self.assertRaisesRegex(ValueError, 'aceitar-revisoes'):
            import_material(self.db, self.manifest)
        self.assertEqual(len(search(self.db)), 11)
        self.assertTrue(all(r['revision'] == 1 for r in search(self.db)))

    def test_accepted_revision_preserves_old_answer_and_occurrence(self):
        import_material(self.db, self.manifest)
        q = json.loads((self.folder / 'questoes.json').read_text())[0]
        key = question_key(q)
        self.revision_fixture()
        result = import_material(self.db, self.manifest, True, 'Teste sintético de retificação')
        self.assertEqual(result['revised'], 1)
        records = history(self.db, key)
        self.assertEqual([r['record']['resposta'] for r in records], ['E', 'A'])
        row = next(r for r in search(self.db) if r['key'] == key)
        self.assertEqual({o['revision'] for o in row['occurrences']}, {1, 2})

    def test_official_answer_change_requires_a_different_evidence_hash(self):
        q = json.loads((self.folder / 'questoes.json').read_text())[0]
        other = copy.deepcopy(q)
        other['resposta'] = 'A'
        with self.assertRaisesRegex(ValueError, 'nova evidência'):
            validate_transition(q, other)

    def test_final_key_cannot_regress_to_preliminary(self):
        q = json.loads((self.folder / 'questoes.json').read_text())[0]
        old = copy.deepcopy(q)
        old['fonte_original']['gabarito_status'] = 'definitivo'
        with self.assertRaisesRegex(ValueError, 'regredir'):
            validate_transition(old, q)

    def test_stale_evidence_cannot_replace_current_revision(self):
        q = json.loads((self.folder / 'questoes.json').read_text())[0]
        older = copy.deepcopy(q)
        older['fonte_original']['conferido_em'] = '2020-01-01'
        with self.assertRaisesRegex(ValueError, 'antiga'):
            validate_transition(q, older)

    def test_export_cannot_overwrite_database(self):
        import_material(self.db, self.manifest)
        with self.assertRaisesRegex(ValueError, 'sobrescrever'):
            export_catalog(self.db, self.db)
        self.assertEqual(len(search(self.db)), 11)

    def test_export_contains_revision_history_and_material_snapshots(self):
        import_material(self.db, self.manifest)
        self.revision_fixture()
        import_material(self.db, self.manifest, True, 'Fixture de revisão')
        output = Path(self.temp.name) / 'catalog.json'
        export_catalog(self.db, output)
        result = json.loads(output.read_text())
        self.assertEqual(len(result['materials']), 2)
        self.assertEqual(max(len(rows) for rows in result['revisions'].values()), 2)

    def test_other_sqlite_database_is_preserved(self):
        with sqlite3.connect(self.db) as db:
            db.execute('CREATE TABLE user_notes(note TEXT)')
        with self.assertRaisesRegex(ValueError, 'outro banco'):
            connect(self.db, create=True)

    def test_authorial_identity_preserves_operator_changes(self):
        q = json.loads((self.folder / 'questoes.json').read_text())[3]
        q['enunciado'] = 'x > 2'
        other = copy.deepcopy(q)
        other['enunciado'] = 'x >= 2'
        self.assertNotEqual(question_key(q), question_key(other))
