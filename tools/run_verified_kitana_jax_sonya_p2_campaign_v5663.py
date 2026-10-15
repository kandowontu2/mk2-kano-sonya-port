"""Full native P2 campaign, qualified Kitana4/Jax11 Ring controller contexts."""
import inspect,json,re,traceback
import run_verified_kitana_sonya_p2_campaign_v5642 as base
import run_sonya_p2_jax_ring_bound_probe_v5658 as probe
ROOT,need,sha=base.ROOT,base.need,base.sha
native,original=base.native,base.original
OUT=ROOT/'audit_v5664_verified_kitana_jax_sonya_p2_campaign'
LUA='mk2ks_sonya_p2_verified_kitana_jax_campaign_v5662.lua'
CONTROLLERS=[LUA,*probe.CONTROLLERS]
capture_source=base.capture_source
qualify_payload_metadata_warning=base.qualify_payload_metadata_warning

def source_boundary():
 base.source_boundary()
 report=json.loads((ROOT/'audit_v5661_sonya_p2_jax_ring_probe_checked/report.json').read_text())
 need(report['passed']and report['native']['actualJaxEncounterWon']and
  report['native']['actualOwnJaxRoundWins']==2 and len(report['actualInputStateAndNativeWinnerFaultsRejected'])==11 and
  all(sha(p)==h for p,h in report['inputHashes'].items()),'Actually completed/fault-qualified ordinary Jax strategy')
 text='\n'.join((ROOT/n).read_text()for n in CONTROLLERS)
 need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|return\s+data',text),
  'Every transitive source, buttons/read observers only, no guest-state assistance')
 return dict(passed=True,physicalSlot=2,trueIdentity=18,originalPhysicalPolicyUnchanged=True,
  declaration='Qualified existing Ring strategy includes Kitana4 and Jax11; other input policies unchanged; only probe exit removed',
  actualCurrentNaturalClearAccepted=False,fullPortAcceptance=False)

def capture():
 source_boundary()
 scope=dict(vars(original),__file__=__file__,native=native,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS,
  qualify_payload_metadata_warning=qualify_payload_metadata_warning)
 exec(compile(capture_source(),__file__+'::entire_full_native_campaign_host','exec'),scope)
 return scope['capture']()

if __name__=='__main__':
 try:capture()
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():(OUT/'capture_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise
