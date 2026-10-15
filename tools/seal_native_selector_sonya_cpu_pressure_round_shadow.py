"""Seal full retained pressure geometry/failures with exact small-file LZX.

Current compiled source, original host/Popen and public endpoints remain intact.
No builds, ROM copies, raw media, ZIPs or deletions. Entire port still active.
"""
import json
import subprocess
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_round_shadow_bound as rendering
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=rendering.ROOT,rendering.need,rendering.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_round_shadow_storage_checked.json'


def execute():
    need(not OUT.exists(),'Fresh immutable whole pressure geometry/storage receipt')
    parent=rendering.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    held=rendering.capture.NATIVE_HANDLES[rendering.capture.KEY]
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         host['CommandLine']=='"'+host['ExecutablePath']+'" -B tools/capture_native_selector_special_shadow.py',
         'Exact original retained live host, not a replacement or stale lock')
    need(proof['passed']and held['process'].poll()==proof['nativeExit']==0 and
         held['identity']==proof['actualNativeIdentity']and held['identity']['ProcessId']==44780 and
         not rendering.capture.base.choices.current.prior.identity.census(),
         'Same original terminal44780 Popen and fresh exact empty native census')
    case=proof['wholePressureBodyShadowGeometry']
    need(proof['wholePressureLiveRoundResetGeometryAccepted']and case['actualContiguousActorFields']==2150 and
         case['state']['actualDrawFrames']==1075 and case['state']['trueLiveOwnersNeverReallocated'] and
         proof['independentEligibleBodyFields']==2081 and proof['independentHiddenVictimBodyFields']==69 and
         len(proof['originalBodyShadowFaultsRejected'])==len(proof['wholeRoundFaultsRejected'])==11,
         'Whole independently expected live body/shadow eligibility and22 effective counterexamples')
    files=set()
    for suffix in ('checked','clip_checked','eligibility_checked','bound_checked'):
        at=(ROOT/('audit_native_selector_sonya_cpu_pressure_round_shadow_'+suffix)).resolve()
        need(at.is_relative_to(ROOT.resolve())and at.is_dir(),'Exact newly created audit subtree only')
        files.update(p.resolve()for p in at.rglob('*')if p.is_file())
    for name in ('qualify_native_selector_sonya_cpu_pressure_round_shadow.py',
                 'qualify_native_selector_sonya_cpu_pressure_round_shadow_clip.py',
                 'qualify_native_selector_sonya_cpu_pressure_round_shadow_eligibility.py',
                 'qualify_native_selector_sonya_cpu_pressure_round_shadow_bound.py',
                 'seal_native_selector_sonya_cpu_pressure_round_shadow.py'):
        files.add((ROOT/'tools'/name).resolve())
    for p in (Path(__file__),parent,ROOT/'audit_native_selector_sonya_cpu_pressure_storage_checked.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace an existing evidence/source pin');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every complete source/evidence hash intact before compression')
    before={p:dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))for p in files}
    entries=[]
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve())and p.suffix.lower()in('.py','.json'),
             'Exact new small source/report/failure files only, never media or build artifacts')
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0 and sha(p)==before[p]['sha256'],'Whole file bytes unchanged after exact LZX')
        entries.append(dict(path=str(p),**before[p],storedAfter=storage.stored(p)))
    sync=storage.source.verify();need(sync['passed'],'Whole current canonical compiled-source inventory unchanged')
    endpoints={str(p):sha(p)for p in storage.source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in storage.source.FIXED.items()),'Private current and public older CMD/ZIP endpoints unchanged')
    need(all(sha(p)==h for p,h in pins.items()),'Fresh whole input census after all faults and compression')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualHostIdentity=host,bodyShadowReportSHA256=sha(parent),effectiveFaultsRejected=22,
        wholePressureLiveRoundResetGeometryAccepted=True,files=entries,inputHashes=pins,
        fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,wholeSourceSyncPassed=True,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,deletions=0,
        wholeDisplayedPixelsAccepted=False,wholeSourceAudioAccepted=False,completeFinisherChoreographyAccepted=False,
        allArenaCPUContextsAccepted=False,fullPortAcceptance=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n');digest=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==digest,'Whole new storage receipt intact after LZX')
    return value
