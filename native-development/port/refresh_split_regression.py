"""Four own split roles plus representative unchanged original controls."""
import sys
from refresh_ingestion_regression import plan as ingestion_plan, run


def plan(prefix):
    fixtures = [(name, ['--lao-split-victim' if a == '--body-suck-victim' else a for a in args])
                for name, args in ingestion_plan(prefix)]
    fixtures += [(f'{prefix}_control_{actor}', ['--game', '--lao-split-victim',
                   f'--lao-split-control={actor}', '--sound-candidate']) for actor in (1, 4)]
    return fixtures


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Supply a fresh prefix'
    run(sys.argv[1], fixture_plan=plan, qualifier='qualify_lao_split.py', label='split')
