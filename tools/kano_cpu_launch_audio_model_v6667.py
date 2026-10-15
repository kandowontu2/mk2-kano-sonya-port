"""Whole terminal6664 DAC plus two real roll starts and native winner source.

Complete retained stereo PCM, source-derived clocks, native double positions,
all14 precise channel states, original gain/interpolation/EOF operations.
No PCM fitting, omitted callbacks, modified guest state or native replay.
Video-frequency ownership and interruption acceptance remain separate.
"""
import hashlib,inspect,json,struct,wave
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
import numpy as np
import current_tomb_winner_mix_fault_model_v5789 as native
import current_cpu_compound_audio_model_v6444 as compound
import verify_current_cpu_blade_knife_audio_v6370 as packets
import kano_ball_launch_context_v6642 as candidate
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
rows=native.rows


def sources(text,pins):
 events=[]
 binding={(int(r['frame']),int(r['slot'])):r for r in rows(text,'MK2_MAUDIO_BINDING')}
 choices=rows(text,'MK2_CPU_CHOICE_EVENT')
 for marker in rows(text,'MK2_MAUDIO_SOUND'):
  if marker['pc']=='FFFB7140':
   need(marker['word']=='FFFE'and marker['mask']=='FFFF','Actual true Kano winner marker')
   values,frequency=native.read_winner('kano',pins)
   channel,sample_id,gain=0,2,np.float32(np.float32(.70)*np.float32(.30))
  elif marker['word']=='6B03':
   owned=binding[int(marker['frame']),2]
   route=[r for r in choices if r['frame']==marker['frame']and r['kind']=='ball']
   need(len(route)==1 and marker['mask']=='FFFF'and marker['pc']=='FFFFDEC0'and
        marker['a8']==owned['actor']==owned['owner']==route[0]['a8']and
        marker['a13']==owned['main']==route[0]['a13']and owned['id']==owned['roster']=='17',
        'Every startup originates in actual source-chosen Kano17 roll owned by physical CPU slot2')
   asset=ROOT/candidate.NAME/'samples/mk2ks/kano_ball_launch.wav'
   need(sha(asset)==candidate.ASSET_SHA,'Whole original donor waveform unchanged')
   pins[str(asset)]=candidate.ASSET_SHA
   with wave.open(str(asset),'rb')as clip:
    need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes(),clip.getcomptype())==(1,2,48000,55465,'NONE'),
         'Entire original donor latency, waveform and finite tail')
    values=np.frombuffer(clip.readframes(clip.getnframes()),'<i2').copy();frequency=48000
   channel,sample_id,gain=12,16,np.float32(.70)
  else:continue
  sample,positions=native.sample_values(values,frequency)
  events.append(dict(marker=marker,channel=channel,sample_id=sample_id,gain=gain,frequency=frequency,
                     length=len(values),start=native.sample_clock(marker['seconds'],True),sample=sample,positions=positions))
 need([e['marker']['word']for e in events]==['6B03','FFFE','6B03'],
      'All actual source events: two native CPU starts surrounding a genuine round winner')
 for a,b in zip([e for e in events if e['channel']==12],[e for e in events if e['channel']==12][1:]):
  need(a['start']+len(a['sample'])<b['start'],'Distinct complete finite launch tails before replacement')
 return events


def window(carrier):
 text=carrier['text'];headers=carrier['pcm_headers'];dac=carrier['dac_headers']
 begin,end=rows(text,'MK2_MAUDIO_BEGIN'),rows(text,'MK2_MAUDIO_RESULT')
 need(len(begin)==len(end)==1 and begin[0]['origin']==begin[0]['frame']=='1813'and end[0]['frame']=='3615'and end[0]['origin']=='1813',
      'Whole real pre-entry to natural terminal native window')
 first=int((Decimal(begin[0]['seconds'])*50).to_integral_value(rounding=ROUND_CEILING))
 last=int((Decimal(end[0]['seconds'])*50).to_integral_value(rounding=ROUND_FLOOR))
 need([Decimal(h['seconds'])for h in headers]==[Decimal(t)/50 for t in range(first,last+1)]and
      headers==rows(text,'MK2_BBAUDIO_PCM_DIGEST')and dac==rows(text,'MK2_NATIVE_DAC_RAM_DIGEST')and
      len(headers)==len(dac)==len(carrier['pcm_chunks'])==len(carrier['dac_chunks'])and
      all(h['bytes']=='3840'and 1813<=int(h['frame'])<=3615 for h in headers),
      'Every complete scheduled50Hz PCM and DAC callback; no video-clock substitute or trimmed tail')
 for raw,h in zip(carrier['pcm_chunks'],headers,strict=True):
  need(len(raw)==3840 and hashlib.sha256(raw).hexdigest().upper()==h['sha256'],
       'Every exact full native stereo48k callback binds its retained digest')
 return dict(firstSoundTick=first,lastSoundTick=last,completeCallbacks=len(headers),completeStereoFrames=len(headers)*960)


