"""Full finite pressure interruption/body-shadow evidence and exact audit LZX.

All original requirements remain active. Whole current source hashes and actual
terminal native handle retained; no release promotion, media copies or deletion.
"""
import json
import subprocess
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_body_shadow_bound as rendering
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=rendering.ROOT,rendering.need,rendering.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_storage_checked.json'


def execute():
    need(not OUT.exists(),'Fresh immutable pressure evidence/storage receipt')
    parent=rendering.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    mechanics_path=rendering.mechanics.OUT/'report.json';mechanics=json.loads(mechanics_path.read_text())
    capture=rendering.capture;held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         host['CommandLine']=='"'+host['ExecutablePath']+'" -B tools/capture_native_selector_special_shadow.py',
         'Original exact currently live retained host, no replacement')
    need(proof['passed']and mechanics['passed']and held['process'].poll()==proof['nativeExit']==0 and
         held['identity']==proof['actualNativeIdentity']==mechanics['actualNativeIdentity'] and
         held['identity']['ProcessId']==44780 and not capture.base.choices.current.prior.identity.census(),
         'Original actual44780 native handle terminal0 and fresh empty native census')
    need(proof['finiteCPUInterruptionBodyShadowAccepted']and
         proof['wholeActualInterruptedWindowBodyShadow']['actualContiguousActorFields']==54 and
         proof['actualFrames']==list(range(1917,1944)) and
         len(proof['originalBodyShadowFaultsRejected'])==11 and
         len(mechanics['effectiveInterruptionFaultsRejected'])==13,
         'Entire finite interrupted/startup/hurt/cleanup body-shadow model and all24 effective faults')
    for p in (Path(__file__),parent,mechanics_path):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No original input pin replaced');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every whole source/native/evidence input intact')
    files=set()
    for folder in ('audit_native_selector_sonya_cpu_pressure_bound_ram',
                   'audit_native_selector_sonya_cpu_pressure_bound_capture_checked',
                   'audit_native_selector_sonya_cpu_pressure_interrupt_checked',
                   'audit_native_selector_sonya_cpu_pressure_body_shadow_checked',
                   'audit_native_selector_sonya_cpu_pressure_body_shadow_bound_checked'):
        at=(ROOT/folder).resolve();need(at.is_relative_to(ROOT.resolve())and at.is_dir(),'Exact new audit subtree')
        files.update(p.resolve()for p in at.rglob('*')if p.is_file())
    for name in ('mk2ks_native_selector_sonya_cpu_pressure.lua',
                 'mk2ks_native_selector_sonya_cpu_pressure_bound.lua',
                 'tools/capture_native_selector_sonya_cpu_pressure.py',
                 'tools/capture_native_selector_sonya_cpu_pressure_bound.py',
                 'tools/qualify_native_selector_sonya_cpu_pressure_interrupt.py',
                 'tools/qualify_native_selector_sonya_cpu_pressure_body_shadow.py',
                 'tools/qualify_native_selector_sonya_cpu_pressure_body_shadow_bound.py',
                 'tools/seal_native_selector_sonya_cpu_pressure_storage.py'):
        files.add((ROOT/name).resolve())
    before={p:dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))for p in files}
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve())and p.suffix.lower()not in ('.exe','.zip','.wav','.png','.bin'),
             'Exact small source/audit/config/digest only; raw media and other artifacts untouched')
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0,'Exact individual file force-LZX succeeded')
    entries=[]
    for p,old in before.items():
        need(sha(p)==old['sha256'],'Every whole byte hash unchanged after compression')
        entries.append(dict(path=str(p),**old,storedAfter=storage.stored(p)))
    need(all(sha(p)==h for p,h in pins.items()),'All full source/evidence hashes freshly rechecked after compression')
    sync=storage.source.verify();need(sync['passed'],'Every synchronized current compile input independently checked')
    endpoints={str(p):sha(p)for p in storage.source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in storage.source.FIXED.items()),'Current private and older public CMD/ZIP endpoints unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualHostIdentity=host,mechanicsReportSHA256=sha(mechanics_path),bodyShadowReportSHA256=sha(parent),
        effectiveFaultsRejected=24,finiteCPUInterruptionMechanicsAndBodyShadowAccepted=True,
        files=entries,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        wholeSourceSyncPassed=True,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,deletions=0,
        allMoveArenaInterruptionsAccepted=False,wholePressureRoundResetRenderingAccepted=False,
        wholeDisplayedPixelsAccepted=False,wholeSourceAudioAccepted=False,fullPortAcceptance=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n');digest=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==digest,'Whole storage receipt unchanged after LZX')
    return value
