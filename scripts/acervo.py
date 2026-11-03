"""Importar, buscar e versionar questões locais com proveniência."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

from catalog import import_material, search, history, export_catalog


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, required=True, help='Banco local, preferencialmente em build/ ou work/')
    commands = parser.add_subparsers(dest='command', required=True)
    ingest = commands.add_parser('importar')
    ingest.add_argument('manifest', type=Path)
    ingest.add_argument('--aceitar-revisoes', action='store_true')
    ingest.add_argument('--motivo')
    find = commands.add_parser('buscar')
    find.add_argument('--banca')
    find.add_argument('--ano', type=int)
    find.add_argument('--assunto')
    find.add_argument('--origem', choices=['REAL', 'ADAPTADA', 'AUTORAL'])
    find.add_argument('--status', choices=['preliminar', 'definitivo', 'retificado', 'anulada'])
    past = commands.add_parser('historico')
    past.add_argument('key')
    export = commands.add_parser('exportar')
    export.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'importar':
            result = import_material(args.db, args.manifest, args.aceitar_revisoes, args.motivo)
        elif args.command == 'buscar':
            result = search(args.db, args.banca, args.ano, args.assunto, args.origem, args.status)
        elif args.command == 'historico':
            result = history(args.db, args.key)
        else:
            result = export_catalog(args.db, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, sqlite3.Error) as error:
        print(f'Falha no acervo: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
