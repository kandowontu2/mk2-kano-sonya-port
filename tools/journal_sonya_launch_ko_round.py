"""Bounded current Sonya KO evidence and storage, with exact prior pins."""
import json, subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT, need, sha = current.ROOT, current.need, current.sha
OUT = ROOT/'audit_sonya_launch_ko_round_progress_storage'

def main():
 need(not OUT.exists() and not native.census(), 'Fresh journal; native jobs terminal')
 current.expected()
 parent_path=ROOT/'audit_launch_ko_round_progress_storage/report.json'
 parent=json.loads(parent_path.read_text())
 need(parent['passed'] and len(parent['remaining'])==6, 'Full original remaining scope')
 pins={str(parent_path):sha(parent_path)}; migrations=[]
 for p,h in parent['inputHashes'].items():
  path=Path(p).resolve()
  if path.parent==ROOT and path.name in ('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
   old=ROOT/'status_history_sonya_launch_ko_round'/path.name
   need(sha(old)==h, 'Exact preceding document history')
   migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)))
   path=old
  need(sha(path)==h, 'Inherited pin unchanged: '+str(path)); pins[str(path)]=h
 paths=[]; proofs=[]; rejections=[]
 for side,pid in ((1,148212),(2,172856)):
  path=ROOT/f'audit_sonya_launch_ko_round_checked_p{side}/report.json'
  proof=json.loads(path.read_text()); paths.append(path); proofs.append(proof)
  need(proof['passed'] and proof['candidate']==current.NAME and not proof['fullPortAcceptance'], 'Actual finite current proof')
  terminal=proof['nativeTerminal']
  need(terminal['pid']==pid and terminal['nativeExit']==0 and not terminal['hostDecodeErrors'], 'Actual full terminal identity')
  state=proof['physicalKOResetRearm']
  need(state['nativeModeSequence']==['2','5','6','7','2'] and state['actualPostResetWalkJumpPunchAccepted'], 'Native KO/reset/rearm/ordinary recovery')
  need(len(proof['sourceEvents'])==(6 if side==1 else 8) and proof['completeSourceWaveform']['differentChannelSamples']==0, 'Whole current owned starts and PCM equality')
  path=ROOT/f'audit_sonya_ko_round_faults_p{side}/report.json'
  fault=json.loads(path.read_text()); paths.append(path); proofs.append(fault)
  need(fault['passed'] and len(fault['actualFaultsRejected'])==22 and fault['nativeTerminal']['pid']==pid, 'All actual same-run state/input/body/source faults')
  path=ROOT/f'audit_sonya_ko_missing_observer_p{side}/failure.json'
  rejected=json.loads(path.read_text()); paths.append(path); rejections.append(rejected)
  need(not rejected['passed'] and not rejected['nativeGameFailure'] and rejected['actualBoundaryFields']==0 and rejected['nativeTerminal']['nativeExit']==0,
       'Original observer deficiency remains rejected, not accepted game coverage')
 path=ROOT/'audit_sonya_ko_predictor_source_retrieval_failure/failure.json'
 rejected=json.loads(path.read_text()); paths.append(path); rejections.append(rejected)
 need(not rejected['passed'] and not rejected['nativeGameFailure'], 'Original predictor lookup failure preserved')
 for path in paths:
  proof=json.loads(path.read_text()); pins[str(path)]=sha(path)
  for p,h in proof['inputHashes'].items():
   need(sha(p)==h, 'Whole actual executed source/evidence unchanged: '+p); pins[p]=h
 full=[p for p in proofs if 'physicalKOResetRearm' in p]
 fields=sum(p['physicalKOResetRearm']['continuousPhysicalFields'] for p in full)
 owners=sum(p['completeIndependentOwnership']['completeOwnerFields'] for p in full)
 channels=sum(p['completeIndependentOwnership']['completeBattleChannelFields'] for p in full)
 frames=sum(p['completeSourceWaveform']['comparedStereoFrames'] for p in full)
 audio_faults=sum(len(p['completeSourceWaveform']['actualRawAndSourceFaultsRejected'])+len(p['sourceDAC']['faults'])+len(p['wholeSoundROM']['faults']) for p in full)
 need(fields==owners==7774 and channels==15548 and frames==3408960 and audio_faults==40, 'Entire finite both-slot proof scope')
 leaves=[ROOT/f'audit_sonya_launch_ko_round_{suffix}_square_p{side}_delay1' for suffix in ('full',) for side in (1,2)]
 leaves += [ROOT/f'audit_sonya_launch_ko_round_square_p{side}_delay1' for side in (1,2)]
 leaves += [p.parent for p in paths]+[ROOT/'status_history_sonya_launch_ko_round']
 files={p for leaf in leaves for p in leaf.rglob('*') if p.is_file()}
 files.update(ROOT/p for p in ('mk2ks_sonya_launch_ko_round.lua','mk2ks_sonya_launch_ko_round_full.lua',
   'tools/capture_sonya_launch_ko_round.py','tools/capture_sonya_launch_ko_round_full.py',
   'tools/qualify_sonya_launch_ko_round.py','tools/qualify_sonya_launch_ko_round_v2.py',
   'tools/preserve_sonya_ko_observer_rejection.py','tools/check_sonya_ko_round_faults.py',
   'tools/journal_sonya_launch_ko_round.py','CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(all(p.resolve().is_relative_to(ROOT) and not p.is_symlink() for p in files) and
      not any(p.suffix.lower() in ('.png','.wav','.bin','.exe','.zip') for p in files), 'Bounded source/gzip/digest/proof only')
 total=0; seen=set(); storage=[]
 for p in sorted(files):
  h=sha(p); stat=p.stat(); key=stat.st_dev,stat.st_ino; before=allocated(p)
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h, 'Exact lossless compression')
  after=allocated(p); unique=key not in seen; seen.add(key)
  if unique: total+=after
  pins[str(p)]=h; storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique))
 builds=[p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not (ROOT/'mame-mkp/build/mingw-gcc').exists() and not native.census(), 'No new builds/cache/native job')
 need(all(sha(p)==h for p,h in pins.items()), 'Every inherited/current pin stable')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],
   previousGoalTurnClassification='no progress: acknowledgement only; revalidated actual held sessions and completed outstanding same-run checks',
   thisGoalTurnClassification='progress: both-slot Sonya Square actual KO/native reset/rearm/ordinary controls; full source-exact audio;44 semantic and40 audio/DAC/ROM faults',
   nextAction='Continue Bicycle KO/reset and selection/morph source ownership, then combined current integration and matching release; preserve the whole original scope.',
   actualNativePIDs=[5628,39792,148212,172856],incompleteObserverPIDs=[5628,39792],fullyQualifiedPIDs=[148212,172856],
   continuousPhysicalFields=fields,completeOwnerFields=owners,completeBattleChannelFields=channels,comparedStereoFrames=frames,differentChannelSamples=0,
   actualSemanticFaultsRejected=44,actualWaveformDACROMFaultsRejected=audio_faults,finiteProofs=[str(p) for p in paths],
   fullRasterAcceptance=False,allKOResetMorphCoverageAccepted=False,allRAMHostsReleased=True,publicPlayableChanged=False,
   inputHashes=pins,intentionalDocumentationPinMigrations=migrations,exactCompressedTargets=storage,selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,
   retainedCompiledCandidates=16,compilerCacheAbsent=True,newNativeBootsInCheckpoint=4,newNativeBootsThisContinuation=0,
   newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,newRasterFiles=0,deletedOldArtifacts=0)
 OUT.mkdir(); path=OUT/'report.json'; path.write_text(json.dumps(report,indent=2)+'\n'); h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h, 'Exact journal compression')
 print(json.dumps({k:report[k] for k in ('passed','continuousPhysicalFields','comparedStereoFrames','actualSemanticFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','publicPlayableChanged')}),flush=True)

if __name__=='__main__': main()
