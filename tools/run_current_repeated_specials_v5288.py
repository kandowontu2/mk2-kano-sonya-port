"""Same complete physical two-cycle observer on the corrected current executable.

Only the capture leaf and candidate context change. Existing victim routes
are used exactly; no guest/health/position/CPU writes or easier command policy.
The current native ROM declaration must produce an empty stderr.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import run_special_repeat_v5101 as original
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=original.LUA
def collector():
    source=inspect.getsource(original.capture)
    before='audit_v5102_special_repeat_{move}_p{side}_{victim}'
    need(source.count(before)==1,'Only exact fresh repeated-special capture leaf')
    source=source.replace(before,'audit_v5289_current_special_repeat_{move}_p{side}_{victim}',1)
    scope=dict(original.capture.__globals__,__file__=__file__,native=current)
    exec(compile(source,__file__+'::entire_original_physical_repeat_capture_current_candidate','exec'),scope)
    return scope['capture']
def run(move,side,victim):
    baseline=ROOT/'audit_v5116_special_repeat_checked/report.json'
    old=json.loads(baseline.read_text());key=str(LUA.resolve())
    need(old['passed']and old['allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified']and
      key in old['inputHashes']and sha(LUA)==old['inputHashes'][key],
      'Exact full actual source-qualified original physical two-cycle controller, no gameplay-policy edit')
    report=collector()(move,side,victim)
    folder=ROOT/f'audit_v5289_current_special_repeat_{move}_p{side}_{victim}'
    need((folder/'stderr.log').read_text()=='','Current exact metadata has no native warning waiver')
    report['nativeStderrEmpty']=True
    report['inputHashes'][str(baseline)]=sha(baseline)
    report['additionalVictimContextNotYetIndependentlyAccepted']=True
    return report
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--move',required=True,choices=original.MOVES)
    parser.add_argument('--side',required=True,type=int,choices=(1,2))
    parser.add_argument('--victim',required=True,choices=('kitana','sub_zero','kano','sonya'))
    a=parser.parse_args();out=ROOT/f'audit_v5290_current_special_repeat_{a.move}_p{a.side}_{a.victim}_observed'
    need(not out.exists(),'Fresh immutable actual current repeat terminal')
    try:report=run(a.move,a.side,a.victim)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
