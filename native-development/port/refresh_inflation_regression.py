"""Fresh current-ROM inflation victims on both sides, no guest writes."""
import sys
from refresh_ingestion_regression import plan as ingestion_plan, run


def plan(prefix):
    return [(name, ['--kitana-kiss-victim' if arg == '--body-suck-victim' else arg for arg in args])
            for name, args in ingestion_plan(prefix)]


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Supply a fresh prefix'
    run(sys.argv[1], fixture_plan=plan, qualifier='qualify_inflation_runtime.py', label='inflation')
