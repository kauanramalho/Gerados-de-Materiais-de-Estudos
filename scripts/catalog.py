"""Local question catalog: stable identity, explicit revisions and safe exports."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
import unicodedata

from material import load_material


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def folded(value):
    value = unicodedata.normalize('NFKD', str(value)).casefold()
    return ' '.join(''.join(c for c in value if not unicodedata.combining(c)).split())


def content_text(value):
    # Preserve case, punctuation, numbers and operators: normalization is not adaptation.
    return ' '.join(unicodedata.normalize('NFC', str(value)).split())


def question_key(q):
    if q['origem'] == 'AUTORAL':
        identity = [content_text(q['enunciado']),
                    {k: content_text(v) for k, v in q['alternativas'].items()}]
    else:
        source = q['fonte_original']
        identity = [folded(source[k]) for k in ('banca', 'orgao', 'cargo', 'ano', 'caderno', 'numero')]
        if q['origem'] == 'ADAPTADA':
            identity += [content_text(q['enunciado']), q['alternativas']]
    return q['origem'].lower() + '-' + digest(identity)


def public_record(q):
    fields = ('origem', 'formato', 'direitos', 'dificuldade', 'resposta', 'comentarios',
              'reasoning', 'fonte_original', 'adaptacoes', 'permission_evidence')
    record = {k: q[k] for k in fields if k in q}
    if q['direitos'] != 'somente-link':
        record.update(enunciado=q['enunciado'], alternativas=q['alternativas'])
    return record


def connect(path, create=False):
    path = Path(path)
    if not create and not path.is_file():
        raise ValueError('Acervo inexistente; importe um manifesto primeiro')
    if create:
        path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    db.enable_load_extension(False)
    version = db.execute('PRAGMA user_version').fetchone()[0]
    if version not in (0, 1):
        db.close()
        raise ValueError('Versão de acervo não suportada; preserve o arquivo original')
    if version == 0:
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
        if tables:
            db.close()
            raise ValueError('Arquivo SQLite já contém outro banco; escolha um destino vazio')
        if not create:
            db.close()
            raise ValueError('Arquivo não é um acervo inicializado')
        db.executescript('''
          CREATE TABLE IF NOT EXISTS materials (
            id TEXT NOT NULL, version TEXT NOT NULL, title TEXT NOT NULL,
            inputs_hash TEXT NOT NULL, imported_at TEXT NOT NULL,
            PRIMARY KEY(id,version));
          CREATE TABLE IF NOT EXISTS questions (
            key TEXT PRIMARY KEY, origin TEXT NOT NULL, revision INTEGER NOT NULL,
            record TEXT NOT NULL, record_hash TEXT NOT NULL, bank TEXT, year INTEGER,
            status TEXT, search_text TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS revisions (
            key TEXT NOT NULL REFERENCES questions(key), revision INTEGER NOT NULL,
            record TEXT NOT NULL, record_hash TEXT NOT NULL, reason TEXT NOT NULL,
            imported_at TEXT NOT NULL, PRIMARY KEY(key,revision));
          CREATE TABLE IF NOT EXISTS occurrences (
            material_id TEXT NOT NULL, version TEXT NOT NULL, local_id TEXT NOT NULL,
            key TEXT NOT NULL REFERENCES questions(key), revision INTEGER NOT NULL,
            search_text TEXT NOT NULL, PRIMARY KEY(material_id,version,local_id),
            FOREIGN KEY(material_id,version) REFERENCES materials(id,version),
            FOREIGN KEY(key,revision) REFERENCES revisions(key,revision));
          CREATE INDEX IF NOT EXISTS question_filters ON questions(origin,bank,year,status);
          CREATE INDEX IF NOT EXISTS occurrences_key ON occurrences(key);
          PRAGMA user_version=1;
        ''')
    return db


def validate_transition(old, new):
    previous, current = old.get('fonte_original'), new.get('fonte_original')
    if previous and current:
        if current['conferido_em'] < previous['conferido_em']:
            raise ValueError('Evidência mais antiga que a revisão corrente')
        if previous['gabarito_status'] in ('definitivo', 'retificado', 'anulada'):
            if current['gabarito_status'] == 'preliminar':
                raise ValueError('Não regredir gabarito consolidado para preliminar')
        if old['resposta'] != new['resposta']:
            if current['gabarito_sha256'] == previous['gabarito_sha256']:
                raise ValueError('Mudança de resposta oficial exige nova evidência de gabarito')


def import_material(path, manifest, accept_revisions=False, reason=None):
    data = load_material(manifest)
    config = data['config']
    fingerprint = digest({str(p.relative_to(data['folder'])): sha256(p.read_bytes()).hexdigest()
                          for p in data['inputs']})
    timestamp = datetime.now(timezone.utc).isoformat()
    result = {'material': config['id'], 'version': config['version'], 'inserted': 0,
              'reused': 0, 'revised': 0, 'questions': len(data['questions'])}
    db = connect(path, create=True)
    try:
        with db:
            known = db.execute('SELECT inputs_hash FROM materials WHERE id=? AND version=?',
                               (config['id'], config['version'])).fetchone()
            if known:
                if known['inputs_hash'] != fingerprint:
                    raise ValueError('Edição já registrada com entradas diferentes; incremente version')
                result['reused'] = len(data['questions'])
                return result
            db.execute('INSERT INTO materials VALUES (?,?,?,?,?)',
                       (config['id'], config['version'], config['title'], fingerprint, timestamp))
            for q in data['questions']:
                key, record = question_key(q), public_record(q)
                encoded, record_hash = canonical(record), digest(record)
                old = db.execute('SELECT * FROM questions WHERE key=?', (key,)).fetchone()
                revision = old['revision'] if old else 1
                if old and old['record_hash'] != record_hash:
                    if not accept_revisions or not reason or not reason.strip():
                        raise ValueError('Revisão divergente: use --aceitar-revisoes e --motivo após conferir a evidência')
                    validate_transition(json.loads(old['record']), record)
                    revision += 1
                    result['revised'] += 1
                elif old:
                    result['reused'] += 1
                else:
                    result['inserted'] += 1
                source = record.get('fonte_original', {})
                params = (key, q['origem'], revision, encoded, record_hash,
                          folded(source['banca']) if source else None, source.get('ano'),
                          source.get('gabarito_status'), folded(canonical(record)))
                if not old or old['record_hash'] != record_hash:
                    if old:
                        db.execute('''UPDATE questions SET origin=?,revision=?,record=?,record_hash=?,
                                      bank=?,year=?,status=?,search_text=? WHERE key=?''', params[1:] + (key,))
                    else:
                        db.execute('INSERT INTO questions VALUES (?,?,?,?,?,?,?,?,?)', params)
                    db.execute('INSERT INTO revisions VALUES (?,?,?,?,?,?)',
                               (key, revision, encoded, record_hash,
                                reason.strip() if old else 'Importação inicial', timestamp))
                coverage = [r['edital_item'] for r in data['coverage']
                            if q['id'] in r['questions'] or q['objetivo'] in r['objectives']]
                terms = folded(' '.join([config['title'], config['scope'], q['objetivo'], *coverage]))
                db.execute('INSERT INTO occurrences VALUES (?,?,?,?,?,?)',
                           (config['id'], config['version'], q['id'], key, revision, terms))
    finally:
        db.close()
    return result


def _search(db, bank=None, year=None, topic=None, origin=None, status=None):
    clauses, values = [], []
    for column, value in (('bank', folded(bank) if bank else None), ('year', year),
                          ('origin', origin), ('status', status)):
        if value is not None:
            clauses.append(f'q.{column}=?')
            values.append(value)
    if topic:
        term = folded(topic)
        clauses.append('''(instr(q.search_text,?)>0 OR EXISTS (
                          SELECT 1 FROM occurrences o WHERE o.key=q.key AND instr(o.search_text,?)>0))''')
        values += [term, term]
    sql = 'SELECT q.* FROM questions q' + (' WHERE ' + ' AND '.join(clauses) if clauses else '')
    results = []
    for row in db.execute(sql + ' ORDER BY q.key', values):
        record = json.loads(row['record'])
        source = record.get('fonte_original', {})
        contexts = [dict(r) for r in db.execute('''SELECT material_id,version,local_id,revision
                   FROM occurrences WHERE key=? ORDER BY material_id,version,local_id''', (row['key'],))]
        results.append({'key': row['key'], 'revision': row['revision'], 'origin': row['origin'],
                        'bank': source.get('banca'), 'year': source.get('ano'),
                        'status': source.get('gabarito_status'), 'record': record,
                        'occurrences': contexts})
    return results


def search(path, bank=None, year=None, topic=None, origin=None, status=None):
    db = connect(path)
    try:
        db.execute('BEGIN')
        return _search(db, bank, year, topic, origin, status)
    finally:
        db.close()


def _history(db, key):
    rows = db.execute('SELECT * FROM revisions WHERE key=? ORDER BY revision', (key,)).fetchall()
    if not rows:
        raise ValueError('Questão não localizada pelo ID estável')
    return [{**dict(r), 'record': json.loads(r['record'])} for r in rows]


def history(path, key):
    db = connect(path)
    try:
        return _history(db, key)
    finally:
        db.close()


def export_catalog(path, destination):
    if Path(path).resolve() == Path(destination).resolve():
        raise ValueError('Exportação não pode sobrescrever o banco do acervo')
    db = connect(path)
    try:
        db.execute('BEGIN')
        questions = _search(db)
        payload = {'catalog_version': 1, 'generated_at': datetime.now(timezone.utc).isoformat(),
                   'questions': questions,
                   'materials': [dict(r) for r in db.execute('SELECT * FROM materials ORDER BY id,version')],
                   'revisions': {q['key']: _history(db, q['key']) for q in questions}}
    finally:
        db.close()
    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'questions': len(payload['questions']), 'output': str(output)}
