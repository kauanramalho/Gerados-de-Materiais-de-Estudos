"""Read-only edition comparison: preserve IDs and trace the impact of changed sources."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from material import load_material, compose_material
from resources import markdown_document, image_path


def figure_dependencies(data):
    """Resolve cross-file reference definitions in full documents and retain every use."""
    dependencies, unassigned = {}, set()
    chapter_ids = {c['id'] for c in data['config']['chapters']}
    kinds = ['apostila','caderno'] + (['simulado'] if data.get('simulation') else []) + (['revisao'] if data.get('revision') else [])
    for kind in kinds:
        owner = None

        def visit(node):
            nonlocal owner
            if isinstance(node, dict):
                if node.get('t') == 'Header' and node['c'][0] == 1:
                    ident = node['c'][1][0]
                    owner = ident if ident in chapter_ids else None
                if node.get('t') == 'Image':
                    file = image_path(data['folder'],node['c'][2][0]).relative_to(data['folder']).as_posix()
                    if owner:
                        dependencies.setdefault(file,set()).add(owner)
                    else:
                        unassigned.add(file)
                for value in node.values():visit(value)
            elif isinstance(node,list):
                for value in node:visit(value)

        visit(markdown_document(data['config']['title']+'\n\n'+compose_material(data,kind)))
    return dependencies, unassigned


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
    figures_old = {f['id']: f for f in old['figures']}
    figures_new = {f['id']: f for f in new['figures']}
    figure_changes = sorted(k for k in figures_old.keys() | figures_new.keys()
                            if figures_old.get(k) != figures_new.get(k) or any(
                                (data['folder']/figure['file']).resolve().relative_to(data['folder']).as_posix() in files
                                for data, figure in ((old, figures_old.get(k)), (new, figures_new.get(k))) if figure))
    metadata_old = {k:v for k,v in old['config'].items() if k != 'version'}
    metadata_new = {k:v for k,v in new['config'].items() if k != 'version'}
    altered = bool(files or metadata_old != metadata_new or changed or removed or added or source_changes)
    if altered and old['config']['version'] == new['config']['version']:
        raise ValueError('Conteúdo modificado exige nova versão')
    all_chapters = old['config']['chapters']+new['config']['chapters']
    chapter_before = {c['id']:c for c in old['config']['chapters']}
    chapter_after = {c['id']:c for c in new['config']['chapters']}
    chapters = {c['id'] for c in all_chapters
                if set(c['objectives']) & objectives or c['file'] in files
                or chapter_before.get(c['id']) != chapter_after.get(c['id'])}
    for data in (old, new):
        chapters.update(c['id'] for c in (data.get('revision') or {}).get('chapters', []) if c['file'] in files)
    policy = 'not-needed'
    if figure_changes:
        policy = 'resolved-chapter-uses'
        dependencies = [figure_dependencies(old), figure_dependencies(new)]
        for ident in figure_changes:
            owners = set()
            uncertain = False
            for data, figures, (uses,unassigned) in zip((old,new),(figures_old,figures_new),dependencies):
                if ident in figures:
                    file = (data['folder']/figures[ident]['file']).resolve().relative_to(data['folder']).as_posix()
                    owners.update(uses.get(file, set()))
                    uncertain = uncertain or file in unassigned
            if owners and not uncertain:
                chapters.update(owners)
            else:
                # Context/question-only figures and cross-file reference definitions
                # cannot be assigned safely to one chapter: review conservatively.
                chapters.update(c['id'] for c in all_chapters)
                policy = 'conservative-all-chapters'
        impacted_objectives = {o for c in all_chapters if c['id'] in chapters for o in c['objectives']}
        affected = sorted(set(affected) | {q['id'] for q in old['questions']+new['questions']
                                         if q['objetivo'] in impacted_objectives})
    other_metadata_changed = ({k:v for k,v in metadata_old.items() if k!='chapters'} !=
                              {k:v for k,v in metadata_new.items() if k!='chapters'})
    if source_changes or other_metadata_changed:
        # Chapter prose can depend on a source without a per-sentence citation index.
        chapters = {c['id'] for c in all_chapters}
    return dict(material=old['config']['id'],before=old['config']['version'],after=new['config']['version'],
                reason=reason,changed=altered,changed_files=files,changed_sources=source_changes,
                changed_questions=changed,added_questions=added,removed_questions=removed,
                affected_questions=affected,chapters_to_review=sorted(chapters),
                changed_figures=figure_changes,figure_review_policy=policy,
                source_review='Mudança de fonte exige revisar todos os capítulos; dependência textual não é inferida automaticamente.',
                action='Revisar conteúdo, regenerar artefatos e reauditar links; PDFs anteriores permanecem na edição original.')


def render_errata(report):
    rows = ['# Errata e impacto de edição', '', f'Material: {report["material"]}. Edição {report["before"]} → {report["after"]}.',
            '', 'Motivo: '+report['reason'], '', '## Revisões necessárias', '',
            '- Questões: '+(', '.join(report['affected_questions']) or 'nenhuma questão sinalizada'),
            '- Capítulos: '+(', '.join(report['chapters_to_review']) or 'nenhum capítulo sinalizado'),
            '- Fontes: '+(', '.join(report['changed_sources']) or 'nenhuma mudança de fonte'),
            '- Figuras: '+(', '.join(report['changed_figures']) or 'nenhuma figura sinalizada'),
            '- Política de impacto das figuras: '+report['figure_review_policy'],
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
