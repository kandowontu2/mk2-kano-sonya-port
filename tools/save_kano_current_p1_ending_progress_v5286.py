"""Additive full-goal checkpoint: actual Kano complete native ending pixels/pages."""
import ast,datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5277_current_p1_ending_export_repair_progress/progress.json'
OUT=ROOT/'audit_v5287_kano_complete_current_p1_ending_progress'
def main():
    need(not OUT.exists(),'Fresh immutable whole-goal progress')
    parent=json.loads(PARENT.read_text())
    need(len(parent['remaining'])==5 and all(sha(p)==h for p,h in parent['newInputHashes'].items()),
      'All five original requirements and prior whole evidence chain retained')
    pins={str(PARENT):sha(PARENT),str(Path(__file__).resolve()):sha(__file__)}
    reports={}
    names={
      'pixels':'audit_v5281_kano_current_p1_ending_terminal_pixels_checked/report.json',
      'pages':'audit_v5283_kano_current_p1_original_ending_pages_checked/report.json',
      'hardware':'audit_v5285_kano_current_p1_complete_native_pixels_hardware_checked/report.json',
      'diagnostic':'audit_v5279_closed_current_p1_native_metadata_diagnostic/report.json'}
    for label,name in names.items():
        p=ROOT/name;proof=json.loads(p.read_text())
        need(proof['passed']and all(sha(k)==h for k,h in proof['inputHashes'].items()),'Actual immutable report/source/capture '+label)
        reports[label]=proof;pins[str(p)]=sha(p)
    pixel,page,hw=map(reports.get,('pixels','pages','hardware'))
    need(pixel['actualCurrentP1EndingAttractNativeRendererVideoAccepted']and
      pixel['actualColdNativeCampaignExactlyUnchanged']and pixel['exactConsecutiveNativeVideoFields']==3040 and
      pixel['actualAttractRendererFields']==300 and pixel['noNewNativeBoot']and
      page['actualCurrentP1EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted']and
      page['physicalSlot']==1 and page['identity']==17 and page['actualFullRGBPixelsCompared']==406400 and
      len(page['actualRAMRecordFaultsRejected'])==8 and
      all(len(p['originalPhotoFaults'])==len(p['originalGlyphShadowFaults'])==4 for p in page['pages'])and
      hw['fullEndingVRAMRGBPixelsAccepted']and hw['metadataNeverSubstitutedForPixels']and not hw['dummyVRAMUsed']and
      hw['completeActualMetadataFields']==3040 and hw['physicalSlot']==1 and hw['identity']==17 and
      len(hw['actualMetadataFaultsRejected'])==27 and len(hw['actualTerminalFaultsRejected'])==8 and
      len(hw['actualNativePixelBitFaultsRejected'])==2 and hw['actualNativeDisplayIOStores']==4407 and
      not hw['allEndingContextsAccepted']and not hw['fullPortAcceptance'],
      'Complete original actual native per-field pixels/photo/font/shadow/common-background/timing/IO/opcode/allfault scope')
    failpath=ROOT/'audit_v5264_kano_current_p1_ending_pixels_checked/report.json'
    failed=json.loads(failpath.read_text())
    need(not failed['passed']and failed['error']=="ValueError('One base only, all actual targets consumed; no floor classification substituted for cinematic semantics')",
      'Real final cleanup failure remains immutable; not silently converted to pass')
    pins[str(failpath)]=sha(failpath)
    cmd='Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @(143232,143496,142528,140956) } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',cmd],capture_output=True,text=True)
    need(census.returncode==0,'Authoritative exact native/host current census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    need(not any(p['ProcessId']in(143232,143496)for p in live),'Kano same2505 actual terminal consumed; no duplicate native run')
    folder=ROOT/'audit_v5250_sonya_current_p1_ending_pixels'
    terminal=ROOT/'audit_v5250_sonya_current_p1_ending_pixels_checked/report.json'
    sonya=json.loads(terminal.read_text())if terminal.exists()else None
    hosts=[p for p in live if p['ProcessId']==142528 and 'run_p1_ending_pixels_v5247.py'in p['CommandLine']and '--fighter sonya'in p['CommandLine']]
    natives=[p for p in live if p['ProcessId']==140956 and p['ParentProcessId']==142528 and
      current.NAME in p['CommandLine']and str(folder)in p['CommandLine']]
    need(sonya is not None or len(hosts)==len(natives)==1,'Pending only with same87441 exact current native/host verified live')
    for name in ('process.json','guest_memory_proof.json','input_hashes_before.json'):
        pins[str(folder/name)]=sha(folder/name)
    if sonya is not None:pins[str(terminal)]=sha(terminal)
    files=['tools/check_closed_p1_ending_hardware_v5278.py','tools/verify_actual_p1_ending_terminal_pixels_v5280.py',
      'tools/verify_current_p1_ending_pages_v5282.py','tools/verify_current_p1_native_ending_hardware_v5284.py']
    for name in files:
        p=ROOT/name;ast.parse(p.read_text(),filename=str(p));pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All original failure/current proof/source bytes exact')
    report=dict(schema=1,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=parent['remaining'],
      mergeRule='Additive only. All original requirements stay intact. One complete current Kano P1 native ending does not prove all choreography/art/audio/cinematic/finisher/gameplay contexts or full port.',
      previousGoalTurnClassification='progress: unique exporter alias/deferred inactive-tap source gates passed; actual native Kano successor launched;70.64MiB lossless retained-executable compression preserved',
      thisGoalTurnClassification='progress: same2505 native0 completed3040exact full VRAM/RGB fields, actual2bit faults and same cold physical chronology. Host final cleanup failed only because the real original unrendered next-notifier seed remains queued. Full retained per-field/buffer/RGB exports preserved. Fresh5280 accepted only that exact original source-order terminal record with whole independent ledger, no new native boot or discarded rendered operation. Full original page/photo/glyph/shadow/background gate5283 and entire independent native hardware/opcode/per-field ledger5285 passed all27metadata/8terminal/2actualpixel faults. Same87441 Sonya polled/verified live; no timeout or loss restart.',
      actualKanoCurrentP1Ending=dict(capture=pixel['capture'],nativeExit=0,nativeStop=85094,
        endingStart=82054,attractStart=84794,lastCompletedRendererField=85093,
        consecutiveWholeNativeFields=3040,actualAttractFields=300,
        actualRGBPixelsCompared=308864000,actualVRAMWordsCompared=796917760,
        completedNativeClocks=141262,actualNativeStopSeed=1,actualOriginalIOStores=4407,
        wholePixelsPagesAndHardwareAccepted=True,allEndingContextsOrAudioAccepted=False),
      resultPaths=names,failedFinalCleanupPreserved=str(failpath),
      actualSonyaProcess=dict(execSession=87441,hostPID=142528,nativePID=140956,
        exactCurrentlyLiveHost=hosts,exactCurrentlyLiveNative=natives,terminal=sonya,
        knownOriginalExporterAliasBug=True,growingLogNotPinned=True),
      newBuilds=0,newRawROMVRAMImageAudioFilesWritten=0,newDeletedFiles=0,
      publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,
      newInputHashes=pins,
      nextAction='Poll same87441/142528/140956 until actual terminal. Consume original real native result and expected post-export bool collision without restarting live. Then use source-qualified5266 --fighter sonya fresh capture with retained per-field exports, knowing original final cleanup requires exact native stop-seed qualification5280. Run5282 pages then5284 full independent hardware on that actual completed Sonya capture. Maintain all five original groups; broader choreography/audio/gameplay/finishers/final combined regression/release remain incomplete.')
    OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),goalStatus='active',
      currentKanoP1EndingFullPixelsPagesHardwareAccepted=True,wholeNativeFields=3040,
      sonyaSameNativeRunLive=bool(natives),fullPortAcceptance=False,newBuilds=0,rawMediaFilesWritten=0),indent=2),flush=True)
if __name__=='__main__':main()