def predict(carrier,pins):
 admission=window(carrier);text=carrier['text'];headers=carrier['pcm_headers']
 pcm=np.frombuffer(b''.join(carrier['pcm_chunks']),'<i2').reshape(-1,2)
 dcs,clocks=native.float_model()(carrier['dac_chunks'],carrier['dac_headers'])
 need(dcs.shape==pcm.shape,'Whole original native5596 DAC/cache/resampler retained')
 events=sources(text,pins);voices={c:np.zeros_like(dcs)for c in(0,12)}
 for event in events:
  for index,head in enumerate(headers):
   tick=int(Decimal(head['seconds'])*50);mixer_start=(tick-1)*960*(native.ATTO//48000)
   sec,fraction=divmod(mixer_start,native.ATTO);view=sec*48000+fraction//native.PERIOD
   at=np.arange(view,view+960,dtype=np.int64)-event['start'];valid=(at>=0)&(at<len(event['sample']))
   segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(event['sample'][at[valid]]*event['gain'])
   voices[event['channel']][index*960:(index+1)*960]+=segment[:,None]
 voice=np.zeros_like(dcs)
 for channel in range(14):
  if channel in voices:voice=np.float32(voice+voices[channel])
 convert=lambda value:(np.clip(value,-1,1).astype(np.float64)*32767.0).astype('<i2')
 predicted=convert(np.float32(dcs+voice));different=np.argwhere(predicted!=pcm);faults=[]
 if not len(different):
  for label,n,c in [('first actual sample',0,0),('last actual sample',len(pcm)-1,1)]:
   bad=pcm.copy();bad[n,c]^=1;need(not np.array_equal(predicted,bad),'Entire actual PCM bit counterexample')
   faults.append(dict(fault=label,differentChannelSamples=int(np.count_nonzero(predicted!=bad))))
  for label,bad in [('missing first stereo frame',pcm[1:]),('missing last stereo frame',pcm[:-1])]:
   need(predicted.shape!=bad.shape,'Complete output shape rejects omitted stereo frame');faults.append(dict(fault=label,rejectedBy='whole source shape'))
  for channel in voices:
   bad=convert(np.float32(dcs+np.float32(voice-voices[channel])))
   need(not np.array_equal(bad,pcm),'Actual imported source has nonvacuous audible coverage')
   faults.append(dict(fault=f'channel{channel} source omitted',differentChannelSamples=int(np.count_nonzero(bad!=pcm))))
  late=np.zeros_like(voice);late[1:]=voice[:-1]
  for label,bad in [('source one sample late',convert(np.float32(dcs+late))),
                    ('native source prematurely quantized',convert(np.float32(convert(dcs).astype('<f4')/np.float32(32767)+voice)))]:
   need(not np.array_equal(bad,pcm),'Original source operation fault actually changes native output')
   faults.append(dict(fault=label,differentChannelSamples=int(np.count_nonzero(bad!=pcm))))
 return dict(passed=not len(different),wholeAudioWindow=admission,comparedStereoFrames=len(pcm),differentChannelSamples=len(different),
             actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
             firstDifferences=[dict(stereoFrame=int(n),channel=int(c),expected=int(predicted[n,c]),actual=int(pcm[n,c]),
                                    nativeFloat=float(dcs[n,c]),importedFloat=float(voice[n,c]))for n,c in different[:16]],
             sourceEvents=[{k:(float(v)if k=='gain'else v)for k,v in e.items()if k not in('sample','positions')}for e in events],
             sourceClocks=clocks,actualRawAndSourceFaultsRejected=faults,
             fullInterruptionCoverageAccepted=False,fullPortAcceptance=False)


def channels(text,headers,pins):
 events=sources(text,pins);precise=rows(text,'MK2_TOMB_MIX_CHANNEL')
 need(len(precise)==len(headers)*14 and {(int(r['index']),int(r['channel']))for r in precise}==
      {(i,c)for i in range(1,len(headers)+1)for c in range(14)},'Every actual14-channel precise state at every full native sound callback')
 path=ROOT/'samples/mk2ks/kano_select.wav';pins[str(path)]=sha(path)
 with wave.open(str(path),'rb')as clip:
  need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,16000,18400),'Actual preceding entire native selection source')
  _,selection_positions=native.sample_values(np.frombuffer(clip.readframes(18400),'<i2').copy(),16000)
 source=ROOT/'mame-mkp/src/devices/sound/samples.cpp'
 need(sha(source)=='8BF4BB350F40B309A5CECB4591DF8EE32A3563C3E061F2D2338C8CBA76B5353F'and
      'chan.source_num = (chan.source_len > 0) ? samplenum : -1;\n\tchan.source_len = sample.data.size();'in source.read_text(),
      'Exact source-number saved-item assignment uses previous length, not pointer playback')
 pins[str(source)]=sha(source)
 active={0:[],12:[]}
 for row in precise:
  index,channel=int(row['index']),int(row['channel']);head=headers[index-1]
  need(row['frame']==head['frame']and row['seconds']==head['seconds']and row['writes']=='0'and row['assistance']=='none'and
       row['loop']==row['paused']=='0','Every actual sound callback source/provenance, no loop or pause')
  tick=int(Decimal(head['seconds'])*50);end_tick=tick*960*(native.ATTO//48000);s,f=divmod(end_tick,native.ATTO)
  end=s*48000+(f+native.PERIOD-1)//native.PERIOD
  launches=[e for e in events if e['channel']==channel and e['start']<=end]
  number,length,position=0xffffffff,0,0.0
  if channel==0:length,position=18400,selection_positions[-1]
  if launches:
   event=launches[-1];count=min(len(event['positions']),max(0,end-event['start']))
   length=event['length'];position=event['positions'][count-1]if count else 0.0
   playing=0<count<len(event['positions'])
   prior_length=(18400 if channel==0 else 0)if len(launches)==1 else launches[-2]['length']
   number=event['sample_id']if playing and prior_length>0 else 0xffffffff
   if playing:active[channel].append(index)
  need(int(row['sample'])==number and int(row['length'])==length and float(row['position'])==position and
       row['bits']==struct.pack('<d',position).hex().upper(),'All physical source IDs, full lengths, exact native repeated-double bits and finite EOF positions')
 need(all(active[c]for c in active),'Both startup and winner actual playback sampled throughout whole window')
 return dict(passed=True,preciseSourceChannelStates=len(precise),activeCallbackCounts={str(c):len(v)for c,v in active.items()},
             allRepeatedDoubleBitsExact=True,firstLaunchSavedSourceNumberDerivedFromPreviousLength=True,
             allFourteenPreciseChannelsChecked=True,wholeVideoChannelClockAcceptance=False,
             fullInterruptionCoverageAccepted=False,fullPortAcceptance=False)


def packet_gate(text):
 # Preserve the entire old native packet/port/ADSP chronology. Exactly the
 # two independently owned startup stores are additionally accounted for.
 source=inspect.getsource(packets.packet_gate)
 scope=dict(packets.__dict__)
 exec(compile(source,__file__+'::old_complete_packet_builder','exec'),scope)
 captured=[]
 def remember(code,filename,mode):captured.append(code);return compile(code,filename,mode)
 scope['compile']=remember
 try:scope['packet_gate'](text)
 except ValueError:pass
 need(len(captured)==1,'One entire original native packet gate extracted')
 code=captured[0]
 before='len(all_sounds)==len(sounds)+1'
 need(code.count(before)==1,'Entire packet accounting only adds actual owned startup markers')
 code=code.replace(before,"len(all_sounds)==len(sounds)+1+len(launches)",1)
 before="packets=audio('PACKET');all_sounds=audio('SOUND');"
 need(code.count(before)==1,'Original packet inventory intact')
 code=code.replace(before,before+"launches=[r for r in all_sounds if r['word']=='6B03'];need(len(launches)==2 and all(r['pc']=='FFFFDEC0'and r['mask']=='FFFF'for r in launches),'Both actual full startup port stores accounted');",1)
 final=dict(packets.old.gate.__globals__,old=packets.old)
 exec(compile(code,__file__+'::whole_native_packets_plus_owned_launches','exec'),final)
 result=final['gate'](text);sources(text,{})
 result.update(ownedStartupMarkers=2,unaccountedPortWrites=0)
 return result
