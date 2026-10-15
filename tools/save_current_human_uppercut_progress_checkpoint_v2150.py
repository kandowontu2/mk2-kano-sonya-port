"""Correct CPU-versus-human uppercut classification, preserving all prior evidence."""
import json
from pathlib import Path
import verify_current_boss_human_uppercut_campaign_v2148 as model

ROOT=model.ROOT
PREVIOUS=ROOT/'audit_v2147_current_pit_campaign_progress_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2150_current_human_uppercut_progress_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=model.digest(Path(path))
  assert wanted is None or actual==wanted,'Changed accepted dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting accepted dependency '+path
  pins[path]=actual
 pin(PREVIOUS);pin(__file__)
 corrected={}
 kano_rows=None
 for name,capture in (
  ('kano_p1','audit_v2143_current_kano_p1_delayed_ground_counter_campaign'),
  ('sonya_p1','audit_v2144_current_sonya_p1_delayed_ground_counter_campaign')):
  path=ROOT/f'audit_v2149_current_{name}_human_uppercut_checked/report.json'
  report=json.loads(path.read_text())
  assert report['passed']and report['bounded_campaign_evidence_proven']and not report['unassisted_clear_proven']
  assert report['fullPortAcceptance']is False and report['humanUppercutNativeAction']=='0107'
  assert report['cpu106NeverUsedToClassifyHumanUppercut']is True
  for file,wanted in report['inputHashes'].items():pin(file,wanted)
  pin(path)
  rows=model.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),1,name.split('_')[0])
  real=[row for row in rows if row['tag']=='BOSS_ACTION'and row['after']==0x107]
  assert len(real)==report['actualNativeUppercutAssignments']
  case=prior['currentGroundedBossCampaigns'][capture]
  case['supersededCPU106OnlyReport']=case['report']
  case['report']=str(path)
  case['nativeHumanUppercut107Assignments']=len(real)
  case['humanUppercutFrames']=report['uppercutAssignmentFrames']
  case.pop('native106UppercutAssignments',None)
  corrected[name]=dict(report=str(path),humanAction='0107',CPU106NotHumanPath=True,
   actualAssignments=len(real),frames=report['uppercutAssignmentFrames'])
  if name=='kano_p1':kano_rows=rows
 assert corrected['kano_p1']['frames']==[55628]and corrected['sonya_p1']['actualAssignments']==0
 # Bind the observed interrupted attack to actual own fields, native health
 # subtraction and original hurt-task store. Do not credit a missed attack.
 fields={row['frame']:row for row in kano_rows if row['tag']=='BOSS_FIELD'}
 actions=[row for row in kano_rows if row['tag']=='BOSS_ACTION']
 health=[row for row in kano_rows if row['tag']=='HEALTH']
 start=next(row for row in actions if row['frame']==55628 and row['after']==0x107)
 assert start['id']==start['roster']==17 and start['pc']==0xff83c340
 assert all(fields[frame]['human_action']==0x107 and
            fields[frame]['human_actor']==start['actor']and fields[frame]['human_main']==start['main']
            for frame in range(55629,55632))
 damage=[row for row in health if row['frame']==55631 and row['slot']==1 and row['pc']==0xff836700]
 assert len(damage)==1 and (damage[0]['before'],damage[0]['after'])==(41,1)
 assert damage[0]['a8']==fields[55631]['cpu_actor']and damage[0]['a13']==fields[55631]['cpu_main']
 hurt=next(row for row in actions if row['frame']==55631 and row['before']==0x107 and row['after']==0x503)
 assert hurt['actor']==start['actor']and hurt['main']==start['main']and hurt['pc']==0xff8d49b0
 assert fields[55632]['human_action']==0x503 and fields[55632]['health']=='1,106'
 assert all(fields[frame]['health'].split(',')[1]=='106'for frame in range(55628,55633))
 interrupted=dict(actor=start['actor'],main=start['main'],id=17,assignment=55628,
  humanAction='0107',incomingNativeDamageFrame=55631,damage=40,hurtAction='0503',
  ownHitProven=False,fullMoveRecoveryArtAudioAccepted=False)
 for file,wanted in pins.items():assert model.digest(Path(file))==wanted,'Changed checkpoint dependency '+file
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='progress: all four controlled Pit negative suites and five independently checked grounded boss trajectories',
  thisGoalTurnClassification='progress: original human uppercut animation28/action107 distinguished from CPU106; corrected two current campaign proofs and bound actual Kano activation/interruption to original collision damage and native hurt action',
  humanUppercutClassifierCorrection=corrected,currentKanoHumanUppercutInterrupted=interrupted,
  supersededUppercutClassifier='Earlier2142/2146countedCPU106 rather than original human107. Their trajectory proofs remain bounded; their count is not accepted as the number of human uppercuts. New2148/2149uses unchanged original human routine bytes, main-animation28, action107 and original assignment instruction/register ownership.',
  nextAction='Run a clean physical two-player Down/HP command with neutral input history beyond the native history window; prove both genuine human uppercuts and full move/ground/shadow/recovery. Use that evidence to improve physical boss tactics, then prove both full campaigns/endings and every remaining finisher/victim/morph/secret/cinematic/audio requirement before final regression, cleanup and release.',
  inputHashes=pins,goalStatus='active',finishedRelease=False,fullPortAcceptance=False)
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable checkpoint only'
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',humanUppercutAction='0107',
  actualKanoAssignments=report['humanUppercutClassifierCorrection']['kano_p1']['actualAssignments'],
  actualSonyaAssignments=report['humanUppercutClassifierCorrection']['sonya_p1']['actualAssignments'],
  KanoAssignmentInterruptedByNative40Damage=True,rejectedSpecificPitCounterexamples=report['rejectedSpecificPitCounterexamples'],
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False),indent=2))
