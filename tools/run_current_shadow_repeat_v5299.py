"""Full original every-field body/shadow observer on the corrected current build.

Only fresh output leaf and exact metadata-only candidate context change.
Physical controls, true victim selection and all native observers stay intact.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import run_special_shadow_v5133 as original
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=original.LUA
def collector():
    text=inspect.getsource(original.capture)
    before='audit_v5134_special_repeat_{move}_p{side}_{victim}'
    need(text.count(before)==1,'Only exact fresh native shadow capture leaf')
    text=text.replace(before,'audit_v5300_current_special_shadow_{move}_p{side}_{victim}',1)
    scope=dict(original.capture.__globals__,__file__=__file__,native=current)
    exec(compile(text,__file__+'::entire_original_native_body_shadow_RAM_capture_current','exec'),scope)
    return scope['capture']
def run(move,side,victim):
    base=ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json'
    baseline=json.loads(base.read_text())
    need(baseline['passed']and baseline['case']['entryBodyPublicationProven']and
      all(sha(p)==baseline['inputHashes'][str(p.resolve())]for p in (LUA,Path(original.__file__))),
      'Exact actually passed full original every-field body/shadow and physical-control sources')
    report=collector()(move,side,victim)
    folder=ROOT/f'audit_v5300_current_special_shadow_{move}_p{side}_{victim}'
    need((folder/'stderr.log').read_text()=='','No native metadata warning or stderr waiver')
    report['nativeStderrEmpty']=True;report['inputHashes'][str(base)]=sha(base)
    report['additionalVictimShadowContextNotYetIndependentlyAccepted']=True
    return report
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--move',required=True,choices=original.MOVES)
    parser.add_argument('--side',type=int,required=True,choices=(1,2))
    parser.add_argument('--victim',required=True,choices=('kitana','sub_zero','kano','sonya'))
    a=parser.parse_args();out=ROOT/f'audit_v5301_current_special_shadow_{a.move}_p{a.side}_{a.victim}_observed'
    need(not out.exists(),'Fresh immutable actual native shadow terminal')
    try:report=run(a.move,a.side,a.victim)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
