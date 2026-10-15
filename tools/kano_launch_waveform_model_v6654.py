"""Original DAC float/resampler plus complete real Kano launch sample sources.

Native port clocks alone choose both starts. No waveform fits, packet pruning,
gain tuning, cached-value omissions, tail trimming or invented sound commands.
"""
import hashlib,json,wave
from decimal import Decimal
import numpy as np
import current_tomb_winner_mix_fault_model_v5789 as original
import kano_ball_launch_context_v6642 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
rows=original.rows

def predict(record):
 buffers,text,side,enabled=record['buffers'],record['text'],record['side'],record['enabled']
 pcm=np.frombuffer(b''.join(buffers['pcm']),'<i2').reshape(-1,2)
 dcs,clocks=original.float_model()(buffers['dac'],buffers['dacHeaders'])
 headers=buffers['pcmHeaders']
 need(dcs.shape==pcm.shape and len(headers)*960==len(pcm),'Entire native DAC and output window')
 markers=[r for r in rows(text,'MK2_MAUDIO_SOUND')if r['word']=='6B03']
 entries=[r for r in rows(text,'MK2_HSPECIAL_EVENT')if r['entry']=='FFFFDE00']
 need(len(markers)==len(entries)==2 and [m['frame']for m in markers]==[e['frame']for e in entries]and
      all(m['mask']=='FFFF'and m['a8']==e['actor']and m['a13']==e['main']and m['pc']=='FFFFDEC0'for m,e in zip(markers,entries)),
      'Exactly one real native port cue at each of the two true owned roll entries')
 asset=ROOT/current.NAME/'samples/mk2ks/kano_ball_launch.wav'
 need(sha(asset)==current.ASSET_SHA,'Complete exact original donor startup asset')
 with wave.open(str(asset),'rb')as file:
  need(file.getnchannels()==1 and file.getsampwidth()==2 and file.getframerate()==48000 and file.getnframes()==55465 and file.getcomptype()=='NONE',
       'Original full mono signed16 48k latency/tail-preserving source')
  values=np.frombuffer(file.readframes(file.getnframes()),'<i2').copy()
 sample,positions=original.sample_values(values,48000);voice=np.zeros_like(dcs)
 source=ROOT/'mame-mkp/src/devices/sound/samples.cpp'
 need(sha(source)=='8BF4BB350F40B309A5CECB4591DF8EE32A3563C3E061F2D2338C8CBA76B5353F'and
      'chan.source_num = (chan.source_len > 0) ? samplenum : -1;\n\tchan.source_len = sample.data.size();'in source.read_text(),
      'Exact native first-start saved source-number assignment uses previous length; pointer playback remains independent')
 gain=np.float32(.70);channel=10+(side-1)*2
 starts=[original.sample_clock(m['seconds'],True)for m in markers]
 for start in starts:
  for i,head in enumerate(headers):
   tick=int(Decimal(head['seconds'])*50);mixer_start=(tick-1)*960*(original.ATTO//48000)
   sec,fraction=divmod(mixer_start,original.ATTO);view=sec*48000+fraction//original.PERIOD
   at=np.arange(view,view+960,dtype=np.int64)-start;valid=(at>=0)&(at<len(sample))
   segment=np.zeros(960,dtype='<f4')
   if enabled:segment[valid]=np.float32(sample[at[valid]]*gain)
   voice[i*960:(i+1)*960]+=segment[:,None]
 expected_active=[]
 channels=rows(text,'MK2_TOMB_MIX_CHANNEL')
 need(len(channels)==len(headers)*14 and {(int(r['index']),int(r['channel']))for r in channels}==
      {(i,c)for i in range(1,len(headers)+1)for c in range(14)},'Every physical source at every complete native sound callback')
 by={(int(r['index']),int(r['channel'])):r for r in channels}
 for i,head in enumerate(headers):
  tick=int(Decimal(head['seconds'])*50);end_tick=tick*960*(original.ATTO//48000);s,f=divmod(end_tick,original.ATTO)
  output_end=s*48000+(f+original.PERIOD-1)//original.PERIOD
  latest=[start for start in starts if start<=output_end]
  processed=min(len(positions),max(0,output_end-latest[-1]))if latest else 0
  active=enabled and bool(latest)and 0<processed<len(positions)
  for c in range(14):
   row=by[i+1,c];need(row['frame']==head['frame']and row['seconds']==head['seconds']and row['writes']==row['loop']==row['paused']=='0',
                       'Exact unpaused nonlooping physical callback source provenance')
   if c==channel and enabled and latest:
    saved_source=16 if active and len(latest)>1 else 4294967295
    need(int(row['length'])==len(values)and float(row['position'])==positions[processed-1]and
         int(row['sample'])==saved_source,'Entire real owned launch source clock, exact first-start saved source assignment and native EOF retirement')
   else:need(row['sample']=='4294967295'and float(row['position'])>=int(row['length']),
             'Every other physical source remains genuinely retired; no unmodeled cue or wrong-slot roll')
  if active:expected_active.append(i+1)
 mixed=np.float32(dcs+voice)
 convert=lambda value:(np.clip(value,-1,1).astype(np.float64)*32767.0).astype('<i2')
 predicted=convert(mixed);different=np.argwhere(predicted!=pcm);faults=[]
 if not len(different):
  for label,n,c in [('first real PCM sample',0,0),('final real PCM sample',len(pcm)-1,1)]:
   bad=pcm.copy();bad[n,c]^=1;need(not np.array_equal(predicted,bad),'Real complete PCM bit counterexample rejected')
   faults.append(dict(kind=label,differentChannelSamples=int(np.count_nonzero(predicted!=bad))))
  for label,bad in [('first cached stereo frame omitted',pcm[1:]),('complete final stereo frame omitted',pcm[:-1])]:
   need(predicted.shape!=bad.shape,'Whole native PCM shape counterexample rejected');faults.append(dict(kind=label,rejectedBy='complete source shape'))
  if enabled:
   late=np.zeros_like(voice);late[1:]=voice[:-1]
   for label,bad in [('launch source omitted',convert(dcs)),('launch one sample late',convert(np.float32(dcs+late))),
                    ('original .70 sample route omitted',convert(np.float32(dcs+voice/gain)))]:
    need(not np.array_equal(predicted,bad)and not np.array_equal(bad,pcm),'Actual nonvacuous launch source-operation counterexample '+label)
    faults.append(dict(kind=label,differentChannelSamples=int(np.count_nonzero(bad!=pcm))))
 return dict(passed=not len(different),samplesEnabled=enabled,physicalSlot=side,physicalChannel=channel,sampleIndex=16,
             comparedStereoFrames=len(pcm),differentChannelSamples=len(different),actualActiveCallbacks=len(expected_active),
             actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
             firstDifferences=[dict(stereoFrame=int(n),channel=int(c),expected=int(predicted[n,c]),actual=int(pcm[n,c]),
                                   nativeFloat=float(dcs[n,c]),launchFloat=float(voice[n,c]))for n,c in different[:16]],
             nativePortEvents=markers,nativeSourceClocks=clocks,effectiveActualPCMFaults=faults,
             fullInterruptionCoverageAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False)
