"""Finite same-run interruption progress, unexercised attempts and storage.

Preserve all prior captured reports and the full remaining port objective.
Only lossless exact-target compression; no build, deletion or raw transport.
"""
import gzip,json,re,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as process
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6702_launch_interruption_progress_storage_checked'


def main():
 need(not OUT.exists()and not process.census(),'Fresh journal, actual native jobs terminal')
 current.expected();pins={};migrations=[]
 parent_path=ROOT/'audit_v6676_kano_cpu_launch_progress_storage_checked/report.json'
 parent=json.loads(parent_path.read_text());need(parent['passed']and len(parent['remaining'])==6,'Full prior objective retained')
 history=ROOT/'status_history_v6700'
 for p,h in parent['inputHashes'].items():
  path=Path(p).resolve()
  if path.parent==ROOT and path.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
   old=history/path.name;need(sha(old)==h,'Exact previously pinned documentation preserved')
   migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)));path=old
  need(sha(path)==h,'Protected prior source/evidence intact: '+str(path));pins[str(path)]=h
 pins[str(parent_path)]=sha(parent_path)
 proof_paths=[ROOT/'audit_v6692_launch_interruption_checked_square_p1_delay1/report.json',
              ROOT/'audit_v6697_launch_jump_interruption_checked_square_p2_delay1/report.json']
 proofs=[json.loads(p.read_text())for p in proof_paths]
 need(all(p['passed']and not p['fullPortAcceptance']and p['nativeTerminal']['nativeExit']==0 and
          not p['nativeTerminal']['hostDecodeErrors']and p['completeSourceWaveform']['passed']and
          p['completeSourceWaveform']['differentChannelSamples']==0 for p in proofs),'Both complete same-terminal finite proofs')
 need(sum(p['completeSourceWaveform']['comparedStereoFrames']for p in proofs)==1053120 and
      sum(len(p['actualSemanticFaultsRejected'])for p in proofs)==36 and
      all(len(p['physicalAndOwnership']['actualInterruptedCycles'])==2 for p in proofs),'Four genuine contacts/recoveries, full output and actual fault totals')
 for path,proof in zip(proof_paths,proofs,strict=True):
  pins[str(path)]=sha(path)
  for p,h in proof['inputHashes'].items():need(sha(p)==h,'Executed qualifier/candidate/capture/source intact');pins[p]=h
 def version(p):
  match=re.search(r'_v(\d+)',p.name);return int(match[1])if match else -1
 leaves=[p for p in ROOT.iterdir()if p.is_dir()and 6680<=version(p)<=6700 and p.name.startswith(('audit_','status_history_'))]
 attempts=[]
 for folder in leaves:
  terminal_path=folder/'native_terminal.json'
  if not terminal_path.is_file():continue
  terminal=json.loads(terminal_path.read_text());capture=json.loads((folder/'report.json').read_text())
  need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors']and capture['passed']and capture['transportOnlyAccepted']and
       not capture['gameplayInterruptionAccepted'],'Actual transport-only reports stay unchanged, not retroactively made semantic passes')
  with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as reader:text=reader.read()
  rows=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_INTERRUPT_HEALTH ')]
  incoming=[r for r in rows if int(r['slot'])==capture['side']and int(r['after'])<int(r['before'])]
  accepted=next((str(p)for p,q in zip(proof_paths,proofs,strict=True)if q['nativeTerminal']==terminal),None)
  need((len(incoming)==2)if accepted else not incoming,'Actual incoming contacts distinguish qualified runs from all physical misses')
  attempts.append(dict(folder=str(folder),nativePID=terminal['pid'],nativeExit=0,move=capture['move'],physicalSlot=capture['side'],
                       incomingHealthStores=incoming,interruptionAccepted=bool(accepted),qualification=accepted,
                       classification='qualified genuine interruption'if accepted else'unexercised: no actual incoming contact'))
 need(len(attempts)==11 and sum(bool(a['interruptionAccepted'])for a in attempts)==2,'All eleven actual attempts, exactly two qualified contexts')
 docs=(ROOT/'CURRENT_PLAYTEST_STATUS.md').read_text()
 need('1,053,120'in docs and all(p.parent.name in docs for p in proof_paths),'Current status reflects complete bounded evidence')
 files=[p for leaf in leaves for p in leaf.rglob('*')if p.is_file()]
 files.extend(p for base in(ROOT,ROOT/'tools')for p in base.iterdir()if p.is_file()and 6680<=version(p)<=6701)
 files.extend(ROOT/name for name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(len(files)==len(set(files))and all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files),'Unique exact resolved finite targets')
 need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'No new binary/ROM/media/release allocations')
 storage=[];seen=set();total=0
 for p in sorted(files):
  h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact-target compression')
  after=allocated(p);unique=key not in seen;seen.add(key)
  if unique:total+=after
  storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique))
  pins[str(p)]=h
 builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not process.census(),'Sixteen retained compiled folders, no compiler cache or native job')
 need(all(sha(p)==h for p,h in pins.items()),'All protected logical bytes remain intact')
 report=dict(passed=True,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],candidate=current.NAME,
             finiteInterruptionProofs=[str(p)for p in proof_paths],genuineInterruptedCycles=4,sourceExactStereoFrames=1053120,
             actualSemanticFaultsRejected=36,actualNativeAttempts=attempts,unexercisedAttempts=9,
             fullInterruptionCoverageAccepted=False,fullRasterAcceptance=False,publicPlayableChanged=False,
             previousGoalTurnClassification='no progress: acknowledgement only; retained live RAM handle revalidated before qualification',
             thisGoalTurnClassification='progress: four real both-slot Square contacts, complete recovery/ownership and complete source-output accepted; distinct stock jump inputs resolve P2 misses',
             intentionalDocumentationPinMigrations=migrations,inputHashes=pins,exactCompressedTargets=storage,
             selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,retainedCompiledCandidates=len(builds),compilerCacheAbsent=True,
             newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,deletedOldArtifacts=0)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless finite journal')
 print(json.dumps({k:report[k]for k in('passed','genuineInterruptedCycles','sourceExactStereoFrames','unexercisedAttempts','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds')}),flush=True)

if __name__=='__main__':main()
