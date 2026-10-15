"""Record main-agent actual visual inspection, including a genuine failure."""
import json
from pathlib import Path
import verify_stock_scorpion_secondary_v1212 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1215_stock_secondary_visual_review';assert not OUT.exists()
inventory_path=ROOT/'audit_v1213_stock_secondary_contacts/inventory.json'
inventory=json.loads(inventory_path.read_text());assert inventory['sceneCount']==102
pins={str(inventory_path):proof.state.digest(inventory_path)};cases=[]
for record in inventory['cases']:
 for scene in record['scenes']:
  path=Path(scene['path']);assert proof.state.digest(path)==scene['sha256'];pins[str(path)]=scene['sha256']
 sheet=Path(record['sheet']);assert proof.state.digest(sheet)==record['sha256'];pins[str(sheet)]=record['sha256']
 stock=record['case'].startswith('control_');kano=record['case'].startswith('kano')
 cases.append(dict(case=record['case'],actualScenesReviewed=17,reviewer='main_agent_actual_view_image',
  naturalSecondaryAppearanceAccepted=stock,currentContinueScreenVisuallyAccepted=True,
  findings=(["Original headed spear reaction, severed upper body/lower stump, win/fatality and clean continue present."] if stock else
   ["The true victim body disappears during headed reaction; visible detached "+('knife' if kano else 'energy-ring')+" projectile art replaces it.",
    "Severed upper torso/lower stump appears afterwards; state completion does not cure the preceding missing body.",
    "Correct KANO/SONYA label and clean sampled continue; broader name/shadow/UI acceptance remains open."])))
report=dict(passed=False,manualVisualReviewComplete=True,sceneCount=102,cases=cases,inputHashes=pins,
 currentContinueScreenVisuallyAccepted=True,stockScorpionSecondaryNormalDeadPoolAppearanceAccepted=False,
 failure='Both true added victims select MK3 projectile artwork at native primary animation 55 in both slots.',
 sourceCause='build_mk2ks_mk3.py lacks a semantic primary-55 translation; its default equal-number MK3 primary-55 is detached projectile art.',
 failedOwnedGroups={'kano':['FF0131C0','FF013200','FF013240','FF013280','FF0132C0'],
                   'sonya':['FF0332E0','FF033320','FF033360','FF0333A0','FF0333E0']},
 nextRequiredFix='Give the original MKII primary-55 headed reaction its own true Kano/Sonya body-pose stream, preserving original control grammar and all detached projectile paths; test a new candidate.',
 fullScreenDMAReplayAccepted=False,allFatalityArtAccepted=False,allFloorShadowsAccepted=False,
 allSelectionGraphicsAccepted=False,audioAccepted=False,alternateCostumesAccepted=False,fullPortAccepted=False)
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print('102 actual scenes reviewed: stock controls look native; all four added-victim appearances FAIL primary-55 mapping')
