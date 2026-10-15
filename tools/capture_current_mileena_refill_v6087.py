"""Entire6082 current native capture, with complete stock inter-round refill gate."""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_mileena_native_v6082 as prior
import current_mileena_native_refill_v6085 as health
ROOT,need,sha=prior.ROOT,prior.need,prior.sha

def run(fighter,side):
 source=inspect.getsource(prior.run)
 replacements=(
  ('audit_v6083_current_mileena_{fighter}_p{side}','audit_v6088_current_mileena_{fighter}_p{side}'),
  ('state=original.gate(original.parse(log),fighter,side)',
   'state=health.gate(original.parse(log),fighter,side,guest)'),
  ('Path(__file__).resolve(),Path(current.__file__).resolve(),Path(original.__file__).resolve(),',
   'Path(__file__).resolve(),Path(prior.__file__).resolve(),Path(health.__file__).resolve(),Path(current.__file__).resolve(),Path(original.__file__).resolve(),'),
  (' env={k:v for k,v in os.environ.items()',
   " (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\\n')\n env={k:v for k,v in os.environ.items()"))
 for before,after in replacements:
  need(source.count(before)==1,'Exact whole native collector refill adaptation')
  source=source.replace(before,after,1)
 scope=dict(prior.run.__globals__,prior=prior,health=health,__file__=__file__)
 exec(compile(source,__file__+'::whole_current_native_capture_with_source_refill','exec'),scope)
 return scope['run'](fighter,side)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
 out=ROOT/f'audit_v6089_current_mileena_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh full native terminal report')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
