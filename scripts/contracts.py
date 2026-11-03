"""Validate project-owned JSON contracts without fetching external schemas."""
from functools import lru_cache
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@lru_cache
def validator(filename):
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as error:
        raise ValueError('Instale as dependências: pip install -r requirements-core.txt') from error
    schema = json.loads((ROOT / 'schemas' / filename).read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def schema_errors(value, filename, label):
    messages = []
    for error in sorted(validator(filename).iter_errors(value),
                        key=lambda e: tuple(str(p) for p in e.absolute_path)):
        path = label + ''.join(f'[{p}]' if isinstance(p, int) else f'.{p}'
                               for p in error.absolute_path)
        rule, expected = error.validator, error.validator_value
        if rule == 'type':
            detail = f'tipo esperado: {expected}'
        elif rule == 'required':
            missing = [k for k in expected if k not in error.instance]
            detail = 'campos obrigatórios ausentes: ' + ', '.join(missing)
        elif rule == 'additionalProperties':
            unknown = set(error.instance) - set(error.schema.get('properties', {}))
            detail = 'campos não permitidos: ' + ', '.join(sorted(unknown))
        elif rule == 'format':
            detail = f'formato inválido; esperado: {expected}'
        elif rule == 'enum':
            detail = 'valor fora das opções permitidas'
        else:
            detail = f'regra {rule} não atendida'
        messages.append(f'{path}: {detail}')
        if len(messages) == 12:
            messages.append('Corrija estes campos e execute a validação novamente.')
            break
    return messages


def require_schema(value, filename, label):
    errors = schema_errors(value, filename, label)
    if errors:
        raise ValueError('\n'.join(errors))
