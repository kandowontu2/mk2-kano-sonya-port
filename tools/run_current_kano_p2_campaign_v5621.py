"""Current5219 Kano P2: frozen physical policy, RAM-only media, gzip chronology.

Only host slot/provenance, hidden launch and preview printing change from5195.
No build, ROM copy, guest writes, save states or victory assistance.
"""
import inspect,json,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as native
import run_current_kano_p1_campaign_v5195 as original
import run_corrected_p1_campaigns_v5230 as corrected
import qualify_kano_current_p2_campaign_source_v4482 as boundary

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5622_current_kano_p2_campaign'
LUA=boundary.LUA
CONTROLLERS=list(boundary.TRANSITIVE_LUA)
qualify_payload_metadata_warning=corrected.metadata_clean

def capture_source():
 source=inspect.getsource(original.capture)
 changes=[
  ("MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='1'","MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='2'"),
  ('fighter=\'kano\',physicalSlot=1,','fighter=\'kano\',physicalSlot=2,'),
  ('Current4992 Kano P1 campaign started','Current5219 Kano P2 campaign started'),
  ("stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:",
   "stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict',\n  creationflags=subprocess.CREATE_NO_WINDOW)as process:"),
  ("      print('MK2_CURRENT_CAMPAIGN_PREVIEW_DATAURL data:image/png;base64,'+\n       base64.b64encode(preview.getvalue()).decode(),flush=True)",
   "      # RGB and generated preview remain RAM-only; print only the scene digest.")]
 for before,after in changes:
  need(source.count(before)==1,'One guarded whole host adaptation '+before)
  source=source.replace(before,after,1)
 return source

def capture():
 proof=boundary.source_boundary()
 need(proof['passed']and proof['physicalInputsExactlyUnchanged']and proof['physicalSlot']==2,
  'Previously qualified complete genuine Kano P2 physical controller unchanged')
 scope=dict(vars(original),__file__=__file__,native=native,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS,
  qualify_payload_metadata_warning=qualify_payload_metadata_warning)
 exec(compile(capture_source(),__file__+'::entire_host_capture','exec'),scope)
 return scope['capture']()

if __name__=='__main__':
 try:capture()
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():
   p=OUT/'capture_failure.json';need(not p.exists(),'Immutable failure')
   p.write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise
