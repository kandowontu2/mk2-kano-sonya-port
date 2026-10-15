"""Full-goal additive progress: real Sonya clear observed and metadata-only fix."""
import ctypes,json,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v5212_current_campaign_progress/progress.json'
OUT=ROOT/'audit_v5228_campaign_and_metadata_progress'

def main():
 need(not OUT.exists(),'Fresh immutable whole-goal journal')
 parent=json.loads(PARENT.read_text())
 capture=ROOT/'audit_v5208_extended_sonya_p1_campaign'
 actual=json.loads((capture/'result.json').read_text())
 events=actual['nativeEvents']
 need(actual['passed']and actual['nativeExit']==0 and actual['actualStages']==list(range(13))+[14,15,16]and
  any(s.startswith('MK2_NAT_CAMPAIGN_ENDING_START frame=344923 ')and 'roster=18'in s for s in events)and
  any(s.startswith('MK2_NAT_CAMPAIGN_ENDING_COMPLETED frame=347665 ')and 'pictures=1,1 texts=3,3'in s for s in events)and
  any(s.startswith('MK2_NAT_CAMPAIGN_RESULT frame=347965 ')for s in events)and
  not actual['nativeCacheOverrunObserved'],'Actual observed normal Sonya own boss clear/ending/300attract terminal')
 metadata_path=ROOT/'audit_v5226_current_metadata_native_startup_checked/report.json'
 metadata=json.loads(metadata_path.read_text())
 need(metadata['passed']and metadata['metadataOnlyFixCompiledAndNativeStartupAccepted']and
  metadata['actualNativeROMVerificationPassedWithoutWarnings']and
  len(metadata['compiledSourceChanges'])==1 and len(metadata['cases'])==2 and
  all(r['actualGuestSHA256']==native.GUEST_SHA and r['actualGuestBytesComparedInRAM']==1048576 and
   r['actualObservedFields']==6000 and r['stderrEmpty']and r['nativeChecksumWarningAbsent']and
   r['exactPriorCompleteChronologyPrefix']for r in metadata['cases']),
  'Actual new compiled metadata-only repair, no warning waiver; full guest and6000exact early fields for each fighter')
 wholepath=ROOT/'audit_v5214_extended_sonya_p1_whole_campaign_checked/report.json'
 whole=json.loads(wholepath.read_text())if wholepath.exists()else None
 command='Get-CimInstance Win32_Process -Filter "Name=\'python.exe\'" | Where-Object {$_.ProcessId -eq 134844} | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress'
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
 need(census.returncode==0,'Fresh exact independent qualifier process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 if whole is None:
  need(any(r['ProcessId']==134844 and 'verify_extended_sonya_p1_whole_campaign_v5213.py'in r['CommandLine']for r in live),
   'Pending whole proof only with actual currently live exact qualifier')
 accepted=bool(whole and whole.get('passed')and whole.get('actualNaturalCurrentSonyaP1BossesOwnEndingAttractAccepted'))
 pins=dict(parent['inputHashes'])
 for p,h in metadata['inputHashes'].items():
  need(p not in pins or pins[p]==h,'Consistent tested/new actual source bytes');pins[p]=h
 if whole and whole.get('passed'):
  for p,h in whole['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent full native campaign sources');pins[p]=h
 files=[PARENT,metadata_path,Path(__file__).resolve(),ROOT/'tools/verify_extended_sonya_p1_whole_campaign_v5213.py',
  ROOT/'tools/verify_current_metadata_native_startup_v5221.py',
  ROOT/'tools/verify_current_metadata_native_startup_v5223.py',
  ROOT/'audit_v5222_current_metadata_native_startup_checked/failure.json',
  ROOT/'tools/qualify_current_payload_rom_metadata_v5216.py',
  ROOT/'audit_v5217_current_payload_rom_metadata_source_checked/report.json',
  ROOT/'tools/build_current_payload_rom_metadata_v5218.ps1']
 if whole:files.append(wholepath)
 files.extend(p for p in capture.rglob('*')if p.is_file())
 for p in files:pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All original failed/passed/candidate/public evidence bytes preserved')
 api=ctypes.windll.kernel32.GetCompressedFileSizeW
 api.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];api.restype=ctypes.c_uint32
 exe=ROOT/metadata['candidate']/'mkport_candidate.exe';high=ctypes.c_uint32();low=api(str(exe),ctypes.byref(high))
 allocated=(high.value<<32)|low
 need(allocated==17997824 and sha(exe)==metadata['executableSHA256'],'Actual lossless LZX allocation and unchanged executable bytes')
 report=dict(schema=1,parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=parent['remaining'],
  mergeRule='Read with5212and all preceding whole-goal journals. Original requirements/evidence/exclusions persist. New metadata source/build changes only declaration; actual prior full campaigns and new6000field starts are not silently substituted for new-executable tower/art/audio/full-port acceptance.',
  previousGoalTurnClassification='progress: actual full KanoP1 native/boss/end/300attract proof accepted; Sonya reached Kintaro with35native uppercuts and240legs; unchanged-control longer observation launched.',
  thisGoalTurnClassification='progress: consumed same44535actual Sonya terminal0at347965; both own bosses/two native ending pages/300attract observed. Complete original whole native/physical verifier running at exact process below. Prepared/source-qualified one CRC32/SHA1 metadata declaration against immutable current payload with5actual source faults; compiled new candidate with all other sources/game/payload/guest unchanged. Native ROM verifier passed with no checksum warning; both actual6000field cold starts have exact entire guest and every cold selection/ladder/live/gameplay/RGB event prefix equal to tested candidate. Dirty sources/installed exe exactly restored. New executable losslessly LZX-compressed107422872logical to17997824allocated bytes, saving24690688additional bytes; prior cleanup not recounted.',
  sonyaCurrentActualTerminal=dict(capture=str(capture),execSession=44535,execTerminalConsumed=True,nativeExit=0,
   frames=347965,stages=list(range(13))+[14,15,16],paidLosses=75,selections=76,
   endingStart=344923,endingCompleted=347665,returnToAttractFields=300,
   nativeEndingPictureReads=[1,1],nativeEndingTextReads=[3,3],cacheGlobalStores=0,
   independentWholeCampaignAccepted=accepted,independentQualifierSession=46710,
   independentQualifierPID=134844,exactLiveQualifier=live,wholeReport=str(wholepath)if whole else None,
   wholeResult=whole if whole and not whole.get('passed')else None),
  metadataOnlyProductionCorrection=dict(candidate=metadata['candidate'],report=str(metadata_path),
   executableSHA256=metadata['executableSHA256'],payloadSHA256=metadata['payloadSHA256'],
   guestSHA256=metadata['guestSHA256'],compiledMetadataSourceDelta=metadata['compiledSourceChanges'],
   actualNativeROMAuditWithoutWarning=True,actualFullGuestRAMContexts=2,actualEarlyGameplayFields=12000,
   actualExactChronologyRows=[r['actualExactNativeChronologyRows']for r in metadata['cases']],
   nativeCandidateMetadataDefectClosed=True,actualNewCandidateTowerClearsAccepted=False,
   publicPlayableChanged=False,existingDirtySourceAndInstalledExeRestored=True),
  failedCheckerAttemptsPreserved=[
   dict(source='tools/verify_current_metadata_native_startup_v5221.py',actualNativeROMExit=0,
    issue='Status parser omitted actual [mk2] parent annotation; never a native checksum failure.'),
   dict(source='tools/verify_current_metadata_native_startup_v5223.py',
    issue='Fresh parser source syntax rejected before native launch; preserved.'),
   dict(source='tools/verify_current_metadata_native_startup_v5225.py',passed=True,
    note='Exact actual native parent-qualified status; empty stderr, no warning waiver.')],
  inputHashes=pins,newBuilds=1,newCandidateExecutableLogicalBytes=107422872,
  newCandidateExecutableAllocatedBytes=allocated,currentTurnAdditionalAllocatedReclaimedBytes=24690688,
  publicPlayableChanged=False,rawGuestMediaAudioFilesWritten=0,newlyDeletedFiles=0,
  fullPortAcceptance=False,finishedRelease=False,
  nextAction='Poll same46710and actual134844 while live; consume actual complete native/physical qualifier and inspect its exact result. Do not restart for observation timeout. If native/physical proof passes, current4992KanoP1andSonyaP1bosses/own endings/300attract are accepted finite contexts; full pixels/audio and broader original five groups remain. New5219metadata repair has actual ROM/no-warning/full guest/12000earlyfield proof and all other sources identical, but actual new-executable tower clears remain explicitly unaccepted until obtained. Continue whole ending pixels/hardware and stage/victim/audio/art/shadow/CPU/KO/finisher/morph/secret/cinematic/combined selection/ladder/names/cleanup/refreshed-release requirements.',
  storage='One new immutable metadata-only executable, allocated17.16MiB after lossless LZX; existing payload hardlinked, no duplicate full build tree/ROM assets. New text gzip-streamed. Prior32.49GiB/61.46MiB savings not recounted.')
 need(len(report['remaining'])==5,'All five original unfinished groups preserved verbatim')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),goalStatus='active',
  actualSonyaNormalEndingAttractObserved=True,independentSonyaWholeCampaignAccepted=accepted,
  wholeQualifierLive=live,currentMetadataCompiledNativeStartupAccepted=True,newExecutableAllocatedBytes=allocated,
  additionalLosslessCompressionReclaimedBytes=24690688,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
