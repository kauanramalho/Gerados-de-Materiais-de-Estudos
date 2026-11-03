"""Prepare a private request from text or an image; never invent contest identity."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys

from request import initial_request, read_request, request_errors, instruction_inventory


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    start = sub.add_parser('iniciar')
    start.add_argument('--id', required=True)
    start.add_argument('--texto', default='')
    start.add_argument('--imagem', type=Path)
    start.add_argument('--origem', choices=['texto', 'foto', 'print'], default='texto')
    start.add_argument('--tipo', choices=['apostila', 'caderno', 'simulado', 'revisao'], default='apostila')
    start.add_argument('--output', type=Path, required=True)
    check = sub.add_parser('verificar')
    check.add_argument('pedido', type=Path)
    sub.add_parser('contexto')
    args = parser.parse_args(argv)
    try:
        if args.command == 'contexto':
            print(json.dumps(instruction_inventory(), ensure_ascii=False, indent=2))
            return 0
        if args.command == 'verificar':
            errors = request_errors(read_request(args.pedido))
            if errors:
                raise ValueError('\n'.join(errors))
            print('Pedido estruturalmente pronto; revisão factual das evidências continua obrigatória.')
            return 0
        if not args.texto.strip() and not args.imagem:
            raise ValueError('Forneça texto ou imagem')
        if args.origem != 'texto' and not args.imagem:
            raise ValueError('Foto/print exige --imagem')
        if args.output.exists() and any(args.output.iterdir()):
            raise ValueError('Pasta de pedido não está vazia; retome os arquivos existentes')
        image = None
        if args.imagem:
            raw = args.imagem.read_bytes()
            valid = raw.startswith(b'\x89PNG\r\n\x1a\n') or raw.startswith(b'\xff\xd8\xff') or (raw.startswith(b'RIFF') and raw[8:12] == b'WEBP')
            if not valid:
                raise ValueError('Imagem precisa ser PNG, JPEG ou WebP; converter outros formatos antes')
            image = {'arquivo': 'entrada'+args.imagem.suffix.lower(), 'sha256': sha256(raw).hexdigest(),
                     'transcricao': '', 'conferida': False}
        value = initial_request(args.id, args.texto, args.tipo, args.origem, image)
        args.output.mkdir(parents=True, exist_ok=True)
        if image:
            shutil.copyfile(args.imagem, args.output/image['arquivo'])
        (args.output/'pedido.json').write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print('Pedido registrado em '+str(args.output/'pedido.json')+'. Pesquisa e leitura pelo agente pendentes.')
        return 0
    except (ValueError, OSError, KeyError) as error:
        print('Falha no pedido: '+str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
