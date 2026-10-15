"""Exact bounded Bicycle KO/reset evidence, original failures and prior pins."""
import json,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_bicycle_launch_ko_round_progress_storage'

def main():
 need(not OUT.exists()and not native.census(),'Fresh journal; native jobs terminal')
 current.expected();parent_path=ROOT/'audit_sonya_launch_ko_round_progress_storage/report.json';parent=json.loads(parent_path.read_text())
 need(parent['passed']and len(parent['remaining'])==6,'Whole original release/integration scope retained')
 pins={str(parent_path):sha(parent_path)};migrations=[]
 for p,h in parent['inputHashes'].items():
  path=Path(p).resolve()
  if path.parent==ROOT and path.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
   old=ROOT/'status_history_bicycle_launch_ko_round'/path.name;need(sha(old)==h,'Exact preceding document history')
   migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)));path=old
  need(sha(path)==h,'Inherited pin stable: '+str(path));pins[str(path)]=h
 paths=[];full=[];semantic_faults=0;projectile_faults=0
 for side,pid in((1,156136),(2,111536)):
  path=ROOT/f'audit_bicycle_launch_ko_round_checked_p{side}/report.json';p=json.loads(path.read_text());paths.append(path);full.append(p)
  need(p['passed']and p['candidate']==current.NAME and not p['fullPortAcceptance']and p['nativeTerminal']['pid']==pid and p['nativeTerminal']['nativeExit']==0 and not p['nativeTerminal']['hostDecodeErrors'],'Actual current complete normal terminal, not whole-port acceptance')
  need(p['physicalKOResetRearm']['nativeModeSequence']==['2','5','6','7','2']and p['physicalKOResetRearm']['actualPostResetWalkJumpPunchAccepted']and p['completeSourceWaveform']['differentChannelSamples']==0 and len(p['completeSourceWaveform']['sourceEvents'])==18 and len(p['completeNativeProjectileBranches']['actualStockProjectileContacts'])==9,'Whole physical/native projectile/source lifecycle through reset')
  for name,key,count in(('audit_bicycle_ko_round_faults','semantic',22),('audit_bicycle_ko_projectile_faults','projectile',7)):
   path=ROOT/f'{name}_p{side}/report.json';fault=json.loads(path.read_text());paths.append(path)
   need(fault['passed']and fault['nativeTerminal']['pid']==pid and len(fault['actualFaultsRejected'])==count,'All actual same-run counterexamples reject')
   if key=='semantic':semantic_faults+=count
   else:projectile_faults+=count
 first=ROOT/'audit_bicycle_launch_ko_round_bicycle_p1_delay1/report.json';failed=json.loads(first.read_text());paths.append(first)
 need(not failed['passed']and failed['nativeTerminal']['pid']==169780 and failed['nativeTerminal']['nativeExit']==3,'Original pre-game adapter failure retained')
 need('attempt to index a nil value'in(first.parent/'stderr.log').read_text(),'Actual failed nested adapter runtime')
 for name in('audit_bicycle_ko_original_context_failure','audit_bicycle_ko_high_only_descriptor_rejection','audit_bicycle_ko_fault_binding_rejection'):
  path=ROOT/name/'failure.json';failure=json.loads(path.read_text());paths.append(path)
  need(not failure['passed']and not failure['nativeGameFailure']and failure['nativeTerminal']['pid']==156136,'Actual rejected checker sources remain false')
 for path in paths:
  p=json.loads(path.read_text());pins[str(path)]=sha(path)
  for source,h in p['inputHashes'].items():need(sha(source)==h,'Whole executed source/evidence pin unchanged');pins[source]=h
 fields=sum(p['physicalKOResetRearm']['continuousPhysicalFields']for p in full)
 owners=sum(p['completeIndependentOwnership']['completeOwnerFields']for p in full)
 channels=sum(p['completeIndependentOwnership']['completeBattleChannelFields']for p in full)
 frames=sum(p['completeSourceWaveform']['comparedStereoFrames']for p in full)
 branches=sum(p['completeNativeProjectileBranches']['completeHitMissBranches']for p in full)
 audio_faults=sum(len(p['completeSourceWaveform']['actualRawAndSourceFaultsRejected'])+len(p['sourceDAC']['faults'])+len(p['wholeSoundROM']['faults'])for p in full)
 need(fields==owners==8350 and channels==16700 and frames==3661440 and branches==115 and semantic_faults+projectile_faults==58 and audio_faults==40,'Entire actual both-slot scope')
 leaves=[ROOT/f'audit_bicycle_launch_ko_round_v2_bicycle_p{side}_delay1'for side in(1,2)]+[p.parent for p in paths]+[ROOT/'status_history_bicycle_launch_ko_round']
 files={p for leaf in leaves for p in leaf.rglob('*')if p.is_file()}
 files.update(ROOT/p for p in('mk2ks_bicycle_launch_ko_round.lua','mk2ks_bicycle_launch_ko_round_v2.lua','tools/capture_bicycle_launch_ko_round.py','tools/capture_bicycle_launch_ko_round_v2.py','tools/qualify_bicycle_launch_ko_round.py','tools/qualify_bicycle_launch_ko_round_v2.py','tools/qualify_bicycle_launch_ko_round_v3.py','tools/check_bicycle_ko_round_faults.py','tools/check_bicycle_ko_round_faults_v2.py','tools/journal_bicycle_launch_ko_round.py','CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Exact finite source/gzip/digest/proof only')
 total=0;seen=set();storage=[]
 for p in sorted(files):
  h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact lossless bounded compression')
  after=allocated(p);unique=key not in seen;seen.add(key)
  if unique:total+=after
  pins[str(p)]=h;storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique))
 builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census()and all(sha(p)==h for p,h in pins.items()),'All sources/public launcher stable; no new build/cache/live native job')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],
  previousGoalTurnClassification=parent['previousGoalTurnClassification'],
  thisGoalTurnClassification='progress: completed held Square fault checks and both-slot native Bicycle KO/reset/rearm/state/body/projectile/source-audio qualification; no playable changes',
  nextAction='Audit the remaining concrete current selection/morph and changed-source integration gaps against existing accepted campaign/arena/finisher evidence, then complete combined acceptance and matching launcher/release ZIP; do not rerun already accepted contexts merely to relabel them.',
  actualNativePIDs=[169780,156136,111536],rejectedPreGameAdapterPID=169780,continuousPhysicalFields=fields,completeOwnerFields=owners,completeBattleChannelFields=channels,
  comparedStereoFrames=frames,differentChannelSamples=0,actualNativeProjectileBranches=branches,actualSemanticAndProjectileFaultsRejected=58,actualWaveformDACROMFaultsRejected=audio_faults,
  finiteProofs=[str(p)for p in paths],fullRasterAcceptance=False,allKOResetMorphCoverageAccepted=False,allRAMHostsReleased=True,publicPlayableChanged=False,
  inputHashes=pins,intentionalDocumentationPinMigrations=migrations,exactCompressedTargets=storage,selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,
  retainedCompiledCandidates=16,compilerCacheAbsent=True,newNativeBootsThisContinuation=3,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,newRasterFiles=0,deletedOldArtifacts=0)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact journal')
 print(json.dumps({k:report[k]for k in('passed','continuousPhysicalFields','comparedStereoFrames','actualSemanticAndProjectileFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','publicPlayableChanged')}),flush=True)

if __name__=='__main__':main()
