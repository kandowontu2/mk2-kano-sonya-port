"""Whole5994 native transport: settled crouch, correct exit and bounded previews.

Keep the actual6008 pre-native graft failure. Insert preview substitutions into
the actual underlying collector replacement map, not its wrapper's source text.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_basic_ground_v5994 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
LUA=ROOT/'mk2ks_basic_settled_crouch_v6007.lua'

def run(fighter,side):
 failure=ROOT/'audit_v6010_settled_basic_kano_p1_observed/report.json'
 need(not json.loads(failure.read_text())['passed']and 'One bounded native preview selection'in json.loads(failure.read_text())['error'],
      'Actual pre-native collector-wrapper mismatch retained')
 source=inspect.getsource(earlier.run)
 for before,after in(
  ('audit_v5995_basic_{fighter}_p{side}','audit_v6012_basic_{fighter}_p{side}'),
  ("results[0]['terminalAge']=='1540'","results[0]['terminalAge']=='1541'"),
  ("LUA,ROOT/'mk2ks_special_shadow_v5131.lua'","LUA,ROOT/'mk2ks_special_shadow_v5131.lua',ROOT/'mk2ks_basic_ground_shadow_v5993.lua',ROOT/'mk2ks_basic_ground_separator_v6001.lua'"),
  ("\"(folder/'ordinary_preview.png').write_bytes(png.getvalue())\",",
   "\"(folder/'ordinary_preview.png'if 'sheet'in locals()else folder/('native_'+f['stage']+'.png')).write_bytes(png.getvalue())\",")):
  need(source.count(before)==1,'Exact whole original settled controls adaptation '+before[:70]);source=source.replace(before,after,1)
 before=' for before,after in replacements.items():'
 after=""" replacements[\"if f['attempt']=='1'and f['stage']=='phase_16': # One native full frame plus compact sheet.\"]=\"if f['stage']in('idle_phase12','crouch_phase12','standing_block_phase12','forward_jump_phase12','ordinary_final'): # Bounded exact native preview.\"
 for before,after in replacements.items():"""
 need(source.count(before)==1,'Actual underlying collector preview map insertion');source=source.replace(before,after,1)
 scope=dict(earlier.run.__globals__,LUA=LUA,__file__=__file__)
 exec(compile(source,__file__+'::entire_native_transport_settled_controls_previews','exec'),scope)
 report=scope['run'](fighter,side)
 for p in(Path(earlier.__file__).resolve(),ROOT/'tools/capture_current_basic_separator_v6002.py',ROOT/'tools/capture_current_settled_basic_v6008.py',failure,
          ROOT/f'audit_v6004_basic_{fighter}_p{side}_observed/report.json'):
  report['inputHashes'][str(p)]=sha(p)
 folder=ROOT/f'audit_v6012_basic_{fighter}_p{side}'
 report.update(settledCrouchActivationVerificationPending=True,fullOrdinaryStateBodyShadowProofPending=True,
               previewPNGArtifactsWritten=len(list(folder.glob('*.png'))),retainedPreNativePreviewGraftFailure=str(failure))
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v6013_basic_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh immutable settled native preview capture')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
