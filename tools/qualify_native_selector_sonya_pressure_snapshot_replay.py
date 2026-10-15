"""Full original CPU/DMA source renderer on retained actual pressure passes.

Every source-scheduled flip with its genuine BEFORE-DMA anchor is checked.
Held snapshots retain the separate complete scanout proof. Never claim
inter-pass erasure, unobserved terminal3618 or effect-specific ownership.
"""
import json
import traceback
from pathlib import Path
import capture_native_selector_sonya_pressure_snapshot as capture
import qualify_native_selector_sonya_pressure_snapshot_binding as binding
import qualify_native_selector_walkin_knife_display_ram as original
import qualify_native_selector_walkin_knife_display_face_rows as names
import qualify_native_selector_walkin_knife_vram as ram

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_snapshot_replay_checked'


def execute(state):
    need(not OUT.exists(),'Fresh full original pressure native pass replay')
    parent_path=binding.OUT/'report.json';parent=json.loads(parent_path.read_text())
    held=capture.NATIVE_HANDLES[capture.KEY];folder,text,_=capture.RAM_CASES[capture.KEY]
    need(parent['passed']and held['process'].poll()==parent['nativeExit']==0 and
         held['identity']==parent['actualNativeIdentity']and held['identity']['ProcessId']==47004,
         'Exact retained terminal native game, no replay of gameplay')
    pins=dict(parent['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Whole source/capture/scanout inventory unchanged')
    display=capture.DISPLAY;image=names.runtime_graphics(state,pins)
    ram.verify_transport(display);ram.graphics(display,image)
    groups,*_=original.data(text,display)
    expected=sorted(r['snapshot']for r in groups['FLOOR_LATCH'])
    need(len(set(expected))==len(expected)and all(r['snapshot']==r['flip_frame']==r['frame']for r in groups['FLOOR_LATCH']),
         'Every genuine current flip callback has one original full independent pass')
    render=original.bindings(text,display)
    result=render(folder)
    need([r['frame']for r in result['records']]==expected and
         all(r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in result['records']),
         'Every complete independently decoded native CPU/DMA pass and all512x512 words exact')
    need(len(expected)+parent['heldSnapshotCount']==parent['completeCurrentSnapshots'],
         'All consecutive source-scheduled images accounted: actual flips plus separately proved held scanouts')
    for p in (Path(__file__),Path(original.__file__),Path(original.original.__file__),Path(original.scaling.__file__),
              ROOT/'tools/inspect_natural_arena_floor_v602.py',ROOT/'tools/verify_native_floor_display_v602.py',parent_path):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed renderer/source/evidence edits');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Whole source/native inventory intact after full independent pass replay')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        completeActualPassReplay=result,wholeExactPassVRAMWords=len(expected)*512*512,
        wholeCurrentSnapshots=parent['completeCurrentSnapshots'],heldScanoutsIndependentlyBound=parent['heldSnapshotCount'],
        actualNativeCommands=len(groups['FLOOR_DMA']),actualCPUVRAMWrites=len(groups['FLOOR_CPU']),
        allCurrentSourceScheduledImagesAccounted=True,sourceExactSavedPassCPUAndDMAReplayAccepted=True,
        rendererFaultSuiteAccepted=False,interPassErasureAccepted=False,corpseEffectOwnershipAccepted=False,
        terminal3618FrameDoneObserved=False,fullPortAcceptance=False,publicPlayableChanged=False,
        inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS whole actual pressure CPU/DMA/packed graphics/native flip passes',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual full pressure native renderer rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
