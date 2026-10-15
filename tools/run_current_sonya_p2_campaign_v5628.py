"""Current5219 Sonya P2, existing extended physical policy and RAM/gzip transport."""
import inspect,json,re,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as native
import run_extended_sonya_p1_campaign_v5207 as original
import run_corrected_p1_campaigns_v5230 as corrected
ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5629_current_sonya_p2_campaign'
LUA='mk2ks_sonya_current_p2_extended_ram_v5627.lua'
CONTROLLERS=[LUA,*original.CONTROLLERS]
qualify_payload_metadata_warning=corrected.metadata_clean

def source_boundary():
 prior=json.loads((ROOT/'audit_v5235_sonya_corrected_p1_campaign_checked/report.json').read_text())
 need(prior['passed']and prior['actualCorrectedExecutableNaturalTowerOwnEndingAttractAccepted'],
  'Existing current complete Sonya P1 native clear/ending/attract proof')
 for name in original.CONTROLLERS:
  p=ROOT/name
  need(prior['inputHashes'][str(p.resolve())]==sha(p),'Every original physical source unchanged '+name)
 text='\n'.join((ROOT/name).read_text()for name in CONTROLLERS)
 need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|return\s+data',text),
  'All source loaders/controller/observers have no guest/AI/health/ID/RNG writes or tap replacement')
 wrapper=(ROOT/LUA).read_text()
 names=set(re.findall(r"\['([^']+\.lua)'\]=true",wrapper))
 need(names==set(original.CONTROLLERS)-{'mk2ks_mileena_campaign_trace_v3848.lua'},
  'Every exact existing transitive source is declared once; original passive cache observer retained')
 need(wrapper.count("set_value")==wrapper.count("clear_value")==0 and
  "local prefix=source:sub(1,first-1);local observer=source:sub(first)"in wrapper and
  "source=prefix..observer"in wrapper,'Wrapper only changes preconditions and independent readonly observer; no buttons')
 return dict(passed=True,physicalSlot=2,trueIdentity=18,originalPhysicalPolicyUnchanged=True,
  actualCurrentNaturalClearAccepted=False,fullPortAcceptance=False)

def capture_source():
 source=inspect.getsource(original.capture)
 changes=[
  ("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'","MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='2'"),
  ("fighter='sonya',physicalSlot=1,","fighter='sonya',physicalSlot=2,"),
  ('Current4992 exact-tested-prime Sonya P1 campaign started','Current5219 Sonya P2 campaign started'),
  ("stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:",
   "stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict',\n  creationflags=subprocess.CREATE_NO_WINDOW)as process:"),
  ("      print('MK2_CURRENT_CAMPAIGN_PREVIEW_DATAURL data:image/png;base64,'+\n       base64.b64encode(preview.getvalue()).decode(),flush=True)",
   "      # Native RGB and preview stay RAM-only; emit scene digest only.")]
 for before,after in changes:
  need(source.count(before)==1,'Exact single host slot/printing adaptation '+before)
  source=source.replace(before,after,1)
 return source

def capture():
 source_boundary()
 scope=dict(vars(original),__file__=__file__,native=native,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS,
  qualify_payload_metadata_warning=qualify_payload_metadata_warning)
 exec(compile(capture_source(),__file__+'::entire_host_capture','exec'),scope)
 return scope['capture']()

if __name__=='__main__':
 try:capture()
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():
   p=OUT/'capture_failure.json';need(not p.exists(),'Immutable failure');p.write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise
