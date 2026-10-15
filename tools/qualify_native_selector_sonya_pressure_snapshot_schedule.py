"""Original native stop-before-frame_done contract, all actual images retained.

Keep the real1801-count failure. No new run, trim, fabricated image or altered
controller. The original controller exits at first_live+1800 in register_frame;
its terminal3618 has no frame_done display observation. Whole goal stays open.
"""
import hashlib
import json
from pathlib import Path
import capture_native_selector_sonya_pressure_snapshot as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_snapshot_schedule_checked'
FRAMES=list(range(1818,3618))


def execute(state):
    need(not OUT.exists(),'Fresh whole source-defined pressure callback schedule evidence')
    failure=capture.OUT/'failure.json';failed=json.loads(failure.read_text())
    need(not failed['passed']and failed['error']==
         "ValueError('Every dense live/nonlive callback and all source-scheduled VRAM/palette/prepass buffers; no guessed count')",
         'Actual original terminal-cardinality failure remains immutable')
    folder,text,_=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta_path=folder/'result.json';meta=json.loads(meta_path.read_text())
    parent=json.loads(capture.PARENT.read_text())
    need(meta['passed']and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (47004,38752,1791773031.802763)and not meta['nativeTerminal']['hostDecodeErrors']and
         not capture.reference.base.choices.current.prior.identity.census(),
         'Same original47004 genuinely terminal0; full native transport passed')
    pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every original complete source/native pin intact')
    rows=capture.reference.base.choices.native_state.rows
    driver=ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua'
    code=driver.read_text()
    need('emu.register_frame(function()\n    frame=frame+1\n    if first_live and frame>=first_live+1800 then manager.machine:exit();return end'in code,
         'Whole original controller exits in the frame callback, before terminal frame_done')
    need(capture.LUA.read_text().startswith("-- Same single pressure controller; complete passive live/nonlive display data.\ndofile('mk2ks_native_selector_sonya_cpu_pressure_bound.lua')"),
         'Unchanged original controller loaded before the additional observer callbacks')
    select=rows(text,'MK2_P2CPU_SELECT_RESULT');begin=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_BEGIN')
    result=rows(text,'MK2_CPU_PAIR_RESULT');end=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_RESULT')
    need(len(select)==len(begin)==len(result)==len(end)==1 and select[0]['live']=='1818'and begin[0]['origin']=='1817',
         'Actual original live admission and first Ring observation independently present')
    stop=int(select[0]['live'])+1800
    expected=list(range(int(begin[0]['origin'])+1,stop))
    need(expected==FRAMES and result[0]['frame']==end[0]['frame']==str(stop)and end[0]['snapshots']==str(len(expected)),
         'Every actual source-scheduled callback before genuine native exit, not a target-fitted cardinality')
    display=capture.DISPLAY
    need([int(h['frame'])for h in display['rgbHeaders'].values()]==expected and
         [int(r['frame'])for r in rows(text,'MK2_NAT_CAMPAIGN_FLOOR_SNAP')]==expected and
         [int(r['frame'])for r in rows(text,'MK2_NAT_CAMPAIGN_FLOOR_STATE')]==list(range(1817,stop)),
         'All source-scheduled current images and actual live/nonlive frame_done fields; terminal no image invented')
    dma_frames=sorted({int(r['frame'])for r in rows(text,'MK2_NAT_CAMPAIGN_FLOOR_DMA')if 1817<=int(r['frame'])<stop})
    need([int(r['frame'])for r in rows(text,'MK2_NAT_CAMPAIGN_FLOOR_PRE_FRAME')]==dma_frames,
         'Every actual first DMA anchor before a requested callback retained, even final unused prepass')
    buffers={'guest_maincpu.bin','display_base.bin'}
    buffers.update('display_pre_%d.bin'%f for f in dma_frames)
    buffers.update('display_%s_%d.bin'%(kind,f)for f in expected for kind in ('vram','palette'))
    need(set(display['buffers'])==buffers and display['gfx'],'Every original source-scheduled buffer, no discarded extra anchors')
    tags=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
          'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_STARTUP_PROJECTILE_',
          'MK2_SONYA_HORIZONTAL_','MK2_MAUDIO_','MK2_TOMB_MIX_',
          'MK2_BBAUDIO_PCM_DIGEST ','MK2_NATIVE_DAC_RAM_DIGEST ','MK2_HPHASE_')
    old=capture.reference.RAM_CASES[capture.reference.KEY][1]
    need([l for l in text.splitlines()if l.startswith(tags)]==[l for l in old.splitlines()if l.startswith(tags)],
         'Whole original44780 actual gameplay/inputs/state/HP/choices/body-shadow/PCM/DAC history unchanged')
    for p in (Path(__file__),Path(capture.__file__),capture.LUA,failure,meta_path,driver,capture.PARENT):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Executed original source/evidence remains unchanged');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every whole pin after exact actual callback schedule')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        originalCardinalityFailurePreserved=True,sourceScheduledFrames=expected,
        originalControllerExitFrame=stop,terminalFrameDoneObserved=False,
        wholeCurrentSnapshotCallbacks=len(display['rgb']),volatileBuffers=len(display['buffers']),
        volatileStoredBytes=sum(len(v)for v in display['buffers'].blocks.values()),actualGFXStreams=len(display['gfx']),
        displayBufferHeaders=display['headers'],rgbHeaders=display['rgbHeaders'],wholeOriginalTrajectoryUnchanged=True,
        independentRendererAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS all1800 real source-scheduled pressure snapshots; terminal3618 unobserved, original failure retained',flush=True)
    return value
