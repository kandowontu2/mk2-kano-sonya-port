"""Whole-goal carry-forward, two actual terminal mirrors, bounded storage."""
import json,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_dual_roll_progress_storage'

def main():
 need(not OUT.exists()and not native.census(),'Fresh journal; actual native jobs terminal')
 current.expected();parent_path=ROOT/'audit_native_projectile_interruption_progress_storage/report.json'
 parent=json.loads(parent_path.read_text());need(parent['passed']and len(parent['remaining'])==6,'Complete original integration goal unchanged')
 pins={};migrations=[]
 for p,h in parent['inputHashes'].items():
  path=Path(p).resolve()
  if path.parent==ROOT and path.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
   old=ROOT/'status_history_native_dual_roll'/path.name;need(sha(old)==h,'Exact preceding document bytes retained')
   migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)));path=old
  need(sha(path)==h,'Whole protected previous source/evidence pin unchanged: '+str(path));pins[str(path)]=h
 pins[str(parent_path)]=sha(parent_path)
 proof_paths=[ROOT/f'audit_launch_dual_roll_checked_p{s}/report.json'for s in(1,2)]
 fault_paths=[ROOT/f'audit_launch_dual_roll_faults_p{s}/report.json'for s in(1,2)]
 proofs=[json.loads(p.read_text())for p in proof_paths];faults=[json.loads(p.read_text())for p in fault_paths]
 for path,proof in zip(proof_paths+fault_paths,proofs+faults,strict=True):
  need(proof['passed']and proof['nativeTerminal']['nativeExit']==0 and not proof['nativeTerminal']['hostDecodeErrors']and not proof['fullPortAcceptance'],'Actual finite clean terminal evidence')
  pins[str(path)]=sha(path)
  for p,h in proof['inputHashes'].items():need(sha(p)==h,'Actually executed finite source/evidence intact');pins[p]=h
 need({p['nativeTerminal']['pid']for p in proofs}=={173196,60688},'The two actual native jobs, never a replay')
 need(all(p['wholePhysicalAndBodyContract']['twoRealSpecialCyclesAndCleanupVerified']and
          p['completeIndependentOwnership']['independentHitAndEOFRetirement']and
          p['physicalInputDelivery']['wholeBothPlayerPhysicalBitDeliveryAccepted']and
          p['completeSourceWaveform']['comparedStereoFrames']==639360 and
          p['completeSourceWaveform']['differentChannelSamples']==0 and len(p['sourceEvents'])==4 for p in proofs),'Full dual source lifetimes, button delivery, body/FIFO/recovery and complete output')
 need(all(len(p['actualSemanticFaultsRejected'])==28 and p['originalPositiveRestored']for p in faults),'All actual owner/cancellation/body/FIFO/input faults and restored full positives')
 captures=[ROOT/f'audit_launch_dual_roll_ball_p{s}_delay1'for s in(1,2)]
 leaves=captures+[p.parent for p in proof_paths+fault_paths]+[ROOT/'status_history_native_dual_roll']
 files={p for leaf in leaves for p in leaf.rglob('*')if p.is_file()}
 files.update(ROOT/p for p in('mk2ks_launch_dual_roll.lua','tools/capture_launch_dual_roll.py','tools/qualify_launch_dual_roll.py','tools/check_launch_dual_roll_faults.py','tools/journal_native_dual_roll.py','CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and
      not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Exact finite source/evidence compression only, no raw media or builds')
 storage=[];seen=set();total=0
 for p in sorted(files):
  h=sha(p);stat=p.stat();before=allocated(p);key=stat.st_dev,stat.st_ino
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact target compression')
  after=allocated(p);unique=key not in seen;seen.add(key)
  if unique:total+=after
  storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique));pins[str(p)]=h
 builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census(),'No extra build, compiler cache or live native job')
 need(all(sha(p)==h for p,h in pins.items()),'All inherited/actual source and evidence bytes intact')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],
             previousGoalTurnClassification='progress: eight genuine roll/Bicycle projectile interruptions and exact full source audio',
             thisGoalTurnClassification='progress: two actual selected-Kano mirror runs, eight simultaneous roll starts, four independent hit stops/four full opponent tails, complete body recovery and source waveform, actual cross-slot faults',
             nextAction='Check remaining launch overlap/relaunch/KO/selection/reset/morph and current full UI/ground/render/audio before public promotion; preserve complete other integration and finished-release scope.',
             finiteProofs=[str(p)for p in proof_paths+fault_paths],actualNativePIDs=[p['nativeTerminal']['pid']for p in proofs],
             completeStereoFrames=1278720,actualSemanticFaultsRejected=56,allRAMHostsReleased=True,publicPlayableChanged=False,
             inputHashes=pins,intentionalDocumentationPinMigrations=migrations,exactCompressedTargets=storage,selectedFileCount=len(files),
             uniqueSelectedAllocatedBytes=total,retainedCompiledCandidates=16,compilerCacheAbsent=True,newNativeBootsThisGoalTurn=2,
             newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,deletedOldArtifacts=0)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless finite journal')
 print(json.dumps({k:report[k]for k in('passed','completeStereoFrames','actualSemanticFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds','publicPlayableChanged')}),flush=True)

if __name__=='__main__':main()
