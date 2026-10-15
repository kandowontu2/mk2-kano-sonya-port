"""Preserve full goal scope and actual pressed mirror drop progress/failures."""
import ctypes,hashlib,json,subprocess
from pathlib import Path
import run_pressed_mirror_render_ram_v4401 as render
import run_pressed_tomb_mirror_audio_ram_v4395 as audio
ROOT,need,sha=audio.ROOT,audio.need,audio.sha
PARENT=ROOT/'audit_v4371_tomb_mirror_render_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4405_pressed_mirror_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable complete-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited original goal/source/evidence/playable byte unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();h=sha(p);key=str(p)
        need(key not in pins or pins[key]==h,'Inherited/shared exact byte identity')
        need(wanted is None or wanted==h,'Exact report/input manifest identity');pins[key]=h
    pin(PARENT);pin(__file__)
    matrixpath=ROOT/'audit_v4393_both_characters_both_slots_pressed_mirror_drop_checked/report.json'
    matrix=json.loads(matrixpath.read_text());pin(matrixpath)
    need(matrix['passed'] and matrix['actualNativeBothDownMirrorDropContexts']==4 and
      matrix['actualPairedCaptures']==8 and matrix['actualWriterAndInputFaultsRejected']==40 and
      matrix['current3836BothCharactersBothSlotsNativePressedMirrorTombDropPhaseCleanupLateVictimRouteDCSDeliveryWinnerMixAccepted'] and
      matrix['successfullyQualifiedP1PCMContextsReusedNotRerun'] and not matrix['fullPortAcceptance'],
      'Actual four native pressed mirror contexts, not unpressed RNG/render/full-waveform acceptance')
    for p,h in matrix['inputHashes'].items():pin(p,h)
    guest=audio.runtime.old.expected();contexts=[];folders=[];pids=[]
    for case in matrix['cases']:
        need(len(case['actualFaultsRejected'])==12 and len(case['actualNativePhaseFaultsRejected'])==4 and
          len(case['actualSourceWriterInputFaultsRejected'])==10 and len(case['actualVoiceFaultsRejected'])==8,
          'All original earned and actual phase/writer/input/voice fault checks retained')
        drops=[];voices=[]
        for name in (case['capture'],case['baseline']):
            folder=ROOT/name;folders.append(folder);meta=json.loads((folder/'result.json').read_text())
            process=json.loads((folder/'process.json').read_text());pids.append(process['pid'])
            need(meta['exit_code']==0 and meta['guest_writes']==0 and meta['assistance']=='none' and
              meta['guestSHA256']==hashlib.sha256(guest).hexdigest().upper() and
              meta['rawAudioRasterVRAMROMCopiesWritten']==0,'Actual unassisted terminal whole3836 guest and RAM audio')
            log=(folder/'run.log').read_text()
            drops.append(audio.state.qualify_pressed_drop(log,case['fighter'],case['side'],1,'positive',guest))
            scream=next(r for r in audio.runtime.old.rows(log,'ROUTE') if r['entry']=='FFA11FD0')
            voices.append(audio.voice.qualify_scream(log,case['fighter'],case['side'],guest,scream))
            need(audio.state.check_log(log,case['fighter'],case['side'],1,guest=guest)['passed'],
              'Both original full earned/native branch/801callback cleanup contracts')
            for p in folder.rglob('*'):
                if p.is_file():pin(p)
            need(not list(folder.rglob('*.wav')) and not list(folder.rglob('*.png')) and not list(folder.rglob('*.bin')),
              'No persisted native PCM/raster/guest copies')
        need(drops[0]==drops[1] and voices[0]==voices[1] and case['nativePressedBranch']==drops[0] and
          case['nativeRoleVoice']==voices[0],'Actual identical on/off native source/role/input/writer/phase routes')
        contexts.append(dict(fighter=case['fighter'],side=case['side'],victim=case['victim'],
          capture=case['capture'],baseline=case['baseline'],nativeDrop=drops[0],nativeVoice=voices[0],
          everyNativeMixedPCMUpdateComparedInRAM=case['everyNativeMixedPCMUpdateComparedInRAM'],
          nativeDCSDeliveredBytes=len(case['nativeDCSDeliveredBytes']),originalWinnerMix=case['originalWinnerMix'],
          fullPortAcceptance=False))
    need({(c['fighter'],c['side'],c['victim']) for c in contexts}==
      {('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18)},'All four actual true mirror physical roles')
    failurepaths=[ROOT/'audit_v4377_pressed_kano_p1_tomb_mirror_audio_checked/report.json',
      ROOT/'audit_v4386_both_characters_both_slots_pressed_tomb_mirror_audio/report.json',
      ROOT/'audit_v4391_pressed_kano_p2_tomb_mirror_audio_checked/report.json']
    failures=[]
    for path in failurepaths:
        report=json.loads(path.read_text());need(not report['passed'],'Every original failed attempt preserved')
        pin(path);failures.append(dict(report=str(path),error=report['error']))
    # Preserve original terminal failed capture/source bytes as evidence too.
    for name in ('audit_v4378_pressed_tomb_mirror_kano_p1_samples',
      'audit_v4383_pressed_tomb_mirror_kano_p2_samples','audit_v4383_pressed_tomb_mirror_kano_p2_nosamples',
      'audit_v4390_pressed_tomb_mirror_kano_p2_samples','audit_v4390_pressed_tomb_mirror_kano_p2_nosamples'):
        folder=ROOT/name;need(folder.is_dir(),'Original failed attempt capture retained');folders.append(folder)
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
    rasterpath=ROOT/'audit_v4403_kano_p1_pressed_mirror_tomb_render_checked/report.json'
    raster=json.loads(rasterpath.read_text());pin(rasterpath)
    rasterfolder=ROOT/'audit_v4402_kano_p1_pressed_mirror_tomb_render_ram';folders.append(rasterfolder)
    meta=json.loads((rasterfolder/'result.json').read_text());process=json.loads((rasterfolder/'process.json').read_text())
    pids.append(process['pid']);need(meta['exit_code']==0 and meta['captureCompleted'],'Actual render capture terminal')
    for p in rasterfolder.rglob('*'):
        if p.is_file():pin(p)
    visualmatrixpath=ROOT/'audit_v4409_both_characters_both_slots_pressed_mirror_tomb_render/report.json'
    visualcases=[];allvisual=False
    if raster['passed']:
        for p,h in raster['inputHashes'].items():pin(p,h)
        need(raster['current3836KanoP1PressedMirrorNativeTombWholeRenderPaletteShadowEraseAccepted'] and
          raster['nativeScene']['nativeDrop'] and raster['nativeScene']['actualNativeRandomValue'] is None and
          raster['oneInitialBaseOnly'] and raster['laterTargetsNeverUsedAsAnchors'] and
          raster['nativeMirrorPaletteSelectors']=={'1':[False],'2':[True]} and
          len(raster['actualPixelFaultsRejected'])==2 and not raster['fullPortAcceptance'],
          'Complete actual pressed KanoP1 one-base native render, shadows/erase and original pixel faults')
        visualmatrix=json.loads(visualmatrixpath.read_text());pin(visualmatrixpath)
        need(visualmatrix['passed'] and visualmatrix['priorKanoP1NotRerun'] and
          visualmatrix['actualTrueMirrorRenderContexts']==4 and
          visualmatrix['current3836BothCharactersBothPhysicalSlotsPressedMirrorTombWholeRenderPaletteShadowEraseAccepted'] and
          visualmatrix['mirrorDropAndPressedControlBranchesAccepted'] and not visualmatrix['allMirrorBranchesAccepted'] and
          not visualmatrix['allStageVictimAudioAccepted'] and not visualmatrix['fullPortAcceptance'],
          'All four actual pressed renders, no unpressed RNG/native whole-waveform/full-port promotion')
        for p,h in visualmatrix['inputHashes'].items():pin(p,h)
        for case in visualmatrix['cases']:
            path=Path(case['report']);proof=json.loads(path.read_text());pin(path)
            need(proof['passed'] and proof['sampledFrames']>500 and proof['nativeScene']['nativeDrop'] and
              proof['nativeScene']['actualNativeRandomValue'] is None and proof['nativeScene']['nativeInputState']['consecutive_fields']==801 and
              proof['nativeScene']['nativeShadowCopies']>0 and proof['nativeMirrorPaletteSelectors']=={'1':[False],'2':[True]} and
              proof['oneInitialBaseOnly'] and proof['laterTargetsNeverUsedAsAnchors'] and
              len(proof['actualPixelFaultsRejected'])==2 and proof['nativeShiftLoads']==proof['nativeShiftFills']>0 and
              proof['nativeShiftTransfers']>60000 and proof['fullPhysicalPaletteChecks']>proof['sampledFrames'],
              'Each actual full801cleanup, continuous native model, owned shadows/palettes/erase and pixel faults')
            for p,h in proof['inputHashes'].items():pin(p,h)
            folder=(rasterfolder if (proof['fighter'],proof['side'])==('kano',1) else
              ROOT/f"audit_v4407_{proof['fighter']}_p{proof['side']}_pressed_mirror_tomb_render_ram")
            if folder!=rasterfolder:folders.append(folder)
            meta=json.loads((folder/'result.json').read_text());process=json.loads((folder/'process.json').read_text())
            pids.append(process['pid'])
            need(meta['exit_code']==0 and not meta['modelErrors'] and meta['modelExactFields']==proof['sampledFrames'] and
              meta['observedRGBFields']==proof['sampledFrames'] and meta['rawImageAudioVRAMROMCopiesWritten']==0 and
              meta['guest_writes']==0 and meta['assistance']=='none','Actual terminal native render without assistance/raw media')
            visualcases.append(dict(fighter=proof['fighter'],side=proof['side'],report=str(path),
              sampledFrames=proof['sampledFrames'],exactRGBPixels=proof['exactRGBPixels'],
              nativeShadowCopies=proof['nativeScene']['nativeShadowCopies'],fullPortAcceptance=False))
        need({(c['fighter'],c['side']) for c in visualcases}=={('kano',1),('kano',2),('sonya',1),('sonya',2)},
          'All four actually observed physical pressed mirror renders')
        allvisual=True
    for name in ('mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua','mk2ks_tomb_mirror_pressed_provenance_ram_v4373.lua',
      'mk2ks_tomb_mirror_pressed_audio_ram_v4374.lua','mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua',
      'mk2ks_tomb_mirror_pressed_audio_ram_v4380.lua','tools/verify_pressed_tomb_mirror_contract_v4375.py',
      'tools/run_pressed_tomb_mirror_audio_ram_v4376.py','tools/run_pressed_tomb_mirror_audio_ram_v4381.py',
      'tools/run_remaining_pressed_tomb_mirror_audio_ram_v4385.py','tools/verify_pressed_tomb_mirror_contract_v4387.py',
      'tools/run_pressed_tomb_mirror_audio_ram_v4388.py','tools/finish_pressed_tomb_mirror_matrix_v4392.py',
      'tools/verify_native_tomb_scream_roles_v4394.py','tools/run_pressed_tomb_mirror_audio_ram_v4395.py',
      'mk2ks_pressed_mirror_display_ram_v4400.lua','tools/run_pressed_mirror_render_ram_v4401.py',
      'tools/run_remaining_pressed_mirror_render_ram_v4406.py'):
        pin(ROOT/name)
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_pressed_tomb_mirror_audio_ram_v4395.py|finish_pressed_tomb_mirror_matrix_v4392.py|run_pressed_mirror_render_ram_v4401.py|run_remaining_pressed_mirror_render_ram_v4406.py|audit_v4396_|audit_v4402_|audit_v4407_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    observed=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(observed.returncode==0 and not observed.stdout.strip(),'Actual jobs terminal, never restart from observation timeout')
    get=ctypes.windll.kernel32.GetCompressedFileSizeW
    get.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];get.restype=ctypes.c_uint32
    files={p for folder in folders for p in folder.rglob('*') if p.is_file()};allocated=0
    for p in files:
        high=ctypes.c_uint32();low=get(str(p),ctypes.byref(high));need(low!=0xffffffff,'Exact diagnostic allocated bytes')
        allocated+=(high.value<<32)|low
    next_action=('All four current3836 true mirrors now pass source/IO/native ceiling-writer-qualified physical both-Down Tomb '
      'drop, original earned1731/269motion/801cleanup gates, owned gender/Main-role late victim route, DCS byte delivery '
      'and whole imported winner PCM/finite cleanup. P1 accepted PCM pairs reused, not rerun. Preserve all three original '
      'failed attempts: wrapper literal guard, fixed P1 ceiling arrival assumed for P2, and fixed P2-victim male scream range. '
      'Original Main+20 role code and actual A2/A1 prove P1 victim32/33 versus P2 victim34/35; Sonya18 genuine female38/39. '
      'No game/public build bytes changed. Actual pressed KanoP1 whole render outcome is recorded separately; if failed, '
      'inspect its actual model error before any repair and retain source/capture/report. If passed, extend unchanged '
      'complete continuous CPU/FIFO/DMA/shift/one-base/VRAM/RGB/palette/native floor-shadow/erase/retirement model to '
      'remaining pressed SonyaP1/KanoP2/SonyaP2 contexts using frozen4393same-role physical references, without rerunning '
      'completed contexts. Native unpressed RNG drops, broader Pit/Tomb combinations and whole native DCS victim/effect '
      'waveforms remain unproved. All original full move-phase art/ground/shadows/cleanup across arenas/CPU/repeated/KO/'
      'overlap, other finishers/victims/morphs/secrets/cinematics, true natural Kintaro/Shao clears/own endings/attract, '
      'final combined selection/ladder/names/audio/dependency cleanup/refreshed release remain requirements. '
      'Keep4300preferred SonyaP2 campaign, reject4320backward policy; strict CPU/Main reuse/throw gaps unchanged. '
      'Public1836 remains unchanged playtest, not a finished release.')
    if allvisual:
        next_action=('All four actual current3836 pressed Kano/Kano and Sonya/Sonya mirror renders now passed whole continuous '
          'CPU/FIFO/DMA/shift/one-base/VRAM/RGB/normalP1-alternateP2 palette/source-owned native floor-shadow/erase/retirement '
          'checks with original801cleanup gates and eight actual pixel faults. All4 native source/IO/ceiling-writer-qualified '
          'drop phases, owned role/gender late voice, real DCS byte delivery and whole imported winner PCM checks passed too. '
          'No completed pressed or held scenes should be rerun. Next missing native branch is unpressed RNG mirror drop: '
          'observe only legitimate physical command timing variation and actual50/1000 compare; never force RNG, position, '
          'identity, health, flags or inputs beyond genuine controls. Preserve original3643unpressed qualification distinct '
          'from pressed4387. Broaden original Pit/Tomb victim combinations and whole native stage/victim DCS waveform '
          'fidelity. All original five full-goal groups, campaign clears, strict CPU/Main reuse/throw gaps and final '
          'release/dependency cleanup remain unproved and required. Public1836 remains unchanged playtest, not final.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='All original full-goal requirement groups and inherited evidence retained; actual pressed mirror progress/failures added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: all four actual source/IO/writer-qualified pressed mirror drops and complete paired winner PCM/native victim routing/DCS delivery/cleanup proven; actual role assumption repaired from native code, strict faults retained; pressed raster outcome recorded separately.',
      current3836PressedMirrorTombMatrix=str(matrixpath),current3836PressedMirrorTombCases=contexts,
      current3836BothCharactersBothSlotsPressedMirrorTombNativePhaseVoiceDeliveryWinnerMixAccepted=True,
      current3836PressedMirrorTombOriginalFailedAttempts=failures,
      current3836KanoP1PressedMirrorRenderReport=str(rasterpath),current3836KanoP1PressedMirrorWholeRenderAccepted=raster['passed'],
      current3836AllPressedMirrorRendersAccepted=allvisual,current3836PressedMirrorRenderMatrix=(str(visualmatrixpath) if allvisual else None),
      current3836PressedMirrorRenderCases=visualcases,current3836UnpressedRandomMirrorDropsAccepted=False,
      nativeUnpressedProbeTimingDiscovery=dict(controller='mk2ks_current_stage_ram_driver_v3594.lua',
        originalThreshold='if not command and frame-window>=65 then',
        originalContract='tools/native_stage_variant_checks_v1731.py',
        originalGate='begin >= number(windows[-1], \'frame\') + 65',
        possibleNextOrdinaryInputOnlyVariation='Delay the original command start within the genuine finish window; keep original facing/button/range/health/selection/state/cleanup gates and observe actual RNG only.',
        actualNewUnpressedRandomDropExercised=False),
      current3836TrueMirrorTombAllDropAndPressedBranchesAccepted=False,current3836TrueMirrorTombFullStageVictimAudioAccepted=False,
      currentPressedMirrorNativePIDs=pids,currentPressedMirrorExecHandles=dict(kanoP2=5074,matrix=19605),
      retainedPressedBranchDiagnosticLogicalBytes=sum(p.stat().st_size for p in files),retainedPressedBranchDiagnosticAllocatedBytes=allocated,
      currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnReclaimedAllocatedBytes=0,
      cleanupAccounting='Compressed text/digest/source reports only; no native media/ROM copies, no deletion, no repeated prior savings.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All five original full-goal groups intact')
    need(all(sha(p)==h for p,h in pins.items()),'Every source/evidence/playable pinned byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),actualPressedMirrorContexts=4,
      actualKanoP1PressedRenderPassed=raster['passed'],originalRemainingGroups=5,fullPortAcceptance=False,
      diagnosticAllocatedBytes=allocated),indent=2),flush=True)

if __name__=='__main__':main()
