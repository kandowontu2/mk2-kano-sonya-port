"""Additive actual current CPU contact/audio checkpoint; full goal stays active."""
import ctypes,datetime,json,re,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5327_current_cpu_contact_audio_progress'
PARENT=ROOT/'audit_v5322_current_subzero_all_special_body_shadow_progress/progress.json'
REPORT=ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json'
REMAINING=[
 'Broader native Pit/Tomb victim/mirror/branch combinations and complete stage effect/victim audio fidelity',
 'Full move-phase art, grounding, native floor shadows and cleanup across arenas; broader CPU, repeated, KO and overlap cases',
 'All other finishers, victims, morphs, secrets and cinematics',
 'Actual natural Kintaro/ShaoKahn campaign clears, own endings and return to attract',
 'Final combined selection/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed release ZIP']

def run():
 current.expected()
 parent=json.loads(PARENT.read_text());report=json.loads(REPORT.read_text())
 need(parent['remaining']==REMAINING and parent['goalStatus']=='active','Entire original unfinished scope retained verbatim')
 need(report['passed']and report['candidate']==current.NAME and report['originalEntireNativeCPUHitAudioContractRetained']and
      report['fullCapturedNaturalCPUBicycleLaunchCryPlaybackAndOwnershipAccepted']and not report['fullPortAcceptance'],
      'Actual finite current CPU phase/audio acceptance, no broader promotion')
 pins={str(PARENT):sha(PARENT),str(REPORT):sha(REPORT),str(Path(__file__).resolve()):sha(__file__)}
 for table in(parent['newInputHashes'],report['inputHashes']):
  for p,h in table.items():need(sha(p)==h,'Retained authoritative input/evidence unchanged: '+p)
 for p,h in report['inputHashes'].items():pins[p]=h
 captures=[];files=[];rgb=[]
 for suffix in('samples','nosamples'):
  folder=ROOT/f'audit_v5324_current_cpu_bicycle_ram_{suffix}'
  meta=json.loads((folder/'result.json').read_text());process=json.loads((folder/'process.json').read_text())
  scenes=json.loads((folder/'rgb_memory_proofs.json').read_text());log=(folder/'run.log').read_text()
  need(meta['exit_code']==0 and meta['candidate']==current.NAME and meta['wholeActualGuestComparedInRAM']and
       meta['rawAudioRGBGuestFilesWritten']==0 and (folder/'stderr.log').read_text()=='','Real warning-free terminal and RAM-only buffers')
  need(len(scenes)==meta['actualRGBFields']==77 and all(r['bytes']=='406400'for r in scenes),'All original snapshot callbacks transported to complete RAM RGB')
  need(not re.search(r'hex=|LUA ERROR|stack traceback|Fatal error',log),'No persisted media or observer failure')
  need(not any(p.suffix.lower()in('.bin','.png','.wav')for p in folder.rglob('*')if p.is_file()),'No new raw ROM/RGB/audio files')
  captures.append(dict(folder=str(folder),pid=process['pid'],command=process['command'],nativeExit=meta['exit_code'],
    originalNativeRGBFields=len(scenes),wholeGuestSHA256=current.GUEST_SHA,
    actualRoundFields=sum(s.startswith('MK2_CPU_ROUND_FIELD ')for s in log.splitlines()),
    actualPairFields=sum(s.startswith('MK2_CPU_PAIR_FIELD ')for s in log.splitlines()),
    actualPCMBytesVerifiedInRAM=meta['mixedPCMBytes']))
  rgb.append(scenes)
  for p in folder.rglob('*'):
   if p.is_file():files.append(p);pins[str(p)]=sha(p)
 need(rgb[0]==rgb[1],'All actual enabled/disabled native RGB fields identical, not just chosen samples')
 # Authoritative process census, not inference from a result file or old handle.
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True)
 need(census.returncode==0,'Actual native process census available')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 for process in live:
  need(not any(process['ProcessId']==c['pid']and c['folder']in(process.get('CommandLine')or'')for c in captures),
       'No captured native process still live under the exact PID/command')
 public={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  ROOT/'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'}
 for p,h in public.items():need(sha(p)==h,'Public playable/release unchanged');pins[str(p)]=h
 kernel=ctypes.WinDLL('kernel32',use_last_error=True)
 measure=kernel.GetCompressedFileSizeW;measure.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong));measure.restype=ctypes.c_ulong
 allocated=0
 for p in files:
  high=ctypes.c_ulong();ctypes.set_last_error(0);low=measure(str(p),ctypes.byref(high))
  need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual retained trace allocated size')
  allocated+=(high.value<<32)|low
 return dict(passed=True,schema=1,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=REMAINING,
  previousGoalTurnClassification='no progress: brief acknowledgment; current state and live process census revalidated before next safe physical test',
  thisGoalTurnClassification='progress: two actual cold current-candidate CPU boots, natural Sonya18 versus selected Kano17; entire original input/RNG/state/health trajectory identical; native Bicycle contact, separate recovery and complete mixed launch/cry finite ownership accepted. Only observation transport changed. No gameplay/build/public changes.',
  currentNaturalCPUContactAudioReport=str(REPORT),actualColdBoots=2,captures=captures,phase=report['phase'],
  actualNativeCPUChoiceNotPrescribed=True,actualContactDamage=22,mixedPCMUpdatesPerCapture=report['mixedPCMUpdates'],
  cueCorrelation=report['correlation'],cueGain=report['gain'],cueCompletedFrames=report['completedFrames'],
  wholeBothSlotNativeRGBTransportComparedFields=154,fullArtRasterOrShadowAcceptance=False,
  previewObservation='Host preview sheet too large for image tool; no visual-art acceptance inferred. Future preview must be a bounded selection, not all77 tiles.',
  nativeProcessCensus=live,noCapturedNativeProcessStillLive=True,
  newTraceLogicalBytes=sum(p.stat().st_size for p in files),newTraceAllocatedBytes=allocated,
  rawGuestGFXRGBPCMOrWAVFilesWritten=0,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,
  refreshedReleaseZIP=False,fullPortAcceptance=False,allCPUContextsOrArenasOrContactDCSAudioAccepted=False,
  allOriginalFiveGroupsRemainActive=True,newInputHashes=pins,
  nextAction='Current natural CPU Square and actual CPU Kano contexts; bounded RAM preview, full body/shadow/native erase and phase/push replay. Broader naturally reached arenas, KO/overlap, complete effect/victim/DCS waveform fidelity, all remaining finishers/morphs/secrets/cinematics and independent transition choreography; final combined selection/ladder/names/audio/release regression and dependency-aware cleanup. Do not rerun finished P1 campaigns/endings or this accepted CPU Bicycle audio pair.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh additive journal')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','captures','nativeProcessCensus','remaining')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
