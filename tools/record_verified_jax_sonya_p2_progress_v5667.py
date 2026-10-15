"""Additive Jax physical/native proof, preserved failures, exact fresh live job."""
import datetime,json,subprocess
from pathlib import Path
import run_verified_kitana_jax_sonya_p2_campaign_v5663 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v5668_verified_jax_sonya_p2_progress'

def run():
 need(not OUT.exists(),'Fresh immutable additive receipt')
 parent_path=ROOT/'audit_v5647_verified_kitana_sonya_p2_progress/progress.json'
 parent=json.loads(parent_path.read_text())
 probe_path=ROOT/'audit_v5661_sonya_p2_jax_ring_probe_checked/report.json'
 probe=json.loads(probe_path.read_text())
 input_path=ROOT/'audit_v5656_sonya_p2_jax_input_bound_checked/report.json'
 inputs=json.loads(input_path.read_text())
 need(probe['passed']and probe['native']['actualJaxEncounterWon']and probe['native']['actualOwnJaxRoundWins']==2 and
  len(probe['actualInputStateAndNativeWinnerFaultsRejected'])==11 and inputs['passed']and
  len(inputs['actualRecordFaultsRejected'])==8 and not inputs['nativeGroundPoundCarryGateAccepted'],
  'Both actual complete Jax input strategies qualified; unexecuted native ground branch not credited')
 for report in(probe,inputs):need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every executed source and actual proof byte intact')
 old=ROOT/'audit_v5643_verified_kitana_sonya_p2_campaign'
 terminal=json.loads((old/'result.json').read_text())
 need(not terminal['passed']and terminal['nativeExit']==4294967295 and (old/'host_cancellation_reason.json').is_file(),
  'Deliberately cancelled superseded test failure retained, never crash/clear acceptance')
 manifest=json.loads((capture.OUT/'process.json').read_text())
 query=f"Get-CimInstance Win32_Process -Filter 'ProcessId={manifest['pid']} OR ProcessId={manifest['hostPID']}' | Select-Object ProcessId,Name,CommandLine,@{{Name='createdUnix';Expression={{([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}}}} | ConvertTo-Json -Compress"
 jobs=json.loads(subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout)
 need(isinstance(jobs,list)and len(jobs)==2,'Exact new native/host jobs freshly verified live')
 native=next(p for p in jobs if p['ProcessId']==manifest['pid']);host=next(p for p in jobs if p['ProcessId']==manifest['hostPID'])
 need(native['Name']=='mkport_candidate.exe'and 0<=native['createdUnix']-manifest['startedUnix']<30 and
  str(ROOT/capture.LUA)in native['CommandLine']and host['Name']=='python.exe'and
  'run_verified_kitana_jax_sonya_p2_campaign_v5663.py'in host['CommandLine'],'Current live job identity/creation/source, not reused PID')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public CMD/ZIP unchanged')
 evidence_folders=[old,ROOT/'audit_v5649_sonya_p2_jax_prefix_checked',ROOT/'audit_v5651_sonya_p2_jax_input_prefix_checked',
  ROOT/'audit_v5654_sonya_p2_jax_ring_probe',ROOT/'audit_v5656_sonya_p2_jax_input_bound_checked',
  ROOT/'audit_v5659_sonya_p2_jax_ring_bound_probe',ROOT/'audit_v5661_sonya_p2_jax_ring_probe_checked']
 sealed=[p for folder in evidence_folders for p in folder.rglob('*')if p.is_file()]
 sources=[ROOT/n for n in('tools/verify_sonya_p2_jax_prefix_v5648.py','tools/verify_sonya_p2_jax_input_prefix_v5650.py',
  'tools/verify_sonya_p2_jax_input_bound_v5655.py','mk2ks_sonya_p2_jax_ring_probe_v5652.lua',
  'tools/run_sonya_p2_jax_ring_probe_v5653.py','mk2ks_sonya_p2_jax_ring_bound_probe_v5657.lua',
  'tools/run_sonya_p2_jax_ring_bound_probe_v5658.py','tools/verify_sonya_p2_jax_ring_probe_v5660.py',
  'mk2ks_sonya_p2_verified_kitana_jax_campaign_v5662.lua','tools/run_verified_kitana_jax_sonya_p2_campaign_v5663.py',
  'tools/verify_verified_kitana_jax_sonya_p2_campaign_v5665.py')]+[Path(__file__).resolve()]
 pins={str(p.resolve()):sha(p)for p in[parent_path,*sealed,*sources,*public]}
 journal=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(parent_path),
  previousGoalTurnClassification='progress: Kitana native Ring win and11fault proof; superseded first test cancelled; updated full campaign started',
  thisGoalTurnClassification='progress: all1334actual first-Jax close-guard fields with8actual faults qualified; absent137ground/jump branch not credited, both original proof/namespace failures retained. Corrected bounded Ring probe qualified1303Jax fields/two genuine own wins/stage5advancement with11actual faults; failed loader source preserved. Superseded Jax-loss controller host-cancelled, qualified Kitana/Jax full campaign launched and exact jobs verified live.',
  jaxCloseGuardInputProof=str(input_path),jaxRingNativeProof=str(probe_path),
  actualJaxRingFields=probe['actualFullRingSpacingReplay']['actualFieldsByNativeStage']['4'],
  actualOwnJaxRoundWins=2,actualJaxLossesInProbe=0,
  actualFaultsRejected=dict(closeGuardInput=8,ringInputStateAndWinner=11),
  unexecutedFirstJaxGroundPoundAndJumpGateAccepted=False,
  preservedFailures=[str(f)for f in evidence_folders if f.name in(
   'audit_v5649_sonya_p2_jax_prefix_checked','audit_v5651_sonya_p2_jax_input_prefix_checked','audit_v5654_sonya_p2_jax_ring_probe')],
  cancelledSupersededTest=str(old/'host_cancellation_reason.json'),
  freshFullCampaign=str(capture.OUT),fullCampaignToolSession=29503,observedLiveProcesses=jobs,
  newNativeProcessStartsThisTurn=3,newBuilds=0,deletedFiles=0,rawGuestRGBPCMFilesWritten=0,
  publicPlayableChanged=False,publicZIPChanged=False,fullSonyaP2TowerAccepted=False,
  fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,sourceInputs=pins,
  next='Poll29503 and exact native127684/host141652 creation identities; never infer stop from timeout. At terminal use5665 whole campaign/boss/own-ending/attract/18fault plus full input gates. Broader native ground/jump branches and all five original groups remain unproven.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(journal,indent=2)+'\n')
 targets=[p for p in sealed if p.suffix in('.json','.log','.cfg')]+sources+[path]
 before={str(p):sha(p)for p in targets}
 for p in targets:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded static evidence compression')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,'Lossless compression succeeded')
 need(all(sha(p)==h for p,h in before.items())and all(sha(p)==h for p,h in pins.items()),
  'Original failures/source/public/evidence bytes preserved; current growing stream untouched')
 print(json.dumps({k:v for k,v in journal.items()if k not in('sourceInputs','observedLiveProcesses')},indent=2),flush=True)

if __name__=='__main__':run()
