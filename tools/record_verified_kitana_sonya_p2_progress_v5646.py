"""Additive verified physical-strategy improvement and fresh live full-campaign receipt."""
import datetime,json,subprocess
from pathlib import Path
import run_verified_kitana_sonya_p2_campaign_v5642 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v5647_verified_kitana_sonya_p2_progress'

def run():
 need(not OUT.exists(),'Fresh immutable whole-goal journal')
 parent_path=ROOT/'audit_v5635_current_sonya_p2_live_campaign_progress/progress.json'
 parent=json.loads(parent_path.read_text())
 proof_path=ROOT/'audit_v5640_sonya_p2_kitana_ring_probe_checked/report.json'
 proof=json.loads(proof_path.read_text())
 need(proof['passed']and proof['native']['actualKitanaEncounterWon']and
  len(proof['actualInputStateAndNativeWinnerFaultsRejected'])==11 and
  all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual true Kitana win and complete per-field physical/native fault proof retained')
 old=ROOT/'audit_v5629_current_sonya_p2_campaign'
 cancelled=json.loads((old/'host_cancellation_reason.json').read_text())
 terminal=json.loads((old/'result.json').read_text())
 need(not terminal['passed']and terminal['nativeExit']==cancelled['terminalNativeExit']==4294967295 and
  terminal['actualStages']==[0,1,2]and (old/'capture_failure.json').is_file(),
  'Original deliberate host-cancelled failure retained, not relabeled crash or successful tower')
 folder=capture.OUT;manifest=json.loads((folder/'process.json').read_text())
 query=f"Get-CimInstance Win32_Process -Filter 'ProcessId={manifest['pid']} OR ProcessId={manifest['hostPID']}' | Select-Object ProcessId,Name,CommandLine,@{{Name='createdUnix';Expression={{([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}}}} | ConvertTo-Json -Compress"
 processes=json.loads(subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout)
 need(isinstance(processes,list)and len(processes)==2,'Exact new native/host jobs authoritatively live')
 native=next(p for p in processes if p['ProcessId']==manifest['pid'])
 host=next(p for p in processes if p['ProcessId']==manifest['hostPID'])
 need(native['Name']=='mkport_candidate.exe'and 0<=native['createdUnix']-manifest['startedUnix']<30 and
  str(ROOT/capture.LUA)in native['CommandLine']and host['Name']=='python.exe'and
  'run_verified_kitana_sonya_p2_campaign_v5642.py'in host['CommandLine'],'Actual new full campaign identities, no reused PID inference')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public CMD and ZIP unchanged')
 paths=[parent_path,proof_path,Path(__file__).resolve(),ROOT/'tools/verify_verified_kitana_sonya_p2_campaign_v5644.py',
  *public,*[p for p in old.rglob('*')if p.is_file()],
  *[p for p in(ROOT/'audit_v5638_sonya_p2_kitana_ring_probe').rglob('*')if p.is_file()]]
 pins={str(p.resolve()):sha(p)for p in paths}
 journal=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(parent_path),
  previousGoalTurnClassification='progress and verified wait: first native P2 Kitana physical Leg encounter qualified, old full campaign live',
  thisGoalTurnClassification='progress: independently qualified1226Kitana Ring fields/16native Ring tasks, two genuine own round wins and native stage3 advancement with11effective faults; obsolete losing policy deliberately host-cancelled with original failure retained, new full campaign launched and exact jobs verified live',
  actualKitanaStrategyProbeProof=str(proof_path),actualKitanaOwnRoundWins=2,actualKitanaLossesInProbe=0,
  actualCompleteRingFields=proof['actualFullRingSpacingReplay']['actualCompleteRangeFields'],
  actualNativeOwnRingTasks=proof['actualFullRingSpacingReplay']['actualNativeOwnRingTasks'],
  actualInputStateWinnerFaultsRejected=proof['actualInputStateAndNativeWinnerFaultsRejected'],
  obsoletePolicyHostCancellation=str(old/'host_cancellation_reason.json'),oldNativeTerminal=terminal['nativeExit'],
  freshFullCampaign=str(folder),fullCampaignToolSession=4656,observedLiveProcesses=processes,
  newNativeBootsThisTurn=2,newBuilds=0,deletedFiles=0,rawGuestRGBPCMFilesWritten=0,
  fullSonyaP2TowerAccepted=False,fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,
  publicPlayableChanged=False,publicZIPChanged=False,sourceInputs=pins,
  next='Poll existing4656 handle and verify native15656/host151068 creation identities. On actual terminal use5644 whole native campaign/boss/ending/attract/18fault plus full physical-input gates; all five original groups remain in scope.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(journal,indent=2)+'\n')
 sealed=[path,proof_path,Path(__file__).resolve(),ROOT/'tools/verify_verified_kitana_sonya_p2_campaign_v5644.py',
  ROOT/'tools/run_verified_kitana_sonya_p2_campaign_v5642.py',ROOT/capture.LUA,
  ROOT/'mk2ks_sonya_p2_kitana_ring_probe_v5636.lua',ROOT/'tools/run_sonya_p2_kitana_ring_probe_v5637.py',
  ROOT/'tools/verify_sonya_p2_kitana_ring_probe_v5639.py']+[
  p for p in paths if p.suffix in('.json','.log','.cfg')and p.resolve().is_relative_to(old.parent.resolve())and p not in public]
 before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded sealed-evidence compression')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,'Lossless compression succeeded')
 need(all(sha(p)==h for p,h in before.items())and all(sha(p)==h for p,h in pins.items()),
  'Original failures, all evidence/public bytes unchanged; current growing stream untouched')
 print(json.dumps({k:v for k,v in journal.items()if k not in('sourceInputs','observedLiveProcesses','actualInputStateWinnerFaultsRejected')},indent=2),flush=True)

if __name__=='__main__':run()
