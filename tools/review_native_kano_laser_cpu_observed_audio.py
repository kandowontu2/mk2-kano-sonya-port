"""Independent CPU-vs-Sonya evidence from retained terminal failed fixture.

Do not relabel transport failure. Its mirror-only lifecycle adapter missed
two genuine CPU actions, and its751-field terminal assertion was violated.
The first full751-field audio window, both whole sound-ROM reads, actual
native0 terminal and subsequent ordinary continues remain directly testable.
No all-CPU choice/spacing/scene/visual/full-port claim.
"""
import gzip
import json
import traceback
from pathlib import Path
import review_native_kano_laser_audio as original
import native_process_census_v6647 as identity

ROOT,need,sha=original.ROOT,original.need,original.sha
rows=original.rows
OUT=ROOT/'audit_native_kano_laser_cpu_observed_audio_review'


def review(capture):
    need(not OUT.exists(),'Fresh independent observed-CPU review; retain failed fixture');OUT.mkdir()
    try:
        folder=capture['folder'];receipt=json.loads((folder/'report.json').read_text())
        checked=json.loads((folder/'checked_observer_sources.json').read_text())
        need(not receipt['passed'] and not receipt['transportOnlyAccepted'] and receipt['nativeExit']==0 and
             receipt['wholeGuestMatched'] and not receipt['errors'] and checked['passed'] and
             not any(r['ProcessId']==receipt['actualWindowsIdentity']['ProcessId'] for r in identity.census()),
             'Original failed fixture retained; same actual native0 handle terminal; whole guest/source inputs exact')
        need(all(sha(p)==h for report in (receipt,checked) for p,h in report['inputHashes'].items()),'Every actual executed input frozen')
        stderr=(folder/'stderr.log').read_text()
        expected='[LUA ERROR] in execute_function: ...b_winner_mix_observer_v5779.lua::full_native_laser_audio:140: Both complete sound ROM checks and same physical laser terminal\n'
        need(stderr==expected,'Only the exact actual stop-window observer assertion, never a game-error waiver')
        text=capture['text'];begin=rows(text,'MK2_MAUDIO_BEGIN')
        need(len(begin)==1 and begin[0]['id']=='17','One actual own-native Kano performer opcode origin')
        origin=int(begin[0]['frame']);terminal=rows(text,'MK2_LASER_RESULT')
        need(len(terminal)==1 and terminal[0]['started']==terminal[0]['completed']=='-1' and
             int(terminal[0]['frame'])>origin+751,'Mirror-only observer explicitly failed to own actual Sonya victim; no fabricated stop')
        live=rows(text,'MK2_NAT_CAMPAIGN_LIVE')
        parsed=json.loads(gzip.open(ROOT/'audit_native_kano_laser_cpu_audio_lua_context_source/executed_sources.json.gz','rt').read())
        need('if mode==2 and state==1 and p:read_u16(slots[opponent].state)==0 and human and other and human.owner==human.actor and other.owner==other.actor then' in
             parsed['MK2_CPU_PARSE_CAMPAIGN'],'Actual parsed LIVE requires human1/CPU0 and true own actor contexts')
        before=[r for r in live if origin-30<=int(r['frame'])<origin]
        after=[r for r in live if origin<int(r['frame'])<=origin+30]
        need(len(before)==len(after)==1,'Actual immediately bracketing native LIVE fields, not inferred player roles')
        for r in before+after:
            need(r['human_slot']=='1' and r['human']=='18:18' and r['cpu']=='17:17' and r['health']=='0,155' and
                 r['cpu_actor']==begin[0]['a8'] and r['cpu_main']==begin[0]['a13'],
                 'Actual defeated true Sonya human and autonomous true Kano CPU/main, never proxy or P2 human input')
        hx=int(after[0]['hpos'].split(',')[0]);cx=int(after[0]['cpos'].split(',')[0])
        need(abs(hx-cx)==150,'Actual native CPU positioned at150 pixels before charge, not a forced geometry assignment')
        markers=rows(text,'MK2_LAUDIO_MARKER')
        charges=[r for r in markers if r['marker']=='6B40'];need(len(charges)==2,'Two real own charge port instructions observed')
        activations=[]
        for charge in charges:
            start=int(charge['frame'])-20
            events=[r for r in markers if start<=int(r['frame'])<=start+196]
            need([r['marker'] for r in events]==['6B40','6B41','6B42','6B43','6B44'] and
                 [int(r['frame'])-start for r in events]==[20,68,68,164,164],
                 'Each actual CPU charge/beam/Sonya scream/two burst sequence at source timing')
            victims=[r for r in events if r['marker']=='6B42']
            need(charge['id']=='17' and victims[0]['id']=='18','Actual own Kano charge and true Sonya victim marker')
            following=[r for r in live if int(r['frame'])>start+750 and int(r['health'].split(',')[0])>0]
            need(following,'Normal combat re-admitted after this CPU laser; not a frozen winner scene')
            losses=[r for r in rows(text,'MK2_NAT_CAMPAIGN_LOSS') if start+196<int(r['frame'])<int(following[0]['frame'])]
            need(losses,'Actual loss/normal continue between CPU laser and fresh combat')
            activations.append(dict(observedOrigin=start,actualPortEvents=events,actualSubsequentLoss=losses[0],actualSubsequentCombat=following[0]))
        need(not rows(text,'MK2_LASER_OVERRUN'),'No actual native body-copier/global overrun observed throughout same run')
        pins={str(Path(__file__).resolve()):sha(__file__),str(folder/'report.json'):sha(folder/'report.json'),
              str(folder/'checked_observer_sources.json'):sha(folder/'checked_observer_sources.json'),str(folder/'stderr.log'):sha(folder/'stderr.log'),
              str(folder/'run.log.gz'):sha(folder/'run.log.gz'),str(ROOT/'audit_native_kano_laser_cpu_audio_lua_context_source/executed_sources.json.gz'):
              sha(ROOT/'audit_native_kano_laser_cpu_audio_lua_context_source/executed_sources.json.gz')}
        pcm=[r['header'] for r in capture['pcm']];dac=[r['header'] for r in capture['dac']];chunks=[r['pixels'] for r in capture['dac']]
        need(pcm and int(pcm[0]['frame'])>=origin and int(pcm[-1]['frame'])<=origin+750,
             'Same full original actual audio origin through750, not a retrospectively selected excerpt')
        gate,faults=original.dac_models(len(chunks));dac_proof=gate(chunks,dac,pcm);dac_faults=faults(chunks,dac,pcm)
        expected_rom,source_roms=original.mixer.expected_region(pins)
        rom_gate,rom_fault=original.mixer.rom_models(expected_rom);roms=[];rom_faults=[]
        for phase in ('startup','terminal'):
            parts=[r for r in capture['romChunks'] if r['header']['phase']==phase]
            need(len(parts)==192 and [int(r['header']['offset']) for r in parts]==list(range(0,0xc00000,65536)),
                 'All actual native firmware/data lanes and mirrors at real startup and later terminal')
            raw=b''.join(r['pixels'] for r in parts);roms.append(rom_gate(raw,phase));rom_faults+=rom_fault(raw,phase)
        sound=original.waveform(capture,pins)
        (OUT/'waveform_comparison.json').write_text(json.dumps(sound,indent=2)+'\n')
        need(sound['passed'],'Entire original CPU laser mixed PCM equals exact source prediction; no fit/trim/native impact omission')
        channels=rows(text,'MK2_TOMB_MIX_CHANNEL')
        need(len(channels)==len(chunks)*19 and {(r['index'],int(r['channel'])) for r in channels}==
             {(str(i+1),c) for i in range(len(chunks)) for c in range(19)},'Every actual channel at every consecutive sound callback')
        for r in channels:
            need(r['loop']==r['paused']==r['writes']=='0','Actual sources nonlooping/unpaused/passive')
            if int(r['channel']) not in (0,14,15,16):need(r['sample']=='4294967295','No omitted imported source from the full mix')
        end=rows(text,'MK2_LAUDIO_CHANNEL_TERMINAL')
        need(len(end)==19 and {int(r['channel']) for r in end}==set(range(19)) and all(r['sample']=='4294967295' for r in end),
             'All19 sources inactive at the actual later terminal, not a751-field cleanup inference')
        pool=[r for r in rows(text,'MK2_LAUDIO_POOL') if r['phase']=='terminal']
        need(len(pool)==1 and pool[0]['actor']==pool[0]['main']=='00000000' and pool[0]['slots']=='0000,0;0000,0;0000,0;0000,0;0000,0',
             'Actual later-terminal owner and all five priorities/timers cleared')
        parent=json.loads((ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json').read_text())
        for path in (Path(original.__file__),Path(original.mixer.__file__),Path(original.dac_source.__file__),ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json'):
            pins[str(path)]=sha(path)
        report=dict(passed=True,originalTransportFailurePreserved=True,nativeExit=0,
                    finiteNaturalCPUKanoSonyaLaserActivationObserved=True,twoActualCPUActivations=activations,
                    firstActualCPUWholeAudioAccepted=True,wholeNativeMixedWaveform=sound,all19ChannelsObserved=True,
                    actualLaterTerminalAudioCleanupAccepted=True,nativeDAC=dac_proof,dacFaultsRejected=dac_faults,
                    originalSoundROMProofs=roms,soundROMFaultsRejected=rom_faults,originalSoundROMInputs=source_roms,
                    observedCPUPhysicalSlot=2,observedVictimID=18,bracketingOwnedNativeFields=before+after,
                    nativeCPUDispatchTraceAccepted=False,allCPULaserContextsAccepted=False,fullFinisherAccepted=False,
                    wholeNewVisualRegressionAccepted=False,fullPortAcceptance=False,
                    originalNaturalIntegrationRequirements=parent['originalNaturalIntegrationRequirements'],
                    originalRemainingWorkGroups=parent['originalRemainingWorkGroups'],inputHashes=pins,
                    previousGoalTurnClassification='no progress: requested status was answered without new implementation/test evidence',
                    thisGoalTurnClassification='progress: actual installed parser and cold physical CPU run; two natural CPU laser activations, first full exact mix and subsequent native combat verified despite retained fixture-stop failure',
                    limitations=['The first full native audio window is accepted independently; original transport remains false.',
                                 'Second activation has genuine source-port/native continue evidence, but no second full PCM window.',
                                 'Spacing is one observed150pixel result, not full native dispatch/spacing branch proof.',
                                 'No entire visual, mirror CPU, other opponent, arena/reset/rejoin/full14+6acceptance.'],
                    newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,goalStatus='active')
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original objective preserved')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,naturalCPUActivations=2,exactFirstAudioStereoFrames=sound['comparedStereoFrames'],originalTransportStillFalse=True)),flush=True)
        return report
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise
