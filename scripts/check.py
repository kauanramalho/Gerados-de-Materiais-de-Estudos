"""Validate documentation links, skill contracts, sample data and optional HTML."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote
from integrity import validate_questions, validate_navigation

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
    if len(skills) != 12:
        errors.append(f'Esperadas 12 skills, encontradas {len(skills)}')
    for skill in skills:
        content = skill.read_text(encoding='utf-8')
        for field in ('name:', 'description:', '## Entradas', '## Procedimento', '## Saídas', '## Validação'):
            if field not in content:
                errors.append(f'{skill.parent.name}: contrato incompleto: {field}')
    questions = json.loads((ROOT / 'examples/redes/questoes.json').read_text(encoding='utf-8'))
    errors += validate_questions(questions)
    for schema in (ROOT / 'schemas').glob('*.json'):
        data = json.loads(schema.read_text(encoding='utf-8'))
        if data.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            errors.append(f'Schema sem versão: {schema.name}')
    html = ROOT / 'build/amostra.html'
    if html.exists():
        errors += validate_navigation(html.read_text(encoding='utf-8'), questions)
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK: {len(files)} Markdowns, 12 skills, {len(questions)} questões e contratos JSON; '
          + ('HTML conferido.' if html.exists() else 'HTML ainda não gerado.'))
    print('Limite: existência de referências não comprova conteúdo, direitos ou qualidade pedagógica.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
