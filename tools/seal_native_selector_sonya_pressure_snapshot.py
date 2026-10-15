"""Exact small evidence compression; retain full scope and native handles."""
import hashlib
import json
import subprocess
from pathlib import Path
import capture_native_selector_sonya_pressure_snapshot as capture
import qualify_native_selector_sonya_pressure_snapshot_schedule as schedule
import qualify_native_selector_sonya_pressure_snapshot_binding as binding
import qualify_native_selector_sonya_pressure_snapshot_replay as replay
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_snapshot_storage_checked.json'


def execute(visual_notes=None):
    need(not OUT.exists(),'Fresh immutable original whole pressure snapshot storage receipt')
    parent_path=schedule.OUT/'report.json';parent=json.loads(parent_path.read_text())
    report_path=binding.OUT/'report.json'
    if not report_path.exists():report_path=binding.OUT/'failure.json'
    bound=json.loads(report_path.read_text())
    replay_path=replay.OUT/'report.json'
    if not replay_path.exists():replay_path=replay.OUT/'failure.json'
    model=json.loads(replay_path.read_text())
    held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(parent['passed']and held['process'].poll()==parent['nativeExit']==0 and
         held['identity']==parent['actualNativeIdentity']and held['identity']['ProcessId']==47004 and
         host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         not capture.reference.base.choices.current.prior.identity.census(),
         'Original47004 terminal handle and original38752 live host, no timeout replay')
    if visual_notes is not None:
        frames=visual_notes['selectedFrames']
        need(len(frames)==len({r['frame']for r in frames})==12,
             'Exactly twelve actually inspected distinct source-bound views, not every-frame art acceptance')
        for r in frames:
            file='display_%d.png'%r['frame']
            need(r['header']==capture.DISPLAY['rgbHeaders'][file]and
                 r['nativeRGBSHA256']==hashlib.sha256(capture.DISPLAY['rgb'][file].tobytes()).hexdigest().upper(),
                 'Each actual reviewed complete RGB buffer still matches its original whole native callback')
    pins=dict(model['inputHashes']if model['passed']else bound['inputHashes']if bound['passed']else parent['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'All original entire source/evidence pins intact')
    files=set()
    for subtree in (capture.BASE,capture.OUT,schedule.OUT,binding.OUT,replay.OUT):
        at=subtree.resolve();need(at.is_relative_to(ROOT.resolve())and at.is_dir(),'Exact new snapshot evidence subtree')
        files.update(p.resolve()for p in at.rglob('*')if p.is_file())
    for name in ('capture_native_selector_sonya_pressure_snapshot.py',
                 'qualify_native_selector_sonya_pressure_snapshot_schedule.py',
                 'qualify_native_selector_sonya_pressure_snapshot_binding.py',
                 'qualify_native_selector_sonya_pressure_snapshot_replay.py',
                 'read_native_selector_sonya_pressure_snapshot.py',
                 'read_native_selector_sonya_pressure_snapshot_remote.py',
                 'seal_native_selector_sonya_pressure_snapshot.py'):
        files.add((ROOT/'tools'/name).resolve())
    files.add(capture.LUA.resolve())
    need(all(p.suffix.lower()in ('.py','.lua','.json','.gz','.log','.cfg')for p in files),
         'Only actual new small source/audit/metadata files; no ROM/build/raw-media copies')
    for p in sorted(files):
        key=str(p);h=sha(p);need(key not in pins or pins[key]==h,'Never overwrite an executed source/evidence pin');pins[key]=h
    entries=[]
    for p in sorted(files):
        before=dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0 and sha(p)==before['sha256'],'Whole exact file unchanged through forced LZX')
        entries.append(dict(path=str(p),**before,storedAfter=storage.stored(p)))
    sync=storage.source.verify();need(sync['passed'],'All15 compiled canonical inputs source-synchronized')
    endpoints={str(p):sha(p)for p in storage.source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in storage.source.FIXED.items())and
         all(sha(p)==h for p,h in pins.items()),'Every complete pin and private/public endpoint unchanged')
    value=dict(passed=True,goalStatus='active',actualHostIdentity=host,actualNativeIdentity=held['identity'],nativeExit=0,
        captureReportSHA256=sha(parent_path),bindingReportSHA256=sha(report_path),
        wholeCurrentSnapshotsCaptured=parent['wholeCurrentSnapshotCallbacks'],
        completeCurrentScanoutBindingPassed=bool(bound['passed']),
        sourceExactSavedPassCPUAndDMAReplayPassed=bool(model['passed']),
        actualReplayRejection=model.get('error'),replayReportSHA256=sha(replay_path),
        actualReplayedPasses=model.get('completeActualPassReplay',{}).get('frames'),
        wholeExactPassVRAMWords=model.get('wholeExactPassVRAMWords'),
        exactCurrentDisplayedPixels=bound.get('exactCurrentDisplayedPixels'),
        actualBindingRejection=bound.get('error'),effectiveFaultsRejected=len(bound.get('effectiveFaultsRejected',[])),
        limitedActualVisualInspection=visual_notes,files=entries,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,wholeSourceSyncPassed=True,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        newNativeGames=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,deletions=0,
        unsavedInterPassErasureAccepted=False,rendererFaultSuiteAccepted=False,
        allCorpseEffectsOwnershipAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n');h=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==h,'Whole snapshot source/storage receipt intact after LZX')
    return value
