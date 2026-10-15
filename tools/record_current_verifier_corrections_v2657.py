"""Retain failed test versions, exact corrections and repeated untouched controls.
Neither failure is accepted as game evidence; both are verifier-only defects.
"""
import json,re
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
OUT=ROOT/'audit_v2658_current_verifier_corrections_boundary'

def need(ok,label):
 if not ok:raise ValueError(label)

def verify():
 pins={}
 def pin(path,wanted=None):
  actual=launch.sha(path);need(wanted is None or actual==wanted,'Unchanged executed evidence '+str(path));pins[str(path)]=actual
 bad=ROOT/'tools/test_current_shao_cooldown_retreat_inputs_v2638.py'
 good=ROOT/'tools/test_current_shao_cooldown_retreat_inputs_v2645.py'
 pin(bad,'C94F68421181A7216C1D934A04DFD8E597E3060EBE9E810A952DA95DA5BD2A11')
 pin(good,'6BD21254696435822C220E619821BEC144B05E86F7D4B028AD5D5AF681BC27B2')
 text=bad.read_text().rstrip()+'\n'
 corrected=text.replace("r' frame=(\\\\d+)'","r' frame=(\\d+)'")
 corrected=corrected.replace(' outcomes=[]',' mutations=mutations[-2:]+mutations[:-2] # Exercise new cooldown-specific cases first.\n outcomes=[]')
 corrected=corrected.replace("  result=native.verify(folder,text_override=''.join(changed))","  need(changed!=lines,'Non-vacuous actual input/plan corruption '+name)\n  result=native.verify(folder,text_override=''.join(changed))")
 need(corrected==good.read_text().rstrip()+'\n','Exact sole negative-test regex, ordering and non-vacuity guard corrections')
 capture=ROOT/'audit_v2633_current_kano_p1_shao_cooldown_retreat_campaign/run.log';pin(capture)
 actual_line=next(line for line in capture.read_text(encoding='utf-8-sig').splitlines()if line.startswith('MK2_NAT_CAMPAIGN_BOSS_PLAN ')and 'stage=16'in line)
 old_mutation=re.sub(r' frame=(\\d+)',lambda m:' frame='+str(int(m[1])+12),actual_line,count=1)
 new_mutation=re.sub(r' frame=(\d+)',lambda m:' frame='+str(int(m[1])+12),actual_line,count=1)
 need(old_mutation==actual_line and new_mutation!=actual_line,'Actual captured row proves old mutation vacuous and corrected mutation non-vacuous')
 negatives={}
 for fighter in ('kano','sonya'):
  path=ROOT/f'audit_v2646_current_{fighter}_shao_cooldown_retreat_input_counterexamples/report.json';r=json.loads(path.read_text())
  need(r['passed'] and r['rejectedSpecificCounterexamples']==30 and r['finalUnmodifiedFullCampaignControlPassed'] and not r['fullPortAcceptance'],'Corrected full30-negative native control passed')
  for file,wanted in r['inputHashes'].items():pin(file,wanted)
  pin(path);negatives[fighter]=str(path)
 failed_source=ROOT/'tools/verify_current_friendship_v2652.py';correct_source=ROOT/'tools/verify_current_friendship_v2655.py'
 pin(failed_source,'F9B71B4C732A5D0C0B6477C71544F48A07E49B2C1F93C692CF0CA8BB5885E1D7')
 failed_path=ROOT/'audit_v2654_current_kano_friendship_p1_checked/report.json';pin(failed_path,'BA5DF505E5876B11D2D6FBF636F30C2544667E07DE2B48F8ADD9512B9A98EEC4')
 failure=json.loads(failed_path.read_text());need(not failure['passed'] and "multiple values for keyword argument 'scope'"in failure['error'],'Exact failed metadata-packaging error retained')
 restored=(failed_source.read_text().rstrip()+'\n').replace('return dict(passed=True,case=case,**control,currentWholeGuestAndPayloadReconstructed=True,',"return dict(passed=True,case=case,**{k:v for k,v in control.items()if k!='scope'},currentWholeGuestAndPayloadReconstructed=True,")
 need(restored==correct_source.read_text().rstrip()+'\n','Only duplicate scope packaging corrected; every native test untouched')
 pin(correct_source)
 friends={}
 for fighter in ('kano','sonya'):
  for side in (1,2):
   path=ROOT/f'audit_v2656_current_{fighter}_friendship_p{side}_checked/report.json';r=json.loads(path.read_text())
   need(r['passed'] and r['currentBuildPhysicalFriendshipAccepted'] and r['rejectedSpecificCounterexamples']==12 and r['finalUnmodifiedControlPassed'] and not r['fullPortAcceptance'],'Every corrected current physical Friendship control passed')
   for file,wanted in r['inputHashes'].items():pin(file,wanted)
   pin(path);friends[f'{fighter}_p{side}']=str(path)
 pin(Path(__file__).resolve());launch.module_pins(pins)
 return dict(passed=True,failedOriginalNegativeCheck=dict(source=str(bad),unifiedExecSession=35295,terminalExitCode=1,
  observedError='ValueError: Intended invariant rejects delayed_actual_48to59_cooldown_plan []',originalCheckAccepted=False,
  actualCapturedMutationWasVacuous=True),correctedNativeFullInputChecks=negatives,
  failedOriginalFriendshipMetadataCheck=dict(source=str(failed_source),report=str(failed_path),terminalExitCode=1,originalCheckAccepted=False),
  correctedCurrentFriendshipChecks=friends,executedSourcesAndCapturedGameplayNeverEdited=True,
  exactVerifierOnlyCorrections=True,gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Immutable correction/failure boundary')
 r=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
