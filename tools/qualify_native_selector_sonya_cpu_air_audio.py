"""Whole native audio, three real Bicycle cues and same-channel cry replacement.

All original DAC/cache/resampler/sample/float-route operations retained. The
next source replaces the old channel at its native source-port sample clock,
as samples_device::start requires. No waveform/gain/time fit or game replay.
Precise owner retirement, all19 channel clocks and heard quality remain open.
"""
import hashlib,inspect,json,struct,traceback
from pathlib import Path
import numpy as np
import qualify_native_selector_sonya_cpu_air_contact_recovery as contact
import current_cpu_compound_audio_model_v6444 as compound
import qualify_native_selector_sonya_cpu_pressure_audio as prior

ROOT,need,sha=contact.ROOT,contact.need,contact.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_air_audio_checked'
ORDER=['FFFD','6B01','6B02','6B01','6B02','6B01','6B02','FFFD']


def bindings(replace_channel=True):
    source=inspect.getsource(compound.predict_mix)
    before="['FFFD','6B01','6B02','6B00','FFFD']"
    need(source.count(before)==1,'Only actual three-kick/two-winner event inventory differs')
    source=source.replace(before,repr(ORDER),1)
    if replace_channel:
        before=' for event in events:\n  for index,head in enumerate(headers):'
        after=" for event in events:\n  next_start=min((e['start'] for e in events if e['channel']==event['channel'] and e['start']>event['start']),default=10**30)\n  for index,head in enumerate(headers):"
        need(source.count(before)==1,'Original per-channel independent sample source histories intact')
        source=source.replace(before,after,1)
        before="valid=(at>=0)&(at<len(event['sample']))"
        need(source.count(before)==1,'All original EOF/interpolation operations, only native next-launch cutoff')
        source=source.replace(before,before+"&(at<next_start-event['start'])",1)
    scope=dict(vars(compound),__file__=__file__)
    exec(compile(source,__file__+'::whole_native_sample_channel_replacement','exec'),scope)
    return scope['predict_mix'],hashlib.sha256(source.encode()).hexdigest().upper()


