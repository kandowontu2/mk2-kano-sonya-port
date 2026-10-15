"""Same complete source/cause contract with exact inserted blank-line boundary.

The original checker's source-normalization failure remains immutable.
"""
import inspect
import qualify_native_paired_stumble_table as prior

OUT = prior.ROOT / 'audit_native_paired_stumble_table_spacing_source'


def run(ram):
    failure = prior.OUT / 'failure.json'
    prior.need(failure.exists() and not OUT.exists(), 'Original spacing failure preserved, fresh successor')
    source = inspect.getsource(prior.source_contract)
    before = "first = after.index('\\n\\t' + BEGIN)"
    after = "first = after.index('\\n\\n\\t' + BEGIN)"
    prior.need(source.count(before) == 1, 'Exact inserted block boundary only')
    scope = dict(vars(prior), __file__=__file__, OUT=OUT)
    exec(compile(source.replace(before, after), __file__ + '::whole_source_contract', 'exec'), scope)
    qualify = inspect.getsource(prior.qualify)
    needle = 'paths = [Path(__file__), *STAGE.iterdir(), payload_path,'
    prior.need(qualify.count(needle) == 1, 'Conserve entire original input set and pin failed predecessor')
    qualify = qualify.replace(needle, 'paths = [Path(__file__), Path(prior_file), prior_failure, *STAGE.iterdir(), payload_path,')
    scope.update(prior_file=prior.__file__, prior_failure=failure)
    exec(compile(qualify, __file__ + '::whole_original_cause_guest_fault_contract', 'exec'), scope)
    exec(compile(inspect.getsource(prior.run), __file__ + '::whole_failure_preserving_run', 'exec'), scope)
    return scope['run'](ram)
