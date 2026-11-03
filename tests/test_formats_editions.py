"""Exercise scoring, revision routing and edition impact; all altered answers are synthetic fixtures."""
from copy import deepcopy
import json
from pathlib import Path
import shutil,sys,tempfile,unittest

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from material import load_material,compose_material
from formats import prepare_format,score_simulation,validate_simulation
from edicoes import comparison,render_errata
from acessibilidade import contrast,svg_accessibility


class FormatTests(unittest.TestCase):
    def setUp(self):
        self.data=deepcopy(load_material(ROOT/'materials/matematica-basica/material.json'))
        self.correct={q['id']:q['resposta'] for q in self.data['questions']}

    def test_correct_wrong_and_blank_match_independent_example(self):
        responses=json.loads((ROOT/'materials/matematica-basica/respostas-exemplo.json').read_text())
        result=score_simulation(self.data,responses)
        self.assertEqual(result['points'],3.75);self.assertEqual(result['maximum'],6)
        self.assertEqual([r['result']for r in result['rows']].count('branco'),1)

    def test_all_correct_and_all_blank(self):
        self.assertEqual(score_simulation(self.data,self.correct)['points'],6)
        self.assertEqual(score_simulation(self.data,{})['points'],0)

    def test_weights_and_fractional_points(self):
        self.data['simulation']['scoring'].update(correct=.1,wrong=-.1,weights={'Q-AUT-001':2})
        result=score_simulation(self.data,self.correct)
        self.assertEqual(result['points'],.7);self.assertEqual(result['maximum'],.7)

    def test_annulled_credit_ignores_the_choice(self):
        self.data['simulation']['annulled_ids']=['Q-AUT-001']
        self.assertEqual(score_simulation(self.data,{})['points'],1)

    def test_annulled_exclusion_changes_denominator(self):
        self.data['simulation']['annulled_ids']=['Q-AUT-001'];self.data['simulation']['scoring']['annulled']='exclude'
        result=score_simulation(self.data,self.correct)
        self.assertEqual(result['points'],5);self.assertEqual(result['maximum'],5)

    def test_all_annulled_excluded_has_no_division_by_zero(self):
        self.data['simulation']['annulled_ids']=list(self.correct);self.data['simulation']['scoring']['annulled']='exclude'
        self.assertIsNone(score_simulation(self.data,{})['percent'])

    def test_unknown_question_or_alternative_is_rejected(self):
        for responses in [{'Q-NOT-FOUND':'A'},{'Q-AUT-001':'Z'},[]]:
            with self.assertRaises(ValueError):score_simulation(self.data,responses)

    def test_order_and_matrix_must_match_actual_questions(self):
        self.data['simulation']['order'].pop()
        with self.assertRaisesRegex(ValueError,'Ordem'):validate_simulation(self.data,self.data['simulation'])
        self.data=load_material(ROOT/'materials/matematica-basica/material.json')
        self.data['simulation']['matrix'][0]['count']+=1
        with self.assertRaisesRegex(ValueError,'Matriz'):validate_simulation(self.data,self.data['simulation'])

    def test_unknown_weight_and_nonfinite_points_are_rejected(self):
        self.data['simulation']['scoring']['weights']['Q-OTHER']=2
        with self.assertRaises(ValueError):score_simulation(self.data,{})
        self.data['simulation']['scoring']['weights']={};self.data['simulation']['scoring']['correct']=float('inf')
        with self.assertRaisesRegex(ValueError,'finitos'):score_simulation(self.data,{})

    def test_official_rules_require_hashed_source(self):
        self.data['simulation']['basis'].update(type='oficial',source_id='M01')
        with self.assertRaisesRegex(ValueError,'fonte identificada'):score_simulation(self.data,{})

    def test_simulation_answers_follow_the_question_block(self):
        text=compose_material(self.data,'simulado');boundary=text.index('# Gabarito comentado')
        self.assertNotIn('**Resposta do projeto:',text[:boundary])
        self.assertIn('**Resposta do projeto:',text[boundary:])
        self.assertIn('folha de respostas',text)
        for q in self.data['questions']:
            self.assertIn('#res-'+q['id'].lower(),text)

    def test_revision_uses_short_files_and_local_theory_targets(self):
        prepared=prepare_format(self.data,'revisao')
        self.assertTrue(all(c['file'].startswith('revisao-')for c in prepared['config']['chapters']))
        text=compose_material(self.data,'revisao')
        self.assertIn('Revisão ativa',text)
        for q in self.data['questions']:self.assertIn('{#'+q['theory']+'}',text)

    def test_revision_missing_chapter_is_rejected(self):
        self.data['revision']['chapters'].pop()
        with self.assertRaisesRegex(ValueError,'cada capítulo'):prepare_format(self.data,'revisao')

    def test_revision_file_cannot_escape_material_folder(self):
        self.data['revision']['chapters'][0]['file']='../secret.md'
        with self.assertRaisesRegex(ValueError,'fora da pasta'):prepare_format(self.data,'revisao')


