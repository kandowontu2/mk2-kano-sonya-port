"""Additive qualified full SonyaP2 clear and four-case native matrix receipt.

Preserve all original scope, prior losses/failures and actual declarations.
No campaign remains live. Full art/audio/release acceptance stays open.
"""
import datetime,json,subprocess
from pathlib import Path
import run_verified_subzero_sonya_p2_campaign_v5688 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v5696_sonya_p2_campaign_clear_progress'


def run():
 need(not OUT.exists(),'Fresh immutable additive goal receipt')
 parent_path=ROOT/'audit_v5681_subzero_sonya_p2_progress/progress.json'
 parent=json.loads(parent_path.read_text())
 whole_path=ROOT/'audit_v5691_verified_subzero_sonya_p2_campaign_checked/report.json'
 whole=json.loads(whole_path.read_text())
 retry_path=ROOT/'audit_v5686_sonya_p2_subzero_ring_retries_checked/report.json'
 retry=json.loads(retry_path.read_text())
 callback_path=ROOT/'audit_v5693_actual_jax_ring_callbacks_checked/report.json'
 callbacks=json.loads(callback_path.read_text())
 matrix_path=ROOT/'audit_v5698_current_campaign_four_case_matrix_checked/report.json'
 matrix=json.loads(matrix_path.read_text())
 need(whole['passed']and whole['actualNaturalCurrentSonyaP2BossesOwnEndingAttractAccepted']and
  whole['case']['unassisted_clear_proven']and len(whole['actualNativeAndRAMProofFaultsRejected'])==18 and
  len(whole['actualFullNativeJaxCallbacks']['actualNativeCallbackFaultsRejected'])==5 and
  whole['actualAttractFollowThroughFields']==300 and whole['actualNativeCacheGlobalStores']==0 and
  not whole['unexecutedSubZeroHuman107BranchAccepted'],
  'Entire actual native P2 bosses/own ending/300attract and all18native/RAM plus5Jax faults retained')
 need(retry['passed']and retry['actualSubZeroAdvanceAccepted']and retry['native']['actualFinalMatchOwnRoundWins']==2 and
  retry['native']['actualFinalMatchCpuRoundWins']==0 and len(retry['actualInputStateAndNativeWinnerFaultsRejected'])==11 and
  len(retry['actualContext8TaskAndActionFaultsRejected'])==8 and callbacks['passed']and matrix['passed']and
  matrix['actualNativeFourCaseBossOwnEndingAttractMatrixAccepted']and len(matrix['cases'])==4,
  'Actual qualified Sub-Zero win, native callback and all four current complete campaign cases')
 for report in(whole,retry,callbacks,matrix):
  need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All actually executed/current/old proof bytes intact')
 terminal=json.loads((capture.OUT/'result.json').read_text())
 need(terminal['passed']and terminal['nativeExit']==0 and terminal['rawMediaGuestAudioFilesWritten']==0,
  'Actual ordinary new campaign terminal, not observer timeout')
 old=ROOT/'audit_v5664_verified_kitana_jax_sonya_p2_campaign'
 cancelled=json.loads((old/'result.json').read_text())
 cancellation=old/'host_cancellation_reason.json'
 need(not cancelled['passed']and cancelled['nativeExit']==4294967295 and cancellation.is_file()and
  json.loads(cancellation.read_text())['engineCrashAccepted']is False,
  'Explicit deliberate cancellation and old failure preserved, never an engine crash or clear')
 manifests=[json.loads((folder/'process.json').read_text())for folder in [old,capture.OUT,
  ROOT/'audit_v5684_sonya_p2_subzero_ring_retries']]
 pids=sorted({m[key]for m in manifests for key in('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={pid}'for pid in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 for m in manifests:
  for job in jobs:
   native=job['ProcessId']==m['pid']and job['Name']=='mkport_candidate.exe'and
   0<=job['createdUnix']-m['startedUnix']<30 and m['command'][-1]in job['CommandLine']
   host=job['ProcessId']==m['hostPID']and job['Name']=='python.exe'and m['hostSource']in job['CommandLine']
   need(not(native or host),'Every exact test process is terminal; a bare reused PID is not treated as a live run')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public CMD/ZIP unchanged, no partial promotion')
 sources=[ROOT/n for n in('mk2ks_sonya_p2_subzero_ring_retries_v5682.lua',
  'tools/run_sonya_p2_subzero_ring_retries_v5683.py','tools/verify_sonya_p2_subzero_ring_retries_v5685.py',
  'mk2ks_sonya_p2_verified_subzero_campaign_v5687.lua','tools/run_verified_subzero_sonya_p2_campaign_v5688.py',
  'tools/verify_verified_subzero_sonya_p2_campaign_v5690.py','tools/verify_actual_jax_ring_callbacks_v5692.py',
  'tools/cancel_superseded_subzero_controller_v5694.py','tools/verify_current_campaign_four_case_matrix_v5697.py')]+[Path(__file__).resolve()]
 folders=[old,capture.OUT,retry_path.parent,callback_path.parent,whole_path.parent,matrix_path.parent,
  ROOT/'audit_v5684_sonya_p2_subzero_ring_retries']
 sealed=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
 need(not any(p.suffix.lower()in('.png','.wav','.bin')for p in sealed),
  'No raw buffer/guest/audio files or automatic timed-stop PNG in new/retired tests')
 pins={str(p.resolve()):sha(p)for p in[parent_path,*sources,*sealed,*public]}
 journal=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(parent_path),
  previousGoalTurnClassification='progress: first Sub-Zero guard/Leg and Ring encounters with real target-bound faults qualified; same original job verified live; failed row lookup retained',
  thisGoalTurnClassification='progress: finite real Ring retry won Sub-Zero2-0 after1loss,3646actual target fields/40actual tasks/19faults qualified;7actual native Jax ground/Carry/jump callbacks and5faults qualified. Superseded170loss controller deliberately cancelled, failure retained. New full SonyaP2 current native campaign cleared both bosses, own ending and300attract with18native/RAM faults and all actual physical replays. All four current K/S,P1/P2 full native campaign cases revalidated; full art/audio/release remains open.',
  nativeSubZeroRetryProof=str(retry_path),actualNativeJaxCallbackProof=str(callback_path),
  actualWholeSonyaP2CampaignProof=str(whole_path),actualFourCaseMatrixProof=str(matrix_path),
  actualCurrentFourCaseNativeBossOwnEndingAttractMatrixAccepted=True,
  actualFullSonyaP2TowerAccepted=True,actualSonyaP2EndingCompletionAccepted=True,
  actualSonyaP2AttractFollowThroughFields=300,actualSonyaP2OwnRoundWins=whole['case']['native_own_round_wins'],
  actualSonyaP2BossRoundWins=whole['case']['actualBossRoundWins'],actualSonyaP2PaidLosses=whole['case']['paid_continue_losses'],
  actualSonyaP2Uppercut107Assignments=whole['case']['actualNativeUppercutAssignments'],
  actualSonyaP2SpecialEntries=whole['case']['native_owned_special_entries'],
  actualSonyaP2FullRangeFields=whole['actualFullRingSpacingInputReplay']['actualCompleteRangeFields'],
  actualFaultsRejected=dict(subZeroRetry=19,nativeJaxCallbacks=5,wholeNativeAndGuest=18),
  unexecutedSubZeroCloseGuardHuman107BranchAccepted=False,
  unexecutedMovingAirborneJaxGroundResultSkipAccepted=False,
  allFourActualCurrentCampaignCases=matrix['cases'],
  deliberatelyCancelledSupersededTest=str(cancellation),retainedCancelledResult=str(old/'result.json'),
  exactNativeCampaignProcessesStillLive=[],observedOtherOrReusedPIDs=jobs,
  consumedCaptureToolSessions=[35289,29503,57004],consumedWholeVerifierToolSession=21571,
  newNativeProcessStartsThisTurn=2,newBuilds=0,deletedFiles=0,rawGuestRGBPCMFilesWritten=0,
  publicPlayableChanged=False,publicZIPChanged=False,sourceInputs=pins,
  fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,
  next='No campaign is still running and no restart is needed. Continue source-timed complete P2 ending renderer/photo/font/shadow/background and audio proof using the now qualified cold native controls; retain native clear acceptance without claiming unobserved branch/art/audio. Then broader native Pit/Tomb/victim/morph/move/KO/arena/secret/cinematic coverage, final combined regression, dependency-aware obsolete-folder cleanup and refreshed release; all original scope remains intact.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(journal,indent=2)+'\n')
 targets=[p for p in sealed if p.suffix in('.json','.log','.cfg')]+sources+[path]
 before={str(p):sha(p)for p in targets}
 for p in targets:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded sealed-file compression only')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Lossless sealed source/evidence compression')
 need(all(sha(p)==h for p,h in before.items())and all(sha(p)==h for p,h in pins.items()),
  'Actual prior failures/source/proof/public bytes preserved; no raw files, deletions or guessed savings')
 print(json.dumps({k:v for k,v in journal.items()if k not in('sourceInputs','allFourActualCurrentCampaignCases')},indent=2),flush=True)


if __name__=='__main__':run()
