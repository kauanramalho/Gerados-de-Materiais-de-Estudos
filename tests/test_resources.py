"""Reproduce the resource and figure-impact gaps with disposable, non-private assets."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from material import load_material, publish
from resources import markdown_images, validate_svg
from edicoes import comparison
from acessibilidade import contrast, inspect as inspect_accessibility


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)/'material'
        shutil.copytree(ROOT/'materials/matematica-basica', self.folder)
        (self.folder.parent/'outside.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><text>OUTSIDE-FIXTURE</text></svg>')

    def append(self, file, text):
        path=self.folder/file
        path.write_text(path.read_text()+'\n'+text+'\n')

    def edit(self, file, transform):
        path=self.folder/file;data=json.loads(path.read_text());transform(data)
        path.write_text(json.dumps(data,ensure_ascii=False))

    def load(self):
        return load_material(self.folder/'material.json')

    def test_outside_and_remote_images_are_rejected_in_all_rendered_inputs(self):
        files=['01-porcentagens.md','revisao-porcentagens.md','contexto-questoes.md']
        for file in files:
            for target in ['../outside.svg','%2e%2e%2foutside.svg','https://example.invalid/image.png','https%3A%2F%2Fexample.invalid/x.svg','//example.invalid/image.png','file:///tmp/image.svg','data:image/png;base64,AAAA']:
                with self.subTest(file=file,target=target):
                    path=self.folder/file;previous=path.read_text()
                    self.append(file,'![Descrição]('+target+')')
                    with self.assertRaisesRegex(ValueError,'Imagem'):
                        self.load()
                    path.write_text(previous)

    def test_reference_and_angle_image_syntax_cannot_bypass_validation(self):
        for fragment in ['![Descrição][externa]\n\n[externa]: ../outside.svg "Legenda"',
                         '![Descrição](<../outside.svg> "Legenda")']:
            with self.subTest(fragment=fragment):
                path=self.folder/'revisao-porcentagens.md';previous=path.read_text()
                self.append(path.name,fragment)
                with self.assertRaisesRegex(ValueError,'Imagem'):
                    self.load()
                path.write_text(previous)

    def test_code_examples_are_not_treated_as_rendered_images(self):
        self.append('01-porcentagens.md','```markdown\n![exemplo](../outside.svg)\n```\n\n`![exemplo](https://example.invalid/x)`')
        self.load()
        self.assertEqual(markdown_images('`![exemplo](../outside.svg)`'),())

    def test_images_in_question_comments_and_scope_are_also_checked(self):
        self.edit('questoes.json',lambda rows:rows[0]['comentarios'].update(A='![Comentário](../outside.svg)'))
        with self.assertRaisesRegex(ValueError,'Imagem'):
            self.load()
        shutil.copyfile(ROOT/'materials/matematica-basica/questoes.json',self.folder/'questoes.json')
        self.edit('material.json',lambda config:config.update(scope='![Escopo](../outside.svg)'))
        with self.assertRaisesRegex(ValueError,'Imagem'):
            self.load()

    def test_symlink_cannot_escape_material_folder(self):
        (self.folder/'linked.svg').symlink_to(self.folder.parent/'outside.svg')
        self.append('contexto-questoes.md','![Descrição](linked.svg)')
        with self.assertRaisesRegex(ValueError,'fora da pasta'):
            self.load()

    def test_missing_description_and_undeclared_internal_file_are_rejected(self):
        shutil.copyfile(self.folder.parent/'outside.svg',self.folder/'inside.svg')
        for fragment in ['![Descrição](inside.svg)','![](figuras/fatores.svg)']:
            path=self.folder/'contexto-questoes.md';previous=path.read_text()
            self.append(path.name,fragment)
            with self.assertRaisesRegex(ValueError,'Imagem'):
                self.load()
            path.write_text(previous)

    def add_figure(self, file='figuras/extra.svg'):
        (self.folder/file).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="40"><text x="2" y="25">INSIDE-FIXTURE</text></svg>')
        self.edit('figuras.json',lambda rows:rows.append(dict(id='FIG-003',file=file,caption='Figura original de teste',alt='Marcador local de teste',rights='original-projeto',source='original-projeto')))

    def test_declared_revision_only_and_context_only_figures_are_hashed(self):
        self.add_figure()
        self.append('revisao-porcentagens.md','![Descrição](figuras/extra.svg)')
        self.append('contexto-questoes.md','![Descrição][local]\n\n[local]: figuras/extra.svg "Legenda"')
        data=self.load()
        self.assertIn(self.folder/'figuras/extra.svg',data['inputs'])
        for kind in ['revisao','caderno','simulado']:
            self.assertIn('figuras/extra.svg',data['image_usage'][kind])
        output=Path(self.temp.name)/'out'
        report=publish(data,output,'revisao')
        self.assertIn('INSIDE-FIXTURE',(output/'revisao.html').read_text())
        self.assertTrue(report['inputs']['figuras/extra.svg'])

    def test_title_and_spaces_in_local_image_syntax_are_supported(self):
        self.add_figure('figuras/extra diagram.svg')
        self.append('revisao-porcentagens.md','![Descrição com **ênfase**](<figuras/extra diagram.svg> "Legenda")')
        self.assertIn('figuras/extra diagram.svg',self.load()['image_usage']['revisao'])

    def test_publisher_rechecks_changed_inputs_in_each_format_before_writing(self):
        for kind,file in [('apostila','01-porcentagens.md'),('caderno','contexto-questoes.md'),('simulado','contexto-questoes.md'),('revisao','revisao-porcentagens.md')]:
            with self.subTest(kind=kind):
                data=self.load();path=self.folder/file;previous=path.read_text()
                self.append(file,'![Descrição](../outside.svg)')
                output=Path(self.temp.name)/kind
                with self.assertRaisesRegex(ValueError,'Imagem'):
                    publish(data,output,kind)
                self.assertFalse(output.exists())
                path.write_text(previous)

    def test_svg_cannot_introduce_unhashed_nested_resources_or_scripts(self):
        fragments=['<image href="../outside.svg"/>','<image href="https://example.invalid/x"/>',
                   '<style>rect{fill:url(https://example.invalid/x)}</style>',
                   '<style>@import "https://example.invalid/x";</style>',
                   '<script>bad()</script>','<rect onload="bad()"/>',
                   '<style>rect{fill:\\75rl(https://example.invalid/x)}</style>']
        for fragment in fragments:
            with self.subTest(fragment=fragment):
                with self.assertRaisesRegex(ValueError,'SVG'):
                    validate_svg('<svg xmlns="http://www.w3.org/2000/svg">'+fragment+'</svg>')
        validate_svg('<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="x"/></defs><rect fill="url(#x)"/></svg>')

    def test_in_memory_figure_addition_requires_reloading_hashed_inputs(self):
        data=self.load()
        self.add_figure();self.append('contexto-questoes.md','![Descrição](figuras/extra.svg)')
        data['figures']=json.loads((self.folder/'figuras.json').read_text())
        with self.assertRaisesRegex(ValueError,'inventário de hashes'):
            publish(data,Path(self.temp.name)/'out','caderno')

    def test_code_palette_meets_small_text_contrast_on_the_code_background(self):
        theme=json.loads((ROOT/'styles/code-accessible.theme').read_text())
        colors=[theme['line-number-color']]+[s['text-color']for s in theme['text-styles'].values()if s['text-color']]
        for color in colors:
            with self.subTest(color=color):
                rgb=[int(color[i:i+2],16)for i in (1,3,5)]
                self.assertGreaterEqual(contrast(rgb,[244,247,248]),4.5)

    @unittest.skipUnless(importlib.util.find_spec('playwright') and importlib.util.find_spec('pymupdf'), 'PDF/browser optional toolchain')
    def test_highlighted_sql_has_contrast_and_negative_tabindex_anchors_do_not_break_keyboard_order(self):
        self.append('01-porcentagens.md','```sql\nSELECT 1 AS numero;\n```')
        output=Path(self.temp.name)/'accessible'
        publish(self.load(),output,'apostila',pdf=True)
        self.assertIn('tabindex="-1"',(output/'apostila.html').read_text())
        result=inspect_accessibility(output/'apostila.html',output/'apostila.pdf')
        self.assertTrue(result['passed'],result['errors'])
        self.assertEqual(result['html']['keyboard_links'],result['html']['keyboard_links_expected'])


class FigureEditionTests(unittest.TestCase):
    setUp = ResourceTests.setUp
    append = ResourceTests.append
    edit = ResourceTests.edit
    load = ResourceTests.load
    add_figure = ResourceTests.add_figure
    def compare_changed(self, change):
        original=self.load();newfolder=Path(self.temp.name)/'new'
        shutil.copytree(self.folder,newfolder)
        change(newfolder)
        path=newfolder/'material.json';config=json.loads(path.read_text());config['version']='0.6.0';path.write_text(json.dumps(config))
        return comparison(original,load_material(path),'Mudança sintética de figura para regressão')

    def test_figure_bytes_signal_the_dependent_chapter_and_questions(self):
        def change(folder):
            p=folder/'figuras/fatores.svg';p.write_text(p.read_text().replace('240','250'))
        report=self.compare_changed(change)
        self.assertEqual(report['changed_figures'],['FIG-001'])
        self.assertIn('cap-percentuais',report['chapters_to_review'])
        self.assertNotIn('cap-medias',report['chapters_to_review'])
        self.assertIn('Q-AUT-001',report['affected_questions'])
        self.assertEqual(report['figure_review_policy'],'resolved-chapter-uses')

    def test_figure_caption_change_also_signals_review(self):
        def change(folder):
            p=folder/'figuras.json';rows=json.loads(p.read_text());rows[0]['caption']='Legenda corrigida de teste';p.write_text(json.dumps(rows))
        report=self.compare_changed(change)
        self.assertEqual(report['changed_figures'],['FIG-001'])
        self.assertIn('cap-percentuais',report['chapters_to_review'])

    def test_context_only_figure_uses_explicit_conservative_review(self):
        self.add_figure();self.append('contexto-questoes.md','![Descrição](figuras/extra.svg)')
        def change(folder):
            p=folder/'figuras/extra.svg';p.write_text(p.read_text().replace('INSIDE-FIXTURE','CHANGED-FIXTURE'))
        report=self.compare_changed(change)
        self.assertEqual(report['figure_review_policy'],'conservative-all-chapters')
        self.assertEqual(len(report['chapters_to_review']),3)

    def test_removed_figure_keeps_its_previous_chapter_in_the_review(self):
        def change(folder):
            p=folder/'figuras.json';rows=json.loads(p.read_text());rows.pop(0);p.write_text(json.dumps(rows))
            p=folder/'01-porcentagens.md';p.write_text('\n'.join(line for line in p.read_text().splitlines() if 'figuras/fatores.svg' not in line))
            (folder/'figuras/fatores.svg').unlink()
        report=self.compare_changed(change)
        self.assertIn('FIG-001',report['changed_figures'])
        self.assertIn('cap-percentuais',report['chapters_to_review'])

    def test_shared_reference_defined_in_another_chapter_keeps_each_owner(self):
        self.add_figure()
        self.append('01-porcentagens.md','![Direta](figuras/extra.svg)')
        self.append('02-medias.md','![Referência][shared]')
        self.append('03-probabilidade.md','[shared]: figuras/extra.svg')
        def change(folder):
            p=folder/'figuras/extra.svg';p.write_text(p.read_text().replace('INSIDE-FIXTURE','CHANGED-FIXTURE'))
        report=self.compare_changed(change)
        self.assertIn('cap-percentuais',report['chapters_to_review'])
        self.assertIn('cap-medias',report['chapters_to_review'])

    def test_same_figure_in_chapter_and_context_still_requests_conservative_review(self):
        self.add_figure()
        self.append('01-porcentagens.md','![Descrição](figuras/extra.svg)')
        self.append('contexto-questoes.md','![Descrição](figuras/extra.svg)')
        def change(folder):
            p=folder/'figuras/extra.svg';p.write_text(p.read_text().replace('INSIDE-FIXTURE','CHANGED-FIXTURE'))
        report=self.compare_changed(change)
        self.assertEqual(report['figure_review_policy'],'conservative-all-chapters')
        self.assertEqual(len(report['chapters_to_review']),3)


if __name__=='__main__':
    unittest.main()
