"""Verify approved educational SQL fixtures in fresh, in-memory databases."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys
from material import local_path


def check_cases(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text(encoding='utf-8'))
    setup = local_path(path.parent, data['setup']).read_text(encoding='utf-8')
    results = []
    ids = [case['id'] for case in data['cases']]
    if len(set(ids)) != len(ids):
        raise ValueError('Casos SQL com IDs duplicados')
    for case in data['cases']:
        connection = sqlite3.connect(':memory:')
        connection.enable_load_extension(False)
        connection.set_authorizer(lambda action, *_: sqlite3.SQLITE_DENY
                                  if action in (sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH)
                                  else sqlite3.SQLITE_OK)
        try:
            connection.executescript(setup)
            if connection.execute('PRAGMA foreign_keys').fetchone()[0] != 1:
                raise ValueError('A fixture deve habilitar chaves estrangeiras')
            if case.get('before_sql'):
                connection.executescript(case['before_sql'])
            try:
                rows = [list(row) for row in connection.execute(case['sql']).fetchall()]
                ok = 'expect_error' not in case and rows == case['expected']
                results.append({'id': case['id'], 'passed': ok, 'actual': rows})
            except sqlite3.IntegrityError:
                results.append({'id': case['id'], 'passed': case.get('expect_error') == 'integrity',
                                'actual': 'integrity-error'})
        finally:
            connection.close()
    return {'engine': 'SQLite ' + sqlite3.sqlite_version, 'cases': results,
            'passed': all(row['passed'] for row in results)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cases', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        result = check_cases(args.cases)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        for case in result['cases']:
            print(('OK' if case['passed'] else 'FALHA') + ': ' + case['id'])
        return 0 if result['passed'] else 1
    except (ValueError, KeyError, OSError, sqlite3.Error) as error:
        print(f'Falha de verificação SQL: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
