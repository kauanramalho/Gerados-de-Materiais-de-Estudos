import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from integrity import validate_questions, validate_navigation


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.q = json.loads((Path(__file__).resolve().parents[1] /
                             'examples/redes/questoes.json').read_text(encoding='utf-8'))

    def test_original_sample_is_consistent(self):
        self.assertEqual(validate_questions(self.q), [])

    def test_duplicate_question_is_rejected(self):
        self.assertTrue(any('duplicado' in e for e in validate_questions(self.q + [self.q[0]])))

    def test_answer_outside_alternatives_is_rejected(self):
        self.q[0]['resposta'] = 'D'
        self.assertTrue(any('resposta fora' in e for e in validate_questions(self.q)))

    def test_uncommented_alternative_is_rejected(self):
        del self.q[0]['comentarios']['B']
        self.assertTrue(any('comentário' in e for e in validate_questions(self.q)))

    def test_real_question_without_provenance_is_rejected(self):
        self.q[0].update(id='Q-REAL-001', origem='REAL')
        self.assertTrue(any('origem real incompleta' in e for e in validate_questions(self.q)))

    def test_false_source_on_authorial_question_is_rejected(self):
        self.q[0]['fonte_original'] = {'banca': 'atribuição fictícia'}
        self.assertTrue(any('autoria' in e for e in validate_questions(self.q)))

    def test_missing_return_target_is_rejected(self):
        html = '<h2 id="q-aut-001">Questão</h2><a href="#res-q-aut-001">Resposta</a>'
        self.assertTrue(validate_navigation(html, self.q[:1]))

    def test_complete_question_resolution_pair_passes(self):
        html = ('<h2 id="q-aut-001">Questão</h2><a href="#res-q-aut-001">Resposta</a>'
                '<h2 id="res-q-aut-001">Resolução</h2><a href="#q-aut-001">Voltar</a>')
        self.assertEqual(validate_navigation(html, self.q[:1]), [])

    def test_duplicate_anchor_is_rejected(self):
        self.assertTrue(validate_navigation('<p id="x"></p><p id="x"></p>'))


if __name__ == '__main__':
    unittest.main()
