"""Additive whole-goal checkpoint; actual failures, live handles and full scope."""
import ast,datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import run_p1_ending_deferred_pixels_v5266 as fresh
import run_p1_ending_pixels_v5247 as older
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5252_corrected_campaign_and_p1_ending_progress/progress.json'
OUT=ROOT/'audit_v5277_current_p1_ending_export_repair_progress'
def main():
    need(not OUT.exists(),'Fresh immutable whole-goal journal')
    parent=json.loads(PARENT.read_text())
    need(len(parent['remaining'])==5 and all(sha(p)==h for p,h in parent['newInputHashes'].items()),
      'All five original groups and whole prior evidence preserved')
    pins={str(PARENT):sha(PARENT),str(Path(__file__).resolve()):sha(__file__)}
    sourcepath=ROOT/'audit_v5267_p1_ending_deferred_source_checked/report.json'
    gatepath=ROOT/'audit_v5275_current_p1_complete_ending_gate_source_checked/report.json'
    for p in (sourcepath,gatepath):
        proof=json.loads(p.read_text())
        need(proof['passed']and proof['sourceOnly']and all(sha(k)==h for k,h in proof['inputHashes'].items()),
          'Actual complete observer/export/hardware/page source gate retained')
        pins[str(p)]=sha(p)
    oldfolder=ROOT/'audit_v5250_kano_current_p1_ending_pixels'
    failpath=ROOT/'audit_v5250_kano_current_p1_ending_pixels_checked/report.json'
    old=json.loads((oldfolder/'result.json').read_text());failed=json.loads(failpath.read_text())
    need(old['nativeExit']==0 and old['passed']and not old['endingModelErrors']and
      old['exactContinuousEndingFields']==old['observedEndingRGBFields']==3040 and
      len(old['endingNativePixelFaults'])==2 and not failed['passed']and
      "'bool' object has no attribute 'records'"in failed['error'],
      'Actual native success then real post-terminal exporter collision; not complete final acceptance')
    need(not any((oldfolder/p).exists()for p in ('ending_buffer_digests.json',
      'ending_visible_digests.json','ending_continuous_records.json')),
      'Missing per-field export explicitly unaccepted; aggregate counts never substitute')
    for p in (failpath,oldfolder/'result.json',oldfolder/'run.log.gz'):pins[str(p)]=sha(p)
    compresspath=ROOT/'audit_v5256_recent_retained_executable_compression/report.json'
    compression=json.loads(compresspath.read_text())
    need(compression['passed']and compression['additionalAllocatedBytesReclaimed']==74076160 and
      compression['oldFilesDeleted']==0 and not compression['publicPlayableChanged']and
      all(sha(p)==h for p,h in compression['inputHashes'].items()),
      'Actual lossless additional70.64MiB compression, not previously reclaimed bytes')
    for item in compression['files']:
        need(sha(item['Path'])==item['SHA256']and Path(item['Path']).stat().st_size==item['LogicalBytes'],
          'Every retained compressed executable whole byte/length exact')
    pins[str(compresspath)]=sha(compresspath)
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',
      'Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @(143232,143496,142528,140956) } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'],
      capture_output=True,text=True)
    need(census.returncode==0,'Fresh authoritative exact process census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    runs=[]
    for fighter,hostpid,nativepid,session,leaf,module in [
      ('kano',143232,143496,2505,'audit_v5264_',fresh),
      ('sonya',142528,140956,87441,'audit_v5250_',older)]:
        folder=ROOT/f'{leaf}{fighter}_current_p1_ending_pixels'
        terminal=ROOT/f'{leaf}{fighter}_current_p1_ending_pixels_checked/report.json'
        proof=json.loads(terminal.read_text())if terminal.exists()else None
        hosts=[p for p in live if p['ProcessId']==hostpid and Path(module.__file__).name in p['CommandLine']and
          f'--fighter {fighter}'in p['CommandLine']]
        natives=[p for p in live if p['ProcessId']==nativepid and p['ParentProcessId']==hostpid and
          current.NAME in p['CommandLine']and str(folder)in p['CommandLine']and module.source.LUA in p['CommandLine']]
        need(proof is not None or len(hosts)==len(natives)==1,'Pending only if exact current collector/native verified live')
        guest=json.loads((folder/'guest_memory_proof.json').read_text())
        process=json.loads((folder/'process.json').read_text())
        need(process['pid']==nativepid and process['hostPID']==hostpid and
          guest['sha256']==current.GUEST_SHA and guest['everyActualByteComparedInRAM']and
          guest['captureSourceSHA256']==sha(module.__file__)and guest['transportSourceSHA256']==sha(ROOT/module.source.LUA),
          'Each actual current whole1MiB guest/source/control wrapper proof exact')
        for name in ('process.json','guest_memory_proof.json','input_hashes_before.json'):
            pins[str(folder/name)]=sha(folder/name)
        if proof:pins[str(terminal)]=sha(terminal)
        need(not any(p.suffix.lower()in('.png','.bin','.wav')for p in folder.rglob('*')if p.is_file()),
          'No new raw ROM/VRAM/RGB/audio media files')
        runs.append(dict(fighter=fighter,capture=str(folder),execSession=session,hostPID=hostpid,nativePID=nativepid,
          exactCurrentlyLiveHost=hosts,exactCurrentlyLiveNative=natives,terminal=proof,
          actualWholeGuestComparedInRAM=True,terminalPending=proof is None,
          knownPostExportAliasBug=(module is older),growingLogNotPinned=True))
    files=['tools/qualify_p1_ending_deferred_source_v5262.py','tools/run_p1_ending_deferred_pixels_v5261.py',
      'tools/qualify_p1_ending_deferred_source_v5265.py','tools/run_p1_ending_deferred_pixels_v5266.py',
      'tools/verify_current_p1_ending_pages_v5268.py','tools/verify_current_p1_native_ending_hardware_v5270.py',
      'tools/verify_current_p1_native_ending_hardware_v5272.py','tools/qualify_current_p1_ending_hardware_source_v5274.py',
      *fresh.source.EXTRA]
    for name in files:
        p=ROOT/name
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
        pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every preserved failure/fresh source/report byte exact')
    report=dict(schema=1,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      parentAdditiveJournal=str(PARENT),goalStatus='active',remaining=parent['remaining'],
      mergeRule='Additive only. Every original requirement/evidence/exclusion remains. Current campaign clears do not prove every move/art/audio/finisher/cinematic/full-port context.',
      previousGoalTurnClassification='no progress: acknowledgement only; revalidated live handles and authoritative terminal/source evidence',
      thisGoalTurnClassification='progress: consumed61838 actual preflight failure, preserved and corrected exact nonvacuous fault anchor. Full fresh source gates5267 and5275 passed. Consumed original Kano41152 native0/full3040model match but hostexport1; missing per-field evidence stays unaccepted. Unique ram_transport alias repaired. Inactive taps deferred without changing any callback; actual cold admission taps kept. Launched exact same native Kano route after actual terminal, reached own ending and first600actual continuous VRAM/RGB fields matching. Sonya same87441 remains live and was polled without restart. Fresh full original page and independent hardware-ledger adapters prepared/preflighted, retaining all original faults.',
      originalKanoVideo=dict(nativeExit=0,exactObservedModelFields=3040,actualPixelBitFaultsRejected=old['endingNativePixelFaults'],
        fullFinalP1PixelHardwareAcceptance=False,hostExportFailed=True,failure=str(failpath),missingPerFieldExport=True),
      sourcePreflights=[str(sourcepath),str(gatepath)],nativeProcesses=runs,
      preparedOriginalPageVerifier='tools/verify_current_p1_ending_pages_v5268.py',
      preparedWholeIndependentHardwareVerifier='tools/verify_current_p1_native_ending_hardware_v5272.py',
      additionalAllocatedBytesReclaimed=74076160,newDeletedFiles=0,
      storage='Lossless compression only of three exact old non-running executables; all bytes/time/length retained. Prior savings not recounted. Native guest/VRAM/RGB remain RAM-only; logs gzip; no new build trees or raw media.',
      newBuilds=0,newRawROMVRAMImageAudioFilesWritten=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
      actualFullCurrentP1PixelHardwarePagesAccepted=False,completeAudioAccepted=False,fullPortAcceptance=False,
      newInputHashes=pins,
      nextAction='Poll same2505/143232/143496 and87441/142528/140956 while actually live. No timeout/loss restart. Once5264Kano actual terminal passes full pixel+perfield gate, run5268 original pages then5272 whole independent hardware ledger (all27metadata/8terminal/2actualpixel faults). Only after original5250Sonya actual native terminal consume knownexport outcome; then fresh5266Sonya successor can run. Keep all five original groups intact; no public/release promotion.')
    OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),goalStatus='active',
      liveNativeFighters=[r['fighter']for r in runs if r['exactCurrentlyLiveNative']],
      sourceGatesPassed=True,fullPortAcceptance=False,additionalReclaimedMiB=74076160/1048576),indent=2),flush=True)
if __name__=='__main__':main()
