"""Source-exact native float resampler plus original samples.cpp winner mix.

No waveform/time/gain fits. Keep native resampling unquantized until original
float32 speaker addition, then original clamp/truncating s16 conversion.
The entire native5596 resampler/cache loop is preserved in the float carrier.
"""
import hashlib,inspect,json,math,re,wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import current_tomb_source_audio_model_v5748 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
dac_models=native.dac_models
expected_region=native.expected_region
rom_models=native.rom_models
ATTO=10**18
PERIOD=(ATTO+48000-1)//48000


def float_model():
 original=native.predict_waveform
 code=inspect.getsource(original)
 before='def predict_waveform(chunks,headers,pcm):'
 need(code.count(before)==1,'Whole original native predictor function')
 code=code.replace(before,'def native_float(chunks,headers):',1)
 before='def convert(value):return int(max(-1.0,min(1.0,float(value)))*32767.0)'
 need(code.count(before)==1,'Only original final conversion delayed until complete speaker mix')
 code=code.replace(before,'def convert(value):return np.float32(value)',1)
 marker="    guessed=np.asarray(predicted,dtype='<i2')"
 need(code.count(marker)==1,'Original full resampler/cache body retained without trimming')
 code=code[:code.index(marker)]+"    return np.asarray(predicted,dtype='<f4'),clocks\n"
 scope=dict(original.__globals__)
 exec(compile(code,__file__+'::whole5596_native_float_before_final_mix','exec'),scope)
 fn=scope['native_float'];fn.source=code;return fn


def sample_clock(seconds,up):
 at=int(Decimal(seconds)*ATTO);sec,fraction=divmod(at,ATTO)
 return sec*48000+(fraction+(PERIOD-1 if up else 0))//PERIOD


def read_winner(fighter,pins):
 path=ROOT/'samples/mk2ks'/('kano_wins.wav'if fighter=='kano'else'sonya_wins.wav')
 expected={'kano':'92F3DAB113955587D74CC9E36141000E4A7BCB387FE38C5D07BBF9DA7ABD18B2',
  'sonya':'E48F2273BE4262D116FD62513693CD7EF8B17B61B6797C0CA6064263CD0B3564'}[fighter]
 need(sha(path)==expected,'Whole original donor winner clip bytes retained')
 pins[str(path)]=expected
 with wave.open(str(path),'rb')as reader:
  need(reader.getnchannels()==1 and reader.getsampwidth()==2 and reader.getframerate()==16000 and
   reader.getnframes()==32000 and reader.getcomptype()=='NONE','Actual original mono16000Hz/32000sample signed16 winner source')
  values=np.frombuffer(reader.readframes(32000),dtype='<i2').copy()
 return values,16000


def sample_values(values,frequency):
 # Original repeated-double position advances; not closed-form n*step.
 step=float(frequency)/48000
 position=0.0;positions=[];output=[]
 scale=np.float32(1.0/32768.0)
 while position<len(values):
  floor=math.floor(position);fraction=position-floor
  v=float(scale)*((1.0-fraction)*float(values[floor])+fraction*float(values[(floor+2)%len(values)]))
  output.append(np.float32(v));position+=step;positions.append(position)
 # samples.cpp fills beginning at the terminating sampindex, overwriting its
 # just-written interpolated sample; every native tail remains represented.
 output[-1]=np.float32(0.0)
 return np.asarray(output,dtype='<f4'),positions


def rows(text,tag):
 result=[]
 for line in text.splitlines():
  if line.startswith(tag+' '):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);r=dict(pairs)
   need(len(pairs)==len(r),'Unique actual mixed source-clock keys');result.append(r)
 return result


