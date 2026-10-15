"""Full captured attract PCM versus native name clips and muted startup windows.

No baseline replay, timing/gain fitting or native state changes. If original
DCS contributes to a window, exact name-only equality will not be accepted.
This finite default-mute run cannot prove the enabled-demo-sound DIP path.
"""
import copy
import hashlib
import json
import wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import current_tomb_winner_mix_fault_model_v5789 as audio
import qualify_native_ai_response_attract as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha

def predict(c,clip_overrides=None):
    sounds=runtime.rows(c['text'],'SOUND')
    names=[r for r in sounds if r['word'] in ('FFFC','FFFB')]
    need([r['word'] for r in names]==['FFFC','FFFB'] and
         all(r['pc']=='FFFB77C0' and r['mode']=='1' and r['mute']=='0' for r in names),
         'Both actual native unmuted biography announcements, no stock packet alias')
    pins={};events=[]
    for row in names:
        identity=17 if row['word']=='FFFC' else 18
        path=ROOT/'samples/mk2ks'/('kano_select.wav' if identity==17 else 'sonya_select.wav')
        pins[str(path)]=sha(path)
        with wave.open(str(path),'rb') as wav:
            need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate(),wav.getnframes(),wav.getcomptype())==(1,2,16000,18400,'NONE'),
                 'Whole original mono16kHz18400-sample native name waveform')
            values=np.frombuffer(wav.readframes(18400),'<i2').copy()
        if clip_overrides and identity in clip_overrides:values=clip_overrides[identity]
        signal,positions=audio.sample_values(values,16000)
        events.append(dict(identity=identity,marker=row,start=audio.sample_clock(row['seconds'],True),signal=signal))
    gain=np.float32(np.float32(.70)*np.float32(.30))
    expected=[];actual=[];headers=[]
    for record in c['pcm']:
        head,raw=record['header'],record['pixels']
        need(hashlib.sha256(raw).hexdigest().upper()==head['sha256'] and len(raw)==3840,'Every full unchanged captured stereo960-frame native PCM callback')
        tick=int(Decimal(head['seconds'])*50)
        start=(tick-1)*960*(audio.ATTO//48000)
        sec,fraction=divmod(start,audio.ATTO)
        view=sec*48000+fraction//audio.PERIOD
        segment=np.zeros(960,dtype='<f4')
        for event in events:
            at=np.arange(view,view+960,dtype=np.int64)-event['start']
            valid=(at>=0)&(at<len(event['signal']))
            segment[valid]=np.float32(segment[valid]+np.float32(event['signal'][at[valid]]*gain))
        mono=(np.clip(segment,-1,1).astype(np.float64)*32767.0).astype('<i2')
        expected.append(np.column_stack((mono,mono)))
        actual.append(np.frombuffer(raw,'<i2').reshape(960,2))
        headers.append(head)
    return np.concatenate(expected),np.concatenate(actual),events,pins,headers

def qualify(c):
    out=c['folder']/'native_attract_audio_finite.json'
    need(not out.exists() and c['terminal']['nativeExit']==0,'Fresh finite actual audio proof on same terminal native run')
    expected,actual,events,pins,headers=predict(c)
    differences=np.argwhere(expected!=actual)
    owners={int(r['frame']):r for r in runtime.rows(c['text'],'AUDIO_OWNER')}
    channels=runtime.rows(c['text'],'CHANNEL')
    muted=[r for r in channels if owners[int(r['frame'])]['mode']=='1' and owners[int(r['frame'])]['mute']=='1' and int(r['channel'])>=10]
    need(muted and all(r['length']=='0' and float(r['pos'])==0 and r['sample']=='4294967295' for r in muted),
         'All four actual startup channels stay silent and unowned in every captured native-muted attract field')
    faults=[]
    if not len(differences):
        for label,at,channel in (('first actual PCM sample',0,0),('final actual PCM sample',len(actual)-1,1)):
            bad=actual.copy();bad[at,channel]^=1
            need(not np.array_equal(expected,bad),'Actual PCM bit counterexample rejected')
            faults.append(dict(fault=label,differentSamples=int(np.count_nonzero(expected!=bad))))
        need(expected.shape!=actual[:-1].shape,'Entire final stereo frame cannot be omitted')
        faults.append(dict(fault='omitted final stereo frame',rejected=True))
    result=dict(passed=not len(differences),finiteDefaultAttractAudioAccepted=not len(differences),
        fullAttractAudioAccepted=False,enabledDemoSoundPathAccepted=False,fullPortAcceptance=False,
        nativeTerminal=c['terminal'],comparedPCMCallbacks=len(headers),comparedStereoFrames=len(actual),
        actualSHA256=hashlib.sha256(actual.tobytes()).hexdigest().upper(),expectedSHA256=hashlib.sha256(expected.tobytes()).hexdigest().upper(),
        differentChannelSamples=len(differences),firstDifferences=[dict(stereoFrame=int(n),channel=int(ch),expected=int(expected[n,ch]),actual=int(actual[n,ch])) for n,ch in differences[:8]],
        actualBiographyMarkers=[e['marker'] for e in events],nativeMutedStartupChannelSnapshots=len(muted),
        actualRawPCMCorruptionsRejected=faults,sourceFloat32Gain=float(np.float32(np.float32(.70)*np.float32(.30))),
        wholeCapturedPCMHeaders=headers,inputHashes={**pins,str(Path(__file__).resolve()):sha(__file__),str(Path(audio.__file__)):sha(audio.__file__)},
        comparison='Entire captured native stereo buffer, exact source stream clocks, repeated-double +2 lookahead interpolation, finite last-sample fill, float32 .70*.30 route and native s16 truncation. No fitted gain/onset or removed first/tail.',goalStatus='active')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','comparedPCMCallbacks','comparedStereoFrames','differentChannelSamples','nativeMutedStartupChannelSnapshots','fullAttractAudioAccepted')}),flush=True)
    return result
