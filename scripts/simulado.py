"""Score a simulation using its versioned matrix, weights and annulment rules."""
import argparse,json
from pathlib import Path
import sys
from material import load_material
from formats import score_simulation


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--respostas', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    args=parser.parse_args(argv)
    try:
        data=load_material(args.manifest)
        result=score_simulation(data,json.loads(args.respostas.read_text(encoding='utf-8')))
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'Pontuação: {result["points"]} de {result["maximum"]}.')
        return 0
    except (ValueError,OSError,KeyError) as error:
        print('Falha na pontuação: '+str(error),file=sys.stderr);return 1


if __name__=='__main__':sys.exit(main())
