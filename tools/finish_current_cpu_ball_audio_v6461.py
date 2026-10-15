"""Qualify the same terminal6460 RAM carrier, using the real50Hz boundary."""
import inspect,json,re,struct
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
from pathlib import Path
import numpy as np
import capture_current_cpu_ball_audio_v6459 as capture
import verify_current_cpu_blade_knife_audio_v6370 as packets
import verify_current_cpu_blade_knife_audio_v6372 as clocks
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
mix=capture.mix
OUT=ROOT/'audit_v6462_current_cpu_ball_audio_checked'


def state(text,guest):
 source=inspect.getsource(capture.state)
 before="""need(pcm and all(r['bytes']=='3840'and 1813<=int(r['frame'])<=3615 for r in pcm)and
      int(pcm[0]['frame'])<=1814 and int(pcm[-1]['frame'])>=3614 and
      all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(pcm,pcm[1:])),
      'Whole consecutive50Hz window, no callback or tail trimming')"""
 after="""first=int((Decimal(marks[0]['seconds'])*50).to_integral_value(rounding=ROUND_CEILING))
 last=int((Decimal(ends[0]['seconds'])*50).to_integral_value(rounding=ROUND_FLOOR))
 need(pcm and all(r['bytes']=='3840'and 1813<=int(r['frame'])<=3615 for r in pcm)and
      [Decimal(r['seconds'])for r in pcm]==[Decimal(t)/50 for t in range(first,last+1)],
      'Every scheduled50Hz callback from passive origin to natural terminal, no first/last/tail trimming')"""
 need(source.count(before)==1,'Only erroneous video-frame assumption changes; exact native sound clock covers all callbacks')
 scope=dict(capture.state.__globals__,Decimal=Decimal,ROUND_CEILING=ROUND_CEILING,ROUND_FLOOR=ROUND_FLOOR)
 exec(compile(source.replace(before,after,1),__file__+'::whole_original_state_exact_sound_clock','exec'),scope)
 return scope['state'](text,'kano',2,guest)


