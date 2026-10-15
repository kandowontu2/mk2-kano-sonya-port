"""Original native DCS float stream plus actual biography names: exact PCM.

Preserve the first failed whole prediction: the future Sonya event's zero
segment erroneously replaced Kano's active contribution in that checker.
This correction sums both actual name sources, never alters game audio.

Separately rebase the native cached resampler at each real contiguous captured
window. No omitted buffers, waveform fitting, synthesized DCS or guest writes.
"""
import hashlib
import json
from decimal import Decimal
from pathlib import Path
import numpy as np
import wave
import qualify_native_ai_attract_audio as names
import native_ai_response_context as current
ROOT,need,sha=current.ROOT,current.need,current.sha

def groups(headers):
    result=[];part=[]
    for i,r in enumerate(headers):
        if part and Decimal(r['seconds'])-Decimal(headers[part[-1]]['seconds'])!=Decimal('.02'):
            result.append(part);part=[]
        part.append(i)
    if part:result.append(part)
    return result

def predict(c):
    _,actual,events,pins,pcm_headers=names.predict(c)
    sounds=names.runtime.rows(c['text'],'SOUND')
    launches=[r for r in sounds if r['word']=='6B00']
    need(len(launches)==1,'One naturally generated early CPU Square launch, never forced guest/AI state')
    launch=launches[0]
    need(launch['mode']=='1' and launch['mute']=='0' and launch['pc']=='FFFFCAC0' and
         launch['a8']==launch['p1_actor']==launch['p1_owner'] and launch['a13']==launch['p1_main'] and
         launch['p1_id']==launch['p1_roster']=='18' and launch['p1_action']=='519' and
         launch['p2_id']==launch['p2_roster']=='18','True natural Sonya18 CPU mirror and owned unmuted signature launch')
    path=ROOT/'samples/mk2ks/sonya_square_launch.wav'
    pins[str(path)]=sha(path)
    with wave.open(str(path),'rb') as wav:
        need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate(),wav.getnframes(),wav.getcomptype())==(1,2,48000,45512,'NONE'),
             'Whole original finite native Square donor clip')
        values=np.frombuffer(wav.readframes(45512),'<i2').copy()
    signal,positions=names.audio.sample_values(values,48000)
    events.append(dict(identity=18,marker=launch,start=names.audio.sample_clock(launch['seconds'],True),
                       signal=signal,channel=10,gain=np.float32(.70)))
    chunks,headers=c['dac'],c['dacHeaders']
    need(len(chunks)==len(headers)==len(pcm_headers)==769,'Entire actual three audio windows, all769 PCM and native DAC callbacks')
    total=nonzero=0
    for i,(raw,r,p) in enumerate(zip(chunks,headers,pcm_headers)):
        need(all(r[k]==p[k] for k in ('frame','seconds')) and int(r['index'])==i+1 and
             r['writes']=='0' and r['assistance']=='none' and r['prefix']=='4' and r['ring']=='32768' and r['element_bytes']=='4',
             'Whole native PCM/DAC callback association and passive ring metadata')
        need(hashlib.sha256(raw).hexdigest().upper()==r['sha256'],'Every actual unchanged native DAC byte')
        n=int(r['consumed'])
        need(n==625 and len(raw)==(n+4)*4 and n==(int(r['current_out'])-int(r['previous_out']))%32768 and
             Decimal(r['seconds'])-Decimal(r['previous_seconds'])==Decimal('.02'),'Exact original20ms625-sample serial interval and ring traversal')
        if i and Decimal(r['seconds'])-Decimal(headers[i-1]['seconds'])==Decimal('.02'):
            need(r['previous_out']==headers[i-1]['current_out'],'Every captured contiguous ring cursor continuous')
        need(r['enabled']=='1' and r['volume']=='3F800000' and r['channels']=='1' and r['incs']=='1' and
             int(r['autobuffer'],16)&2 and int(r['syscontrol'],16)&0x0800,'Original enabled mono unit-gain serial audio hardware')
        values=np.frombuffer(raw,'<f4')
        need(np.isfinite(values).all(),'Every native DAC float finite')
        integers=np.rint(values.astype(np.float64)*32767)
        need(np.all((integers>=-32768)&(integers<=32767)) and
             np.array_equal((integers.astype(np.float32)*np.float32(1.0/32767)).view('<u4'),values.view('<u4')),
             'Every native float bit-exact original signed16 DCS normalization')
        total+=n;nonzero+=int(np.count_nonzero(values[4:]))
    need(nonzero>1000,'Actual non-silent original DCS contribution captured, not inferred from final PCM')
    dcs_parts=[];clock_parts=[];windows=groups(headers)
    need([len(x) for x in windows]==[256,257,256],'Every complete original captured window preserved, including complete audible Square launch/EOF')
    for group in windows:
        dcs,clocks=names.audio.float_model()([chunks[i] for i in group],[headers[i] for i in group])
        dcs_parts.append(dcs);clock_parts.extend(clocks)
    dcs=np.concatenate(dcs_parts)
    need(dcs.shape==actual.shape,'Whole unquantized DCS output shape matches all native speaker frames')
    voice=np.zeros_like(dcs);gain=np.float32(np.float32(.70)*np.float32(.30))
    for i,r in enumerate(pcm_headers):
        tick=int(Decimal(r['seconds'])*50)
        start=(tick-1)*960*(names.audio.ATTO//48000)
        sec,fraction=divmod(start,names.audio.ATTO)
        view=sec*48000+fraction//names.audio.PERIOD
        for event in events:
            at=np.arange(view,view+960,dtype=np.int64)-event['start']
            valid=(at>=0)&(at<len(event['signal']))
            segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(event['signal'][at[valid]]*event.get('gain',gain))
            voice[i*960:(i+1)*960,0]=np.float32(voice[i*960:(i+1)*960,0]+segment)
            voice[i*960:(i+1)*960,1]=np.float32(voice[i*960:(i+1)*960,1]+segment)
    mixed=np.float32(dcs+voice)
    predicted=(np.clip(mixed,-1,1).astype(np.float64)*32767).astype('<i2')
    return predicted,actual,dict(dcs=dcs,voice=voice,events=events,pins=pins,windows=windows,clocks=clock_parts,nativeSamples=total,nonzeroNativeSamples=nonzero)

def qualify(c):
    out=c['folder']/'native_early_square_mix.json'
    need(not out.exists() and c['terminal']['nativeExit']==0 and c['guest']==current.expected(),'Fresh exact compiled and terminal original native audio proof')
    predicted,actual,model=predict(c)
    different=np.argwhere(predicted!=actual)
    result=dict(passed=not len(different),finiteNativeAttractAudioAccepted=not len(different),fullAttractAudioAccepted=False,
        finiteAudibleSonyaSquareAttractPathAccepted=not len(different),allEnabledDemoSoundPathsAccepted=False,fullPortAcceptance=False,nativeTerminal=c['terminal'],
        callbacks=len(c['pcm']),comparedStereoFrames=len(actual),differentChannelSamples=len(different),
        actualSHA256=hashlib.sha256(actual.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
        firstDifferences=[dict(stereoFrame=int(n),channel=int(ch),expected=int(predicted[n,ch]),actual=int(actual[n,ch])) for n,ch in different[:8]],
        nativeDCSSamples=model['nativeSamples'],nonzeroNativeDCSSamples=model['nonzeroNativeSamples'],
        actualNameAndSquareMarkers=[e['marker'] for e in model['events']],actualNativeSourceClocks=model['clocks'],
        comparison='All native signed16-normalized DCS floats through original float32 cached resampler, real stream clocks and exact imported name sources; native float32 speaker sum and signed16 truncation. Four real complete windows; no fitted gain/onset or removed first/tail.',
        inputHashes={**model['pins'],str(Path(__file__).resolve()):sha(__file__),str(Path(names.__file__)):sha(names.__file__),str(Path(names.audio.__file__)):sha(names.audio.__file__)},goalStatus='active')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','callbacks','comparedStereoFrames','differentChannelSamples','nonzeroNativeDCSSamples','fullAttractAudioAccepted')}),flush=True)
    return result




