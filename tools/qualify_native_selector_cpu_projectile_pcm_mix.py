"""Same current terminal Kano/Sonya game: complete four-cue native mixer.

Preserve the entire original float32 DCS resampler/cached view and winner
source model. Add all actual Square/bicycle launch/cry sources in native
channel order, using executing marker clocks, not waveform/position fitting.
Whole sample-position bits checked on sound and video callbacks, including
the original60Hz playing() updates and its short-circuit on channel12.
"""
import hashlib,inspect,json,struct,traceback,wave
from bisect import bisect_right
from decimal import Decimal
from pathlib import Path
import numpy as np
import qualify_native_selector_cpu_projectile_pcm_inventory as inventory

capture=inventory.capture
model=capture.prior.audio_model
ROOT,need,sha=inventory.ROOT,inventory.need,inventory.sha
OUT=ROOT/'audit_native_selector_cpu_projectile_pcm_mix_checked'
SPECS=(('6B00',13,12,'sonya_square_launch.wav',45512),
       ('6B01',14,12,'sonya_bicycle_launch.wav',40720),
       ('6B02',15,13,'sonya_bicycle_cry.wav',66523))


def sources(text,pins):
    commands=model.rows(text,'MK2_MAUDIO_SOUND');result=[]
    for word,sample,channel,name,length in SPECS:
        selected=[r for r in commands if r['word']==word]
        need(len(selected)==1,'One actual owned source marker '+word)
        marker=selected[0];path=ROOT/'samples/mk2ks'/name
        need(str(path)in pins and sha(path)==pins[str(path)],'Whole actual compiled source clip '+name)
        with wave.open(str(path),'rb')as clip:
            need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==
                 (1,2,48000,length),'Complete original48kHz source dimensions')
            values=np.frombuffer(clip.readframes(length),dtype='<i2').copy()
        result.append(dict(word=word,sample=sample,channel=channel,name=name,length=length,
            marker=marker,start=model.sample_clock(marker['seconds'],True),values=values))
    return result