def cue_gate(text,guest):
 routes=mix.rows(text,'MK2_MAUDIO_ROUTE');bindings=mix.rows(text,'MK2_MAUDIO_BINDING')
 by={(int(r['frame']),int(r['slot'])):r for r in bindings}
 def owned(r,slot):
  field=by[int(r['frame']),slot]
  need(r['id']==field['id']==field['roster']=='17'and r['a8']==r['owner']==field['actor']==field['owner']and
       r['a13']==field['main']and r['writes']=='0'and r['assistance']=='none','True physical Kano17 actor/Main ownership, never proxy')
 offset=lambda at:(at-0xff800000)//8
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 # Entire original hit reaction, floor/landing effect and queue kernels,
 # not just selected literals. These source paths supply all ball audio.
 for lo,hi in((0xff8e2100,0xff8e24b0),(0xff9b9ed0,0xff9b9fa0),(0xffa12530,0xffa13ed0)):
  need(guest[offset(lo):offset(hi)]==stock[offset(lo):offset(hi)],'Whole original ball contact/landing/queue source unchanged')
 female=bytes.fromhex('02b5f001420bfbff14ca420bfaff11ca80c00002ffff420bfeff08caa2b52000420bfeff01ca0125012d05c00126012d02c00127012d5f0de0ea80ff2014204010c0')
 need(guest[offset(0xffa12220):offset(0xffa12430)]==female,'Entire native gender/Main-role/packed-byte dispatch extension')
 selector=guest[offset(0xffa122d0):offset(0xffa123b0)]
 need(selector==bytes.fromhex('420bfeff08caa2b52000420bfeff01ca0125012d05c00126012d02c0'),
      'Complete original male selector: Main role1 high byte; otherwise SLL8 then SRL24')
 decoder=(ROOT/'mame-mkp/src/devices/cpu/tms34010/34010dsm.cpp').read_text()
 need('case 0x2400:'in decoder and '"SLL    "'in decoder and 'case 0x2c00:'in decoder and '"SRL    "'in decoder,
      'Original CPU instruction semantics for packed-byte shifts')
 cases=[('FF8E22D0',1827,0x19,1),('FF8E24A0',1850,0x1f,1),('FF9B9F70',1869,0x1e,2)]
 for caller,frame,command,slot in cases:
  selected=[r for r in routes if r['entry']=='FFA12530'and r['return_pc']==caller and int(r['frame'])<=1918]
  need(len(selected)==1 and selected[0]['frame']==str(frame)and int(selected[0]['a0'],16)==command,
       'Exact native ball impact/victim floor/own landing producer '+caller)
  owned(selected[0],slot)
 initial=[r for r in routes if r['return_pc']=='FF8E2300'and int(r['frame'])<=1918]
 need([r['entry']for r in initial]==['FFA11FD0','FFA12220','FFA122D0','FFA123D0','FFA12530']and
      all(r['frame']=='1827'for r in initial),'Complete actual ball contact victim grunt chain')
 need(not[r for r in routes if 1813<=int(r['frame'])<1827],'No invented startup cue; whole current ball source uses native contact/landing paths')
 voices=[]
 for i,r in enumerate(routes):
  if r['entry']!='FFA12220':continue
  matches=[slot for slot in(1,2)if by[int(r['frame']),slot]['actor']==r['a8']and by[int(r['frame']),slot]['main']==r['a13']]
  need(len(matches)==1,'Physical role determined by actor/Main, not mirror identity')
  slot=matches[0];owned(r,slot);chain=routes[i:i+4]
  need([q['entry']for q in chain]==['FFA12220','FFA122D0','FFA123D0','FFA12530']and
       all(q['frame']==r['frame']and q['return_pc']==r['return_pc']and q['a8']==q['owner']==r['a8']and
           q['a13']==r['a13']and q['id']=='17'and q['writes']=='0'and q['assistance']=='none'for q in chain),
       'Every complete actual native male voice chain')
  count=int(r['a0'],16);base=(int(r['a1'],16)>>(24 if slot==1 else 16))&255
  need(chain[1]['a0']==r['a0']and chain[1]['a1']==r['a1']and chain[1]['a2']=='00000011'and
       int(chain[2]['a2'],16)==int(chain[3]['a2'],16)==slot and
       int(chain[2]['a1'],16)==int(chain[3]['a1'],16)==base and base<=int(chain[3]['a0'],16)<base+count,
       'Source-exact packed voice byte and native RNG variant for real physical Main role')
  voices.append(dict(frame=int(r['frame']),slot=slot,base=base,count=count,caller=r['return_pc']))
 need(voices and {v['slot']for v in voices}=={1,2},'Both real mirror physical voice roles observed')
 return dict(ballContact=1827,victimLanding=1850,ownLanding=1869,nativeBallCues=3,
             initialVictimGruntSteps=len(initial),wholeNativeVictimVoiceChains=voices,trueBothIdentities=17,
             startupCueAbsentInCurrentSource=True,donorStartupCueParityAccepted=False)


