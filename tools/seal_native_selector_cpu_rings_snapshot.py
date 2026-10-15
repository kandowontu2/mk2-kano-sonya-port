"""Bind current three-Ring native display, actual views and full source sound.

Finite rendering/audio acceptance only. Keep the actual rejected mechanics
check and explicitly missing Block/entry observations. Never invent those
records or claim all arena/CPU/priority/cleanup/finished-port acceptance.
"""
import hashlib
import json
from pathlib import Path
import qualify_native_selector_cpu_rings_snapshot as renderer
import qualify_native_selector_cpu_rings_snapshot_audio as audio
import qualify_native_selector_cpu_rings_snapshot_transport as transport
import qualify_native_selector_cpu_rings_snapshot_mechanics as mechanics
import verify_native_source_sync as source_sync

ROOT,need,sha=renderer.ROOT,renderer.need,renderer.sha
capture=renderer.capture
OUT=ROOT/'audit_native_selector_cpu_rings_snapshot_sealed'


def execute(state):
    need(not OUT.exists(),'Fresh complete finite Ring display/audio seal')
    paths=[m.OUT/'report.json'for m in (transport,renderer,audio)]
    reports=[json.loads(p.read_text())for p in paths]
    t,r,a=reports;held=capture.NATIVE_HANDLES[capture.KEY]
    need(all(v['passed']and v['actualNativeIdentity']==held['identity']for v in reports)and
         held['process'].poll()==t['nativeExit']==r['nativeExit']==0,
         'Same original terminal0 native PID/birth/path/cmd, not substituted captures')
    need(not capture.transport.previous.original.previous.choices.current.prior.identity.census(),
         'Fresh exact native census empty; retained original Popen terminal')
    pins={}
    for proof in reports:
        need(len(proof['requirements'])==14 and len(proof['remainingGroups'])==6 and
             proof['requirements']==r['requirements']and proof['remainingGroups']==r['remainingGroups'],
             'All original fourteen requirements and six groups retained unchanged')
        for path,h in proof['inputHashes'].items():
            need(path not in pins or pins[path]==h,'No conflicting complete source/evidence pin')
            pins[path]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every whole input pin freshly rehashed')
    need(t['completeOriginalSourceSamplingAccepted']and t['originalCardinalityFailurePreserved']and
         t['actualRGBFrames']==r['actualRGBFrames']==319 and
         r['exactWholeDisplayedPixels']==32410400 and r['exactWholeVRAMWords']==83623936 and
         len(r['effectiveOwnershipAndRenderFaultsRejected'])==24,
         'Complete source-scheduled319 current passes and all effective owner/pixel faults')
    inspected=[]
    for window,case in enumerate(r['cases'],1):
        display=capture.DISPLAY[window];renderer.ram.verify_transport(display)
        need(case['window']==window and case['actualRGBFrames']==(106,106,107)[window-1]and
             len(case['independentActualPoses'])==(10,9,10)[window-1]and
             case['actualSourceFIFOAndDMA']['sourceCompositeAndDMAExact']and
             all(v['vram_mismatches']==v['displayed_mismatches']==v['shadow_mismatches']==0
                 for v in case['wholeSavedNativePasses']['records']),
             'Complete independent Ring poses/FIFO/source/DMA/VRAM/RGB/shadow checks')
        views_path=ROOT/f'audit_native_selector_cpu_ring_{window}_snapshot_actual_views.json'
        views=json.loads(views_path.read_text())
        expected=[(1818,1833,1841,1864,1872,1917),(2176,2191,2199,2222,2230,2275),
                  (3028,3043,3051,3074,3082,3127)][window-1]
        callbacks=views['actualViewedCallbacks']
        need(views['passed']and views['actualNativeIdentity']==held['identity']and
             views['identityRevalidatedBeforeAndAfter']and
             [int(v['header']['frame'])for v in callbacks]==list(expected),
             'Six actually viewed native current frames in each complete lifetime')
        for v in callbacks:
            h=v['header'];raw=display['rgb'][h['file']]
            need(h==display['rgbHeaders'][h['file']]and h['window']==str(window)and
                 hashlib.sha256(raw.tobytes()).hexdigest().upper()==v['nativeRGBSHA256'],
                 'Every actually viewed whole RGB buffer digest/phase/window unchanged')
        pins[str(views_path.resolve())]=sha(views_path)
        inspected.append(dict(window=window,actualViewedFrames=list(expected),receiptSHA256=sha(views_path)))
    wave=a['wholeMixedWaveform']
    need(a['completePCMCallbacks']==1646 and a['completeStereoFrames']==1580160 and
         wave['passed']and wave['differentChannelSamples']==0 and wave['comparedStereoFrames']==1580160 and
         wave['actualSHA256']==wave['predictedSHA256']and
         a['wholeStartupAudio']['cue']['actualRingVoiceCalls']==3 and a['nativeDAC']['passed']and
         all(v['everyActualByteComparedInRAM']and v['wholeOriginalSoundRegionSourceExact']
             for v in a['wholeSoundROM'])and
         sum(len(v)for v in (a['nativeDACFaultsRejected'],a['soundROMFaultsRejected'],
             a['actualStartupSourceFaultsRejected'],wave['actualRawMixedPCMFaultsRejected'],
             wave['actualMixedSourceOperationFaultsRejected']))==30,
         'Complete source-exact native PCM/DAC/sound ROM/voice/DCS/clock model and thirty faults')
    failure_path=mechanics.OUT/'failure.json';failed=json.loads(failure_path.read_text())
    need(not failed['passed']and failed['error']=='AssertionError()',
         'Preserve actual original missing native mechanics observer rejection')
    _,text,_=capture.RAM_CASES[capture.KEY]
    need(all(not mechanics.ring.original.rows(text,tag)for tag in ('GUARD','TESTED','BLOCK')),
         'Missing original block observations explicit; damage amount does not prove native branch')
    for p in (*paths,failure_path,Path(__file__),Path(mechanics.__file__),
              ROOT/'tools/read_native_selector_cpu_rings_snapshot_frames.py',
              ROOT/'tools/read_native_selector_cpu_rings_snapshot_frames_remote.py'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Executed sources and receipts immutable');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All complete sources/native/results/views at final seal')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        originalTransportReportSHA256=sha(paths[0]),wholeRendererReportSHA256=sha(paths[1]),
        wholeAudioReportSHA256=sha(paths[2]),actualRGBFrames=319,actualViewedFrames=18,
        exactWholeDisplayedPixels=32410400,exactWholeVRAMWords=83623936,
        completePCMCallbacks=1646,completeStereoFrames=1580160,differentChannelSamples=0,
        effectiveOwnershipAndRenderFaults=24,effectiveSourceAudioFaults=30,actualViews=inspected,
        inputHashes=pins,requirements=r['requirements'],remainingGroups=r['remainingGroups'],
        finiteThreeCPURingSavedDisplayAndWholeRecordedAudioAccepted=True,
        actualVisualReviewAccepted=True,fullRecordedSourceAudioAccepted=True,
        failedMechanicsReportSHA256=sha(failure_path),completeNativeHitBlockMechanicsAccepted=False,
        missingNativeBlockBranchObservations=True,heardAudioQualityAccepted=False,
        interPassEraseAccepted=False,allArenaCPUContextsAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS sealed319 current Ring displays/18 actual views/full1580160 stereo frames; mechanics gap retained',flush=True)
    return result