def mixer():
    source=inspect.getsource(model.predict_mix)
    signature='def predict_mix(chunks,headers,pcm,text,fighter,pins):'
    need(source.count(signature)==1,'Whole original float32 resampler/winner mixer')
    source=source.replace(signature,'def predict_mix(chunks,headers,pcm,text,fighter,pins,extra):',1)
    marker=' mixed=np.float32(dcs+voice)'
    inserted='''
 source_contributions=[]
 # samples.cpp stream output gains and .70 native route; original channel0
 # has separate .30 volume, already preserved in the unchanged winner model.
 for spec in extra:
  sample,_=sample_values(spec['values'],48000)
  part=np.zeros_like(dcs)
  for index,head in enumerate(headers):
   tick=int(Decimal(head['seconds'])*50)
   mixer_start=(tick-1)*960*(ATTO//48000)
   sec,fraction=divmod(mixer_start,ATTO);view=sec*48000+fraction//PERIOD
   at=np.arange(view,view+960,dtype=np.int64)-spec['start']
   valid=(at>=0)&(at<len(sample));segment=np.zeros(960,dtype='<f4')
   segment[valid]=np.float32(sample[at[valid]]*np.float32(.70))
   part[index*960:(index+1)*960,0]=segment;part[index*960:(index+1)*960,1]=segment
  source_contributions.append(part)
  voice=np.float32(voice+part)
 mixed=np.float32(dcs+voice)'''
    need(source.count(marker)==1,'Add every real imported source without replacing native cache/mixer operations')
    source=source.replace(marker,inserted,1)
    # Keep all original actual PCM/source-operation faults; add individual
    # effective source omissions, simultaneous cry timing and channel gain.
    marker=' return dict(passed=not len(different),actualRawMixedPCMFaultsRejected=raw_faults,'
    inserted='''
 additive_faults=[]
 if not len(different):
  convert=lambda value:(np.clip(value,-1,1).astype(np.float64)*32767.0).astype('<i2')
  for spec,part in zip(extra,source_contributions,strict=True):
   wrong_voice=voice-part
   wrong=convert(np.float32(dcs+wrong_voice))
   need(not np.array_equal(wrong,pcm),'Every actual imported source omission is effective '+spec['name'])
   additive_faults.append(dict(fault='omit '+spec['name'],differentChannelSamples=int(np.count_nonzero(wrong!=pcm))))
  late=np.zeros_like(source_contributions[-1]);late[1:]=source_contributions[-1][:-1]
  wrong=convert(np.float32(dcs+np.float32(voice-source_contributions[-1]+late)))
  need(not np.array_equal(wrong,pcm),'Actual simultaneous cry shifted by one output sample rejected')
  additive_faults.append(dict(fault='bicycle cry one-sample late',differentChannelSamples=int(np.count_nonzero(wrong!=pcm))))
  wrong=convert(np.float32(dcs+np.float32(voice-source_contributions[1]+np.float32(source_contributions[1]*np.float32(.30)))))
  need(not np.array_equal(wrong,pcm),'Actual bicycle channel wrongly given announcement volume rejected')
  additive_faults.append(dict(fault='bicycle launch wrong .30 channel volume',differentChannelSamples=int(np.count_nonzero(wrong!=pcm))))
 return dict(additionalActualSourceFaultsRejected=additive_faults,
  completeExtraSources=[{k:v for k,v in spec.items()if k!='values'}for spec in extra],
  passed=not len(different),actualRawMixedPCMFaultsRejected=raw_faults,'''
    need(source.count(marker)==1,'Preserve original complete comparison and all original faults')
    source=source.replace(marker,inserted,1)
    scope=dict(vars(model),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_native_mix_plus_all_actual_cues','exec'),scope)
    return scope['predict_mix'],hashlib.sha256(source.encode()).hexdigest().upper()


def channel_clocks(text,headers,extra,waveform):
    ticks=[Decimal(h['seconds'])for h in headers]
    markers=model.rows(text,'MK2_MAUDIO_SOUND')
    winner=next(r for r in markers if r['pc']=='FFFB7140')
    winner_start=model.sample_clock(winner['seconds'],True)
    winner_values,winner_frequency=model.read_winner('sonya',{})
    _,winner_positions=model.sample_values(winner_values,winner_frequency)
    with wave.open(str(ROOT/'samples/mk2ks/sonya_select.wav'),'rb')as clip:
        selection=np.frombuffer(clip.readframes(clip.getnframes()),'<i2').copy()
    _,selection_positions=model.sample_values(selection,16000)
    period=model.ATTO//60
    def atto(clock):return int(Decimal(clock)*model.ATTO)
    def ceil_index(value):
        sec,fraction=divmod(value,model.ATTO)
        return sec*48000+(fraction+model.PERIOD-1)//model.PERIOD
    def playing_position(spec,clock,video,last_sound):
        if Decimal(clock)<Decimal(spec['marker']['seconds']):return 0
        processed=max(0,model.sample_clock(last_sound,True)-spec['start'])
        if video:
            # Original battle timer starts on Square launch, retires at EOF,
            # then starts afresh on bicycle launch. Native short-circuit only
            # updates cry at60Hz once channel12 has reached its own EOF.
            parent=extra[0]if spec['word']=='6B00'else extra[1]
            origin=atto(parent['marker']['seconds']);now=atto(clock)
            n=max(0,(now-origin)//period)
            if spec['channel']==12 or (spec['word']=='6B02'and n*800>=extra[1]['length']):
                timer_clock=origin+n*period
                processed=max(processed,max(0,ceil_index(timer_clock)-spec['start']))
        return min(spec['length'],processed)
    def expected(channel,clock,video):
        i=bisect_right(ticks,Decimal(clock))-1
        last=headers[i]['seconds']if i>=0 else str(Decimal(headers[0]['seconds'])-Decimal('.02'))
        if channel==0:
            if Decimal(clock)<Decimal(winner['seconds']):return 0xffffffff,18400,selection_positions[-1]
            processed=max(0,model.sample_clock(last,True)-winner_start)
            pos=winner_positions[min(processed,len(winner_positions))-1]if processed else 0.0
            return 3 if 0<=processed<len(winner_positions)else 0xffffffff,32000,pos
        if channel in(12,13):
            candidates=[s for s in extra if s['channel']==channel and Decimal(s['marker']['seconds'])<=Decimal(clock)]
            if not candidates:return 0xffffffff,0,0.0
            spec=candidates[-1];pos=playing_position(spec,clock,video,last)
            number=14 if spec['word']=='6B01'and pos<spec['length']else 0xffffffff
            return number,spec['length'],float(pos)
        return 0xffffffff,0,0.0
    counts={}
    for tag,video in(('MK2_MAUDIO_CHANNEL',True),('MK2_TOMB_MIX_CHANNEL',False)):
        records=model.rows(text,tag);counts[tag]=len(records)
        for r in records:
            want=expected(int(r['channel']),r['seconds'],video)
            actual=(int(r['sample']),int(r['length']),float(r['pos']if video else r['position']))
            need(actual==want,'Every source-derived native channel/length/position '+tag+' '+str((r['frame'],r['channel'],actual,want)))
            if not video:need(r['bits']==struct.pack('<d',want[2]).hex().upper(),'Every exact channel source-position bit')
            need(r['loop']==r['paused']==r['writes']=='0'and r['assistance']=='none','Entire passive nonlooping channel ledger')
    return dict(passed=True,completeVideoRows=counts['MK2_MAUDIO_CHANNEL'],completeSoundRows=counts['MK2_TOMB_MIX_CHANNEL'],
        sourceStarts=[dict(word=s['word'],streamIndex=s['start'],markerSeconds=s['marker']['seconds'])for s in extra],
        sourceChannelOrder=[0,12,13],winnerStart=winner_start,firstLoadMinusOneNotAssumedSilent=True,
        sourceOwnerTimerHz=60,videoPositionsUseNativeShortCircuit=True,noPositionOrWaveformFit=True)


def execute(state):
    need(not OUT.exists()and not capture.prior.current.prior.identity.census(),'Same original terminal capture; no native replay')
    receipt_path=inventory.OUT/'report.json';receipt=json.loads(receipt_path.read_text())
    need(receipt['passed']and receipt['actualNativeIdentity']['ProcessId']==47172 and
         all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Entire current native DAC/ROM/source inventory remains immutable')
    folder,text,images=capture.RAM_CASES[capture.KEY];audio=capture.AUDIO[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY]
    need(held['process'].poll()==0 and held['identity']==receipt['actualNativeIdentity'],'Exact original native terminal handle')
    pins=dict(receipt['inputHashes']);extra=sources(text,pins)
    predict,model_hash=mixer()
    pcm=np.frombuffer(b''.join(audio['pcmChunks']),dtype='<i2').reshape(-1,2)
    waveform=predict(audio['dacChunks'],audio['dacHeaders'],pcm,text,'sonya',pins,extra)
    clocks=None
    if waveform['passed']:clocks=channel_clocks(text,audio['pcmHeaders'],extra,waveform)
    # Always preserve actual whole-window disagreement, not only a green result.
    for path in(Path(__file__),Path(model.__file__),receipt_path,ROOT/'samples/mk2ks/sonya_select.wav'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Complete immutable current source inventory after whole source prediction')
    OUT.mkdir();capture.prior.current.prior.save(OUT/'waveform.json',waveform)
    report=dict(passed=waveform['passed']and clocks is not None,goalStatus='active',actualNativeIdentity=held['identity'],
        entireSourceModelSHA256=model_hash,wholeMixedWaveform=waveform,wholeSourceChannelClocks=clocks,
        requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],inputHashes=pins,
        fullArtAudioAllContextsAcceptance=False,heardAudioQualityAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    capture.prior.current.prior.save(OUT/'report.json',report)
    print('CURRENT_ALL_CUE_PCM '+json.dumps(dict(passed=report['passed'],stereoFrames=waveform['comparedStereoFrames'],differentChannelSamples=waveform['differentChannelSamples'])),flush=True)
    return report


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original actual mixer rejection')
        OUT.mkdir();capture.prior.current.prior.save(OUT/'failure.json',dict(passed=False,goalStatus='active',error=repr(error),
            traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False))
        raise
