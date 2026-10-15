"""Exact final scope/source/host receipt, small new audit files only."""
import json
import subprocess
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_round_shadow_scope as geometry
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=geometry.ROOT,geometry.need,geometry.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_round_scope_storage_checked.json'


def execute():
    need(not OUT.exists(),'Fresh immutable exact whole-round entry-scope/storage receipt')
    parent=geometry.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    capture=geometry.previous.capture;held=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         host['CommandLine']=='"'+host['ExecutablePath']+'" -B tools/capture_native_selector_special_shadow.py',
         'Original exact native host remains live')
    need(proof['passed']and held['process'].poll()==proof['nativeExit']==0 and
         held['identity']==proof['actualNativeIdentity']and not capture.base.choices.current.prior.identity.census(),
         'Original native44780 remains terminal0, no restart and fresh empty native census')
    case=proof['wholePressureBodyShadowGeometry']
    need(case['actualContiguousActorFields']==2150 and case['state']['actualDrawFrames']==1075 and
         case['actualNativeBodyCandidates']==case['actualPublishedBodyParts']==4104 and
         case['actualShadowEligibilityCalls']==2150 and case['actualOwnedShadowComponents']==4102 and
         case['actualSourceBoundShadowCopies']==107405 and case['actualUniqueROMStreams']==279 and
         not case['entryBodyPublicationProven']and case['actualRoutineEntryDrawFrames']==[1918,2847,2921]and
         case['preliveRoutineEntriesWithoutBodyObservation']==[1817,2610]and
         case['actualFirstDrawFollowingOpeningEntries']==[1818,2611]and
         len(proof['originalBodyShadowFaultsRejected'])==len(proof['wholeRoundFaultsRejected'])==11,
         'Complete original whole-round geometry,22 effective faults and truthful opening-entry observation scope')
    comparable=dict(case)
    for key in ('actualRoutineEntryDrawFrames','preliveRoutineEntriesWithoutBodyObservation',
                'actualFirstDrawFollowingOpeningEntries'):comparable.pop(key)
    comparable['entryBodyPublicationProven']=True
    need(comparable==geometry.whole_prior['wholePressureBodyShadowGeometry'],
         'Scope correction changed no original physical/geometry/source positive result')
    previous_receipt=ROOT/'audit_native_selector_sonya_cpu_pressure_round_shadow_storage_checked.json'
    for p in (Path(__file__),parent,Path(geometry.__file__),previous_receipt):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No prior executed source pin replacement');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All complete native/source/evidence inputs intact')
    files=[Path(__file__).resolve(),Path(geometry.__file__).resolve(),parent.resolve(),previous_receipt.resolve()]
    entries=[]
    for p in files:
        need(p.is_relative_to(ROOT.resolve())and p.suffix.lower()in('.py','.json'),'Exact small new source/audit files only')
        old=dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0 and sha(p)==old['sha256'],'Every whole file unchanged after exact LZX')
        entries.append(dict(path=str(p),**old,storedAfter=storage.stored(p)))
    sync=storage.source.verify();need(sync['passed'],'Whole independently synchronized15-input compiled source inventory')
    endpoints={str(p):sha(p)for p in storage.source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in storage.source.FIXED.items())and
         all(sha(p)==h for p,h in pins.items()),'Final fresh whole source/evidence/endpoints census')
    value=dict(passed=True,goalStatus='active',actualHostIdentity=host,actualNativeIdentity=held['identity'],nativeExit=0,
        finalWholeGeometryReportSHA256=sha(parent),wholePressureLiveRoundResetGeometryAccepted=True,
        exactPreliveEntryObservationScopeAccepted=True,effectiveFaultsRejected=22,
        files=entries,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,wholeSourceSyncPassed=True,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,deletions=0,
        wholeDisplayedPixelsAccepted=False,wholeSourceAudioAccepted=False,completeFinisherChoreographyAccepted=False,
        allArenaCPUContextsAccepted=False,fullPortAcceptance=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n');digest=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==digest,'Whole final small scope/storage receipt unchanged after LZX')
    return value
