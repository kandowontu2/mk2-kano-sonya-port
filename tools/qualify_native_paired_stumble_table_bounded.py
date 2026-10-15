"""Complete predecessor contracts; invalid trace pointers reject before reads.

Original spacing and malformed-pointer checker failures are preserved. Native
inputs and the staged game fix are unchanged.
"""
import inspect
from pathlib import Path
import qualify_native_paired_stumble_table_spacing as spacing

OUT = spacing.prior.ROOT / 'audit_native_paired_stumble_table_bounded_source'


def run(ram):
    source = inspect.getsource(spacing.run)
    old = "return scope['run'](ram)"
    spacing.prior.need(source.count(old) == 1, 'Whole predecessor factory, no qualification replay')
    factory = dict(vars(spacing), __file__=__file__, OUT=OUT)
    exec(compile(source.replace(old, 'return scope'), __file__ + '::whole_predecessor_factory', 'exec'), factory)
    scope = factory['run'](ram)
    cause = inspect.getsource(spacing.prior.cause_contract)
    old = "stream = int(result['a9'], 16)"
    new = old + "\n    need(stream == 0xff0210c0, 'Actual own stream before malformed trace dereference')"
    spacing.prior.need(cause.count(old) == 1, 'One actual trace address precondition, no changed positive data')
    exec(compile(cause.replace(old, new), __file__ + '::whole_bounded_cause_contract', 'exec'), scope)
    qualify = inspect.getsource(spacing.prior.qualify)
    old = 'paths = [Path(__file__), *STAGE.iterdir(), payload_path,'
    new = 'paths = [Path(__file__), Path(prior_file), prior_failure, spacing_file, spacing_failure, *STAGE.iterdir(), payload_path,'
    spacing.prior.need(qualify.count(old) == 1, 'All executed contracts and failed outcomes pinned')
    scope.update(spacing_file=Path(spacing.__file__), spacing_failure=spacing.OUT / 'failure.json')
    exec(compile(qualify.replace(old, new), __file__ + '::whole_original_complete_qualification', 'exec'), scope)
    return scope['run'](ram)
