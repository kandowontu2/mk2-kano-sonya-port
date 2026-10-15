"""Add source-qualified carried-victim evidence without narrowing the port goal."""
import json
from datetime import datetime,timezone
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v6074_current_air_native_phases_progress/progress.json'
PROOF=ROOT/'audit_v6078_current_jax_carried_routes_checked/report.json'
OUT=ROOT/'audit_v6080_current_carried_victims_progress'

def run():
 previous=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(previous['passed']and previous['goalStatus']=='active'and len(previous['remaining'])==5,
      'Retain complete original requirements, not only the present airborne subset')
 need(proof['passed']and proof['actualJaxLivingOwnVictimCycles']==6 and
      proof['pairedCarryPreAndPostFields']==840 and len(proof['actualSemanticFaultsRejected'])==24 and
      proof['wholeObservedCarriedVictimChoreographyAccepted']and
      not proof['actualCallbackInvocationLedgerAccepted']and not proof['fullPortAcceptance']and
      all(sha(p)==v for p,v in proof['inputHashes'].items()),
      'Whole actual six-throw source/field/pose/coupling proof and24 real negative controls')
 current.expected()
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C',
      'Protected delivered ZIP remains the actual tested current build')
 audit=previous['requirementAudit']
 item=next(r for r in audit if r['requirement'].startswith('Complete native-feeling moves'))
 item['status']+=' The carried-victim gap is now source-qualified for all six actual living Kano/Sonya Jax throws in both physical slots:840 paired pre/post carry fields, whole fractional copied-VY coupling, native10/48pixel stream offsets, own victim pose progression and exact same/next-field free-flight handoff.24 additional actual record corruptions rejected. Original Jax behavior is verified through the two complete existing Kano-only ID routers. Its callback invocation was not tapped and is not claimed; broader arena/CPU/finisher/audio/integrated scope remains open.'
 item['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 pins=dict(proof['inputHashes']);pins.update({str(PARENT):sha(PARENT),str(PROOF):sha(PROOF),
      str(archive):sha(archive),str(Path(__file__).resolve()):sha(__file__)})
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=previous['remaining'],requirementAudit=audit,
      newInputHashes=pins,previousGoalTurnClassification='progress: native landing/trajectory matrix qualified',
      thisTurnClassification='progress: complete recorded living carried-victim choreography verified against original source and existing ID-only routers',
      actualJaxLivingOwnVictimCycles=6,pairedCarryPreAndPostFields=840,newActualSemanticFaultsRejected=24,
      actualCallbackInvocationLedgerAccepted=False,nativeGameChanges=0,nativeBootsStarted=0,
      newBuildCopies=0,rawMediaFilesWritten=0,currentReleaseZIPUnchanged=True,fullGoalComplete=False,
      nextActions=['Broaden native arena/CPU/repeated-KO/overlap move-phase coverage',
                   'Complete remaining finisher/victim/cinematic/audio consumer checks',
                   'Run final integrated selection-to-gameplay regression and matching release audit'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive whole-scope carry checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','requirementAudit')},indent=2))
