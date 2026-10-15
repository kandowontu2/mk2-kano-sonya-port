"""Add source provenance to the actual current provider before native boot.

The earlier preflight exited before any game started. Preserve its source,
initializer and rejection. Whole original controllers/contracts remain exact.
Keep this host interactive so native rasters survive for same-job review.
"""
import argparse
import code
import inspect
import json
import traceback
from pathlib import Path
import capture_native_kano_laser_cross_continue as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
INIT=ROOT/'audit_native_kano_laser_cross_continue_source_bound_initializer_source'


def expectation():
    source=inspect.getsource(prior.expectation)
    source=prior.replace(source,'current=SimpleNamespace(ROOT=ROOT,','current=SimpleNamespace(__file__=__file__,ROOT=ROOT,')
    scope=dict(vars(prior),INIT=INIT,__file__=__file__)
    exec(compile(source,__file__+'::whole_current_initializer_with_provider_source_provenance','exec'),scope)
    return scope['expectation']()


def run(fighter,side):
    source=inspect.getsource(prior.run)
    source=prior.replace(source,'expectation();contract=contracts(current)','expectation();contract=contracts(current)')if False else source
    scope=dict(vars(prior),expectation=expectation)
    exec(compile(source,__file__+'::whole_original_native_continue_current_source_bound_provider','exec'),scope)
    # Retained generated capture/contract globals must be shared with later cases.
    scope['run'](fighter,side)
    return scope


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
    parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    state=None
    try:state=run(args.fighter,args.side)
    except Exception as error:
        failure=ROOT/f'audit_native_kano_laser_cross_continue_source_bound_failure_{args.fighter}_p{args.side}'
        need(not failure.exists(),'Preserve actual source-bound capture failure');failure.mkdir()
        prior.native_base.save(failure/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            inputHashes={str(Path(__file__)):sha(__file__),str(Path(prior.__file__)):sha(prior.__file__)},
            fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same current native paid-continue buffers retained; no terminal replay.',
                  local=dict(cases=prior.RAM_CASES,module=prior,state=state))
