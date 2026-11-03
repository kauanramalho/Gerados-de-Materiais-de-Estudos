"""Read-only edition comparison: preserve IDs and trace the impact of changed sources."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from material import load_material


def comparison(old, new, reason):
    if not reason.strip():
        raise ValueError('Uma mudança de edição exige motivo')
    if old['config']['id'] != new['config']['id']:
        raise ValueError('Comparar edições do mesmo material')
    questions_old = {q['id']: q for q in old['questions']}
    questions_new = {q['id']: q for q in new['questions']}
    changed = sorted(k for k in questions_old.keys() & questions_new.keys() if questions_old[k] != questions_new[k])
    removed = sorted(questions_old.keys() - questions_new.keys())
    added = sorted(questions_new.keys() - questions_old.keys())
    sources_old = {s['id']: s for s in old['sources']}
    sources_new = {s['id']: s for s in new['sources']}
    source_changes = sorted(k for k in sources_old.keys() | sources_new.keys() if sources_old.get(k) != sources_new.get(k))
    affected = sorted({q['id'] for q in old['questions']+new['questions']
                       if set(q.get('source_ids', [])) & set(source_changes)} | set(changed) | set(removed) | set(added))
    objectives = {q['objetivo'] for q in old['questions']+new['questions'] if q['id'] in affected}
    def fingerprints(data):
        return {str(path.relative_to(data['folder'])): sha256(path.read_bytes()).hexdigest()
                for path in data['inputs'] if path.name != 'material.json'}
    before, after = fingerprints(old), fingerprints(new)
    files = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    metadata_old = {k:v for k,v in old['config'].items() if k != 'version'}
    metadata_new = {k:v for k,v in new['config'].items() if k != 'version'}
    altered = bool(files or metadata_old != metadata_new or changed or removed or added or source_changes)
    if altered and old['config']['version'] == new['config']['version']:
        raise ValueError('Conteúdo modificado exige nova versão')
    chapters = sorted({c['id'] for c in old['config']['chapters']+new['config']['chapters']
                       if set(c['objectives']) & objectives or c['file'] in files})
    if source_changes:
        # Chapter prose can depend on a source without a per-sentence citation index.
        chapters = sorted({c['id'] for c in old['config']['chapters']+new['config']['chapters']})
    return dict(material=old['config']['id'],before=old['config']['version'],after=new['config']['version'],
                reason=reason,changed=altered,changed_files=files,changed_sources=source_changes,
                changed_questions=changed,added_questions=added,removed_questions=removed,
                affected_questions=affected,chapters_to_review=chapters,
                source_review='Mudança de fonte exige revisar todos os capítulos; dependência textual não é inferida automaticamente.',
                action='Revisar conteúdo, regenerar artefatos e reauditar links; PDFs anteriores permanecem na edição original.')


def render_errata(report):
    rows = ['# Errata e impacto de edição', '', f'Material: {report["material"]}. Edição {report["before"]} → {report["after"]}.',
            '', 'Motivo: '+report['reason'], '', '## Revisões necessárias', '',
            '- Questões: '+(', '.join(report['affected_questions']) or 'nenhuma questão sinalizada'),
            '- Capítulos: '+(', '.join(report['chapters_to_review']) or 'nenhum capítulo sinalizado'),
            '- Fontes: '+(', '.join(report['changed_sources']) or 'nenhuma mudança de fonte'),
            '- IDs removidos: '+(', '.join(report['removed_questions']) or 'nenhum'),
            '', report['source_review'], '', report['action'], '',
            '## Revisão editorial a preencher', '',
            'Registrar trecho anterior, correção, fundamento, revisão técnica e links para a edição corrigida. '
            'Este relatório de impacto não aprova a correção automaticamente.']
    return '\n'.join(rows)+'\n'


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('anterior',type=Path);parser.add_argument('nova',type=Path)
    parser.add_argument('--motivo',required=True);parser.add_argument('--report',required=True,type=Path)
    parser.add_argument('--errata',required=True,type=Path);args=parser.parse_args(argv)
    try:
        report=comparison(load_material(args.anterior),load_material(args.nova),args.motivo)
        for target in (args.report,args.errata):target.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        args.errata.write_text(render_errata(report),encoding='utf-8');print('Impacto de edição registrado.');return 0
    except (ValueError,KeyError,OSError) as error:
        print('Falha na comparação: '+str(error),file=sys.stderr);return 1


if __name__=='__main__':sys.exit(main())
