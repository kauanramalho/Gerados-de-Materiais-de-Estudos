"""Validate images with the same Markdown reader used by the PDF publisher."""
from functools import lru_cache
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


def local_path(folder, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError('Referência local deve ser um caminho relativo não vazio')
    resolved = (Path(folder) / relative).resolve()
    if not resolved.is_relative_to(Path(folder).resolve()) or not resolved.is_file():
        raise ValueError(f'Arquivo ausente ou fora da pasta do material: {relative}')
    return resolved


def _alt_text(node):
    if isinstance(node, list):
        return ''.join(_alt_text(value) for value in node)
    if not isinstance(node, dict):
        return ''
    kind, value = node.get('t'), node.get('c')
    if kind == 'Str':
        return value
    if kind in ('Space', 'SoftBreak', 'LineBreak'):
        return ' '
    if kind in ('Code', 'Math'):
        return value[-1]
    return _alt_text(value)


@lru_cache(maxsize=64)
def markdown_document(markdown):
    """Use the publisher's reader without fetching or embedding resources."""
    if not shutil.which('pandoc'):
        raise ValueError('Pandoc é necessário para validar imagens e gerar materiais')
    result = subprocess.run(['pandoc', '--from=markdown-raw_html', '--to=json'],
                            input=markdown, text=True, capture_output=True)
    if result.returncode:
        raise ValueError('Não foi possível analisar as imagens do Markdown com Pandoc')
    return json.loads(result.stdout)


def image_nodes(document):
    """Read only actual Image nodes, never Markdown-looking code examples."""
    images = []

    def walk(node):
        if isinstance(node, dict):
            if node.get('t') == 'Image':
                _, alternative, target = node['c']
                images.append((target[0], _alt_text(alternative)))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(document)
    return tuple(images)


@lru_cache(maxsize=64)
def markdown_images(markdown):
    return image_nodes(markdown_document(markdown))


def image_path(folder, target):
    decoded = unquote(target)
    parsed = urlsplit(decoded)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or '\\' in decoded:
        raise ValueError('Imagem deve usar arquivo local declarado, sem URL remota ou referência externa')
    try:
        return local_path(folder, parsed.path)
    except ValueError as error:
        raise ValueError('Imagem ausente ou fora da pasta do material: '+target) from error


@lru_cache(maxsize=64)
def validate_svg(text):
    """Standalone SVGs cannot silently introduce unhashed or executable dependencies."""
    if re.search(r'<!\s*(DOCTYPE|ENTITY)\b', text, re.I):
        raise ValueError('Imagem SVG deve ser independente de entidades externas')
    try:
        tree = ElementTree.fromstring(text)
    except ElementTree.ParseError as error:
        raise ValueError('Imagem SVG inválida') from error
    for node in tree.iter():
        tag = node.tag.rsplit('}', 1)[-1].lower()
        if tag in ('script', 'foreignobject'):
            raise ValueError('Imagem SVG não pode conter conteúdo ativo')
        for key, value in node.attrib.items():
            attribute = key.rsplit('}', 1)[-1].lower()
            if attribute.startswith('on'):
                raise ValueError('Imagem SVG não pode conter eventos executáveis')
            if attribute in ('href', 'src') and value.strip() and not value.strip().startswith('#'):
                raise ValueError('Imagem SVG não pode carregar recursos externos')
        styles = list(node.attrib.values()) + ([node.text or ''] if tag == 'style' else [])
        for value in styles:
            if '\\' in value:
                raise ValueError('Imagem SVG não pode ocultar referências em escapes CSS')
            if re.search(r'@import\b', value, re.I):
                raise ValueError('Imagem SVG não pode importar estilos externos')
            for reference in re.findall(r'url\s*\((.*?)\)', value, re.I):
                if not reference.strip(' \t\r\n\"\x27').startswith('#'):
                    raise ValueError('Imagem SVG não pode carregar recursos externos')


def validate_images(markdown, folder, figures):
    declared = {local_path(folder, figure['file']) for figure in figures}
    used = set()
    for target, alternative in markdown_images(markdown):
        path = image_path(folder, target)
        if not alternative.strip() or path not in declared:
            raise ValueError('Imagem sem descrição ou fora do manifesto de figuras: '+target)
        if path.suffix.lower() == '.svg':
            validate_svg(path.read_text(encoding='utf-8'))
        used.add(path.relative_to(Path(folder).resolve()).as_posix())
    return used
