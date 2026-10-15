"""Entire real P2 campaign/boss/own-ending/300attract and native fault gates.

Dispatch every actual Ring4/11/8 field through the independent whole replay.
The guard uppercut policy is not executed at8; require actual context8 Ring
tasks instead, retain the full mirrored Leg and original native Jax callback
gates, and explicitly leave the unexecuted Sub-Zero HUMAN107 branch unproven.
All18actual native/guest faults and5native Jax Carry faults remain mandatory.
"""
import inspect,json,traceback
from pathlib import Path
import verify_current_sonya_p2_campaign_v5630 as previous
import verify_sonya_p2_subzero_ring_probe_v5674 as ring
import run_verified_subzero_sonya_p2_campaign_v5688 as capture
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5691_verified_subzero_sonya_p2_campaign_checked'


def whole_run():
 scope=dict(vars(previous),__file__=__file__,capture=capture,OUT=OUT,ring=ring)
 exec(compile(inspect.getsource(previous.matched),__file__+'::entire_current_provenance','exec'),scope)
 source=inspect.getsource(previous.whole_run)
 changes=[('range_replay=original.slot.sonya.spacing.replay','range_replay=ring.make_replay()'),
  ('kitana=SimpleNamespace(make_replay=p2_factory(kitana.make_replay,kitana))','kitana=SimpleNamespace(make_replay=ring.make_replay)'),
  ('jax=SimpleNamespace(make_replay=p2_factory(jax.make_replay,jax))','jax=SimpleNamespace(make_replay=ring.make_replay)'),
  ('subzero_carrier=SimpleNamespace(make_replay=p2_factory(subzero.make_replay,subzero))','subzero_carrier=SimpleNamespace(make_replay=ring.make_replay)')]
 for before,after in changes:
  need(source.count(before)==1,'One actual qualified Ring-context physical replay dispatch '+before)
  source=source.replace(before,after,1)
 old="need(sub['actualNativeHumanUppercut107Stores']>0 and sub['actualNativeLegActivations']>0,\n  'Actual owned original uppercuts/leg moves, not physical attempts alone')"
 new="need(sub['actualFieldsByNativeStage'].get(7,0)>0 and sub['actualNativeOwnRingTasks']>0 and guard['actualNativeLegActivations']>0,\n  'Every actual context8 Ring field, owned Ring tasks and unchanged mirror Leg activation; never credit unexecuted guard/uppercut commands')"
 marker='  for before,after in changes:'
 need(source.count(marker)==1,'One whole original per-function semantic adaptation list')
 source=source.replace(marker,"  if function is original.run:changes.append(("+repr(old)+','+repr(new)+"))\n"+marker,1)
 exec(compile(source,__file__+'::entire_native_campaign_and_actual_Ring_dispatch','exec'),scope)
 report=scope['whole_run']()
 proof_path=ROOT/'audit_v5686_sonya_p2_subzero_ring_retries_checked/report.json'
 proof=json.loads(proof_path.read_text())
 need(proof['passed']and proof['actualSubZeroAdvanceAccepted']and
  len(proof['actualInputStateAndNativeWinnerFaultsRejected'])==11 and
  len(proof['actualContext8TaskAndActionFaultsRejected'])==8 and
  all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual independently qualified context8 strategy and19faults')
 actual=report['actualFullRingSpacingInputReplay']['actualFieldsByNativeStage']
 need(all(actual.get(stage,0)>0 for stage in(2,4,7)),
  'Whole current campaign replays every Kitana/Jax/Sub-Zero field, not just an earlier probe')
 need(len(report['actualFullNativeJaxCallbacks']['actualNativeCallbackFaultsRejected'])==5 and
  len(report['actualNativeAndRAMProofFaultsRejected'])==18 and report['actualAttractFollowThroughFields']==300,
  'Original native callback, whole guest/native faults and all300actual attract fields retained')
 report.update(allActualRingContexts=[4,11,8],
  subzeroPhysicalStrategy='Already qualified actual Ring-and-retreat inputs, not the unused close-guard prime policy',
  unexecutedSubZeroHuman107BranchAccepted=False,priorContext8StrategyProof=str(proof_path),
  fullPortAcceptance=False)
 for p in [Path(__file__),Path(ring.__file__),proof_path]:report['inputHashes'][str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual compiled/control/proof/source byte intact')
 return report


if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal; never restart a live native job')
 need(not OUT.exists(),'Fresh immutable whole native campaign verdict')
 try:report=whole_run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
 if report['passed']:print(json.dumps({k:v for k,v in report['case'].items()if k not in('inputHashes','uppercutAssignmentFrames')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
