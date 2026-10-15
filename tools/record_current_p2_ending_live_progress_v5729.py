"""Current live P2 ending observers: additive receipt, not terminal acceptance.

Do not hash growing gzip streams, restart live processes, or turn transported
snapshots into completed model proof. Retain the full original goal scope.
"""
import datetime,gzip,json,subprocess
from pathlib import Path
import qualify_current_p2_ending_source_complete_v5717 as preflight

ROOT,need,sha=preflight.ROOT,preflight.need,preflight.sha
OUT=ROOT/'audit_v5730_current_p2_ending_live_progress'


def run():
 need(not OUT.exists(),'Fresh additive live ending receipt')
 parentpath=ROOT/'audit_v5700_sonya_p2_campaign_clear_bound_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 prepath=preflight.OUT/'report.json';pre=json.loads(prepath.read_text())
 need(pre['passed']and pre['entireOriginalP2DeferredObserverAndRendererRetained']and
  len(pre['actualSourceFaultsRejected'])==6 and
  all(sha(p)==h for p,h in pre['inputHashes'].items()),'Exact complete corrected P2 observer/model/control preflight retained')
 manifests=[]
 for fighter,session in [('sonya',78988),('kano',4801)]:
  folder=ROOT/f'audit_v5720_{fighter}_current_p2_ending_pixels'
  manifest=json.loads((folder/'process.json').read_text())
  need(manifest['hostSource']==str(ROOT/'tools/run_current_p2_ending_pixels_complete_v5719.py')and
   Path(manifest['command'][-1]).name==preflight.LUA,'Exact declared current native/host observer identity')
  manifests.append((fighter,session,folder,manifest))
 pids=sorted({m[k]for _,_,_,m in manifests for k in ('pid','hostPID')})
 query="Get-CimInstance Win32_Process -Filter '"+' OR '.join(f'ProcessId={p}'for p in pids)+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 output=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout.strip()
 jobs=json.loads(output)if output else []
 if isinstance(jobs,dict):jobs=[jobs]
 cases=[];pins=dict(pre['inputHashes'])
 for fighter,session,folder,m in manifests:
  native=[j for j in jobs if j['ProcessId']==m['pid']and j['Name']=='mkport_candidate.exe'and
   0<=j['createdUnix']-m['startedUnix']<30 and m['command'][-1]in j['CommandLine']]
  host=[j for j in jobs if j['ProcessId']==m['hostPID']and j['Name']=='python.exe'and
   Path(m['hostSource']).name in j['CommandLine']]
  need(len(native)==len(host)==1,'Actual specific ending processes confirmed live now, not a bare PID or stale file')
  need(not(folder/'result.json').exists()and not(folder/'ending_live_model_terminal.json').exists(),
   'Current ending capture remains nonterminal; no acceptance implied')
  need((folder/'stderr.log').read_text()=='','Current native observer has no boot/transport error')
  guest=json.loads((folder/'guest_memory_proof.json').read_text())
  need(guest['sha256']==preflight.current.GUEST_SHA and guest['everyActualByteComparedInRAM'],
   'Actual initialized full current guest independently compared in RAM')
  prefix=[];last_snap=None;snaps=0
  with gzip.open(folder/'run.log.gz','rt')as reader:
   while True:
    try:line=reader.readline()
    except EOFError:break
    if not line or not line.endswith('\n'):break
    if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '):snaps+=1;last_snap=line.rstrip()
    elif line.startswith(('MK2_NAT_CAMPAIGN_ENDING_START ','MK2_NAT_CAMPAIGN_ENDING_DISPLAY_BEGIN ')):
     prefix.append(line.rstrip())
  need(len(prefix)==2 and snaps>0,'Actual flushed native ending admission and transported snapshot prefix')
  rawfiles=[str(p)for p in folder.rglob('*')if p.is_file()and p.suffix.lower()in('.png','.wav','.bin')]
  need(not rawfiles,'No guest/RGB/PCM or automatic timed-stop PNG written')
  for name in ('process.json','guest_memory_proof.json','input_hashes_before.json'):
   p=folder/name;pins[str(p.resolve())]=sha(p)
  cases.append(dict(fighter=fighter,physicalSlot=2,toolSession=session,folder=str(folder),
   nativeProcess=native[0],hostProcess=host[0],actualClosedNativeEndingAdmissionRows=prefix,
   nativeFlushedSnapshotCount=snaps,lastClosedNativeSnapshot=last_snap,
   transportedSnapshotsAreNotTerminalPixelAcceptance=True,actualTerminalPixelProofPending=True))
 sources=[ROOT/n for n in (
  'tools/qualify_current_p2_ending_source_complete_v5717.py','tools/run_current_p2_ending_pixels_complete_v5719.py',
  'tools/verify_actual_current_p2_ending_terminal_pixels_v5721.py','tools/verify_current_p2_ending_pages_v5723.py',
  'tools/verify_current_p2_native_ending_hardware_v5725.py','tools/verify_current_p2_native_ending_hardware_bound_v5727.py')]
 pins.update({str(p.resolve()):sha(p)for p in [parentpath,prepath,Path(__file__),*sources]})
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'No incomplete public promotion')
 pins.update({str(p):h for p,h in public.items()})
 report=dict(passed=True,goalStatus='active',observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  parentAdditiveJournal=str(parentpath),remaining=parent['remaining'],
  previousGoalTurnClassification='progress: four actual current K/S P1/P2 native boss clears, own endings and300attract independently qualified',
  thisGoalTurnClassification='progress: real source-map and observer-composition failures retained and corrected; complete original P2 observer/model/control preflight passed with6actual source faults; both corrected native cold campaigns reached own true-ID endings and remain verified live; complete post-terminal pixel/page/hardware gates prepared',
  actualNewEndingPixelsAccepted=False,actualFourCaseNativeCampaignAcceptanceRetained=True,
  liveNativeEndingCases=cases,completeEndingArtAudioAccepted=False,fullPortAcceptance=False,
  genuineFailuresPreserved=['audit_v5706_current_p2_ending_source_checked/report.json',
   'audit_v5712_sonya_current_p2_ending_pixels/stderr.log'],
  hardwareNamespaceImportErrorPreservedSource='tools/verify_current_p2_native_ending_hardware_v5725.py',
  sourceInputs=pins,growingLogsHashed=False,rawMediaWritten=0,newBuilds=0,deletedFiles=0,
  publicPlayableChanged=False,publicZIPChanged=False,
  next='Poll the SAME Sonya78988/Kano4801 handles, validate exact process identity if needed, never restart on an observation timeout. After real terminal consume full5721 terminal+5723 page+5727 hardware gates for each fighter. Both stages/own-ending state already match qualified current campaign starts. Complete all original remaining scope, final regression/cleanup/release; no complete-port claim.')
 need(all(sha(p)==h for p,h in pins.items()),'All immutable old/new/failure/current/public bytes preserved')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 # Only immutable source/preflight/journal files; leave every active capture alone.
 sealed=[Path(__file__),*sources,prepath,path]
 before={str(p):sha(p)for p in sealed}
 for p in sealed:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded immutable source/evidence compression')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Lossless immutable text compression')
 need(all(sha(p)==h for p,h in before.items()),'Compression retains every exact byte; no guessed savings')
 print(json.dumps({k:v for k,v in report.items()if k not in('sourceInputs','remaining')},indent=2),flush=True)


if __name__=='__main__':run()
