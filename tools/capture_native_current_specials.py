"""Current native-state repair: entire original two-cycle physical specials.

Only candidate, private launcher, evidence path, Windows quoting, and immediate
kernel identity observation differ. All original physical inputs, full guest
and UI graphics checks, native state/damage/body/recovery gates remain intact.
"""
import argparse
import inspect
from pathlib import Path
import capture_current_cmd_specials_v6261 as original_capture
import native_ai_response_full_context as current
import native_process_census_v6647 as identity
need = current.need

def bindings():
    scope = dict(vars(original_capture), __file__=__file__, current=current,
        census=identity.census, identity_tools=identity,
        original_capture=original_capture,
        LAUNCHER=current.ROOT/'TEST_NATIVE_CURRENT_SPECIALS.cmd')
    for function in (original_capture.load_case, original_capture.capture):
        source = inspect.getsource(function)
        changes = {'audit_v6262_current_cmd_special_':'audit_native_current_special_'}
        if function is original_capture.capture:
            changes.update({
                "command=['cmd.exe','/d','/s','/c','\"'+subprocess.list2cmdline(args)+'\"']":
                    "command=[os.environ['ComSpec'],'/d','/c',*args]",
                'for p in(LUA,LAUNCHER,':
                    'for p in(Path(original_capture.__file__),Path(identity_tools.__file__),LUA,LAUNCHER,',
                'canonicalCMDUsed=True':'canonicalCMDUsed=False,isolatedCandidateCMDUsed=True',
                'check,_,_=context.bindings();report':
                    'check,_,_=context.bindings();check.__globals__["native"]=current;report',
                'time.sleep(2);jobs=census()':
                    "jobs=[]\n   for observation in range(100):\n    jobs=census()\n    if any(j['ParentProcessId']==process.pid for j in jobs):break\n    if process.poll()is not None:break\n    time.sleep(.02)",
                "canonical CMD pid={process.pid}":"private current CMD pid={process.pid}",
            })
        for before, after in changes.items():
            need(source.count(before)==1, 'Exact whole original current-special adaptation '+before)
            source = source.replace(before, after, 1)
        exec(compile(source, __file__+'::whole_original_'+function.__name__, 'exec'), scope)
    return scope['capture'], scope['load_case']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--move', choices=original_capture.original.SPECS)
    parser.add_argument('--side', type=int, choices=(1,2))
    args = parser.parse_args()
    need(bool(args.move)==bool(args.side), 'Both move and side, or the complete matrix')
    capture, _ = bindings()
    cases = [(args.move,args.side)] if args.move else [
        (move,side) for move in original_capture.original.SPECS for side in (1,2)]
    for move, side in cases:
        capture(move, side)
