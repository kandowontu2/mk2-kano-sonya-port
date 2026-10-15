"""Persist complete objective and accepted progress without accepting live tests early."""
import json,subprocess
from datetime import datetime,timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_shao_guard_walk_boss_ledger_v2551 as ledger
ROOT=ledger.ROOT;launch=ledger.launch;OUT=ROOT/'audit_v2564_current_guard_walk_verified_pending'

def need(ok,label):
 if not ok:raise ValueError(label)

def save():
 previous=ROOT/'audit_v2535_current_duck_wait_cleanup_checkpoint/checkpoint.json';prior=json.loads(previous.read_text())
 need(prior['goalStatus']=='active'and not prior['fullPortAcceptance']and not prior['finishedRelease'],'Full original objective unfinished')
 pins=dict(prior['inputHashes']);pins[str(previous)]=launch.sha(previous);accepted={}
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Accepted bounded evidence '+str(path))
  for file,wanted in r['inputHashes'].items():need(file not in pins or pins[file]==wanted,'Consistent immutable graph');pins[file]=wanted
  pins[str(path)]=launch.sha(path);accepted[str(path)]=True;return r
 recovery=accept(ROOT/'audit_v2548_dynamic_native_source_dependencies_recovered/report.json')
 compression=accept(ROOT/'audit_v2554_restored_native_dependencies_compressed/report.json')
 accept(ROOT/'audit_v2550_guard_walk_source_boundary_checked/report.json')
 accept(ROOT/'audit_v2539_current_uppercut_collision_timing/report.json')
 cases={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof=accept(ROOT/positive/'report.json');book=accept(ROOT/f'audit_v2556_current_{fighter}_shao_guard_walk_boss_ledger_checked/report.json')
  need(not proof['unassisted_clear_proven']and proof['ending_starts']==proof['ending_completions']==0,'No full ladder or ending acceptance substitution')
  cases[case]=dict(capture=str(ROOT/capture),wholeCampaignTrajectoryPassed=True,orderedLedgerPassed=True,
   human107Assignments=book['originalHuman107Assignments'],actualBossUppercutDamage=book['ownBossUppercutDamage'],
   fullCampaignClear=False,endingAccepted=False,remainingFullInputProof=str(ROOT/f'audit_v2557_current_{fighter}_shao_guard_walk_input_counterexamples/report.json'))
 cmd="Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'test_current_shao_guard_walk_inputs_v2552|verify_restored_native_dependency_archive_v2561' } | Select-Object ProcessId,CreationDate,UserModeTime,KernelModeTime,CommandLine | ConvertTo-Json -Depth 2"
 result=subprocess.run(['powershell.exe','-NoProfile','-Command',cmd],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
 need(result.returncode==0,'Read-only authoritative process inventory')
 processes=json.loads(result.stdout)if result.stdout.strip()else[]
 if isinstance(processes,dict):processes=[processes]
 completed={};pending=[]
 for path in [ROOT/f'audit_v2557_current_{f}_shao_guard_walk_input_counterexamples/report.json'for f in('kano','sonya')]+[ROOT/'audit_v2562_restored_native_dependency_archive_checked/report.json']:
  if path.is_file():completed[str(path)]=accept(path)['passed']
  else:pending.append(str(path))
 for path in(ROOT/'audit_v2546_guard_walk_source_boundary_failure/failure.json',ROOT/'tools/verify_guard_walk_source_boundary_v2545.py',Path(__file__).resolve(),ROOT/'tools/analyze_current_shao_guard_walk_progress_v2555.py',ROOT/'tools/save_current_guard_walk_dependency_checkpoint_v2559.py'):
  pins[str(path)]=launch.sha(path)
 launch.module_pins(pins)
 print('Revalidating full pending progress graph:',len(pins),'actual dependencies',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed authoritative dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(previous),previousGoalTurnClassification='no progress: user-requested status only',
  thisGoalTurnClassification='progress and verified live wait: only fourteen required historical files recovered and whole native ROM/payload reconstruction repaired; both new physical campaigns and ordered native ledgers accepted. Final full-input and archive cross-checks remain independently pending, never accepted from intent or a timer.',
  remaining=prior['remaining'],allOriginalUnfinishedGatesRetained=True,currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
  cases=cases,acceptedReports=accepted,completedAdditionalReports=completed,pendingReports=pending,
  liveProcessesObservedUTC=datetime.now(timezone.utc).isoformat(),authoritativeObservedLiveProcesses=processes,
  resumeSameUnifiedExecHandles=dict(kanoInputs=85298,sonyaInputs=56203,archiveCrosscheck=54936),
  currentRequiredRestoredNativeDependencyFiles=recovery['restoredRequiredFiles'],originalCleanupUnreferencedClaimSuperseded=True,
  remaining68BuildCleanupNetAllocatedSavings=compression['remaining68BuildCleanupNetSavingsAfterRequiredRecovery'],
  currentGameSettingsAndLaunchersUnchanged=True,gameChanged=False,fullPortAcceptance=False,finishedRelease=False,inputHashes=pins,
  nextAction='Resume the same still-live checker handles; do not restart on observation timeout. After terminal acceptance, run analyze_current_shao_guard_walk_progress_v2555.py for both cases into audit_v2558_current_<fighter>_shao_guard_walk_progress, then save_current_guard_walk_dependency_checkpoint_v2559.py. Preserve all original natural Shao/ending/return, all-arena phase/shadow/CPU/KO/audio, finisher/victim/morph/secret/cinematic, final integrated UI/ladder/name/audio and finished ZIP requirements.')

if __name__=='__main__':
 need(not OUT.exists(),'Immutable full-scope verified pending state')
 r=save();OUT.mkdir();(OUT/'pending.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:r[k]for k in('goalStatus','pendingReports','completedAdditionalReports','originalCleanupUnreferencedClaimSuperseded','gameChanged','fullPortAcceptance')},indent=2),flush=True)
