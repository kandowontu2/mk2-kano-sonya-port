"""Successor keeps corrected assembler and whole-window model in one scope.

Both executed failures stay immutable. No original verification is removed.
"""
import inspect
from pathlib import Path
import check_native_shang_drain_compare_source as previous

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_shang_drain_compare_scoped_source'
FAILURE = ROOT / 'audit_native_shang_drain_compare_model_scope_failure/report.json'


def main():
    source = inspect.getsource(previous.main)
    old = '    source = inspect.getsource(prior.main)\n'
    new = ("    exec(compile(inspect.getsource(prior.independent_guest), __file__ + '::same_whole_guest_model_in_corrected_scope', 'exec'), scope)\n"
           "    source = inspect.getsource(prior.main)\n")
    previous.prior.need(source.count(old) == 1, 'Whole guest model must call the same actual corrected scoped assembler')
    source = source.replace(old, new, 1)
    old = 'Path(__file__), Path(prior.__file__), ROOT'
    new = 'Path(__file__), Path(previous.__file__), FAILURE, Path(prior.__file__), ROOT'
    previous.prior.need(source.count(old) == 1, 'Pin executed predecessor and exact scope-failure evidence')
    source = source.replace(old, new, 1)
    scope = dict(vars(previous), previous=previous, OUT=OUT, FAILURE=FAILURE, __file__=__file__)
    # The inner scope gets constants via vars(base), not vars(this wrapper).
    # Make the two added pin objects explicit, without mutating either module.
    old = 'scope = dict(vars(prior), prior=prior, OUT=OUT, FRAGMENT=FRAGMENT,'
    new = 'scope = dict(vars(prior), prior=prior, previous=previous, FAILURE=FAILURE, OUT=OUT, FRAGMENT=FRAGMENT,'
    previous.prior.need(source.count(old) == 1, 'All additional pins are available to the unchanged inner checker')
    source = source.replace(old, new, 1)
    exec(compile(source, __file__ + '::complete_corrected_models_same_scope', 'exec'), scope)
    return scope['main']()


if __name__ == '__main__':
    main()
