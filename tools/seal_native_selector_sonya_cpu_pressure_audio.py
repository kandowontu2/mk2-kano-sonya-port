"""Seal whole real pressure audio, exact small-source/audit LZX only.

Preserve actual earlier waveform/host-binding failure and original handles.
No new game/build/ROM/raw media/ZIP copies/deletions or release promotion.
"""
import json
import subprocess
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_audio_bound as audio
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=audio.ROOT,audio.need,audio.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_audio_storage_checked.json'


def execute():
    need(not OUT.exists(),'Fresh immutable whole pressure source-audio/storage receipt')
    parent=audio.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    held=audio.capture.NATIVE_HANDLES[audio.capture.KEY]
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         host['CommandLine']=='"'+host['ExecutablePath']+'" -B tools/capture_native_selector_special_shadow.py',
         'Exact original retained live host, not a stale lock or replacement')
    need(proof['passed']and held['process'].poll()==proof['nativeExit']==0 and
         held['identity']==proof['actualNativeIdentity']and held['identity']['ProcessId']==44780 and
         not audio.capture.base.choices.current.prior.identity.census(),
         'Same original actual44780 terminal Popen and fresh exact empty native census')
    waveform=proof['wholeMixedWaveform'];positive=proof['wholeActualStartupPacketClocks']
    need(proof['finiteWholePressureSourceExactAudioAccepted']and waveform['passed']and
         waveform['comparedStereoFrames']==1580160 and waveform['differentChannelSamples']==0 and
         waveform['actualSHA256']==waveform['predictedSHA256']==
         '77B605FC70935D9297DDC6D44B249917ADE9A5EF794DBB84212E5050EF7F7311'and
         len(waveform['completeActualWinnerSources'])==2 and
         len(waveform['actualRawMixedPCMFaultsRejected'])==len(waveform['actualMixedSourceOperationFaultsRejected'])==4 and
         len(waveform['actualRepeatedWinnerFaultsRejected'])==2 and
         len(proof['originalDACROMFaultsRejected'])==12 and len(proof['actualSourceClockPacketFaultsRejected'])==18 and
         positive['packets']==dict(packets=142,portWrites=284,nativeDSPReads=284,trueWinnerMarkers=2)and
         positive['channels']['completeVideoRows']==34219 and positive['channels']['completeSoundRows']==31274,
         'Whole complete source-exact pressure PCM/DAC-ROM/packet/channel history and all40 effective faults')
    files=set()
    for name in ('audit_native_selector_sonya_cpu_pressure_audio_checked',
                 'audit_native_selector_sonya_cpu_pressure_audio_bound_checked'):
        at=(ROOT/name).resolve();need(at.is_relative_to(ROOT.resolve())and at.is_dir(),'Exact new audio audit subtree')
        files.update(p.resolve()for p in at.rglob('*')if p.is_file())
    for name in ('qualify_native_selector_sonya_cpu_pressure_audio.py',
                 'qualify_native_selector_sonya_cpu_pressure_audio_bound.py',
                 'seal_native_selector_sonya_cpu_pressure_audio.py'):
        files.add((ROOT/'tools'/name).resolve())
    previous_storage=ROOT/'audit_native_selector_sonya_cpu_pressure_round_scope_storage_checked.json'
    for p in (Path(__file__),parent,previous_storage):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace a prior whole source/evidence pin');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All whole source/native/evidence pins intact before exact compression')
    entries=[]
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve())and p.suffix.lower()in('.py','.json'),
             'Only exact newly created small sources/reports/failures, no media or build artifacts')
        old=dict(sha256=sha(p),logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0 and sha(p)==old['sha256'],'Every whole file unchanged after force-LZX')
        entries.append(dict(path=str(p),**old,storedAfter=storage.stored(p)))
    sync=storage.source.verify();need(sync['passed'],'All15 current canonical compiled-source inputs independently checked')
    endpoints={str(p):sha(p)for p in storage.source.FIXED}
    need(all(endpoints[str(p)]==h for p,h in storage.source.FIXED.items())and
         all(sha(p)==h for p,h in pins.items()),'Final fresh full input/source/private/public endpoint census')
    value=dict(passed=True,goalStatus='active',actualHostIdentity=host,actualNativeIdentity=held['identity'],nativeExit=0,
        finalWholeAudioReportSHA256=sha(parent),wholePressureSourceExactAudioAccepted=True,effectiveFaultsRejected=40,
        wholePCMSHA256=waveform['actualSHA256'],files=entries,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBefore=sum(r['storedBefore']for r in entries),
        storedAfter=sum(r['storedAfter']for r in entries),unchangedEndpoints=endpoints,wholeSourceSyncPassed=True,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,deletions=0,
        allHitGruntProducersIndividuallySourceBound=False,heardAudioQualityAccepted=False,
        allOwnerOverlapPriorityContextsAccepted=False,wholeDisplayedPixelsAccepted=False,fullPortAcceptance=False)
    OUT.write_text(json.dumps(value,indent=2)+'\n');digest=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==digest,'Whole source/audio/storage receipt intact after LZX')
    return value
