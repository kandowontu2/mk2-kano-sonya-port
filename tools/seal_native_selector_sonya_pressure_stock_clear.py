"""Seal finite actual renderer/hide evidence and compress exact small files."""
import hashlib
import json
import subprocess
from pathlib import Path
import qualify_native_selector_sonya_pressure_stock_clear as clear
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=clear.ROOT,clear.need,clear.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_stock_clear_sealed.json'


def execute(views):
    need(not OUT.exists(),'Fresh immutable finite source-clear/storage seal')
    parent_path=clear.OUT/'report.json';proof=json.loads(parent_path.read_text())
    capture=clear.parent.original.faults.serialized.body.original.previous.capture
    handle=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(proof['passed'] and handle['process'].poll()==proof['nativeExit']==0 and
         proof['actualNativeIdentity']==handle['identity'] and
         host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         not census.identity.census(), 'Same retained host and terminal original native, no new boot')
    need(proof['exactGapWords']==18350080 and len(proof['wholeActualHideInterval'])==70 and
         len(proof['effectiveClearFaultsRejected'])==7 and
         len(proof['actualLastPhysicalPageErasure'])==2 and
         all(r['allOwnedPixelsErased']for r in proof['actualLastPhysicalPageErasure']),
         'Entire source-predicted clear and both actual native page masks accepted')
    need(views['passed'] and views['hostPID']==38752 and views['readOnly'] and
         views['actualNativeIdentity']==handle['identity'] and views['newNativeBoots']==0 and
         views['gameWrites']==0 and views['persistentRawFiles']==0 and
         [r['frame']for r in views['selectedFrames']]==[3106,3107,3108,3109],
         'Four actual displayed hide-boundary images inspected on original host')
    for r in views['selectedFrames']:
        name=f"display_{r['frame']}.png"
        need(r['header']==capture.DISPLAY['rgbHeaders'][name] and
             r['nativeRGBSHA256']==hashlib.sha256(capture.DISPLAY['rgb'][name].tobytes()).hexdigest().upper(),
             'Every inspected whole actual RGB still digest-bound to original native callback')
    pins=dict(proof['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Whole earlier source/evidence inventory intact')
    stems=('renderer_faults','renderer_faults_body','renderer_faults_serialized',
           'renderer_faults_bound','hide_lifetime','hide_source','stock_clear')
    files={Path(__file__).resolve(),parent_path.resolve()}
    for stem in stems:
        files.add((ROOT/'tools'/f'qualify_native_selector_sonya_pressure_{stem}.py').resolve())
        folder=(ROOT/f'audit_native_selector_sonya_pressure_{stem}_checked').resolve()
        need(folder.is_relative_to(ROOT.resolve()) and folder.is_dir(),'Exact new small audit subtree')
        files.update(p.resolve()for p in folder.iterdir()if p.is_file())
    entries=[]
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve())and p.suffix in ('.py','.json'),
             'Only exact small sources/reports/failures, never build/ROM/raw media')
        key=str(p);h=sha(p)
        need(key not in pins or pins[key]==h,'Never rewrite executed source or failed evidence')
        pins[key]=h
        old=dict(sha256=h,logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0 and sha(p)==h,'Whole exact audit source unchanged after LZX')
        entries.append(dict(path=key,**old,storedAfter=storage.stored(p)))
    synced=storage.source.verify()
    need(synced['passed'] and all(sha(p)==h for p,h in pins.items()),
         'All15 actual compiled-source sync and full source/native evidence pins unchanged')
    fault=json.loads((ROOT/'audit_native_selector_sonya_pressure_renderer_faults_bound_checked/report.json').read_text())
    need(fault['passed']and fault['finiteActualPressureRendererFaultSuiteAccepted'],
         'Full actual renderer fault suite remains accepted')
    result=dict(proof,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        finiteActualRendererFaultSuiteAccepted=True,
        limitedActualHideBoundaryViews=dict(selectedFrames=views['selectedFrames'],
            observation='Actual physical Kano visible3106/3107, absent3108/3109; stock blood and arena scenery remain. No separate imported corpse observed.'),
        correctedInterpretation='Previous3107 separate-corpse note was physical3106 FIFO shown by next flip; prior immutable report retained.',
        exactNewSmallFileCompression=entries,logicalBytes=sum(r['logicalBytes']for r in entries),
        storedBytes=sum(r['storedAfter']for r in entries),sourceSyncPassed=True,
        publicPlayableUnchanged=True,finalFiniteEvidenceSeal=True)
    OUT.write_text(json.dumps(result,indent=2)+'\n');h=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==h,'Whole final finite receipt unchanged after LZX')
    return result
