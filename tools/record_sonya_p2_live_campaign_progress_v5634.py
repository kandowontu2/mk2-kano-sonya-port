"""Additive completed-encounter proof plus authoritative live native job receipt.

No terminal/clear assertion from a growing log. Static evidence compressed;
running stream untouched and exact live handle retained for next continuation.
"""
import datetime,json,subprocess
from pathlib import Path
import verify_current_sonya_p2_kitana_prefix_v5632 as prefix
ROOT,need,sha=prefix.ROOT,prefix.need,prefix.sha
OUT=ROOT/'audit_v5635_current_sonya_p2_live_campaign_progress'

def run():
 need(not OUT.exists(),'Fresh immutable additive live-job receipt')
 report_path=prefix.OUT/'report.json';report=json.loads(report_path.read_text())
 need(report['passed']and report['physicalSlot']==2 and report['humanIdentity']==18 and
  len(report['actualRecordFaultsRejected'])==8,'Actual complete P2 Kitana state/input replay and8effective faults')
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All immutable captured and independently checked inputs intact')
 capture=prefix.whole.capture
 manifest_path=capture.OUT/'process.json';manifest=json.loads(manifest_path.read_text())
 query=f"Get-CimInstance Win32_Process -Filter 'ProcessId={manifest['pid']} OR ProcessId={manifest['hostPID']}' | Select-Object ProcessId,Name,CommandLine,@{{Name='createdUnix';Expression={{([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}}}} | ConvertTo-Json -Compress"
 probe=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True)
 processes=json.loads(probe.stdout);need(isinstance(processes,list)and len(processes)==2,'Both exact host/native processes authoritatively live now')
 native=next(p for p in processes if p['ProcessId']==manifest['pid'])
 host=next(p for p in processes if p['ProcessId']==manifest['hostPID'])
 need(native['Name']=='mkport_candidate.exe'and 0<=native['createdUnix']-manifest['startedUnix']<30 and
  str(ROOT/capture.native.NAME/'mkport_candidate.exe')in native['CommandLine']and
  str(ROOT/capture.LUA)in native['CommandLine']and host['Name']=='python.exe'and
  'run_current_sonya_p2_campaign_v5628.py'in host['CommandLine'],
  'Exact live jobs, current executable/controller provenance and native creation time; no reused PID inference')
 previous=ROOT/'audit_v5626_current_kano_p2_campaign_progress/progress.json'
 parent=json.loads(previous.read_text())
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':
  '994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public playable launcher and ZIP unchanged')
 pins={str(p.resolve()):sha(p)for p in[previous,report_path,manifest_path,Path(__file__).resolve(),*public]}
 journal=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(previous),
  previousGoalTurnClassification='progress: current Kano P2 full native clear/own ending/300attract with18effective faults',
  thisGoalTurnClassification='progress and verified wait: current Sonya P2 genuine source-slot adaptation, actual complete first Kitana encounter whole input/state/ownership replay with8effective faults and5owned leg activations; exact same native and host processes freshly verified live, full campaign not claimed',
  completeEncounterProof=str(report_path),nativeCapture=str(capture.OUT),candidate=capture.native.NAME,
  physicalSlot=2,trueIdentity=18,actualNativeInitializedGuestBytesComparedInRAM=1048576,
  actualCompleteKitanaFields=report['actualCompletePhysicalReplay']['actualCompleteGuardFields'],
  actualNativeLegActivations=report['actualCompletePhysicalReplay']['actualNativeLegActivations'],
  actualRecordFaultsRejected=report['actualRecordFaultsRejected'],
  fullCampaignPending=True,actualNaturalCurrentSonyaP2ClearAccepted=False,
  observedLiveProcesses=processes,originalCaptureToolSession=90301,
  freshNativeBoots=1,newBuilds=0,rawGuestRGBPCMFilesWritten=0,deletedFiles=0,
  publicPlayableChanged=False,publicZIPChanged=False,sourceInputs=pins,
  growingLogPinnedAsTerminal=False,fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,
  next='Poll existing90301handle and exact native137472/host150512 creation identities; do not launch duplicate or infer stop on timeout. If terminal, inspect true native result and entire campaign proof; repeated Kitana losses are not a proven game engine bug or clear.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(journal,indent=2)+'\n')
 sealed=[report_path,path,manifest_path,capture.OUT/'input_hashes_before.json',capture.OUT/'guest_memory_proof.json',
  ROOT/capture.LUA,Path(capture.__file__).resolve(),Path(prefix.whole.__file__).resolve(),Path(prefix.__file__).resolve(),Path(__file__).resolve()]
 before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded static evidence compression only')
  compressed=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(compressed.returncode==0,'Lossless static evidence compression succeeded')
 need(all(sha(p)==h for p,h in before.items())and all(sha(p)==h for p,h in pins.items())and
  all(sha(p)==h for p,h in report['inputHashes'].items()),'Static captured/public inputs unchanged; running gzip never touched')
 print(json.dumps({k:v for k,v in journal.items()if k not in('sourceInputs','actualRecordFaultsRejected')},indent=2),flush=True)
 return journal

if __name__=='__main__':run()
