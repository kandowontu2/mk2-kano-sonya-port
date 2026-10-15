"""Bounded native morph progress, original rejections and exact doc history."""
import json,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def main():
 out=ROOT/'audit_morph_startup_return_progress_storage';need(not out.exists()and not native.census(),'Fresh journal; every native run terminal')
 parentpath=ROOT/'audit_launch_challenger_transition_p2_progress_storage/report.json';parent=json.loads(parentpath.read_text());need(parent['passed']and len(parent['remaining'])==6,'Full original integration/release scope retained')
 pins={str(parentpath):sha(parentpath)};migrations=[]
 for p,h in parent['inputHashes'].items():
  path=Path(p).resolve()
  if path.parent==ROOT and path.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
   old=ROOT/'status_history_morph_startup_return'/path.name;need(sha(old)==h,'Exact previous current document bytes retained')
   migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)));path=old
  need(sha(path)==h,'Every retained original source/evidence pin stable');pins[str(path)]=h
 reports=[];full=[];fields=channels=frames=semantic=audio_faults=views=0
 for move,side,pid in(('ball',1,94140),('square',1,159400),('ball',2,163964),('square',2,96580)):
  path=ROOT/f'audit_morph_startup_return_checked_{move}_p{side}/report.json';p=json.loads(path.read_text());reports.append(path);full.append(p)
  need(p['passed']and p['candidate']==current.NAME and p['nativeTerminal']['pid']==pid and p['nativeTerminal']['nativeExit']==0 and not p['fullPortAcceptance'],'Actual finite same-terminal morph qualification')
  need(p['completePhysicalAndHealthInventory']['nativeRosterRemainsShang']and p['completePhysicalAndHealthInventory']['actualOrdinaryControlsAfterReturnAccepted']and p['completeSourceWaveform']['differentChannelSamples']==0,'Genuine form/return identities, controls and source-exact entire mixed audio')
  fields+=p['completePhysicalAndHealthInventory']['continuousPhysicalFields'];channels+=p['completeIndependentOwnership']['completeBattleChannelFields'];frames+=p['completeSourceWaveform']['comparedStereoFrames']
  audio_faults+=len(p['completeSourceWaveform']['actualWaveformFaultsRejected'])+len(p['sourceDAC']['faults'])+len(p['wholeSoundROM']['faults'])
  path=ROOT/f'audit_morph_startup_return_faults_{move}_p{side}/report.json';f=json.loads(path.read_text());reports.append(path);need(f['passed']and len(f['actualFaultsRejected'])==18,'All actual semantic/input/source counterexamples rejected');semantic+=18
  path=ROOT/f'audit_morph_startup_return_visual_{move}_p{side}/report.json';v=json.loads(path.read_text());reports.append(path);need(v['passed']and len(v['viewedFrameHeaders'])==3 and not v['fullRasterAcceptance'],'Finite original viewed frames, no broad pixel acceptance');views+=3
  for name in('audit_morph_startup_return_idle_deadline_rejection','audit_morph_startup_return_input_assumption_rejection'):
   path=ROOT/f'{name}_{move}_p{side}/failure.json'
   if side==1 or move=='ball':
    failure=json.loads(path.read_text());need(not failure['passed']and not failure['nativeGameFailure']and failure['nativeTerminal']['pid']==pid,'Actually executed original idle/fixed-facing/frame-latency checker rejection retained');reports.append(path)
 for path in reports:
  p=json.loads(path.read_text());pins[str(path)]=sha(path)
  for source,h in p.get('inputHashes',{}).items():need(sha(source)==h,'Whole executed sources and actual proof inputs stable');pins[source]=h
 need(fields==19208 and channels==38416 and frames==8424960 and semantic==72 and audio_faults==68 and views==12,'Complete actual four-case scope')
 leaves=[p.parent for p in reports]+[ROOT/f'audit_morph_startup_return_{move}_p{side}_delay1'for move in('ball','square')for side in(1,2)]+[ROOT/'status_history_morph_startup_return']
 files={p for leaf in leaves for p in leaf.rglob('*')if p.is_file()}
 files.update(ROOT/name for name in('mk2ks_morph_startup_return.lua','tools/capture_morph_startup_return.py','tools/qualify_morph_startup_return.py','tools/qualify_morph_startup_return_v2.py','tools/qualify_morph_startup_return_v3.py','tools/check_morph_startup_return_faults.py','tools/record_morph_startup_return_review.py','tools/journal_morph_startup_return.py','CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Exact bounded source/gzip/digest/proof/history targets; no raw media')
 total=0;seen=set();storage=[]
 for p in sorted(files):
  h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact compressed bytes')
  after=allocated(p)
  if key not in seen:total+=after;seen.add(key)
  pins[str(p)]=h;storage.append(dict(path=str(p),sha256=h,beforeAllocatedBytes=before,allocatedBytes=after))
 current.expected();builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census()and all(sha(p)==h for p,h in pins.items()),'All sources/candidate/public launcher stable, no new build/cache/live native job')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],previousGoalTurnClassification='progress: both P2 challenger gameplay contracts, Sonya exact mixed audio and explicit Kano CPU carry-in limitation',thisGoalTurnClassification='progress: four native Shang-form late-special/return runs, complete true-ID/floor/health/input/source checks and twelve actual visual frames; no playable changes',actualNativePIDs=[94140,159400,163964,96580],continuousPhysicalFields=fields,completeBattleChannelFields=channels,comparedStereoFrames=frames,differentChannelSamples=0,semanticFaultsRejected=semantic,waveformDACROMFaultsRejected=audio_faults,actualViewedNativeFrames=views,completedMorphStartupContexts=['ball_p1','square_p1','ball_p2','square_p2'],allMorphContextsAccepted=False,fullRasterAcceptance=False,completeKanoP2ChallengerMixedAudioAccepted=False,nextAction='Close the challenger CPU carry-in audio observer gap with a window beginning before the CPU cue; audit unchanged-source conservation against the full original UI/campaign/arena/finisher/secret/continue evidence before final combined acceptance and matching launcher/release ZIP.',allRAMHostsReleased=True,publicPlayableChanged=False,newNativeBoots=4,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,retainedCompiledCandidates=16,selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,inputHashes=pins,intentionalDocumentationPinMigrations=migrations,exactCompressedTargets=storage)
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(report,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Lossless actual checkpoint')
 print(json.dumps({k:report[k]for k in('passed','continuousPhysicalFields','comparedStereoFrames','semanticFaultsRejected','waveformDACROMFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds')}),flush=True)

if __name__=='__main__':main()
