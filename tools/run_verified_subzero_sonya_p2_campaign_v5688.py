"""Full native Sonya P2, genuinely qualified Ring contexts4/11/8."""
import inspect,json,re,traceback
import run_verified_kitana_jax_sonya_p2_campaign_v5663 as previous
import run_sonya_p2_subzero_ring_probe_v5672 as probe
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
native,original=previous.native,previous.original
OUT=ROOT/'audit_v5689_verified_subzero_sonya_p2_campaign'
LUA='mk2ks_sonya_p2_verified_subzero_campaign_v5687.lua'
CONTROLLERS=[LUA,*probe.CONTROLLERS]
capture_source=previous.capture_source
qualify_payload_metadata_warning=previous.qualify_payload_metadata_warning


def source_boundary():
 previous.source_boundary()
 report=json.loads((ROOT/'audit_v5686_sonya_p2_subzero_ring_retries_checked/report.json').read_text())
 need(report['passed']and report['actualSubZeroAdvanceAccepted']and
  report['native']['actualFinalMatchOwnRoundWins']==2 and report['native']['actualFinalMatchCpuRoundWins']==0 and
  report['actualContext8PhysicalFields']==3646 and report['actualContext8RingTasks']==40 and
  len(report['actualInputStateAndNativeWinnerFaultsRejected'])==11 and
  len(report['actualContext8TaskAndActionFaultsRejected'])==8 and
  all(sha(p)==h for p,h in report['inputHashes'].items()),'Actual independently qualified native Sub-Zero clear and19real faults')
 text='\n'.join((ROOT/n).read_text()for n in CONTROLLERS)
 need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|return\s+data',text),
  'All transitive sources remain physical buttons/passive observers only')
 return dict(passed=True,physicalSlot=2,trueIdentity=18,originalPhysicalPolicyUnchanged=True,
  declaration='Qualified existing Ring strategy contexts Kitana4,Jax11,Sub-Zero8; other policies unchanged; only probe exit removed',
  unexecutedCloseGuardUppercut107GateAccepted=False,actualCurrentNaturalClearAccepted=False,fullPortAcceptance=False)


def capture():
 source_boundary()
 scope=dict(vars(original),__file__=__file__,native=native,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS,
  qualify_payload_metadata_warning=qualify_payload_metadata_warning)
 exec(compile(capture_source(),__file__+'::entire_native_full_campaign_host','exec'),scope)
 return scope['capture']()


if __name__=='__main__':
 try:capture()
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():(OUT/'capture_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise
