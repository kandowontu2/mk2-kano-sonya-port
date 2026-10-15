"""Real P2 Jax ground/Carry/owned-jump branches from the completed Ring test.

Retain the full original callback checker and5effective actual-record faults.
No prior close-guard unavailable-branch failure is changed or credited.
"""
import gzip,json,traceback
from pathlib import Path
import verify_current_sonya_p2_campaign_v5630 as whole
import run_sonya_p2_subzero_ring_retries_v5683 as capture
ROOT,need,sha=whole.ROOT,whole.need,whole.sha
OUT=ROOT/'audit_v5693_actual_jax_ring_callbacks_checked'


def run():
 need(not OUT.exists(),'Fresh actual native callback proof')
 positive_path=ROOT/'audit_v5686_sonya_p2_subzero_ring_retries_checked/report.json'
 positive=json.loads(positive_path.read_text())
 need(positive['passed']and positive['actualSubZeroAdvanceAccepted']and
  all(sha(p)==h for p,h in positive['inputHashes'].items()),'Actually completed source/guest/input/winner-qualified native Ring test')
 raw=gzip.open(capture.OUT/'run.log.gz','rb').read();text=raw.decode().replace('\r\n','\n')
 native=whole.jax_callbacks(text,capture.native.expected())
 need(len(native['actualNativeCallbackFaultsRejected'])==5,'All5actual native opcode/register/Carry/slot faults required')
 pins=dict(positive['inputHashes'])
 for p in [Path(__file__),Path(whole.__file__),positive_path]:pins[str(p.resolve())]=sha(p)
 failures=[ROOT/'audit_v5649_sonya_p2_jax_prefix_checked/report.json',
  ROOT/'audit_v5651_sonya_p2_jax_input_prefix_checked/report.json']
 for p in failures:
  need(json.loads(p.read_text())['passed']is False,'Original close-guard unavailable-branch/binding failures retained')
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every actual source/proof/failure byte intact')
 return dict(passed=True,physicalSlot=2,trueIdentity=18,trueJaxID=11,
  actualEntireNativeGroundCarryAndOwnedJumpGate=native,actualNativeInitializedGuestBytesComparedInRAM=1048576,
  inputHashes=pins,priorPhysicalGuestWinnerProof=str(positive_path),preservedUnavailableBranchFailures=list(map(str,failures)),
  scope='Real Jax11/P2Sonya18 ground-helper opcode/register/Carry and genuine human jump callbacks with5actual fault injections from the naturally completed Ring probe. Not a full tower/art/shadow/audio/port pass.',
  fullTowerAccepted=False,fullPortAcceptance=False)


if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable real native callback proof');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