def finish(carrier):
 need(not OUT.exists()and not capture.process_tools.census(),'Same actual terminal process, fresh host proof, no replay')
 terminal=json.loads((capture.OUT/'native_terminal.json').read_text());failure=json.loads((capture.OUT/'failure.json').read_text())
 need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors']and
      failure['error']=="ValueError('Whole consecutive50Hz window, no callback or tail trimming')",'Preserve original executed host timing rejection')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'Every executed/build/current input unchanged')
 capture.FULL_PHASE=capture.phase_gate()
 text=carrier['text'];headers=carrier['pcm_headers'];dac_headers=carrier['dac_headers']
 native=state(text,carrier['guest']);cue=cue_gate(text,carrier['guest']);delivery=packets.packet_gate(text)
 gate,fault,gate_sha=capture.original.dac_models(len(headers))
 dac=gate(carrier['dac_chunks'],dac_headers,headers);dac_faults=fault(carrier['dac_chunks'],dac_headers,headers)
 pcm=np.concatenate([np.frombuffer(raw,dtype='<i2').reshape(-1,2)for raw in carrier['pcm_chunks']],axis=0)
 waveform=mix.predict_mix(carrier['dac_chunks'],dac_headers,pcm,text,'kano',pins)
 need(waveform['passed']and waveform['differentChannelSamples']==0 and len(waveform['actualRawMixedPCMFaultsRejected'])==4 and
      len(waveform['actualMixedSourceOperationFaultsRejected'])==4,'Entire actual native PCM equals full original DAC plus source winner, all8 raw/source faults')
 channels=clocks.channel_gate(text,waveform,headers)
 rg,rf=capture.original.model.rom_models(carrier['expected'])
 rom=[rg(bytes(carrier['rom'][p]),p)for p in carrier['rom']]
 rom_faults=[f for p in carrier['rom']for f in rf(bytes(carrier['rom'][p]),p)]
 faults=[]
 def alter(tag,key,value,where):
  line=next(s for s in text.splitlines()if s.startswith(tag+' ')and where in s)
  changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and changed!=line,'Nonvacuous actual observed field mutation');return text.replace(line,changed,1)
 for label,tag,key,value,where,fn in[
  ('wrong ball impact','MK2_MAUDIO_ROUTE','a0','00000018','return_pc=FF8E22D0',lambda t:cue_gate(t,carrier['guest'])),
  ('proxy ball victim','MK2_MAUDIO_ROUTE','id','1','return_pc=FF8E22D0',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong own landing owner','MK2_MAUDIO_ROUTE','a13','01000000','return_pc=FF9B9F70',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong mirror physical role','MK2_MAUDIO_ROUTE','a2','00000001','frame=3418 entry=FFA123D0',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong real packed voice','MK2_MAUDIO_ROUTE','a1','00000033','frame=1827 entry=FFA123D0',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong native packet','MK2_MAUDIO_PACKET','a3','00010000','',packets.packet_gate),
  ('missing original port prefix','MK2_MAUDIO_SOUND','word','0000','pc=FFA13C90',packets.packet_gate),
  ('wrong actual ADSP delivery','MK2_MAUDIO_DELIVERY','word','FFFF','',packets.packet_gate),
  ('proxy winner announcement','MK2_MAUDIO_SOUND','word','FFFD','pc=FFFB7140',packets.packet_gate),
  ('wrong precise double bits','MK2_TOMB_MIX_CHANNEL','bits','000000000000F03F','channel=0',lambda t:clocks.channel_gate(t,waveform,headers)),
  ('looped completed winner','MK2_TOMB_MIX_CHANNEL','loop','1','channel=0',lambda t:clocks.channel_gate(t,waveform,headers))]:
  # The provenance/time prefix precedes entry; use two substrings for role faults.
  if where.startswith('frame=')and ' entry='in where:
   f,e=where.split(' entry=');line=next(s for s in text.splitlines()if s.startswith(tag+' ')and f in s and 'entry='+e in s)
   bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and bad!=line,'Real role record changed');bad=text.replace(line,bad,1)
  else:bad=alter(tag,key,value,where)
  try:fn(bad)
  except(ValueError,KeyError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual native sound fault admitted '+label)
 need(cue_gate(text,carrier['guest'])==cue and packets.packet_gate(text)==delivery and clocks.channel_gate(text,waveform,headers)==channels,
      'Whole original actual positive restored after faults')
 for p in(capture.OUT/'native_terminal.json',capture.OUT/'failure.json',capture.OUT/'run.log.gz',Path(__file__),
          Path(packets.__file__),Path(clocks.__file__),ROOT/'samples/mk2ks/kano_select.wav',
          ROOT/'mk2/mk2-maincpu.bin',ROOT/'mame-mkp/src/devices/cpu/tms34010/34010dsm.cpp'):
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All executed/current logical inputs unchanged after same-RAM qualification')
 result=dict(passed=True,nativeTerminal=terminal,wholeNativePhysicalPhase=native,cueProvenance=cue,nativeDelivery=delivery,
             allChannelStates=channels,sourceDACGateSHA256=gate_sha,sourceDAC=dac,dacFaultsRejected=dac_faults,
             wholeOriginalSoundROM=rom,originalSoundROMFaultsRejected=rom_faults,pcmHeaders=headers,dacHeaders=dac_headers,
             completeStereoFrames=waveform['comparedStereoFrames'],wholePCMSHA256=waveform['actualSHA256'],
             actualAudioRecordFaultsRejected=faults,inputHashes=pins,preservedExecutedFailure=str(capture.OUT/'failure.json'),
             sourceExactCurrentBallAudioAccepted=True,donorStartupCueParityAccepted=False,remaining=carrier['remaining'],
             newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,fullPortAcceptance=False,goalStatus='active',
             previousGoalTurnClassification='no progress: acknowledgement only; authoritative current files and empty process census revalidated',
             thisGoalTurnClassification='progress: full naturally selected CPU ball native audio qualified from the same terminal RAM carrier')
 OUT.mkdir();capture.original.save(OUT/'waveform.json',waveform);capture.original.save(OUT/'report.json',result)
 print(json.dumps(dict(passed=True,stereoFrames=result['completeStereoFrames'],delivery=delivery,channels=channels)),flush=True)
 return result
