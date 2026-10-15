"""Additive full-scope checkpoint after the actual current air phase gate."""
import json
from datetime import datetime,timezone
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v6064_current_air_roles_progress/progress.json'
PROOF=ROOT/'audit_v6072_current_air_native_phase_scope_checked/report.json'
OUT=ROOT/'audit_v6074_current_air_native_phases_progress'

def run():
 previous=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,
      'Full original scope retained from actual current checkpoint')
 need(proof['passed']and proof['actualAirCatches']==16 and proof['trueKanoAirCycles']==10 and
      proof['stockJaxLivingOwnVictimCycles']==6 and proof['checkedPreAndPostTrajectoryFields']==3074 and
      proof['actualSourceIntegerCallbackFields']==428 and len(proof['actualSemanticFaultsRejected'])==48 and
      proof['nativeLivingLandingTransitionAccepted']and proof['stockJaxSourceBodySeparationAccepted']and
      not proof['fullPortAcceptance']and all(sha(p)==v for p,v in proof['inputHashes'].items()),
      'Entire actual source-native phase proof and negative controls, not a universal gameplay claim')
 current.expected()
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C',
      'Actual delivered current ZIP unchanged; no untested rebuild or package')
 audit=previous['requirementAudit']
 item=next(r for r in audit if r['requirement'].startswith('Complete native-feeling moves'))
 item['status']+=' Additional source-bound airborne phase verification qualifies all16 recorded catches: all3074 pre/post trajectory fields,428 genuine Kano callbacks, native fractional landing remainders, actor-specific living landing poses, and original Jax close-body delayed horizontal publication.48 actual record-corruption tests rejected. No game change was justified by the former test-only assumptions. Full Jax carry animation/invocation ledger and broader declared scope remain open.'
 item['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 pins=dict(proof['inputHashes']);pins.update({str(PARENT):sha(PARENT),str(PROOF):sha(PROOF),
      str(archive):sha(archive),str(Path(__file__).resolve()):sha(__file__)})
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=previous['remaining'],requirementAudit=audit,
      newInputHashes=pins,previousGoalTurnClassification='no progress: gratitude acknowledgement only',
      thisTurnClassification='progress: actual native source/trajectory/landing counterexamples resolved and whole paired matrix qualified',
      actualAirCatches=16,checkedPreAndPostTrajectoryFields=3074,actualSemanticFaultsRejected=48,
      nativeGameChanges=0,nativeBootsStarted=0,newBuildCopies=0,rawMediaFilesWritten=0,
      currentReleaseZIPUnchanged=True,fullGoalComplete=False,
      nextActions=['Finish source-bound stock Jax carry/callback coverage without changing native scratch state',
                   'Extend move and CPU checks to outstanding arena/KO/overlap contexts',
                   'Complete remaining finisher/cinematic/audio consumers and final integrated release regression'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive full-scope current checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','requirementAudit')},indent=2))
