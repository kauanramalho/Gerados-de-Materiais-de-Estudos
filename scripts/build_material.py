"""Publish an agent-authored study material from a local manifest."""
import argparse
from pathlib import Path
import sys
from material import load_material, publish
from request import require_delivery
from formats import prepare_format


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--kind', choices=['apostila', 'caderno', 'simulado', 'revisao'], default='apostila')
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--check', action='store_true', help='Validate sources, paths and coverage without exporting')
    parser.add_argument('--final', action='store_true', help='Exigir pedido, pesquisa e cobertura integral do escopo solicitado')
    args = parser.parse_args()
    try:
        data = load_material(args.manifest)
        if args.check:
            require_delivery(prepare_format(data, args.kind), args.kind, args.final)
            print(f'Pré-validação aprovada: {data["config"]["id"]}; {len(data["questions"])} questões.')
            return 0
        folder = args.output or Path('build') / data['config']['id']
        report = publish(data, folder, args.kind, args.pdf, args.final)
        print(f'Material gerado: {folder.resolve()}')
        print(f'Questões: {report["questions"]}; navegação HTML aprovada.')
        if 'pdf' in report:
            print(f'PDF: {report["pdf"]["pages"]} páginas; '
                  f'{report["pdf"]["internal_links"]} links internos; '
                  f'{report["pdf"]["toc_entries"]} entradas de sumário conferidas.')
        print('Revisão técnica e pedagógica depende de evidência editorial separada.')
        if not args.final:
            print('Build de referência/rascunho; não certifica entrega final de um pedido de concurso.')
        return 0
    except (ValueError, KeyError, OSError) as error:
        print(f'Falha de pré-validação/publicação: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
