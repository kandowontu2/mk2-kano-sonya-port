"""Fresh delayed own-head reactions to Raiden, both victims and sides."""
import sys
from refresh_ingestion_regression import plan as ingestion_plan, run


def plan(prefix):
    return [(name, ['--raiden-burst-victim' if a == '--body-suck-victim' else a for a in args])
            for name, args in ingestion_plan(prefix)]


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Supply a fresh prefix'
    run(sys.argv[1], fixture_plan=plan, qualifier='qualify_raiden_burst.py', label='Raiden burst')
