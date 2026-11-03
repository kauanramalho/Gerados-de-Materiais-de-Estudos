"""Synthetic request metadata tests; no fixture claims real research or full edital coverage."""
import base64
from copy import deepcopy
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from material import load_material
from pedido import main
from request import initial_request, read_request, request_errors, scope_errors, instruction_inventory


def complete_fixture():
    data = deepcopy(load_material(ROOT/'materials/dataprev-sql/material.json'))
    request = initial_request('fixture', 'Vou fazer Concurso Exemplo; quero apostila.', 'apostila')
    request['concurso'].update(orgao='Órgão fictício', cargo='Cargo de teste', ano=2027, banca='Banca de teste')
    request['edital'].update(url='https://concurso.example/edital.pdf', versao='fixture', sha256='a'*64,
                              conferido_em=date.today().isoformat(), retificacoes_verificadas=True)
    for row in request['contexto']:
        row['lido_em'] = date.today().isoformat()
    for row in request['pesquisa']:
        row.update(estado='verificado', relato='Dado sintético exclusivo do teste de contrato.',
                   evidencias=[dict(referencia='https://concurso.example/edital.pdf', localizador='fixture',
                                    conferido_em=date.today().isoformat(), oficial=True)])
    request['lacunas'] = []
    for index, row in enumerate(data['coverage']):
        ident = 'E'+str(index+1)
        row.update(edital_id=ident, status='completo', limits='Metadados sintéticos para testar o contrato.')
        request['programa'].append(dict(id=ident, texto=row['edital_item'], materia='fixture', localizador='fixture'))
        request['escopo']['selecao'].append(ident)
    data['sources'].append(dict(url=request['edital']['url'], sha256='a'*64))
    data['request'] = request
    return data


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.data = complete_fixture()
        self.request = self.data['request']

    def errors(self):
        return '\n'.join(scope_errors(self.data, 'apostila', final=True))

    def test_complete_metadata_passes_both_supported_formats(self):
        self.assertEqual(self.errors(), '')
        self.request['tipo'] = 'caderno'
        self.assertEqual(scope_errors(self.data, 'caderno', final=True), [])

    def test_bare_text_is_accepted_without_inventing_identity(self):
        request = initial_request('novo', 'Quero a apostila do concurso X.', 'apostila')
        self.assertIsNone(request['concurso']['banca'])
        self.assertEqual(request['escopo']['tipo'], 'concurso')
        self.assertTrue(request_errors(request))

    def test_a_pilot_cannot_be_marked_final_without_a_request(self):
        self.data['request'] = None
        self.assertIn('pedido vinculado', self.errors())

    def test_wrong_output_format_is_rejected(self):
        self.assertIn('Formato solicitado', '\n'.join(scope_errors(self.data, 'caderno', True)))

    def test_missing_or_partial_program_item_blocks_final(self):
        self.data['coverage'][0]['status'] = 'parcial'
        self.assertIn('ainda sem conteúdo', self.errors())
        self.data['coverage'].pop(0)
        self.assertIn('Item solicitado omitido: E1', self.errors())

    def test_a_complete_contest_cannot_silently_become_a_subset(self):
        self.request['escopo']['selecao'].pop()
        self.assertIn('não pode reduzir', self.errors())
        self.request['escopo']['tipo'] = 'materia'
        self.assertNotIn('não pode reduzir', '\n'.join(request_errors(self.request)))

    def test_unrelated_coverage_and_duplicate_ids_are_rejected(self):
        self.data['coverage'][0]['edital_id'] = 'OUTRO-CONCURSO'
        self.assertIn('fora do escopo', self.errors())
        self.request['programa'].append(deepcopy(self.request['programa'][0]))
        self.assertIn('programa duplicado', self.errors())

    def test_copied_label_cannot_mask_wrong_program_text(self):
        self.data['coverage'][0]['edital_item'] = 'Texto de outro edital'
        self.assertIn('Texto da cobertura diverge', self.errors())

    def test_unmapped_question_or_wrong_objective_is_rejected(self):
        question = deepcopy(self.data['questions'][0]); question['id'] = 'Q-FORA'
        self.data['questions'].append(question)
        self.assertIn('Questão fora da cobertura', self.errors())
        self.data['questions'][0]['objetivo'] = 'OBJ-FORA'
        self.assertIn('objetivo errado', self.errors())

    def test_unrelated_chapter_and_empty_practice_are_rejected(self):
        self.data['config']['chapters'][0]['objectives'].append('OBJ-EXTRA')
        self.assertIn('Capítulo com objetivo fora', self.errors())
        self.data['coverage'][0]['questions'] = []
        self.assertIn('ainda sem conteúdo/prática completos', self.errors())

    def test_missing_profile_or_wrong_edital_hash_is_rejected(self):
        self.data['config'].pop('profile')
        self.assertIn('perfil da banca', self.errors())
        self.request['edital']['sha256'] = 'b'*64
        self.assertIn('não corresponde às fontes/hash', self.errors())

    def test_missing_or_unsupported_research_does_not_pass(self):
        self.request['pesquisa'] = self.request['pesquisa'][:-1]
        self.assertIn('Pesquisa pendente: acervo', self.errors())
        self.request['pesquisa'][0]['evidencias'][0]['oficial'] = False
        self.assertIn('sem referência oficial', self.errors())

    def test_proofs_not_found_require_search_evidence_and_an_explicit_limit(self):
        row = next(r for r in self.request['pesquisa'] if r['etapa'] == 'provas-alvo')
        row['estado'] = 'nao-localizado'
        self.assertIn('limitação explícita', self.errors())
        self.request['lacunas'] = ['Prova-alvo não localizada na consulta registrada; autorais identificadas.']
        self.assertEqual(self.errors(), '')
        row['evidencias'] = []
        self.assertIn('Pesquisa sem evidência', self.errors())

    def test_unread_and_changed_instructions_force_rereading(self):
        self.request['contexto'][0]['lido_em'] = None
        self.assertIn('Instrução não lida', self.errors())
        self.request['contexto'][0]['lido_em'] = date.today().isoformat()
        self.request['contexto'][0]['sha256'] = '0'*64
        self.assertIn('alterada', self.errors())
        paths = {r['arquivo'] for r in instruction_inventory()}
        self.assertEqual(len([p for p in paths if p.endswith('/SKILL.md')]), 17)

    def test_no_artificial_maximum_for_program_items(self):
        item = self.request['programa'][0]
        self.request['programa'] = [{**item, 'id': 'E'+str(i)} for i in range(1500)]
        self.request['escopo']['selecao'] = [i['id'] for i in self.request['programa']]
        self.assertEqual(request_errors(self.request), [])

    def test_bound_request_reaches_final_cli_preflight(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)/'material'
            shutil.copytree(ROOT/'materials/dataprev-sql', folder)
            config = deepcopy(self.data['config']); config['pedido'] = 'pedido.json'
            sources = deepcopy(self.data['sources'])
            sources[-1].update(id='FIXTURE', title='Fonte sintética de teste', checked_on=date.today().isoformat(),
                               locator='fixture de contrato', rights='somente referência sintética')
            for name, value in [('material.json', config), ('pedido.json', self.request),
                                ('cobertura.json', self.data['coverage']), ('fontes.json', sources)]:
                (folder/name).write_text(json.dumps(value), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT/'scripts/build_material.py'),
                                     str(folder/'material.json'), '--check', '--final'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Pré-validação aprovada', result.stdout)


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        # A tiny fixture tests attachment preservation, not OCR or actual contest research.
        self.image = self.folder/'print.png'
        self.image.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j1ioAAAAASUVORK5CYII='))

    def test_text_intake_and_safe_resume_without_overwrite(self):
        args = ['iniciar', '--id', 'teste', '--texto', 'Quero apostila do concurso X', '--output', str(self.folder/'out')]
        self.assertEqual(main(args), 0)
        p = self.folder/'out/pedido.json'; original = p.read_bytes()
        self.assertEqual(read_request(p)['entrada']['texto'], 'Quero apostila do concurso X')
        self.assertEqual(main(args), 1)
        self.assertEqual(p.read_bytes(), original)

    def test_photo_and_print_preserve_bytes_and_require_visual_confirmation(self):
        for origin in ['foto', 'print']:
            dest = self.folder/origin
            self.assertEqual(main(['iniciar', '--id', origin, '--imagem', str(self.image), '--origem', origin,
                                   '--tipo', 'caderno', '--output', str(dest)]), 0)
            request = read_request(dest/'pedido.json')
            self.assertEqual((dest/request['entrada']['imagem']['arquivo']).read_bytes(), self.image.read_bytes())
            self.assertIn('transcrição conferida', '\n'.join(request_errors(request)))
            (dest/request['entrada']['imagem']['arquivo']).write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Hash da imagem'):
                read_request(dest/'pedido.json')

    def test_image_path_cannot_escape_private_request_folder(self):
        request = initial_request('teste', 'x', 'apostila', 'print', dict(arquivo='../print.png',
                                  sha256=sha256(self.image.read_bytes()).hexdigest(), transcricao='', conferida=False))
        dest=self.folder/'out';dest.mkdir();(dest/'pedido.json').write_text(json.dumps(request))
        with self.assertRaisesRegex(ValueError, 'fora da pasta'):
            read_request(dest/'pedido.json')

    def test_empty_intake_fails_and_cli_cannot_finalize_a_partial_pilot(self):
        self.assertEqual(main(['iniciar', '--id', 'vazio', '--output', str(self.folder/'out')]), 1)
        result = subprocess.run([sys.executable, str(ROOT/'scripts/build_material.py'),
                                 str(ROOT/'materials/dataprev-sql/material.json'), '--check', '--final'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('pedido vinculado', result.stderr)


if __name__ == '__main__':
    unittest.main()
