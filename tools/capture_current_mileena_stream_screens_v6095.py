"""Full current Mileena native transport with actual stream-phase screenshots."""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_mileena_native_v6082 as prior
import current_mileena_global_refill_v6093 as health
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
LUA=ROOT/'mk2ks_current_mileena_lookup_screens_v6090.lua'

def run(fighter,side):
 source=inspect.getsource(prior.run)
 replacements=(
  ('audit_v6083_current_mileena_{fighter}_p{side}','audit_v6096_current_mileena_{fighter}_p{side}'),
  ('state=original.gate(original.parse(log),fighter,side)',
   'state=health.gate(original.parse(log),fighter,side,guest)'),
  ('Path(__file__).resolve(),Path(current.__file__).resolve(),Path(original.__file__).resolve(),',
   "Path(__file__).resolve(),Path(prior.__file__).resolve(),Path(health.__file__).resolve(),ROOT/'tools/current_mileena_native_refill_v6085.py',ROOT/'mk2ks_current_mileena_native_v6081.lua',Path(current.__file__).resolve(),Path(original.__file__).resolve(),"),
  (' env={k:v for k,v in os.environ.items()',
   " (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\\n')\n env={k:v for k,v in os.environ.items()"),
  ("[s['age']for s in scenes]==[0,8,16,24,32,64,128,600]",
   "[s['age']for s in scenes]==[0]+[state['lookupFrame']-state['actionFrame']+i*4 for i in range(state['poseCount'])]+[600]"))
 for before,after in replacements:
  need(source.count(before)==1,'One whole stream-origin native screenshot transport adaptation')
  source=source.replace(before,after,1)
 scope=dict(prior.run.__globals__,prior=prior,health=health,LUA=LUA,__file__=__file__)
 exec(compile(source,__file__+'::whole_current_native_stream_capture','exec'),scope)
 report=scope['run'](fighter,side);report['screensTriggeredByActualNativeVictimLookup']=True
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
 out=ROOT/f'audit_v6097_current_mileena_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh actual native stream terminal report')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
