"""Validate documentation links, skill contracts, sample data and optional HTML."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote
from integrity import validate_questions, validate_navigation
from material import load_material
from contracts import require_schema, validator

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    files = [p for p in ROOT.rglob('*.md') if not any(
        x in p.relative_to(ROOT).parts for x in ('.git', 'build', 'work', 'private'))]
    for path in files:
        content = path.read_text(encoding='utf-8')
        for link in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', content):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                continue
            target = unquote(link.split('#', 1)[0])
            if target and not (path.parent / target).exists():
                errors.append(f'{path.relative_to(ROOT)}: arquivo ausente: {target}')
    skills = list((ROOT / '.agents/skills').glob('*/SKILL.md'))
    inventory = (ROOT / 'docs/skills.md').read_text(encoding='utf-8')
    listed = set(re.findall(r'\.\./\.agents/skills/([^/]+)/SKILL\.md', inventory))
    actual = {p.parent.name for p in skills}
    if actual != listed:
        errors.append(f'Inventário de skills divergente: arquivos={sorted(actual)}, índice={sorted(listed)}')
    for skill in skills:
        content = skill.read_text(encoding='utf-8')
        for field in ('name:', 'description:', '## Entradas', '## Procedimento', '## Saídas', '## Validação'):
            if field not in content:
                errors.append(f'{skill.parent.name}: contrato incompleto: {field}')
    questions = json.loads((ROOT / 'examples/redes/questoes.json').read_text(encoding='utf-8'))
    errors += validate_questions(questions)
    for i, question in enumerate(questions):
        try:
            require_schema(question, 'questao.schema.json', f'amostra[{i}]')
        except ValueError as error:
            errors.append(str(error))
    for schema in (ROOT / 'schemas').glob('*.json'):
        data = json.loads(schema.read_text(encoding='utf-8'))
        if data.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            errors.append(f'Schema sem versão: {schema.name}')
        validator(schema.name)
    materials = list((ROOT / 'materials').glob('*/material.json'))
    for manifest in materials:
        try:
            load_material(manifest)
        except (ValueError, KeyError, OSError) as error:
            errors.append(f'{manifest.relative_to(ROOT)}: {error}')
    html = ROOT / 'build/amostra.html'
    if html.exists():
        errors += validate_navigation(html.read_text(encoding='utf-8'), questions)
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK: {len(files)} Markdowns, {len(skills)} skills, {len(questions)} questões e contratos JSON; '
          + ('HTML conferido.' if html.exists() else 'HTML ainda não gerado.'))
    print('Limite: existência de referências não comprova conteúdo, direitos ou qualidade pedagógica.')
    print(f'Manifestos de materiais conferidos: {len(materials)}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
