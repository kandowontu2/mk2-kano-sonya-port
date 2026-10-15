"""Original native float clock plus separate source-ordered Friendship voices.

Preserve the entire5596 cached native resampler and5789 original samples.cpp
interpolation/end-fill model. Clip starts come from actual native marker times,
not waveform fitting; the speaker adds fourteen inputs in source order.
"""
import hashlib,struct,wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import current_tomb_winner_mix_fault_model_v5789 as original
import run_current_friendship_ram_audio_v3561 as hardware
ROOT,need,sha=original.ROOT,original.need,original.sha
NAMES=['kano_select','sonya_select','kano_wins','sonya_wins','sonya_kiss','kano_extract',
       'sonya_burn_fire','sonya_burn_victim','kano_bubble_pop','sonya_chicken_a5','sonya_chicken_aa',
       'sonya_chicken_af','sonya_chicken_96','sonya_square_launch','sonya_bicycle_launch','sonya_bicycle_cry']

def predict_mix(chunks,headers,pcm,text,fighter,pins):
 native,clocks=original.float_model()(chunks,headers)
 need(native.shape==pcm.shape and len(headers)*960==len(pcm),'Whole native float source and complete PCM window')
 _,assets=hardware.retained_templates()
 # The retained asset dictionary is keyed by actual file stem.
 for name,asset in assets.items():pins[str(ROOT/'samples/mk2ks'/(name+'.wav'))]=asset['sha256']
 pins[str(hardware.OLD)]=sha(hardware.OLD)
 marker_rows=original.rows(text,'MK2_MAUDIO_SOUND');events=[];clips={};positions={}
 for r in marker_rows:
  word=int(r['word'],16);channel=sample=None;gain=None
  if 0x6aa0<=word<=0x6ab3:channel=4+(word-0x6aa0)%5;sample=9+(word-0x6aa0)//5;gain=np.float32(.70)
  elif word==0x6ab4:channel=9;sample=8;gain=np.float32(.70)
  elif r['pc']not in('FFA13C90','FFA13D60')and word in(0xfffe,0xfffd):
   channel=0;sample=2 if word==0xfffe else 3;gain=np.float32(np.float32(.70)*np.float32(.30))
  if channel is None:continue
  need(r['mask']=='FFFF','Actual complete imported marker word')
  if sample not in clips:
   path=ROOT/'samples/mk2ks'/(NAMES[sample]+'.wav');pins[str(path)]=sha(path)
   with wave.open(str(path),'rb')as reader:
    need(reader.getnchannels()==1 and reader.getsampwidth()==2 and reader.getcomptype()=='NONE','Original mono signed16 source')
    frequency=reader.getframerate();values=np.frombuffer(reader.readframes(reader.getnframes()),dtype='<i2').copy()
   if sample in(2,3):original.read_winner('kano'if sample==2 else'sonya',pins)
   else:need(NAMES[sample]in assets and sha(path)==assets[NAMES[sample]]['sha256'],'Whole actual original hardware-derived Friendship clip')
   clips[sample],positions[sample]=original.sample_values(values,frequency)
  events.append(dict(channel=channel,sample=sample,start=original.sample_clock(r['seconds'],True),
                     seconds=r['seconds'],frame=r['frame'],pc=r['pc'],word=r['word'],gain=float(gain)))
 need(sum(e['channel']==0 for e in events)==1 and sum(e['channel']!=0 for e in events)==(1 if fighter=='kano'else 39),
      'Full real own winner and all native Friendship cue events')
 ticks=[int(Decimal(h['seconds'])*50)for h in headers]
 view=[]
 for tick in ticks:
  at=(tick-1)*960*(original.ATTO//48000);sec,fraction=divmod(at,original.ATTO)
  first=sec*48000+fraction//original.PERIOD;view.append(np.arange(first,first+960,dtype=np.int64))
 view=np.concatenate(view);voice=np.zeros(len(pcm),dtype='<f4');components={}
 for channel in range(14):
  component=np.zeros(len(pcm),dtype='<f4');sequence=[e for e in events if e['channel']==channel]
  for i,event in enumerate(sequence):
   values=clips[event['sample']];at=view-event['start'];valid=(at>=0)&(at<len(values))
   if i+1<len(sequence):valid &= view<sequence[i+1]['start']
   component[valid]=np.float32(values[at[valid]]*np.float32(event['gain']))
  voice=np.float32(voice+component)
  if sequence:components[channel]=component
 mixed=np.float32(native+voice[:,None])
 convert=lambda x:(np.clip(x,-1,1).astype(np.float64)*32767.0).astype('<i2')
 predicted=convert(mixed);different=np.argwhere(predicted!=pcm)
 faults=[]
 if not len(different):
  for label,index,channel in [('first real sample',0,0),('last real sample',len(pcm)-1,1)]:
   bad=pcm.copy();bad[index,channel]^=1;need(not np.array_equal(predicted,bad),'Real PCM bit fault rejects')
   faults.append(dict(kind=label,differentChannelSamples=int(np.count_nonzero(predicted!=bad))))
  need(predicted.shape!=pcm[:-1].shape and predicted.shape!=pcm[1:].shape,'Missing actual first/tail rejected')
  faults.extend(dict(kind=k)for k in('first cached stereo frame omitted','last stereo frame omitted'))
  for channel,component in components.items():
   wrong=convert(np.float32(native+np.float32(voice-component)[:,None]))
   need(not np.array_equal(wrong,pcm),'Nonvacuous separate source omission rejects')
   faults.append(dict(kind='source channel '+str(channel)+' omitted',differentChannelSamples=int(np.count_nonzero(wrong!=pcm))))
  late=np.zeros_like(voice);late[1:]=voice[:-1]
  for label,wrong_voice in [('one-sample source-start late',late),('Friendship wrongly reduced to winner level',np.float32(voice*np.float32(.30)))]:
   wrong=convert(np.float32(native+wrong_voice[:,None]));need(not np.array_equal(wrong,pcm),'Wrong source operation rejects')
   faults.append(dict(kind=label,differentChannelSamples=int(np.count_nonzero(wrong!=pcm))))
  need(np.array_equal(predicted,pcm),'Unmodified whole positive restored')
 result=dict(passed=not len(different),comparedStereoFrames=len(pcm),differentChannelSamples=len(different),
      firstDifferences=[dict(stereoFrame=int(n),channel=int(c),expected=int(predicted[n,c]),actual=int(pcm[n,c]),
                            nativeFloat=float(native[n,c]),voiceFloat=float(voice[n]))for n,c in different[:16]],
      actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
      completeMarkerEvents=events,sourceOrderedActiveChannels=sorted(components),maximumMixedMagnitude=float(np.max(np.abs(mixed))),
      actualWholeMixedFaultsRejected=faults,nativeSourceCallbackCount=len(clocks),
      comparison='Entire original native cached resampler and actual source clocks; separate exact original clips/positions/float32 gains and ascending-channel speaker addition; no fit, gain search or trimming')
 return result
