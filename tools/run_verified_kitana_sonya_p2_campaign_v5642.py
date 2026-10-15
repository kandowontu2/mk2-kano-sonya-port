"""Full current native Sonya P2, now using qualified Kitana Ring spacing."""
import json,re,traceback
import run_current_sonya_p2_campaign_v5628 as base
ROOT,need,sha=base.ROOT,base.need,base.sha
native,original=base.native,base.original
OUT=ROOT/'audit_v5643_verified_kitana_sonya_p2_campaign'
LUA='mk2ks_sonya_p2_verified_kitana_campaign_v5641.lua'
CONTROLLERS=[LUA,'mk2ks_sonya_p2_kitana_ring_probe_v5636.lua',*base.CONTROLLERS]
capture_source=base.capture_source
qualify_payload_metadata_warning=base.qualify_payload_metadata_warning

def source_boundary():
 base.source_boundary()
 report=json.loads((ROOT/'audit_v5640_sonya_p2_kitana_ring_probe_checked/report.json').read_text())
 need(report['passed']and report['native']['actualKitanaEncounterWon']and
  report['native']['actualOwnKitanaRoundWins']==2 and len(report['actualInputStateAndNativeWinnerFaultsRejected'])==11 and
  all(sha(p)==h for p,h in report['inputHashes'].items()),'Actually completed/fault-qualified ordinary Kitana strategy; no timer/position/health help')
 text='\n'.join((ROOT/n).read_text()for n in CONTROLLERS)
 need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|return\s+data',text),
  'Whole transitive source, no guest state or tap replacements')
 return dict(passed=True,physicalSlot=2,trueIdentity=18,originalPhysicalPolicyUnchanged=True,
  declaration='Existing physical Ring-spacing strategy now includes Kitana4; all other input policies unchanged',
  actualCurrentNaturalClearAccepted=False,fullPortAcceptance=False)

def capture():
 source_boundary()
 scope=dict(vars(original),__file__=__file__,native=native,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS,
  qualify_payload_metadata_warning=qualify_payload_metadata_warning)
 exec(compile(capture_source(),__file__+'::entire_full_campaign_host','exec'),scope)
 return scope['capture']()

if __name__=='__main__':
 try:capture()
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():(OUT/'capture_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise
