"""Exact actual KO/reset/rearm evidence; retain every original release group."""
import json,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_launch_ko_round_progress_storage'

def main():
 need(not OUT.exists()and not native.census(),'Fresh journal; actual native jobs terminal')
 current.expected();parent_path=ROOT/'audit_launch_ground_progress_storage/report.json';parent=json.loads(parent_path.read_text())
 need(parent['passed']and len(parent['remaining'])==6,'All original broader integration/release groups retained')
 pins={};migrations=[]
 for p,h in parent['inputHashes'].items():
  path=Path(p).resolve()
  if path.parent==ROOT and path.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
   old=ROOT/'status_history_launch_ko_round'/path.name;need(sha(old)==h,'Exact preceding documentation bytes preserved')
   migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)));path=old
  need(sha(path)==h,'Whole inherited source/evidence pin unchanged: '+str(path));pins[str(path)]=h
 pins[str(parent_path)]=sha(parent_path)
 paths=[ROOT/name/'report.json'for name in('audit_launch_ko_round_checked_p1','audit_launch_ko_round_v2_checked_p2','audit_launch_ko_round_faults')]
 proofs=[json.loads(p.read_text())for p in paths];first,second,faults=proofs
 need(all(p['passed']and not p['fullPortAcceptance']for p in proofs)and first['candidate']==second['candidate']==current.NAME,'Actual current finite KO/reset proofs, not release acceptance')
 need(first['nativeTerminal']['pid']==165080 and second['nativeTerminal']['pid']==151240 and
      all(p['nativeTerminal']['nativeExit']==0 and not p['nativeTerminal']['hostDecodeErrors']for p in(first,second)),'Exact two naturally terminal native jobs')
 physical_fields=sum(p['physicalKOResetRearm']['continuousPhysicalFields']for p in(first,second));need(physical_fields==7476,'All actual both-slot physical fields through KO/reset/rearm/followup')
 need(all(p['physicalKOResetRearm']['nativeModeSequence']==['2','5','6','7','2']and p['physicalKOResetRearm']['actualCollisionDamageWrites']==9 and
          p['physicalKOResetRearm']['actualPostResetWalkJumpPunchAccepted']for p in(first,second)), 'Whole original native boundary grammar and actual ordinary control recovery')
 need(not first['completeAudioAccepted']and first['firstHostPCMReleasedBeforeQualification']and second['completeAudioAccepted']and
      second['completeSourceWaveform']['comparedStereoFrames']==1650240 and second['completeSourceWaveform']['differentChannelSamples']==0,'Entire second native audio accepted; missing first PCM never inferred or replayed')
 need(faults['actualFaultsRejected']==44 and len(faults['cases'])==2 and not faults['firstHostFullPCMComparisonAccepted'],'All actual physical/input/body/source-state counterexamples reject without inventing first PCM')
 owners=sum(c['completeIndependentOwnership']['completeOwnerFields']for c in faults['cases']);channels=sum(c['completeIndependentOwnership']['completeBattleChannelFields']for c in faults['cases'])
 need(owners==7476 and channels==14952 and all(len(c['sourceEvents'])==10 for c in faults['cases']),'Whole independent actual native source ownership and channel lifetimes, including rearm')
 rejection_path=ROOT/'audit_launch_ko_round_p2_eof_model_rejection/failure.json';rejection=json.loads(rejection_path.read_text())
 need(not rejection['passed']and not rejection['actualNativeGameFailure']and rejection['originalModelUnchanged'],'Native noncombat cleanup preserved as rejected EOF-only test assumption')
 pins[str(rejection_path)]=sha(rejection_path)
 for p,h in rejection['inputHashes'].items():need(sha(p)==h,'Rejected original model source preserved');pins[p]=h
 for path,proof in zip(paths,proofs,strict=True):
  pins[str(path)]=sha(path)
  for p,h in proof['inputHashes'].items():need(sha(p)==h,'Whole actual executed evidence/source pin stable');pins[p]=h
 leaves=[ROOT/'audit_launch_ko_round_ball_p1_delay1',ROOT/'audit_launch_ko_round_ball_p2_delay1',ROOT/'status_history_launch_ko_round',rejection_path.parent]+[p.parent for p in paths]
 files={p for leaf in leaves for p in leaf.rglob('*')if p.is_file()}
 files.update(ROOT/p for p in('mk2ks_launch_ko_round.lua','tools/capture_launch_ko_round.py','tools/qualify_launch_ko_round.py',
                             'tools/qualify_launch_ko_round_v2.py','tools/check_launch_ko_round_faults.py','tools/journal_launch_ko_round.py',
                             'CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and
      not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Exact finite source/gzip/digest/proof targets only')
 total=0;seen=set();storage=[]
 for p in sorted(files):
  h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless bounded compression')
  after=allocated(p);unique=key not in seen;seen.add(key)
  if unique:total+=after
  pins[str(p)]=h;storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique))
 builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census(),'No new build/cache or live native process')
 need(all(sha(p)==h for p,h in pins.items()),'All inherited/current evidence and normal launcher stable')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],
             previousGoalTurnClassification=parent['thisGoalTurnClassification'],
             thisGoalTurnClassification='progress: two actual collision-earned Kano mirror KOs/native round resets/fresh rolls/ordinary recovery;7476 physical/owner fields;14952 battle-channel states;1650240 second-run stereo frames source-exact;44 semantic and18 PCM/DAC/ROM faults',
             nextAction='Continue Sonya startup KO/reset and selection/morph ownership contexts, then combined current full render/audio/gameplay integration; preserve every other original campaign, arena, finisher, secret and matching release requirement.',
             finiteProofs=[str(p)for p in paths],actualNativePIDs=[165080,151240],continuousPhysicalFields=physical_fields,completeOwnerFields=owners,completeBattleChannelFields=channels,
             completeSecondRunStereoFrames=1650240,firstRunPCMComparisonAccepted=False,firstNoninteractiveHostReleasedPCM=True,
             actualSemanticFaultsRejected=44,actualWaveformDACROMFaultsRejected=18,nativeRoundModeSequence=['2','5','6','7','2'],
             fullRasterAcceptance=False,allKOResetMorphCoverageAccepted=False,allRAMHostsReleased=True,publicPlayableChanged=False,
             inputHashes=pins,intentionalDocumentationPinMigrations=migrations,exactCompressedTargets=storage,selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,
             retainedCompiledCandidates=16,compilerCacheAbsent=True,newNativeBootsThisGoalTurn=2,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,newRasterFiles=0,deletedOldArtifacts=0)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact journal')
 print(json.dumps({k:report[k]for k in('passed','continuousPhysicalFields','completeSecondRunStereoFrames','actualSemanticFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds','publicPlayableChanged')}),flush=True)

if __name__=='__main__':main()
