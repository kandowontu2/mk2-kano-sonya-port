"""Consolidate actual two-slot full-mix evidence without broadening acceptance."""
import gzip
import json
import traceback
from pathlib import Path
import review_native_kano_laser_audio as prior
import native_process_census_v6647 as identity

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_kano_laser_audio_both_slots_review'


def main():
    need(not OUT.exists(),'Fresh immutable combined audio receipt');OUT.mkdir()
    try:
        need(not identity.census(),'Both actual native game handles terminal, never inferred from log text')
        source_path=ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json'
        source=json.loads(source_path.read_text())
        build_path=ROOT/'diagnostic_native_kano_laser_audio/build-info.json'
        build=json.loads(build_path.read_text(encoding='utf-8-sig'))
        need(source['passed'] and build['expected_guest_sha256']==source['proposedGuestSHA256'] and
             not build['public_build_promoted'] and not build['full_port_accepted'], 'Same private source-qualified executable')
        pins={str(Path(__file__).resolve()):sha(__file__),str(source_path):sha(source_path),str(build_path):sha(build_path)}
        cases=[];frames=0;raster_changes=[]
        for side in (1,2):
            folder=ROOT/f'audit_native_kano_laser_audio_p{side}'
            review_path=ROOT/f'audit_native_kano_laser_audio_p{side}_review/report.json'
            record=json.loads(review_path.read_text())
            need(record['passed'] and record['finiteNativeLaserAudioAccepted'] and record['physicalSlot']==side and
                 record['all19ChannelsObserved'] and record['nativeSceneAudioCleanupAccepted'] and
                 record['wholeNativeMixedWaveform']['differentChannelSamples']==0 and
                 not record['fullFinisherAccepted'] and not record['fullPortAcceptance'], 'Finite same-slot native proof only')
            need(all(sha(p)==h for p,h in record['inputHashes'].items()),'Every actually executed waveform/reference/controller input conserved')
            pins[str(review_path)]=sha(review_path)
            text=gzip.open(folder/'run.log.gz','rt').read()
            actual=prior.rows(text,'MK2_LASER_RGB_DIGEST')
            old_path=ROOT/f'audit_native_kano_laser_burst_p{side}/run.log.gz'
            old=prior.rows(gzip.open(old_path,'rt').read(),'MK2_LASER_RGB_DIGEST')
            need(len(actual)==len(old)==33 and [r['age'] for r in actual]==[r['age'] for r in old],
                 'All original raster checkpoints retained, not a smaller easier render scope')
            changed=[r['age'] for a,r in zip(old,actual) if a['sha256']!=r['sha256']]
            raster_changes.append(dict(physicalSlot=side,changedWholeRasterAges=changed,
                                      wholeNewVisualRegressionAccepted=False,reason='Earlier visual proof cannot be automatically inherited by the changed build'))
            pins[str(old_path)]=sha(old_path)
            markers=prior.rows(text,'MK2_LAUDIO_MARKER');entry=prior.rows(text,'MK2_LASER_ENTRY')[0]
            need(len(markers)==5 and [r['marker'] for r in markers]==['6B40','6B41','6B42','6B43','6B44'], 'All five actual core source cues')
            need([int(r['frame'])-int(entry['frame']) for r in markers]==[20,68,69 if side==1 else 68,164,164],
                 'Actual native charge/contact/burst ages; measured one-field player-one victim handoff conserved')
            frames+=record['wholeNativeMixedWaveform']['comparedStereoFrames']
            cases.append(dict(physicalSlot=side,actualMarkers=markers,comparedStereoFrames=record['wholeNativeMixedWaveform']['comparedStereoFrames'],
                              fullMixSHA256=record['wholeNativeMixedWaveform']['actualSHA256'],all19ChannelsTerminal=True))
        cmd=ROOT/'PLAY_LATEST_KANO_SONYA.cmd'
        need(sha(cmd)=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5','Public launcher unchanged')
        pins[str(cmd)]=sha(cmd)
        cache_path=ROOT/'diagnostic_native_kano_laser_audio/cache_retirement.json'
        cache=json.loads(cache_path.read_text(encoding='utf-8-sig'))
        need(cache['passed'] and cache['nativeCompilerExit']==0 and cache['preexistingFilesRestored'] and
             not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'Compiler terminal and generated cache actually retired')
        pins[str(cache_path)]=sha(cache_path)
        record=dict(passed=True,bothPhysicalSlotsFiniteLaserMixAccepted=True,comparedStereoFrames=frames,cases=cases,
                    all19ChannelsTerminal=True,finiteNativeSceneAudioOwnershipClearAccepted=True,
                    nativeStockVictimAudioAccepted=False,kanoMirrorScreamAccepted=False,nativeCPULaserAudioAccepted=False,
                    allLaserPriorityRNGContextsAccepted=False,all14RequirementsAccepted=False,fullFinisherAccepted=False,fullPortAcceptance=False,
                    wholeNewVisualRegressionAccepted=False,actualRasterComparison=raster_changes,
                    originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=source['originalRemainingWorkGroups'],
                    goalStatus='active',previousGoalTurnClassification='progress: new audio source and real Lua parser qualified; one private build initiated',
                    thisGoalTurnClassification='progress: same compiler reached terminal, generated cache retired; both physically earned native slot trials passed exact whole mixed PCM/DAC/ROM/cue/channel/EOS/scene ownership tests',
                    inputHashes=pins,latestPlayableChanged=False,newBuilds=1,newROMCopies=0,newRawMedia=0,newZIPs=0,
                    nextWork=['Actual stock-victim native FFA11FD0 routing, own victim pose/cleanup and original stock sound priority.',
                              'Actual Kano mirror scream and CPU activation/fallback/owner transitions.',
                              'Changed-build full visual/particle/scene, selection/identity/grounding and all remaining original14+6 regressions before public promotion.'])
        need(len(record['originalNaturalIntegrationRequirements'])==14 and len(record['originalRemainingWorkGroups'])==6,'Original goal never narrowed')
        (OUT/'report.json').write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps(dict(passed=True,bothPhysicalSlotsFiniteLaserMix=True,stereoFrames=frames,publicUnchanged=True,fullPortAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise


if __name__=='__main__':main()
