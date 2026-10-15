"""Add current earned Mileena consumer evidence to the unchanged full port goal."""
import json,subprocess
from datetime import datetime,timezone
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v6080_current_carried_victims_progress/progress.json'
PROOF=ROOT/'audit_v6103_current_mileena_lifecycle_checked/report.json'
OUT=ROOT/'audit_v6105_current_mileena_lifecycle_progress'

def run():
 parent=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,
      'Full original objective and every remaining group retained')
 need(proof['passed']and proof['actualContexts']==4 and proof['earnedRoundKOs']==8 and
      proof['ownSwallowingPoses']==30 and proof['nativeRefillStores']==324 and
      proof['pairedPhysicalFields']==19624 and proof['actualSemanticFaultsRejected']==92 and
      proof['retainedNativeTeardownFields']==8 and proof['completeCurrentEarnedSwallowingStateAndRetirementAccepted']and
      not proof['fullArtAcceptance']and not proof['fullAudioAcceptance']and not proof['fullPortAcceptance']and
      all(sha(p)==h for p,h in proof['inputHashes'].items()),'Whole current four-context state/health/physical lifecycle matrix')
 current.expected()
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C',
      'Current delivered ZIP unchanged and still bound to tested current executable/payload')
 # The four actual terminal identities are stored before state assertions.
 # Do not compact any live emulator trace or enumerate unrelated build trees.
 exe=ROOT/current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual current native emulator census empty before terminal-only compression')
 targets=[]
 for c in proof['cases']:
  folder=Path(c['capture']).resolve()
  need(folder.parent==ROOT.resolve()and c['actualTerminal']['nativeExit']==0,'Exact terminal capture folder lies within named workspace')
  for name in ('run.log','stderr.log','native_terminal.json','process.json','memory_proofs.json','scene_proofs.json','input_hashes_before.json'):
   p=folder/name
   if p.exists():need(str(p.resolve())in proof['inputHashes'],'Only already hash-bound terminal log/metadata');targets.append(p)
 compact=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(compact.returncode==0 and all(sha(p)==h for p,h in proof['inputHashes'].items()),
      'Lossless exact-file LZX compression preserves every executed source/trace/image hash')
 audit=parent['requirementAudit'];item=next(r for r in audit if r['requirement'].startswith('Natural finishers'))
 item['status']+=' Current earned Mileena swallowing now has four true character/physical-slot contexts, eight collision-earned KOs,30owned poses,19624paired lifecycle fields,324source-native refill stores and exact disappearance/task retirement. All eight native NULL-actor inter-round teardown observations retained;92actual semantic corruption controls rejected. Sonya P2 has all eight actual lookup-triggered bounded native phase screenshots visually inspected at beginning/middle/end and post-match. No full-scene artwork/audio acceptance is claimed; other finisher/cinematic consumers remain open.'
 item['evidence'].append(dict(path=str(PROOF),sha256=sha(PROOF)))
 return dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],requirementAudit=audit,
      newInputHashes={str(PARENT):sha(PARENT),str(PROOF):sha(PROOF),str(archive):sha(archive),str(Path(__file__).resolve()):sha(__file__)},
      previousGoalTurnClassification='no progress: gratitude acknowledgement; pending native process revalidated and consumed this turn',
      thisTurnClassification='progress: pending genuine current native finisher terminal verified and complete four-context source/physical lifecycle matrix qualified',
      actualCurrentMileenaContexts=4,ownSwallowingPoses=30,pairedPhysicalFields=19624,newActualSemanticFaultsRejected=92,
      terminalOnlyFilesLosslesslyCompressed=len(targets),compressionOutput=compact.stdout,
      filesDeleted=0,nativeGameChanges=0,newNativeBootsStarted=0,newBuildCopies=0,rawMediaFilesWritten=0,
      currentReleaseZIPUnchanged=True,fullGoalComplete=False,
      nextActions=['Exercise current Kitana/KungLao/Jax/Subzero native finisher victim consumers',
                   'Complete broader arena/CPU/KO/overlap move art, shadows and audio coverage',
                   'Run final combined selection-to-gameplay and matching release audit'])

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive current finisher checkpoint')
 report=run();OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','requirementAudit','compressionOutput')},indent=2))