class EditionTests(unittest.TestCase):
    def setUp(self):
        self.old=load_material(ROOT/'materials/matematica-basica/material.json');self.new=deepcopy(self.old)
        self.new['config']['version']='0.5.1'

    def test_identical_content_has_no_impact(self):
        report=comparison(self.old,self.new,'Verificação sem mudança de conteúdo')
        self.assertFalse(report['changed']);self.assertEqual(report['affected_questions'],[])

    def test_answer_change_keeps_id_and_identifies_objective_and_chapter(self):
        self.new['questions'][0]['resposta']='A'
        report=comparison(self.old,self.new,'Mudança sintética de gabarito para teste')
        self.assertIn('Q-AUT-001',report['changed_questions'])
        self.assertIn('cap-percentuais',report['chapters_to_review'])
        self.assertIn('não aprova',render_errata(report))

    def test_source_change_reviews_all_chapters(self):
        self.new['sources'][0]['checked_on']='2026-11-04'
        report=comparison(self.old,self.new,'Teste de impacto')
        self.assertEqual(len(report['chapters_to_review']),3)
        self.assertTrue(report['affected_questions'])

    def test_same_version_after_content_change_is_rejected(self):
        self.new['config']['version']=self.old['config']['version'];self.new['questions'][0]['comentarios']['A']+=' Teste.'
        with self.assertRaisesRegex(ValueError,'nova versão'):comparison(self.old,self.new,'Teste')

    def test_removed_ids_are_reported_and_empty_reason_is_rejected(self):
        self.new['questions'].pop()
        self.assertTrue(comparison(self.old,self.new,'Remoção sintética')['removed_questions'])
        with self.assertRaises(ValueError):comparison(self.old,self.new,'')

    def test_changed_chapter_file_is_traced_without_answer_change(self):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'material';shutil.copytree(self.old['folder'],target)
            p=target/'01-porcentagens.md';p.write_text(p.read_text()+'\nNota editorial de teste.\n')
            config=json.loads((target/'material.json').read_text());config['version']='0.5.1'
            (target/'material.json').write_text(json.dumps(config))
            new=load_material(target/'material.json');report=comparison(self.old,new,'Nota de teste')
            self.assertIn('cap-percentuais',report['chapters_to_review'])

    def test_contrast_matches_black_white_and_equal_colors(self):
        self.assertAlmostEqual(contrast([0,0,0],[255,255,255]),21)
        self.assertAlmostEqual(contrast([120,120,120],[120,120,120]),1)

    def test_inline_svg_alt_is_exposed_as_accessible_name(self):
        html='<svg alt="Painel &amp; portas" id="fig"></svg>'
        actual=svg_accessibility(html)
        self.assertIn('role="img"',actual);self.assertIn('aria-label="Painel &amp; portas"',actual)
        self.assertEqual(svg_accessibility(actual),actual)

    def test_decorative_svg_is_not_reclassified_as_informative(self):
        html='<svg role="presentation" alt="decorativo"></svg>'
        self.assertEqual(svg_accessibility(html),html)


if __name__=='__main__':unittest.main()
