"""Whole ordinary transport, settled crouch input and actual queued-exit frame.

No game code changes. Retain initial failed terminal admission and unactivated
crouch attempts. Render only bounded small native proof PNGs, never raw dumps.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_basic_ground_v5994 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
LUA=ROOT/'mk2ks_basic_settled_crouch_v6007.lua'

def run(fighter,side):
 failed=ROOT/f'audit_v6004_basic_{fighter}_p{side}_observed/report.json';prior=json.loads(failed.read_text())
 need(not prior['passed']and 'All ordinary physical phases and clean live final recovery'in prior['error'],
      'Original actual one-extra-exit-field admission failure preserved')
 source=inspect.getsource(earlier.run)
 before='audit_v5995_basic_{fighter}_p{side}';need(source.count(before)==1,'One new settled-input capture')
 source=source.replace(before,'audit_v6009_settled_basic_{fighter}_p{side}',1)
 before="results[0]['terminalAge']=='1540'";need(source.count(before)==1,'One exact queued-native-exit frame correction')
 source=source.replace(before,"results[0]['terminalAge']=='1541'",1)
 # Bind all runtime-loaded Lua sources, not just the top wrapper.
 before="LUA,ROOT/'mk2ks_special_shadow_v5131.lua'"
 need(source.count(before)==1,'One whole executed source chain pin')
 source=source.replace(before,"LUA,ROOT/'mk2ks_special_shadow_v5131.lua',ROOT/'mk2ks_basic_ground_shadow_v5993.lua',ROOT/'mk2ks_basic_ground_separator_v6001.lua'",1)
 before="if f['attempt']=='1'and f['stage']=='phase_16': # One native full frame plus compact sheet."
 after="if f['stage']in('idle_phase12','crouch_phase12','standing_block_phase12','forward_jump_phase12','ordinary_final'): # Bounded exact full native visual evidence."
 need(source.count(before)==1,'One bounded native preview selection')
 source=source.replace(before,after,1)
 # The original replacement maps both PNG prints to the sheet path; preserve
 # exact full-frame evidence separately before making the final contact sheet.
 before="\"(folder/'ordinary_preview.png').write_bytes(png.getvalue())\","
 need(source.count(before)==1,'One declared compact sheet output mapping')
 source=source.replace(before,"\"(folder/('native_'+f['stage']+'.png')if 'f'in locals()and f.get('stage')in('idle_phase12','crouch_phase12','standing_block_phase12','forward_jump_phase12','ordinary_final')and len(preview)<76 else folder/'ordinary_preview.png').write_bytes(png.getvalue())\",",1)
 scope=dict(earlier.run.__globals__,LUA=LUA,__file__=__file__)
 exec(compile(source,__file__+'::entire_ordinary_transport_settled_crouch','exec'),scope)
 report=scope['run'](fighter,side)
 for p in(Path(earlier.__file__).resolve(),ROOT/'tools/capture_current_basic_separator_v6002.py',failed):report['inputHashes'][str(p)]=sha(p)
 report.update(retainedFailedTerminalAdmission=str(failed),settledCrouchActivationVerificationPending=True,
               fullOrdinaryStateBodyShadowProofPending=True,previewPNGArtifactsWritten=len(list((ROOT/f'audit_v6009_settled_basic_{fighter}_p{side}').glob('*.png'))))
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v6010_settled_basic_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh immutable settled ordinary capture')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
