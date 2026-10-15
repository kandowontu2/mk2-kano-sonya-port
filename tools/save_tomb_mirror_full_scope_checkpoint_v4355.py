"""Record actual mirror progress without shrinking any original full-port scope."""
import ctypes,json,subprocess
from pathlib import Path
import run_tomb_mirror_audio_ram_v4350 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
PARENT=ROOT/'audit_v4339_kintaro_rejection_cleanup_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4356_tomb_mirror_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable complete-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(path)==h for path,h in pins.items()),'All inherited original logical evidence/source/playable bytes unchanged')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);h=sha(path)
        need(key not in pins or pins[key]==h,'Inherited/shared original byte identity')
        need(wanted is None or h==wanted,'Exact actual executed source/report hash');pins[key]=h
    pin(PARENT);pin(__file__)
    matrixpath=ROOT/'audit_v4354_both_characters_both_slots_tomb_mirrors/report.json'
    branchpath=ROOT/'audit_v4358_true_mirror_native_tomb_branches/report.json'
    matrix=json.loads(matrixpath.read_text());branch=json.loads(branchpath.read_text())
    need(matrix['passed']and branch['passed']and matrix['actualTrueMirrorContexts']==4 and matrix['actualPairedCaptures']==8,
      'Actual terminal complete4context8capture mirror matrix and separate native branch qualification')
    need(matrix['current3836NativeTombBothTrueMirrorCharactersBothSlotsEarnedStateCleanupDCSDeliveryWinnerMixAccepted']and
      not matrix['fullTombRasterAndFloorShadowAccepted']and not matrix['nativeDCSStageVictimFullWaveformAccepted']and
      not matrix['allStageMirrorBranchesAccepted']and not matrix['fullPortAcceptance'],'No false scene/audio/branch/full-port acceptance')
    need(branch['actualHeldMirrorContexts']==4 and branch['actualDropMirrorContexts']==0 and
      not branch['allMirrorBranchCoverageAccepted']and not branch['fullPortAcceptance'],'Only actual held branches credited, no prescribed native RNG or imaginary drops')
    need({(c['fighter'],c['side'],c['victim'])for c in matrix['cases']}==
      {('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18)},'Every actual true mirror physical slot')
    need(sum(len(c['actualFaultsRejected'])for c in matrix['cases'])==48 and
      sum(len(c['actualFaultsRejected'])for c in branch['cases'])==16,
      'Actual earned/native/identity/health/cleanup and branch PC/Main/actor/input counterexamples rejected')
    for path,report in ((matrixpath,matrix),(branchpath,branch)):
        pin(path)
        for p,h in report['inputHashes'].items():pin(p,h)
    failed=ROOT/'audit_v4348_tomb_mirror_audio_ram_observed/report.json'
    initial=json.loads(failed.read_text());need(not initial['passed']and
      'Original complete1100field driver retirement' in initial['error'],'Original executed strict exit-timing failure preserved')
    pin(failed)
    folders=[ROOT/'audit_v4345_tomb_mirror_kano_p1_samples',ROOT/'audit_v4345_tomb_mirror_kano_p1_nosamples']
    folders.extend(ROOT/c[k]for c in matrix['cases']for k in ('capture','baseline'))
    native_pids=[]
    for folder in folders:
        meta=json.loads((folder/'result.json').read_text());process=json.loads((folder/'process.json').read_text())
        need(meta['exit_code']==0 and meta['guest_writes']==0 and meta['assistance']=='none'and
          meta['guestSHA256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and
          meta['rawAudioRasterVRAMROMCopiesWritten']==0,'Every actual terminal complete RAM-only initialized3836 guest')
        native_pids.append(process['pid'])
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
    for name in ('mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_tomb_mirror_provenance_ram_v4341.lua',
      'mk2ks_tomb_mirror_audio_ram_v4342.lua','tools/run_tomb_mirror_audio_ram_v4343.py',
      'tools/verify_tomb_mirror_contract_v4344.py','tools/run_tomb_mirror_audio_ram_v4347.py',
      'tools/run_tomb_mirror_audio_ram_v4350.py','tools/run_remaining_tomb_mirrors_ram_v4353.py',
      'tools/verify_tomb_mirror_native_branches_v4357.py'):
        pin(ROOT/name)
    for folder in (ROOT/'audit_v4352_tomb_mirror_audio_ram_observed',ROOT/'audit_v4354_both_characters_both_slots_tomb_mirrors',
      ROOT/'audit_v4358_true_mirror_native_tomb_branches',ROOT/'audit_v4348_tomb_mirror_audio_ram_observed'):
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
    need(not (ROOT/'audit_v4346_tomb_mirror_audio_ram_observed').exists(),'Initial unimportable4343 source retained, no invented runtime result')
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { @("
    query+=','.join(map(str,native_pids))+ ") -contains $_.ProcessId -or $_.CommandLine -match 'run_tomb_mirror_audio_ram_v4347.py|run_tomb_mirror_audio_ram_v4350.py|run_remaining_tomb_mirrors_ram_v4353.py|verify_tomb_mirror_native_branches_v4357.py' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    observed=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(observed.returncode==0 and not observed.stdout.strip(),'Actual native/collector/branch jobs terminal, not inferred from stale files')
    get=ctypes.windll.kernel32.GetCompressedFileSizeW;get.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];get.restype=ctypes.c_uint32
    files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
    allocated=0
    for p in files:
        high=ctypes.c_uint32();ctypes.set_last_error(0);low=get(str(p),ctypes.byref(high))
        need(low!=0xffffffff,'Actual measured native diagnostic allocation');allocated+=(high.value<<32)|low
    logical=sum(p.stat().st_size for p in files)
    next_action=('Actual3836 true17/17 and18/18 mirrors in both physical slots now have normal selected IDs, two earned '
      'full-health KOs in each of two native arenas, normal paid challenger, facing-specific Tomb parser/common gates, '
      '801complete cleanup fields and next-screen retirement. Eight actual samples-on/off pairs have every native audio '
      'update compared in RAM, actual DCS delivery, exact own winner clip/interpolation/onset/finite cleanup; 48actual '
      'full-contract faults and16actual branch faults rejected. All four observed native RNG outcomes are held, not drop. '
      'Do not claim mirror drop/control branches, full DCS waveform or raster/shadows from these audio/state captures. '
      'Next concrete work: current3836 continuous RAM-only mirror CPU/DMA/FIFO/scanout model, source-owned palette/body/'
      'grounding/native floor-shadow/erase through retirement. Inspect3642model and3648fullscene gates first: oldmodel '
      'requires set(ids)=={17,18}; mirrors need explicitly owned17/17 or18/18 slots, not palette-bank inference or proxy. '
      'Use newly frozen4351same-role physical logs as references, preserve entire earned1731/scene/FIFO/native shadow/'
      'pixel fault gates, reconstruct3836whole guest and refuse raw disk sinks. Then natural mirror drop/button variants, '
      'broader Pit/victims and complete stage/victim native audio remain open. Retain all five full-goal groups, original '
      'campaign4300baseline/4309 not rejected4320backward variant, strict CPU/Main-reuse/throw coverage gaps, other finishers/'
      'morphs/secrets/cinematics, true full boss clears/own endings/attract, combined UI/names/audio regression/cleanup/'
      'refreshed release. Public1836 remains unchanged playtest, not a final release.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='Every original requirement/exclusion and inherited logical evidence byte retained; bounded mirror evidence added.'),
      priorRecordedProgressClassification=state['thisGoalTurnClassification'],
      previousGoalTurnClassification='no progress: acknowledgment only; current parent/worktree/live processes revalidated before fresh native mirror tests.',
      thisGoalTurnClassification='progress: genuine unassisted3836 Kano/Kano and Sonya/Sonya Tomb mirrors in both physical slots independently passed full earned/action/retirement and RAM-only paired winner/audio/DCS-delivery checks. Actual held RNG branches/physics source-qualified; missing drop and raster/audio scope explicitly retained.',
      current3836TrueMirrorTombMatrixReport=str(matrixpath),current3836TrueMirrorTombBranchReport=str(branchpath),
      current3836TrueMirrorTombEarnedStateCleanupDCSDeliveryWinnerMixAccepted=True,
      current3836TrueMirrorTombRasterFloorShadowEraseAccepted=False,current3836TrueMirrorTombFullStageVictimAudioAccepted=False,
      current3836TrueMirrorTombHeldContexts=4,current3836TrueMirrorTombDropContexts=0,
      currentTombMirrorNativePIDs=native_pids,currentTombMirrorExecHandles=dict(initialPair=89298,correctedPair=39702,remainingMatrix=98240,branches=46418),
      currentTombMirrorOriginalParseFailureSource=str(ROOT/'tools/run_tomb_mirror_audio_ram_v4343.py'),
      currentTombMirrorOriginalExitTimingFailureReport=str(failed),
      currentTombMirrorExitTimingCorrection='Originaldriver exit requested at age1100; actual deferred native stop at age1101. Fresh4350 source/capture leaves, all801original action fields and1100channel callbacks retained. Original4347 failure never edited/promoted.',
      currentTurnNativeDiagnosticLogicalBytes=logical,currentTurnNativeDiagnosticAllocatedBytes=allocated,
      currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,
      currentTurnReclaimedAllocatedBytes=0,
      cleanupAccounting='No new deletions or storage-reclamation claims this turn; prior1582383104B and3392749568B savings not counted again. Only compressed text/source snapshots created, every native PCM/guest remains RAM-only.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Every original five-group requirement unchanged')
    need(all(sha(path)==h for path,h in pins.items()),'All inherited/new actual byte pins remain exact')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before write')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),mirrorContexts=4,
      heldBranches=4,dropBranches=0,diagnosticLogicalBytes=logical,diagnosticAllocatedBytes=allocated,
      rawNativeMediaCopies=0,originalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