def predict_mix(chunks,headers,pcm,text,fighter,pins):
 fn=float_model();dcs,clocks=fn(chunks,headers)
 need(dcs.shape==pcm.shape and len(headers)*960==len(pcm),'Entire actual unquantized native window and PCM, no removed first/tail')
 markers=[r for r in rows(text,'MK2_MAUDIO_SOUND')if r['pc']=='FFFB7140']
 need(len(markers)==1 and markers[0]['word']==('FFFE'if fighter=='kano'else'FFFD'),
  'One actual true-character native winner marker before sample stream start')
 marker=markers[0]
 values,frequency=read_winner(fighter,pins);sample,positions=sample_values(values,frequency)
 start=sample_clock(marker['seconds'],True)
 gain=np.float32(np.float32(0.70)*np.float32(0.30))
 voice=np.zeros_like(dcs);callback_states=[];first_offset=None
 for index,head in enumerate(headers):
  tick=int(Decimal(head['seconds'])*50)
  mixer_start=(tick-1)*960*(ATTO//48000)
  sec,fraction=divmod(mixer_start,ATTO);view=sec*48000+fraction//PERIOD
  at=np.arange(view,view+960,dtype=np.int64)-start
  valid=(at>=0)&(at<len(sample))
  segment=np.zeros(960,dtype='<f4')
  segment[valid]=np.float32(sample[at[valid]]*gain)
  voice[index*960:(index+1)*960,0]=segment;voice[index*960:(index+1)*960,1]=segment
  if first_offset is None and valid.any():first_offset=index*960+int(np.flatnonzero(valid)[0])
  end_tick=tick*960*(ATTO//48000);s,f=divmod(end_tick,ATTO)
  processed=max(0,s*48000+(f+PERIOD-1)//PERIOD-start)
  expected_pos=positions[min(processed,len(positions))-1]if processed else 0.0
  callback_states.append(dict(index=index+1,frame=int(head['frame']),seconds=head['seconds'],
   samplesProcessed=min(processed,len(positions)),position=expected_pos,
   active=0<processed<len(positions)))
 mixed=np.float32(dcs+voice)
 predicted=(np.clip(mixed,-1,1).astype(np.float64)*32767.0).astype('<i2')
 different=np.argwhere(predicted!=pcm)
 diffs=[dict(stereoFrame=int(n),callback=int(n)//960+1,channel=int(c),expected=int(predicted[n,c]),actual=int(pcm[n,c]),
  nativeFloat=float(dcs[n,c]),winnerFloat=float(voice[n,c]))for n,c in different[:16]]
 raw_faults=[];source_faults=[]
 if not len(different):
  # Alter copies of the actual native PCM in RAM, never guest or audio state.
  for label,index,channel in [('actual first PCM sample',0,0),('actual final PCM sample',len(pcm)-1,1)]:
   bad=pcm.copy();bad[index,channel]^=1
   need(not np.array_equal(predicted,bad),'Actual changed PCM must fail full source equality')
   raw_faults.append(dict(label=label,rejectedBy='complete source equality',differentChannelSamples=int(np.count_nonzero(predicted!=bad))))
   need(np.array_equal(predicted,pcm),'Whole actual positive restored after raw bit counterexample')
  need(predicted.shape!=pcm[:-1].shape,'Actual omitted last stereo frame rejected')
  raw_faults.append(dict(label='actual last stereo frame omitted',rejectedBy='complete source shape',actualFrames=len(pcm)-1))
  bad=pcm[1:].copy()
  need(predicted.shape!=bad.shape,'Actual omitted first cached speaker value rejected')
  raw_faults.append(dict(label='actual first cached stereo frame omitted',rejectedBy='complete source shape',actualFrames=len(bad)))
  convert=lambda value:(np.clip(value,-1,1).astype(np.float64)*32767.0).astype('<i2')
  late=np.zeros_like(voice);late[1:]=voice[:-1]
  native_integer=convert(dcs).astype('<f4')/np.float32(32767.0)
  for label,wrong in [
   ('winner source omitted',convert(dcs)),
   ('one-sample source-start clock late',convert(np.float32(dcs+late))),
   ('original .70 route gain omitted',convert(np.float32(dcs+np.float32(voice/np.float32(.70))))),
   ('native source quantized before speaker addition',convert(np.float32(native_integer+voice)))]:
   need(wrong.shape==pcm.shape and not np.array_equal(wrong,predicted)and not np.array_equal(wrong,pcm),
    'Nonvacuous whole source-operation fault rejected '+label)
   source_faults.append(dict(label=label,rejectedBy='complete actual native mixed waveform',
    differentChannelSamples=int(np.count_nonzero(wrong!=pcm))))
   need(np.array_equal(predicted,pcm),'Entire source-positive restored after every operation fault')
 return dict(passed=not len(different),actualRawMixedPCMFaultsRejected=raw_faults,
  actualMixedSourceOperationFaultsRejected=source_faults,
  actualMixedRawPCMByteFaultSuiteAccepted=not len(different)and len(raw_faults)==4 and len(source_faults)==4,
  comparedStereoFrames=len(pcm),differentChannelSamples=len(different),
  firstDifferences=diffs,actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),
  predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
  sourceSelectedWinnerSample=2 if fighter=='kano'else 3,sourceWinnerFrequency=frequency,
  sourceWinnerLength=len(values),sourceOutputSamples=len(sample),sourceMarker=marker,
  sourceStartStreamIndex=start,sourceFirstWindowSample=first_offset,
  sourceFloat32CompositeGain=float(gain),sourceFloat32CompositeGainBits=hashlib.sha256(gain.tobytes()).hexdigest().upper(),
  maximumMixedMagnitude=float(np.max(np.abs(mixed))),actualCallbackSourceClocks=clocks,
  expectedWinnerCallbackStates=callback_states,comparison='whole native float32 resampler/cache plus original repeated-double/next+2/terminal-fill winner source and native stream-clock/speaker gains; no fit or sample search',
  completeStageVictimAudioAccepted=False,fullPortAcceptance=False)
