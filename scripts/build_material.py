"""Publish an agent-authored study material from a local manifest."""
import argparse
from pathlib import Path
import sys
from material import load_material, publish


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--kind', choices=['apostila', 'caderno'], default='apostila')
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--check', action='store_true', help='Validate sources, paths and coverage without exporting')
    args = parser.parse_args()
    try:
        data = load_material(args.manifest)
        if args.check:
            print(f'Pré-validação aprovada: {data["config"]["id"]}; {len(data["questions"])} questões.')
            return 0
        folder = args.output or Path('build') / data['config']['id']
        report = publish(data, folder, args.kind, args.pdf)
        print(f'Material gerado: {folder.resolve()}')
        print(f'Questões: {report["questions"]}; navegação HTML aprovada.')
        if 'pdf' in report:
            print(f'PDF: {report["pdf"]["pages"]} páginas; '
                  f'{report["pdf"]["internal_links"]} links internos; '
                  f'{report["pdf"]["toc_entries"]} entradas de sumário conferidas.')
        print('Revisão técnica e pedagógica depende de evidência editorial separada.')
        return 0
    except (ValueError, KeyError, OSError) as error:
        print(f'Falha de pré-validação/publicação: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
