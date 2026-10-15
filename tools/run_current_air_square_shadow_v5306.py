"""Original physical airborne Square Wave full-body/shadow capture, current build.

The opponent jumps using the original ordinary three-field Up input. No
actor, health, CPU, floor, position, RNG or opponent identity is forced.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import run_square_air_shadow_v5143 as original
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
def collector():
    source=inspect.getsource(original.capture)
    before='audit_v5144_special_repeat_{move}_p{side}_{victim}'
    need(source.count(before)==1,'Exact original capture, only fresh output path')
    source=source.replace(before,'audit_v5307_current_air_square_shadow_{move}_p{side}_{victim}',1)
    scope=dict(original.capture.__globals__,__file__=__file__,native=current)
    exec(compile(source,__file__+'::entire_original_physical_air_square_capture_current','exec'),scope)
    return scope['capture']
def run(side):
    baseline=ROOT/'audit_v5148_special_shadow_square_p1_checked/report.json'
    old=json.loads(baseline.read_text())
    need(old['passed']and old['case']['state']['actualSquareContactVerified']and
      old['case']['entryBodyPublicationProven']and
      all(sha(p)==old['inputHashes'][str(p.resolve())]for p in (Path(original.__file__),original.LUA)),
      'Complete original physically airborne contact and full body/shadow source unchanged')
    report=collector()('square',side,'sub_zero')
    folder=ROOT/f'audit_v5307_current_air_square_shadow_square_p{side}_sub_zero'
    need((folder/'stderr.log').read_text()=='','Current native ROM metadata exact, no warning waiver')
    report['inputHashes'][str(baseline)]=sha(baseline)
    report['nativeStderrEmpty']=True
    report['trueVictimID']=8
    report['additionalNativeAirContactAndShadowSemanticsNotYetAccepted']=True
    return report
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True)
    a=parser.parse_args();out=ROOT/f'audit_v5308_current_air_square_shadow_square_p{a.side}_sub_zero_observed'
    need(not out.exists(),'Fresh immutable native terminal')
    try:report=run(a.side)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
