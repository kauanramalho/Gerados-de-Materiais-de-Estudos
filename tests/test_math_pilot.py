from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import itertools
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from material import load_material, publish

ROOT = Path(__file__).resolve().parents[1]


class MathPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_material(ROOT / 'materials/matematica-basica/material.json')
        cls.questions = {q['id']: q for q in cls.data['questions']}

    def answer(self, number):
        q = self.questions[f'Q-AUT-{number:03d}']
        return q['alternativas'][q['resposta']]

    def test_successive_rates_match_the_marked_answer(self):
        result = Decimal(240) * Decimal('.85') * Decimal('1.10')
        self.assertEqual(self.answer(1), 'R$ ' + f'{result:.2f}'.replace('.', ','))

    def test_relative_rate_uses_the_original_denominator(self):
        result = Fraction(15 - 12, 12) * 100
        self.assertEqual(self.answer(2), f'{int(result)}%')

    def test_session_table_and_mean_are_consistent(self):
        quantities = [20, 25, 30, 35, 40] * 6
        self.assertEqual(sum(quantities), 900)
        self.assertEqual(self.answer(3), str(sum(quantities) // len(quantities)))

    def test_probability_is_checked_by_counting_ordered_pairs(self):
        pairs = list(itertools.permutations(['A1', 'A2', 'V1', 'V2', 'V3'], 2))
        favorable = sum(a.startswith('A') and b.startswith('A') for a, b in pairs)
        self.assertEqual(self.answer(4), str(Fraction(favorable, len(pairs))))

    def test_group_mean_reconstructs_the_totals(self):
        values = [20] * 2 + [40] * 8
        self.assertEqual(self.answer(5), str(sum(values) // len(values)))

    def test_reversal_is_rounded_only_at_the_end(self):
        result = (Decimal(200 - 180) / Decimal(180) * 100).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        self.assertEqual(self.answer(6), str(result).replace('.', ',') + '%')

    @unittest.skipUnless(shutil.which('pandoc'), 'Pandoc não instalado; integração HTML não executada')
    def test_math_is_exported_as_self_contained_mathml(self):
        with tempfile.TemporaryDirectory() as folder:
            report = publish(self.data, Path(folder), pdf=False)
            text = (Path(folder) / 'apostila.html').read_text()
            self.assertEqual(report['html_navigation'], 'passed')
            self.assertEqual(text.count('<math'), 7)
            self.assertIn('<mfrac>', text)
            self.assertNotIn('<script', text)
