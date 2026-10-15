"""Whole original RAM native transport; close-range controllers and bounded PNGs."""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_basic_ground_v5994 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
LUA=ROOT/'mk2ks_close_contacts_v6025.lua'

def run(fighter,side):
 source=inspect.getsource(earlier.run)
 for before,after in(
  ('audit_v5995_basic_{fighter}_p{side}','audit_v6027_contacts_{fighter}_p{side}'),
  ("results[0]['phases']=='25'and results[0]['terminalAge']=='1540'","results[0]['phases']=='7'"),
  ("len(scenes)>=75 and any(s['stage']=='ordinary_final'for s in scenes)","len(scenes)>=36 and any(s['stage']=='contacts_final'for s in scenes)"),
  ("\"(folder/'ordinary_preview.png').write_bytes(png.getvalue())\",",
   "\"(folder/'contacts_preview.png'if 'sheet'in locals()else folder/('native_'+f['stage']+'.png')).write_bytes(png.getvalue())\",")):
  need(source.count(before)==1,'Exact whole original transport adaptation '+before[:70]);source=source.replace(before,after,1)
 before=' for before,after in replacements.items():'
 after=""" replacements[\"if f['attempt']=='1'and f['stage']=='phase_16': # One native full frame plus compact sheet.\"]=\"if f['stage']in('own_high_punch_block_phase32','own_low_kick_crouch_block_phase32','own_ground_throw_entry','own_ground_throw_phase48','stock_ground_throw_phase48','contacts_final'): # Bounded native interaction previews.\"
 for before,after in replacements.items():"""
 need(source.count(before)==1,'Underlying whole original preview map');source=source.replace(before,after,1)
 scope=dict(earlier.run.__globals__,LUA=LUA,__file__=__file__)
 exec(compile(source,__file__+'::whole_RAM_transport_close_contacts','exec'),scope)
 report=scope['run'](fighter,side)
 report['inputHashes'][str(Path(earlier.__file__).resolve())]=sha(earlier.__file__)
 report.update(actualCloseBlockThrowPhysicalProofPending=True,wholeCurrentBodyShadowProofPending=True)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v6028_contacts_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh immutable native close-range capture')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
