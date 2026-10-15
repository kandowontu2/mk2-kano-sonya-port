"""Completed P2 gameplay and explicit carry-in audio limitation, compactly."""
import json,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def main():
 out=ROOT/'audit_launch_challenger_transition_p2_progress_storage'
 need(not out.exists()and not native.census(),'Fresh journal; native jobs terminal')
 parentpath=ROOT/'audit_launch_challenger_transition_progress_storage/report.json';parent=json.loads(parentpath.read_text())
 need(parent['passed'],'Previous P1 evidence retained');pins=dict(parent['inputHashes']);pins[str(parentpath)]=sha(parentpath)
 fullpath=ROOT/'audit_launch_challenger_transition_checked_square_p2/report.json';full=json.loads(fullpath.read_text())
 finitepath=ROOT/'audit_launch_challenger_transition_finite_ball_p2/report.json';finite=json.loads(finitepath.read_text())
 need(full['passed']and full['nativeTerminal']['pid']==162936 and full['nativeTerminal']['nativeExit']==0 and full['completeSourceWaveform']['differentChannelSamples']==0,'Actual Sonya P2 whole source-qualified normal terminal')
 need(finite['passed']and finite['nativeTerminal']['pid']==87336 and finite['nativeTerminal']['nativeExit']==0 and not finite['completeSourceWaveformAccepted']and not finite['allSlotOwnershipAccepted'],'Actual Kano P2 gameplay pass without unavailable carry-in audio upgrade')
 for p in(full,finite):need(p['wholeOriginalJoinedGameplay']['ordinaryTailFieldsPerSlot']==600 and not p['fullPortAcceptance'],'Whole post-join controls and finite scope retained')
 faultpath=ROOT/'audit_launch_challenger_transition_faults_square_p2/report.json';fault=json.loads(faultpath.read_text());need(fault['passed']and len(fault['actualFaultsRejected'])==16 and len(finite['actualFaultsRejected'])==4,'Actual P2 fault suite')
 reports=[fullpath,finitepath,faultpath]
 for name in('audit_launch_challenger_transition_no_damage_store_rejection_ball_p2','audit_launch_challenger_transition_cpu_carry_rejection_ball_p2','audit_launch_challenger_transition_fault_alias_rejection_square_p2'):
  p=ROOT/name/'failure.json';need(not json.loads(p.read_text())['passed'],'Preserved actual checker rejection');reports.append(p)
 reviewed=[]
 for move in('ball','square'):
  p=ROOT/f'audit_launch_challenger_transition_visual_{move}_p2/report.json';v=json.loads(p.read_text());need(v['passed']and not v['fullRasterAcceptance'],'Finite actual viewed native frames only');reports.append(p);reviewed+=v['viewedFrameHeaders']
 leaves=[p.parent for p in reports]+[ROOT/f'audit_launch_challenger_transition_rgb_{move}_p2_delay1'for move in('ball','square')]
 files={p for leaf in leaves for p in leaf.rglob('*')if p.is_file()}
 files.update(ROOT/name for name in('tools/qualify_launch_challenger_transition_remaining.py','tools/qualify_launch_challenger_transition_remaining_v2.py','tools/check_launch_challenger_transition_remaining_v3.py','tools/qualify_launch_challenger_kano_p2_finite.py','tools/record_launch_challenger_p2_review.py','tools/journal_launch_challenger_p2.py'))
 for p in reports:
  value=json.loads(p.read_text());pins[str(p)]=sha(p)
  for q,h in value.get('inputHashes',{}).items():need(sha(q)==h,'Stable original executed evidence');pins[q]=h
 need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Bounded reports/text/source, no raw media')
 selected=[];total=0;seen=set()
 for p in sorted(files):
  h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact lossless bounded compression')
  after=allocated(p)
  if key not in seen:total+=after;seen.add(key)
  pins[str(p)]=h;selected.append(dict(path=str(p),sha256=h,beforeAllocatedBytes=before,allocatedBytes=after))
 current.expected();builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census()and all(sha(p)==h for p,h in pins.items()),'All playable/source pins intact; no new build/cache/native job')
 fields=sum(p['completePhysicalAndHealthInventory']['continuousPhysicalFields']for p in(full,finite))
 need(fields==7596 and len(reviewed)==5,'Exact completed P2 scope')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,parentJournal=str(parentpath),remaining=parent['remaining'],previousGoalTurnClassification='progress: completed held P1 challenger source/physical/gameplay and fault checks',thisGoalTurnClassification='progress: new actual P2 challenger runs, both joined gameplay contracts and Sonya whole source waveform; Kano CPU-audio carry-in explicitly unverified',completedJoinedGameplayCases=['ball_p1','square_p1','ball_p2','square_p2'],completedWholeAudioCases=['ball_p1','square_p1','square_p2'],completeKanoP2MixedAudioAccepted=False,initialKanoP2CPUCarryInCapturedBeforeLaunch=False,continuousPhysicalFields=fields,sourceExactSonyaStereoFrames=full['completeSourceWaveform']['comparedStereoFrames'],semanticFaultsRejected=20,actualViewedNativeFrames=len(reviewed),actualNativePIDs=[87336,162936],allRAMHostsReleased=True,fullRasterAcceptance=False,nextAction='Capture live morph startup/return ownership. For Kano P2 mixed audio, widen the passive observer before the initial CPU cue; keep this original run and do not infer missing clocks from PCM. Then complete changed-source integration and matching launcher/release.',rootStatusDocumentsUnchanged=True,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,retainedCompiledCandidates=16,selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,inputHashes=pins,exactCompressedTargets=selected)
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(report,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Lossless exact checkpoint')
 print(json.dumps({k:report[k]for k in('passed','continuousPhysicalFields','sourceExactSonyaStereoFrames','semanticFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds')}),flush=True)

if __name__=='__main__':main()
