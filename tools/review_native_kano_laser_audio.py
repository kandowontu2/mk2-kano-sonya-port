"""Whole actual native PCM/DAC and physically dispatched laser source mix.

RAM-only raw media. Native decoder/resampler, sample interpolation/EOF,
stream clocks and float32 gain/order are conserved, never waveform-fitted.
This earned finite case is not full finisher or full-port acceptance.
"""
import gzip
import hashlib
import inspect
import json
import struct
import traceback
import wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import current_tomb_winner_mix_fault_model_v5789 as mixer
import current_native_dac_capture_v5593 as dac_source
import qualify_native_kano_laser_audio as qualified

ROOT,need,sha=qualified.ROOT,qualified.need,qualified.sha
rows=mixer.rows


def dac_models(count):
    need(count>200,'Entire physical laser sound window, not a selected excerpt')
    code=inspect.getsource(dac_source.dac_gate)
    old='len(chunks)==len(headers)==len(pcm_headers)==685'
    need(code.count(old)==1,'Only whole-window callback count adaptation')
    code=code.replace(old,'len(chunks)==len(headers)==len(pcm_headers)==count')
    scope=dict(vars(dac_source),count=count)
    exec(compile(code,__file__+'::whole_original_DAC_gate','exec'),scope)
    exec(compile(inspect.getsource(dac_source.dac_faults),__file__+'::actual_DAC_faults','exec'),scope)
    return scope['dac_gate'],scope['dac_faults']


