"""Seal actual CPU contact/display/audio/finite views and exact metadata storage."""
import hashlib,json,subprocess
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_audio_stop as audio
import qualify_native_selector_sonya_cpu_air_renderer_faults as renderer
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=audio.ROOT,audio.need,audio.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_air_sealed.json'


def execute():
    need(not OUT.exists(),'Fresh immutable actual air-trial integrated finite receipt')
    paths=[audio.contact.control.capture.OUT/'report.json',audio.contact.control.OUT/'report.json',
           renderer.display_proof.OUT/'report.json',renderer.OUT/'report.json',audio.contact.OUT/'report.json',
           audio.OUT/'report.json',ROOT/'audit_native_selector_sonya_cpu_air_actual_views.json']
    reports=[json.loads(p.read_text()) for p in paths]
    capture=audio.contact.control.capture;handle=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in census.census_hosts() if r['ProcessId']==38752)
    need(handle['process'].poll()==0 and all(r['passed'] and r['actualNativeIdentity']==handle['identity'] for r in reports) and
         (host['ParentProcessId'],host['createdUnix'])==(40316,1791734919.6266766) and not census.identity.census(),
         'All whole finite proofs bind same actual50372 terminal and original host, no pending native game')
    pins={}
    for report in reports:
        for p,h in report.get('inputHashes',{}).items():
            need(p not in pins or pins[p]==h,'No differing original source/capture pin replaced');pins[p]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every whole prior source/capture proof intact')
    need(reports[2]['completeCurrentSnapshots']==1800 and reports[2]['wholeExactNativePassVRAMWords']==457703424 and
         len(reports[1]['effectiveFaultsRejected'])==8 and len(reports[3]['effectiveRendererFaultsRejected'])==15 and
         len(reports[4]['effectiveFaultsRejected'])==16 and reports[5]['wholeMixedWaveform']['differentChannelSamples']==0 and
         reports[5]['wholeMixedWaveform']['comparedStereoFrames']==1580160,
         'Full actual controls/renderer/contact/recovery/source-audio coverage and effective fault suites')
    review=reports[-1];seen=review['reviewedFrames']
    need(review['finiteVisualReviewAccepted'] and review['actualHostIdentity']==host and
         [r['frame'] for r in seen]==[2750,2751,2752,2758,2760,2775,2776,2788,2802,2806,2813,2830],
         'Exact actually displayed and inspected twelve contact/release/recovery frames')
    for r in seen:
        file='display_%d.png'%r['frame'];rgb=capture.DISPLAY['rgb'][file]
        need(r['header']==capture.DISPLAY['rgbHeaders'][file] and
             hashlib.sha256(rgb.tobytes()).hexdigest().upper()==r['nativeRGBSHA256'],
             'Each entire visually inspected frame equals same retained native raster')
    samples=(ROOT/'mame-mkp/src/devices/sound/samples.cpp').read_text()
    at=samples.index('void samples_device::stop(uint8_t channel)');end=samples.index('\n}',at)+2
    need('chan.stream->update()' not in samples[at:end] and 'chan.source = nullptr;' in samples[at:end] and
         'chan.source_num = -1;' in samples[at:end], 'Native stop clears pointer without flushing previously ungenerated samples')
    source=(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
    need('if (data != 0x6b02)\n\t\t\t\t\t\t\tmk2ks_battle_audio_stop(slot, "new_launch");' in source and
         'else if (!m_mk2ks_voices->playing(10 + slot * 2) && !m_mk2ks_voices->playing(11 + slot * 2))' in source and
         'm_mk2ks_voices->stop(10 + slot * 2);' in source and 'm_mk2ks_voices->stop(11 + slot * 2);' in source,
         'Whole compiled two-channel new-launch stop and original short-circuit update schedule')
    files={Path(__file__).resolve(),*(p.resolve() for p in paths)}
    folders=(
        'audit_native_selector_sonya_cpu_air_approach_capture_checked',
        'audit_native_selector_sonya_cpu_air_approach_bound_capture_checked',
        'audit_native_selector_sonya_cpu_air_approach_ready_capture_checked',
        'audit_native_selector_sonya_cpu_air_approach_ram',
        'audit_native_selector_sonya_cpu_air_approach_loaded_capture_checked',
        'audit_native_selector_sonya_cpu_air_approach_loaded_ram',
        'audit_native_selector_sonya_cpu_air_approach_checked_capture_checked',
        'audit_native_selector_sonya_cpu_air_approach_checked_ram',
        'audit_native_selector_sonya_cpu_air_control_checked',
        'audit_native_selector_sonya_cpu_air_display_checked',
        'audit_native_selector_sonya_cpu_air_contact_checked',
        'audit_native_selector_sonya_cpu_air_contact_recovery_checked',
        'audit_native_selector_sonya_cpu_air_renderer_faults_checked',
        'audit_native_selector_sonya_cpu_air_audio_checked',
        'audit_native_selector_sonya_cpu_air_audio_startup_checked',
        'audit_native_selector_sonya_cpu_air_audio_stop_checked')
    nvram=set()
    for name in folders:
        at=(ROOT/name).resolve();need(at.is_relative_to(ROOT.resolve()) and at.is_dir(),'Exact new small source/metadata subtree')
        members=[p.resolve() for p in at.rglob('*') if p.is_file()];files.update(members)
        for p in members:
            if p.name=='nvram':
                need(p.parent.name=='mk2ks' and p.parent.parent.name=='nvram' and p.stat().st_size==16384,'Exact normal mapped16KiB CMOS, no extensionless media wildcard')
                nvram.add(p)
    for name in (
        'capture_native_selector_sonya_cpu_air_approach','capture_native_selector_sonya_cpu_air_approach_bound',
        'capture_native_selector_sonya_cpu_air_approach_ready','capture_native_selector_sonya_cpu_air_approach_loaded',
        'capture_native_selector_sonya_cpu_air_approach_checked','qualify_native_selector_sonya_cpu_air_control',
        'qualify_native_selector_sonya_cpu_air_display','qualify_native_selector_sonya_cpu_air_contact',
        'qualify_native_selector_sonya_cpu_air_contact_recovery','qualify_native_selector_sonya_cpu_air_renderer_faults',
        'qualify_native_selector_sonya_cpu_air_audio','qualify_native_selector_sonya_cpu_air_audio_startup',
        'qualify_native_selector_sonya_cpu_air_audio_stop','read_native_selector_sonya_cpu_air','read_native_selector_sonya_cpu_air_remote'):
        files.add((ROOT/'tools'/(name+'.py')).resolve())
    for name in ('mk2ks_native_selector_sonya_cpu_air_approach.lua','mk2ks_native_selector_sonya_cpu_air_approach_loaded.lua','mk2ks_native_selector_sonya_cpu_air_approach_checked.lua'):
        files.add((ROOT/name).resolve())
    mapping=(ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/mame/midway/midtunit.cpp').read_text()
    need('map(0x01400000, 0x0141ffff).rw(FUNC(midtunit_state::midtunit_cmos_r), FUNC(midtunit_state::midtunit_cmos_w)).share("nvram");' in mapping,'Every16KiB native CMOS exact compiled map')
    entries=[]
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve()) and (p.suffix.lower() in ('.py','.lua','.json','.gz','.log','.cfg') or p in nvram),'Exact small metadata/source only, no build/ROM/raw media/ZIP')
        key=str(p);h=sha(p);need(key not in pins or pins[key]==h,'No executed source/original failure edited');pins[key]=h
        old=dict(sha256=h,logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',key],capture_output=True)
        need(call.returncode==0 and sha(p)==h,'Entire original metadata/source bytes unchanged after exact LZX')
        entries.append(dict(path=key,**old,storedAfter=storage.stored(p)))
    sync=storage.source.verify()
    need(sync['passed'] and all(sha(p)==h for p,h in pins.items()),'All15 current compiled-source files, fixed public/private endpoints and full evidence inventory unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        actualHumanInputState=reports[1]['actualAirApproach'],completeCurrentSnapshots=1800,wholeExactNativePassVRAMWords=457703424,
        actualContact=reports[4]['actualContact'],actualControlsFaultsRejected=8,actualRendererFaultsRejected=15,actualContactFaultsRejected=16,
        wholeMixedAudio=reports[5]['wholeMixedWaveform'],nativeSampleReplacementFault=reports[5]['nativeSampleReplacementFault'],
        originalDACROMFaultsRejected=reports[5]['originalDACROMFaultsRejected'],actualVisualReview=review,
        wholeSourceNativeStopCacheAccepted=True,wholeNativePacketsAccepted=False,all19ChannelClocksAccepted=False,
        directContactInstructionTapAccepted=False,releasedHorizontalPushReplayAccepted=False,allUnsavedErasureAccepted=False,
        allEffectOwnershipAccepted=False,heardAudioQualityAccepted=False,allContactsArenasAccepted=False,
        requirements=reports[0]['requirements'],remainingGroups=reports[0]['remainingGroups'],inputHashes=pins,
        fullInputPins=len(pins),inputMismatches=0,sourceSyncPassed=True,exactNewSmallFileCompression=entries,
        logicalBytes=sum(r['logicalBytes'] for r in entries),storedBytes=sum(r['storedAfter'] for r in entries),
        actualAllOriginalFailuresPreserved=True,wholeObjectiveStillActive=True,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGamesThisTurn=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,deletions=0)
    OUT.write_text(json.dumps(value,indent=2)+'\n');h=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==h,'Whole final finite receipt unchanged after LZX')
    return value