def cues(text,guest):
    rows=compound.rows
    marks=[r for r in rows(text,'MK2_MAUDIO_SOUND') if r['pc']=='FFFB7140' or r['word'] in ('6B00','6B01','6B02')]
    need([r['word'] for r in marks]==ORDER,'Every actual imported marker, including repeated overlapping cry')
    choices=[r for r in rows(text,'MK2_SONYA_CHOICE_EVENT') if r['kind']=='bicycle']
    need([r['frame'] for r in choices]==['2391','2731','2806'],'All genuine independent native CPU Bicycle choices')
    need(all(r['mask']=='FFFF' and r['writes']=='0' and r['assistance']=='none' for r in marks),'All genuine port stores passive')
    winners=[r for r in marks if r['word']=='FFFD']
    need([(r['frame'],r['pc'],r['a8'],r['a13']) for r in winners]==
         [('2148','FFFB7140','FFFEFF20','0106AA60'),('3182','FFFB7140','FFFEFF20','0106AA60')],'Both true Sonya winner producers')
    launches=[r for r in marks if r['word'] in ('6B01','6B02')]
    for r in launches:
        need(r['frame'] in [c['frame'] for c in choices] and r['a8']=='010350A0' and r['a13']=='0106BF30' and
             r['pc']==('FFF9A4C0' if r['word']=='6B01' else 'FFF9A520'),'Each launch/cry owned by actual CPU Sonya source instruction')
        word=int(r['word'],16);pc=int(r['pc'],16)
        need(guest[(pc-96-0xff800000)//8:(pc-0xff800000)//8]==struct.pack('<6H',0x09e0,word,0,0x0580,0x1030,0x01d0),'Whole executing MOVI and sample-port instructions')
    need(prior.routing_source(guest)['passed'],'Whole native packet/private source boundary')
    return dict(actualBicycleChoiceFrames=[2391,2731,2806],ownedLaunchCryMarkers=6,trueSonyaWinnerMarkers=2,
        completeImportedMarkerOrder=ORDER,startupRing=prior.startup.startup_cue(text,guest),
        sameChannelReplacementSource='samples_device::start: stream->update(), replace source, pos=0',
        preciseOwnerRetirementAccepted=False,allHitGruntProducersAccepted=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable current whole air-trial source-audio proof')
    parent=contact.OUT/'report.json';proof=json.loads(parent.read_text());capture=contact.control.capture
    held=capture.NATIVE_HANDLES[capture.KEY];pins=dict(proof['inputHashes'])
    need(proof['passed'] and held['process'].poll()==0 and held['identity']==proof['actualNativeIdentity'] and all(sha(p)==h for p,h in pins.items()),'Same terminal50372, no new game or changed source')
    audio=capture.AUDIO[capture.KEY];text=capture.RAM_CASES[capture.KEY][1]
    for tag,chunks,headers in (('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders'])):
        records=compound.rows(text,tag)
        need(len(records)==len(chunks)==len(headers)==1646 and all(r==dict(h,sha256=hashlib.sha256(raw).hexdigest().upper()) for r,h,raw in zip(records,headers,chunks,strict=True)),'Every entire actual native PCM/DAC block independently digest bound')
    need(audio['pcmHeaders'][0]['frame']=='1817' and audio['pcmHeaders'][0]['seconds']=='33.220000000000','Actual opening partial callback retained, no trimmed first/tail')
    samples_path=ROOT/'mame-mkp/src/devices/sound/samples.cpp';samples_source=samples_path.read_text()
    need(sha(samples_path)=='8BF4BB350F40B309A5CECB4591DF8EE32A3563C3E061F2D2338C8CBA76B5353F' and
         'chan.stream->update();\n\n\t// update the parameters' in samples_source and
         'chan.pos = 0;' in samples_source,'Exact native flush-before-replacement source, not fitted playback cutoff')
    source_cues=cues(text,state['guest'])
    native_dac,dac_faults,dac_hash=prior.dac_model.dac_models(1646)
    dac=native_dac(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']);raw_faults=list(dac_faults(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']))
    rom_gate,rom_faults=compound.original.rom_models(audio['expectedROM'])
    rom=[rom_gate(bytes(audio['rom'][phase]),phase) for phase in ('startup','terminal')]
    for phase in ('startup','terminal'):raw_faults.extend(rom_faults(bytes(audio['rom'][phase]),phase))
    need(len(raw_faults)==12,'Original DAC plus both complete sound-ROM counterexamples')
    predict,mix_hash=bindings();pcm=np.frombuffer(b''.join(audio['pcmChunks']),'<i2').reshape(-1,2)
    waveform=predict(audio['dacChunks'],audio['dacHeaders'],pcm,text,'sonya',pins)
    OUT.mkdir();(OUT/'waveform.json').write_text(json.dumps(waveform,indent=2)+'\n')
    need(waveform['passed'] and waveform['comparedStereoFrames']==1580160 and waveform['differentChannelSamples']==0 and
         waveform['actualSHA256']==waveform['predictedSHA256'],'Whole actual mixed PCM with real three-kick cry replacement source exact')
    old_predict,_=bindings(False)
    wrong=old_predict(audio['dacChunks'],audio['dacHeaders'],pcm,text,'sonya',dict(pins))
    need(not wrong['passed'] and wrong['differentChannelSamples']>0,'Allowing old/new cry to sum is an effective real source-operation counterexample')
    for p in (Path(__file__),parent,Path(compound.__file__),Path(compound.original.__file__),Path(prior.__file__),
              Path(prior.dac_model.__file__),Path(prior.startup.__file__),samples_path,OUT/'waveform.json',
              ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json',ROOT/'audit_v5379_current_cpu_square_audio_ram_checked/report.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No original source/current proof changed');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All whole source/audio/native inputs unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        wholeMixedWaveform=waveform,wholeNativeDAC=dac,wholeSoundROM=rom,originalDACROMFaultsRejected=raw_faults,
        actualSourceCueProvenance=source_cues,nativeSampleReplacementFault=dict(rejected=True,differentChannelSamples=wrong['differentChannelSamples'],firstDifferences=wrong['firstDifferences']),
        entireSourceModelSHA256=mix_hash,nativeDACModelSHA256=dac_hash,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        wholeActualAudioWaveformAccepted=True,all19ChannelClocksAccepted=False,wholeNativePacketsAccepted=False,
        allOverlapPriorityContextsAccepted=False,heardAudioQualityAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        if not OUT.exists():OUT.mkdir()
        need(not (OUT/'failure.json').exists(),'Preserve actual whole audio rejection')
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