def waveform(capture,pins):
    text=capture['text'];headers=[r['header'] for r in capture['dac']]
    chunks=[r['pixels'] for r in capture['dac']]
    pcm=np.frombuffer(b''.join(r['pixels'] for r in capture['pcm']),dtype='<i2').reshape(-1,2)
    dcs,clocks=mixer.float_model()(chunks,headers)
    need(dcs.shape==pcm.shape and len(headers)*960==len(pcm),'Every native stereo frame and DAC callback included')
    markers=rows(text,'MK2_MAUDIO_SOUND');events=[]
    cue_names=('kano_laser_charge','kano_laser_beam','sonya_laser_scream','kano_laser_burst_a','kano_laser_burst_b')
    cue_offsets=(0xb0e00,0xb0e20,0xb0e40,0xb0ea0,0xb0ec0)
    cue_channels=(14,15,16,14,15)
    assets=json.loads((ROOT/'audit_native_kano_laser_original_samples/asset_report.json').read_text())
    need(assets['passed'] and assets['hardwareOnlyNotGameplayAcceptance'] and
         all(sha(p)==h for p,h in assets['inputHashes'].items()),'Every complete original source recording remains exact')
    for marker in markers:
        word=int(marker['word'],16)
        if 0x6b40<=word<=0x6b44:
            cue=word-0x6b40
            need(int(marker['pc'],16)==0xff800000+cue_offsets[cue]*8+(52 if cue==2 else 14)*8,
                 'Source event clock is exact actual private port instruction, not audio searched')
            path=ROOT/'audit_native_kano_laser_original_samples'/(cue_names[cue]+'.wav')
            need(sha(path)==assets['inputHashes'][str(path)],'Full original laser waveform pin')
            pins[str(path)]=sha(path)
            with wave.open(str(path),'rb') as reader:
                need(reader.getnchannels()==1 and reader.getsampwidth()==2 and reader.getframerate()==48000 and reader.getcomptype()=='NONE',
                     'Entire original mono48k signed16 source, no tail shortening')
                values=np.frombuffer(reader.readframes(reader.getnframes()),dtype='<i2').copy();frequency=reader.getframerate()
            channel=cue_channels[cue];sample_id=(17,18,19,21,22)[cue];gain=np.float32(.70)
        elif marker['pc']=='FFFB7140' and marker['word']=='FFFE':
            values,frequency=mixer.read_winner('kano',pins);channel=0;sample_id=2
            gain=np.float32(np.float32(.70)*np.float32(.30))
        else:
            continue
        values_out,positions=mixer.sample_values(values,frequency)
        events.append(dict(marker=marker,channel=channel,sample_id=sample_id,frequency=frequency,length=len(values),
                           gain=gain,start=mixer.sample_clock(marker['seconds'],True),samples=values_out,positions=positions))
    need([e['marker']['word'] for e in events]==['6B40','6B41','6B42','6B43','6B44','FFFE'],
         'Whole earned true-Kano versus true-Sonya charge/beam/scream/two-bursts/winner sequence')
    voices={c:np.zeros_like(dcs) for c in (0,14,15,16)}
    for event in events:
        for index,head in enumerate(headers):
            tick=int(Decimal(head['seconds'])*50)
            start_at=(tick-1)*960*(mixer.ATTO//48000);sec,fraction=divmod(start_at,mixer.ATTO)
            view=sec*48000+fraction//mixer.PERIOD
            at=np.arange(view,view+960,dtype=np.int64)-event['start'];valid=(at>=0)&(at<len(event['samples']))
            segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(event['samples'][at[valid]]*event['gain'])
            voices[event['channel']][index*960:(index+1)*960]+=segment[:,None]
    voice=np.zeros_like(dcs)
    for channel in range(19):
        if channel in voices:voice=np.float32(voice+voices[channel])
    convert=lambda data:(np.clip(data,-1,1).astype(np.float64)*32767.0).astype('<i2')
    predicted=convert(np.float32(dcs+voice));different=np.argwhere(predicted!=pcm)
    faults=[]
    if not len(different):
        for label,index,channel in [('first actual sample',0,0),('last actual sample',len(pcm)-1,1)]:
            bad=pcm.copy();bad[index,channel]^=1
            need(not np.array_equal(predicted,bad),'Actual full PCM one-bit fault rejected')
            faults.append(dict(label=label,differences=int(np.count_nonzero(predicted!=bad))))
        for label,bad in [('first stereo frame missing',pcm[1:]),('last stereo frame missing',pcm[:-1])]:
            need(bad.shape!=predicted.shape,'Actual full PCM missing-frame fault rejected');faults.append(dict(label=label))
        for channel in voices:
            bad=convert(np.float32(dcs+np.float32(voice-voices[channel])))
            need(not np.array_equal(bad,pcm),'Each own sound channel has nonvacuous audible coverage')
            faults.append(dict(label=f'channel{channel} omitted',differences=int(np.count_nonzero(bad!=pcm))))
    return dict(passed=not len(different),comparedStereoFrames=len(pcm),differentChannelSamples=len(different),
                actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
                firstDifferences=[dict(stereoFrame=int(n),callback=int(n)//960+1,channel=int(c),expected=int(predicted[n,c]),actual=int(pcm[n,c]),
                                      nativeFloat=float(dcs[n,c]),importedFloat=float(voice[n,c])) for n,c in different[:16]],
                actualRawFaultsRejected=faults,actualCallbackSourceClocks=clocks,
                sourceEvents=[{k:(float(v) if k=='gain' else v) for k,v in e.items() if k not in ('samples','positions')} for e in events],
                comparison='Entire actual native float32 DAC/clock/cache and source-port-clock full samples/interpolation/EOF/gain/output order; no fit, trim or omitted native impacts')


def review(capture):
    folder=capture['folder'];side=int(folder.name[-1]);out=ROOT/f'audit_native_kano_laser_audio_p{side}_review'
    need(not out.exists(),'Fresh immutable actual audio review');out.mkdir()
    try:
        transport=json.loads((folder/'report.json').read_text())
        checked=json.loads((folder/'checked_observer_sources.json').read_text())
        need(transport['passed'] and transport['transportOnlyAccepted'] and transport['nativeExit']==0 and transport['wholeGuestMatched'] and
             checked['passed'] and all(sha(p)==h for r in (transport,checked) for p,h in r['inputHashes'].items()),
             'Same physical game actually terminal; full actual guest and every observer input unchanged')
        text=capture['text'];entry=rows(text,'MK2_LASER_ENTRY');winner=rows(text,'MK2_LASER_WINNER');stop=rows(text,'MK2_LASER_STOP')
        need(len(entry)==len(winner)==len(stop)==1 and winner[0]['age']=='196' and stop[0]['age']=='750',
             'Same genuinely earned laser and natural native winner/scene terminal')
        pcm_headers=[r['header'] for r in capture['pcm']];dac_headers=[r['header'] for r in capture['dac']]
        chunks=[r['pixels'] for r in capture['dac']];gate,fault_gate=dac_models(len(chunks))
        native_dac=gate(chunks,dac_headers,pcm_headers);dac_faults=fault_gate(chunks,dac_headers,pcm_headers)
        pins={str(Path(__file__).resolve()):sha(__file__),str(folder/'report.json'):sha(folder/'report.json'),
              str(folder/'checked_observer_sources.json'):sha(folder/'checked_observer_sources.json'),str(folder/'run.log.gz'):sha(folder/'run.log.gz')}
        expected,source_roms=mixer.expected_region(pins);rom_gate,rom_faults=mixer.rom_models(expected);rom_proofs=[];rom_fault_results=[]
        for phase in ('startup','terminal'):
            parts=[r for r in capture['romChunks'] if r['header']['phase']==phase]
            need(len(parts)==192 and [int(r['header']['offset']) for r in parts]==list(range(0,0xc00000,65536)),
                 'All actual sound firmware/data byte lanes and mirrors, in exact order')
            raw=b''.join(r['pixels'] for r in parts);rom_proofs.append(rom_gate(raw,phase));rom_fault_results+=rom_faults(raw,phase)
        sound=waveform(capture,pins)
        (out/'waveform_comparison.json').write_text(json.dumps(sound,indent=2)+'\n')
        need(sound['passed'],'Entire actual native mixed waveform equals untrimmed source prediction')
        terminal=rows(text,'MK2_LAUDIO_CHANNEL_TERMINAL');pool=rows(text,'MK2_LAUDIO_POOL')
        need(len(terminal)==19 and {int(r['channel']) for r in terminal}==set(range(19)) and
             all(r['sample']=='4294967295' for r in terminal), 'All19 actual channels inactive at natural terminal')
        end=[r for r in pool if r['phase']=='terminal']
        need(len(end)==1 and end[0]['actor']==end[0]['main']=='00000000' and end[0]['slots']=='0000,0;0000,0;0000,0;0000,0;0000,0',
             'Actual native scene clears laser ownership and every priority/timer')
        channels=rows(text,'MK2_TOMB_MIX_CHANNEL')
        need(len(channels)==len(chunks)*19 and {(r['index'],int(r['channel'])) for r in channels}==
             {(str(i+1),c) for i in range(len(chunks)) for c in range(19)}, 'Every actual source channel at every consecutive sound callback')
        for row in channels:
            need(row['loop']==row['paused']==row['writes']=='0','Actual source channels nonlooping/unpaused/passive')
            if int(row['channel']) not in (0,14,15,16):need(row['sample']=='4294967295','No omitted imported source in full mix')
        parent=json.loads((ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json').read_text())
        for path in (Path(mixer.__file__),Path(dac_source.__file__),ROOT/'audit_native_kano_laser_audio_call_frame_source/report.json'):
            pins[str(path)]=sha(path)
        report=dict(passed=True,finiteNativeLaserAudioAccepted=True,physicalSlot=side,wholeNativeMixedWaveform=sound,
                    all19ChannelsObserved=True,nativeSceneAudioCleanupAccepted=True,nativeDAC=native_dac,dacFaultsRejected=dac_faults,
                    originalSoundROMProofs=rom_proofs,soundROMFaultsRejected=rom_fault_results,originalSoundROMInputs=source_roms,
                    fullFinisherAccepted=False,fullPortAcceptance=False,wholeNewVisualRegressionAccepted=False,
                    originalNaturalIntegrationRequirements=parent['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=parent['originalRemainingWorkGroups'],
                    inputHashes=pins,goalStatus='active',latestPlayableChanged=False,newROMCopies=0,newRawMedia=0,newZIPs=0,
                    previousGoalTurnClassification='progress: audio source/call-frame qualification, actual Lua parser and private native build initiated',
                    limitations=['One actual earned true Kano versus Sonya laser in the indicated physical slot only.',
                                 'Whole new rasters still require review; no all-victim/CPU/mirror/arena/interrupted-scene/rejoin/full14+6acceptance.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full objective retained')
        (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,finiteNativeLaserAudio=True,physicalSlot=side,stereoFrames=sound['comparedStereoFrames'])),flush=True)
        return report
    except Exception:
        (out/'failure.txt').write_text(traceback.format_exc());raise
