"""Bind the whole next-case function to the same retained initializer scope.

The earlier host failed before native launch because next_case's globals
belonged to the original module, not the newly generated collector scope.
Recover that actual live host scope, preserve its sources and rejection,
and compile the unchanged next_case into the matching namespace. No new
initializer or game replay, no relaxed controller or acceptance conditions.
"""
import hashlib
import inspect
import json
import traceback
from pathlib import Path
import capture_native_kano_laser_cross_continue as prior
import capture_native_kano_laser_cross_continue_source_bound as source_bound

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_kano_laser_cross_continue_retained_scope_source'


def prepare(scope):
    need(not OUT.exists()and not scope['RAM_CASES']and not prior.native_base.identity.census(),
         'Same actual retained initialized host; both failed preflights launched no game')
    current=scope['current'];build=scope['build']
    need(current.NAME==prior.native_base.audio.NAME and
         hashlib.sha256(scope['guest']).hexdigest().upper()==current.GUEST_SHA and
         sha(ROOT/current.NAME/'mkport_candidate.exe')==current.EXE_SHA and
         all(sha(p)==h for p,h in build['input_hashes'].items()),
         'Actual whole independently initialized current guest and all native compiled inputs retained unchanged')
    failure=ROOT/'audit_native_kano_laser_cross_continue_source_bound_failure_kano_p2/failure.json'
    failed=json.loads(failure.read_text())
    need(failed['error']=="NameError(\"name 'capture' is not defined\")"and
         all(sha(p)==h for p,h in failed['inputHashes'].items()),'Exact original namespace rejection and executed source preserved')
    source=inspect.getsource(prior.next_case)
    exec(compile(source,__file__+'::whole_unchanged_next_case_same_retained_collector_globals','exec'),scope)
    added=[Path(__file__),Path(prior.__file__),Path(source_bound.__file__),failure,
           ROOT/'audit_native_kano_laser_cross_continue_preflight_failure/failure.json',
           source_bound.INIT/'report.json',OUT/'report.json']
    pins={str(p.resolve()):sha(p)for p in added if p!=OUT/'report.json'}
    OUT.mkdir();prior.native_base.save(OUT/'report.json',dict(passed=True,sourceBindingAccepted=True,
        wholeOriginalNextCaseByteUnchanged=True,currentGuestSHA256=current.GUEST_SHA,
        currentExecutableSHA256=current.EXE_SHA,nativeGameAccepted=False,newNativeBoots=0,
        repeatedInitializer=False,originalPreflightFailuresPreserved=True,inputHashes=pins,fullPortAcceptance=False))
    scope['contract'].DEPENDENCIES.extend(added)
    print(json.dumps(dict(passed=True,wholeOriginalNextCaseByteUnchanged=True,
                         repeatedInitializer=False,newNativeBoots=0)),flush=True)


def execute(scope,fighter,side):
    try:scope['next_case'](fighter,side)
    except Exception as error:
        failure=ROOT/f'audit_native_kano_laser_cross_continue_retained_scope_failure_{fighter}_p{side}'
        need(not failure.exists(),'Preserve exact actual terminal capture or host-check failure');failure.mkdir()
        prior.native_base.save(failure/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            inputHashes={str(Path(__file__)):sha(__file__)},fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
