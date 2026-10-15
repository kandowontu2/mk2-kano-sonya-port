"""Whole source native DAC float32 plus all physically launched battle/winner clips.

No waveform fit, event search, raw files, guest edits or omitted sound callbacks.
Launch clocks come from actual native port instructions, never target PCM.
"""
import hashlib,json,struct,wave
from decimal import Decimal
import numpy as np
import current_tomb_winner_mix_fault_model_v5789 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
rows=original.rows


def predict_mix(chunks,headers,pcm,text,fighter,pins):
 need(fighter=='sonya','True physical Sonya CPU context')
 dcs,clocks=original.float_model()(chunks,headers)
 need(dcs.shape==pcm.shape and len(headers)*960==len(pcm),'Entire unquantized native DAC and PCM')
 qualified=json.loads((ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json').read_text())
 square=json.loads((ROOT/'audit_v5379_current_cpu_square_audio_ram_checked/report.json').read_text())
 need(qualified['passed'] and square['passed'],'Existing original launch assets and compiled ownership route qualified')
 events=[]
 for marker in rows(text,'MK2_MAUDIO_SOUND'):
  if marker['pc']=='FFFB7140':
   need(marker['word']in('FFFE','FFFD'),'Native true added-character winner literal')
   name='kano'if marker['word']=='FFFE'else'sonya'
   values,frequency=original.read_winner(name,pins);sample_id=2 if name=='kano'else 3
   channel=0;gain=np.float32(np.float32(.70)*np.float32(.30))
  elif marker['word']in('6B00','6B01','6B02'):
   index=int(marker['word'],16)-0x6b00
   path=ROOT/'samples/mk2ks'/('sonya_square_launch.wav','sonya_bicycle_launch.wav','sonya_bicycle_cry.wav')[index]
   proof=square if index==0 else qualified
   need(sha(path)==proof['inputHashes'][str(path)],'Whole original battle clip source bytes unchanged')
   pins[str(path)]=sha(path)
   with wave.open(str(path),'rb')as file:
    need(file.getnchannels()==1 and file.getsampwidth()==2 and file.getcomptype()=='NONE','Whole original mono signed16 battle source')
    frequency=file.getframerate();values=np.frombuffer(file.readframes(file.getnframes()),dtype='<i2').copy()
   sample_id=13+index;channel=13 if index==2 else 12;gain=np.float32(.70)
  else:continue
  sample,positions=original.sample_values(values,frequency)
  events.append(dict(marker=marker,channel=channel,sample_id=sample_id,frequency=frequency,length=len(values),
                     gain=gain,start=original.sample_clock(marker['seconds'],True),sample=sample,positions=positions))
 need([e['marker']['word']for e in events]==['FFFD','6B01','6B02','6B00','FFFD'],
      'Whole actual two-round winner/Bicycle-launch/cry/Square marker order')
 voices={c:np.zeros_like(dcs)for c in(0,12,13)}
 for event in events:
  for index,head in enumerate(headers):
   tick=int(Decimal(head['seconds'])*50);mixer_start=(tick-1)*960*(original.ATTO//48000)
   sec,fraction=divmod(mixer_start,original.ATTO)
   view=sec*48000+fraction//original.PERIOD
   at=np.arange(view,view+960,dtype=np.int64)-event['start'];valid=(at>=0)&(at<len(event['sample']))
   segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(event['sample'][at[valid]]*event['gain'])
   voices[event['channel']][index*960:(index+1)*960]+=segment[:,None]
 # Each channel's native route is mixed in original ascending output order.
 voice=np.zeros_like(dcs)
 for channel in range(14):
  if channel in voices:voice=np.float32(voice+voices[channel])
 mixed=np.float32(dcs+voice)
 convert=lambda value:(np.clip(value,-1,1).astype(np.float64)*32767.0).astype('<i2')
 predicted=convert(mixed);different=np.argwhere(predicted!=pcm)
 faults=[]
 if not len(different):
  for label,n,c in [('actual first sample',0,0),('actual final sample',len(pcm)-1,1)]:
   bad=pcm.copy();bad[n,c]^=1;need(not np.array_equal(predicted,bad),'Real PCM bit fault rejected')
   faults.append(dict(label=label,differentChannelSamples=int(np.count_nonzero(predicted!=bad))))
  for label,bad in [('first frame missing',pcm[1:]),('last frame missing',pcm[:-1])]:
   need(bad.shape!=predicted.shape,'Real missing stereo frame rejected');faults.append(dict(label=label,rejectedBy='whole source shape'))
  for channel in voices:
   bad=convert(np.float32(dcs+np.float32(voice-voices[channel])))
   need(not np.array_equal(bad,pcm),'Each actual source channel has audible nonvacuous coverage')
   faults.append(dict(label=f'channel{channel} omitted',differentChannelSamples=int(np.count_nonzero(bad!=pcm))))
  late=np.zeros_like(voice);late[1:]=voice[:-1]
  for label,bad in [('one-sample late source',convert(np.float32(dcs+late))),
                    ('native quantized early',convert(np.float32(convert(dcs).astype('<f4')/np.float32(32767)+voice)))]:
   need(not np.array_equal(bad,pcm),'Whole native source operation fault rejected')
   faults.append(dict(label=label,differentChannelSamples=int(np.count_nonzero(bad!=pcm))))
 return dict(passed=not len(different),comparedStereoFrames=len(pcm),differentChannelSamples=len(different),
  actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
  firstDifferences=[dict(stereoFrame=int(n),callback=int(n)//960+1,channel=int(c),expected=int(predicted[n,c]),actual=int(pcm[n,c]),nativeFloat=float(dcs[n,c]),importedFloat=float(voice[n,c]))for n,c in different[:16]],
  actualRawAndSourceFaultsRejected=faults,actualCallbackSourceClocks=clocks,
  sourceEvents=[{k:(float(v)if k=='gain'else v)for k,v in e.items()if k not in('sample','positions')}for e in events],
  completeChannelRetirementAcceptance=False,completeCuePacketAcceptance=False,fullPortAcceptance=False,
  comparison='whole unchanged native DAC resampler plus actual source-port clocks, original donor interpolation/EOF and float32 routes; no fit')
