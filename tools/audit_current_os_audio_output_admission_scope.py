"""Read-only launcher/backend source scope; no audible runtime launched."""
import json
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT
cmd=R/'PLAY_CURRENT_NATIVE_CHECKED.cmd';s=cmd.read_text()
assert '-samples -samplerate 48000' in s and '-sound none' not in s and '-wavwrite' not in s
module=R/'mame-mkp/src/osd/modules/lib/osdobj_common.cpp';m=module.read_text()
assert m.index('REGISTER_MODULE(m_mod_man, SOUND_DSOUND)')<m.index('REGISTER_MODULE(m_mod_man, SOUND_XAUDIO2)')
config=list((R/'play_v5219_checked').glob('*.ini'));assert not config
paths=[cmd,module,R/'mame-mkp/src/osd/modules/sound/direct_sound.cpp',R/'mame-mkp/src/osd/modules/sound/xaudio2_sound.cpp',R/'audit_current_historical_sonya_ending_scope_v2_checked/report.json']
out=R/'audit_current_os_audio_output_admission_scope_checked';assert not out.exists();out.mkdir()
report=dict(defaultLauncherNativeSoundEnabled=True,launcherRequestsStereoSampleRate=48000,publicConfigIniOverridesPresent=False,
 backendDefaultNotAssumed='Windows modules registerDirectSound beforeXAudio2; actualauto-selectedbackend mustbeobserved. Neither backendinitialization nor sampleIDs establishesheardmix.',
 retainedMixerAndDACComponentEvidence='Historicalfinitecompletewaveforms/DCSdecoder/clockproofs retained; currentnativeportword/ownedmarker/sampleposition/healthcleanup sourceinvariants qualified. These support gameaudio generation/transport, not actualOSoutputendpointadmission from previous soundnone boots.',
 actualOSOutputAdmissionObserved=False,audibleProbeExecuted=False,
 safeProposedProbe='ONE fresh ordinary default-auto sound runtime at realthrottle/currentEXE48000, freshconfig, ~40secwall/320MiB/10MiB, no rawPCM/WAV/PNGs; passiveverboseactualbackendinit/format/errors/overunderflow. Read-onlyCoreAudio enumerate render sessions and match exactPID/birth, sample activeState/per-session peak (>0) and mute/volume; neverSetMute/SetVolume/defaultdevice. Actualendpoint-sessionnonzeroadmission is technicallyverifiable; itdoesnotproveaudiblehardwareorheardmixquality. Useactualownselect/voicecue/hit events to label finite contexts; do not require rareCPUball.',
 globalsChanged=False,newEmulatorRuns=0,heardMixAccepted=False,allAudioContextsAccepted=False,fullPortAccepted=False,inputHashes={str(p):sync.sha(p) for p in paths})
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(report=str(out/'report.json'),defaultSoundEnabled=True,actualOSOutputAdmission=False)))
