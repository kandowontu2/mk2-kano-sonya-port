"""Qualify the same terminal6445 RAM carrier through its actual match boundary.

The second winner starts3605; original physical exit3623 is not its EOF.
Preserve the executed idle-at-terminal failure. No additional native replay.
"""
import bisect,inspect,json,re,struct,subprocess,wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import capture_current_cpu_compound_audio_v6443 as capture
import verify_current_cpu_ring_miss_audio_v6428 as cues
import verify_current_cpu_blade_knife_audio_v6370 as packets
mix=capture.mix.original
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v6447_current_cpu_compound_audio_checked'


def state(text,guest):
 source=inspect.getsource(capture.state)
 before="need(all(r['sample']=='4294967295'for r in channels if r['frame']=='3623'),'No imported source still playing at natural match terminal')"
 after="""need(all(r['sample']=='4294967295'for r in channels if r['frame']=='3623'and r['channel']!='0'),
      'All battle clips retired at unchanged physical terminal')
 last=[r for r in channels if r['frame']=='3623'and r['channel']=='0']
 need(len(last)==1 and last[0]['sample']=='3'and last[0]['length']=='32000'and 0<float(last[0]['pos'])<32000,
      'Actual legitimate second Sonya winner remains playing at physical exit, not falsely claimed EOF')"""
 need(source.count(before)==1,'Only incorrect terminal-idle assumption changes; entire physical contract retained')
 scope=dict(capture.state.__globals__)
 exec(compile(source.replace(before,after,1),__file__+'::whole_physical_match_actual_second_winner_boundary','exec'),scope)
 return scope['state'](text,'sonya',2,guest)


def cue_gate(text,guest):
 source=inspect.getsource(cues.cue_gate)
 before="str(parent['frame'])=='1879'"
 need(source.count(before)==1,'Only window starts at first live field, Ring still1879')
 source=source.replace(before,"'1823'",1)
 scope=dict(cues.cue_gate.__globals__)
 exec(compile(source,__file__+'::whole_missed_ring_and_all_native_gender_voice_chains','exec'),scope)
 result=scope['cue_gate'](text,guest)
 rounds=cues.capture.original.physical.miss.phase.rounds
 actual={(r['frame'],r['slot']):r for r in rounds.rows(text,'FIELD')}
 marks=[r for r in mix.rows(text,'MK2_MAUDIO_SOUND')if r['word']in('6B00','6B01','6B02')]
 expected=[('6B01','FFF9A4C0',2663),('6B02','FFF9A520',2663),('6B00','FFFFCAC0',2994)]
 need([(r['word'],r['pc'],int(r['frame']))for r in marks]==expected,'Both actual Bicycle launches and later Square only')
 for r in marks:
  field=actual[int(r['frame']),2]
  need(r['mask']=='FFFF'and int(r['a8'],16)==field['actor']and int(r['a13'],16)==field['main']and field['id']==18,
       'Actual native Sonya18 physical actor/Main launch, never proxy')
  pc=int(r['pc'],16);at=(pc-0xff800000)//8
  need(guest[at-12:at]==struct.pack('<6H',0x09e0,int(r['word'],16),0,0x0580,0x1030,0x01d0),
       'Entire authored MOVI and absolute native full-word sound-port store')
 routes=mix.rows(text,'MK2_MAUDIO_ROUTE')
 for caller,frames,identity,lo,hi,helper in[
  ('FFF80890',[1954,2117,2920],18,0,4,0xffa11d30),
  ('FFF80D70',[1964,2127,2930],18,0x14,0x16,0xffa11ea0),
  ('FF842C50',[1964,2127,2930],17,0x32,0x34,None),
  ('FF8E3530',[3055],17,0x15,0x16,None)]:
  selected=[r for r in routes if r['entry']=='FFA12530'and r['return_pc']==caller]
  need([int(r['frame'])for r in selected]==frames,'All actual leg startup/contact/victim and ordinary cue producers')
  for r in selected:
   field=actual[int(r['frame']),2 if identity==18 else 1]
   need(int(r['id'])==identity and int(r['a8'],16)==int(r['owner'],16)==field['actor']and
        int(r['a13'],16)==field['main']and lo<=int(r['a0'],16)<hi,'Source-owned native randomized swing/impact/actual victim voice')
  if helper:
   at=(int(caller,16)-0xff800000)//8
   need(guest[at-6:at]==struct.pack('<3H',0x0d5f,helper&65535,helper>>16),'Entire authored CALLA to original sound helper')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xffa11d30,0xffa12070),(0xff842be0,0xff842c60),(0xff8e3510,0xff8e3540)):
  a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
  need(guest[a:b]==stock[a:b],'Whole original leg swing/contact/victim/ordinary helper source unchanged')
 result.update(battleMarkers=marks,legStartupFrames=[1954,2117,2920],legContactFrames=[1964,2127,2930],ordinaryImpactFrame=3055)
 return result


def packet_gate(text):
 source=inspect.getsource(packets.old.gate)
 first=source.index(" packets=audio('PACKET');");last=source.index(' return dict(passed=True,',first)
 body=source[first:last]
 before="len(markers)==1 and markers[0]['word']==('FFFE'if identity==17 else'FFFD')and markers[0]['mask']=='FFFF'and\n  len(all_sounds)==len(sounds)+1"
 after="len(markers)==2 and [r['frame']for r in markers]==['2420','3605']and all(r['word']=='FFFD'and r['mask']=='FFFF'for r in markers)and\n  len(all_sounds)==len(sounds)+5"
 need(body.count(before)==1,'Only actual two winners plus three separately owned battle markers differ')
 body=body.replace(before,after,1)
 source="def gate(text):\n records=old.inventory(text)\n audio=lambda tag:records.get('MK2_MAUDIO_'+tag,[])\n ends=audio('RESULT');need(len(ends)==1,'Single actual audio terminal');end=ends[0]\n"+body+"\n return dict(packets=len(packets),portWrites=len(sounds),nativeDSPReads=len(delivery),trueWinnerMarkers=len(markers))\n"
 scope=dict(packets.old.gate.__globals__,old=packets.old)
 exec(compile(source,__file__+'::whole_original_packet_port_ADSP_chronology','exec'),scope)
 return scope['gate'](text)


def channel_gate(text,waveform,headers,dac_headers):
 events=waveform['sourceEvents'];by={c:[e for e in events if e['channel']==c]for c in(0,12,13)}
 positions={}
 for e in events:
  name={3:'sonya_wins',14:'sonya_bicycle_launch',15:'sonya_bicycle_cry',13:'sonya_square_launch'}[e['sample_id']]
  with wave.open(str(ROOT/'samples/mk2ks'/(name+'.wav')),'rb')as f:
   need(f.getnframes()==e['length']and f.getframerate()==e['frequency'],'Entire source format bound to waveform launch')
   values=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()
  _,positions[e['start'],e['channel']]=mix.sample_values(values,e['frequency'])
 with wave.open(str(ROOT/'samples/mk2ks/kano_select.wav'),'rb')as f:
  need((f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getnframes())==(1,2,16000,18400),'Original preceding Kano selection clip')
  _,selection=mix.sample_values(np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy(),16000)
 times=[Decimal(h['seconds'])for h in headers]
 preceding=dac_headers[0]['previous_seconds'];period=mix.ATTO//60
 def expected(row,precise):
  channel=int(row['channel']);now=Decimal(row['seconds'])
  eligible=[e for e in by.get(channel,[])if Decimal(e['marker']['seconds'])<=now]
  if not eligible:return(0xffffffff,18400,selection[-1])if channel==0 else(0xffffffff,0,0.0)
  e=eligible[-1];pos=positions[e['start'],channel]
  index=bisect.bisect_right(times,now)-1
  clock=row['seconds']if precise else(headers[index]['seconds']if index>=0 else preceding)
  count=max(0,mix.sample_clock(clock,True)-e['start'])
  if channel in(12,13)and not precise:
   base=e if channel==12 else by[12][0]
   ticks=max(0,(int(now*mix.ATTO)-int(Decimal(base['marker']['seconds'])*mix.ATTO))//period)
   # samples_device has distinct streams. Cry is queried by the owner timer
   # only after launch channel12 returns false; until then it uses50Hz alone.
   if channel==12 or ticks*800>=by[12][0]['length']:count=max(count,ticks*800)
  count=min(len(pos),count);position=pos[count-1]if count else 0.0
  number=e['sample_id']if channel==0 or len(eligible)>1 else 0xffffffff
  if count==len(pos):number=0xffffffff
  return number,e['length'],position
 precise=mix.rows(text,'MK2_TOMB_MIX_CHANNEL');video=mix.rows(text,'MK2_MAUDIO_CHANNEL')
 need(len(precise)==14*len(headers)and {(int(r['index']),int(r['channel']))for r in precise}==
      {(i,c)for i in range(1,len(headers)+1)for c in range(14)},'All14 precise states at every callback')
 for r in precise:
  h=headers[int(r['index'])-1];number,length,position=expected(r,True)
  need(r['frame']==h['frame']and r['seconds']==h['seconds']and r['writes']=='0'and r['assistance']=='none'and
       int(r['sample'])==number and int(r['length'])==length and r['bits']==struct.pack('<d',position).hex().upper()and
       float(r['position'])==position and r['loop']==r['paused']=='0','Every exact repeated-double native precise source state')
 for r in video:
  number,length,position=expected(r,False)
  need(int(r['sample'])==number and int(r['length'])==length and r['pos']==format(position,'.8f')and
       r['loop']==r['paused']==r['writes']=='0','Every video state under distinct native50Hz and60Hz channel updates')
 need(not mix.rows(text,'MK2_TOMB_MIX_ITEM')and not mix.rows(text,'MK2_TOMB_MIX_GAIN'),'No nonexistent saved per-channel gain coverage claimed')
 return dict(preciseStates=len(precise),videoStates=len(video),everyRepeatedDoubleBitExact=True,
             allThreeBattleClipsAndFirstWinnerEOF=True,secondWinnerObservedThroughPhysicalExitNotEOF=True,
             separateChannelStreamsAndShortCircuitOwnerTimer=True,savedPerChannelGainSnapshotsAvailable=False)


def finish(carrier,waveform):
 need(not OUT.exists()and not capture.prior.process_tools.census(),'Same terminal native process, fresh host proof, no replay')
 terminal=json.loads((capture.OUT/'native_terminal.json').read_text());failure=json.loads((capture.OUT/'failure.json').read_text())
 need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors']and
      failure['error']=="ValueError('No imported source still playing at natural match terminal')",'Preserve real executed terminal-idle assumption failure')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'All executed source/observer/build inputs unchanged')
 proof=json.loads((ROOT/'audit_v5379_current_cpu_square_audio_ram_checked/report.json').read_text())
 compiled=ROOT/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 driver=compiled.with_name('midtunit.cpp');device=ROOT/'mame-mkp/src/devices/sound/samples.cpp'
 for p in(compiled,driver,device):
  need(sha(p)==proof['inputHashes'][str(p)],'Whole qualified compiled ownership/route/sample arithmetic unchanged');pins[str(p)]=sha(p)
 need('m_mk2ks_voices->add_route(ALL_OUTPUTS, "mk2ksvoice", 0.70);'in driver.read_text()and
      'm_mk2ks_voices->set_volume(0, 0.30f);'in compiled.read_text()and
      'unsigned const sample = 13 + data - 0x6b00;'in compiled.read_text(),
      'Independent compiled battle .70/announcer .70*.30 routing, never target gain fit')
 text=carrier['text'];headers=carrier['pcm_headers'];dac_headers=carrier['dac_headers']
 native=state(text,carrier['guest']);cue=cue_gate(text,carrier['guest']);delivery=packet_gate(text)
 clocks=channel_gate(text,waveform,headers,dac_headers)
 need(waveform['passed']and waveform['differentChannelSamples']==0 and len(waveform['actualRawAndSourceFaultsRejected'])==9,
      'Whole actual untrimmed mixed PCM, all raw/source counterexamples')
 gate,fault,gate_sha=capture.prior.original.dac_models(len(headers))
 dac=gate(carrier['dac_chunks'],dac_headers,headers);dac_faults=fault(carrier['dac_chunks'],dac_headers,headers)
 rg,rf=capture.prior.original.model.rom_models(carrier['expected'])
 rom=[rg(bytes(carrier['rom'][p]),p)for p in carrier['rom']]
 rom_faults=[f for p in carrier['rom']for f in rf(bytes(carrier['rom'][p]),p)]
 faults=[]
 def alter(tag,key,value,where):
  line=next(s for s in text.splitlines()if s.startswith(tag+' ')and where in s)
  bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and bad!=line,'Real actual record field changed');return text.replace(line,bad,1)
 for label,tag,key,value,where,fn in[
  ('proxy launch actor','MK2_MAUDIO_SOUND','a8','01000000','word=6B00',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong Bicycle command','MK2_MAUDIO_SOUND','word','6B00','word=6B01',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong leg swing cue','MK2_MAUDIO_ROUTE','a0','00000099','return_pc=FFF80890',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong leg contact owner','MK2_MAUDIO_ROUTE','id','1','return_pc=FFF80D70',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong native female role','MK2_MAUDIO_ROUTE','a2','00000001','entry=FFA123B0',lambda t:cue_gate(t,carrier['guest'])),
  ('wrong native packet','MK2_MAUDIO_PACKET','a3','00010000','',packet_gate),
  ('missing native port prefix','MK2_MAUDIO_SOUND','word','0000','pc=FFA13C90',packet_gate),
  ('wrong ADSP delivery','MK2_MAUDIO_DELIVERY','word','FFFF','',packet_gate),
  ('proxy second winner','MK2_MAUDIO_SOUND','word','FFFE','frame=3605',packet_gate),
  ('wrong precise launch bits','MK2_TOMB_MIX_CHANNEL','bits','000000000000F03F','channel=12',lambda t:channel_gate(t,waveform,headers,dac_headers)),
  ('wrong cry video position','MK2_MAUDIO_CHANNEL','pos','1.00000000','channel=13',lambda t:channel_gate(t,waveform,headers,dac_headers)),
  ('looped battle clip','MK2_TOMB_MIX_CHANNEL','loop','1','channel=12',lambda t:channel_gate(t,waveform,headers,dac_headers))]:
  try:fn(alter(tag,key,value,where))
  except(ValueError,KeyError,AssertionError)as e:faults.append(dict(label=label,rejectedBy=str(e)))
  else:raise ValueError('Actual audio record fault admitted '+label)
 need(cue_gate(text,carrier['guest'])==cue and packet_gate(text)==delivery and channel_gate(text,waveform,headers,dac_headers)==clocks,
      'Entire actual positive restores after every source record counterexample')
 for p in(capture.OUT/'native_terminal.json',capture.OUT/'failure.json',capture.OUT/'run.log.gz',Path(__file__),
          Path(cues.__file__),Path(packets.__file__),ROOT/'samples/mk2ks/kano_select.wav',
          ROOT/'mame-mkp/src/devices/sound/samples.cpp',ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json',
          ROOT/'audit_v5379_current_cpu_square_audio_ram_checked/report.json'):
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every protected/current input unchanged after full RAM qualification')
 result=dict(passed=True,nativeTerminal=terminal,wholeNativePhysicalPhase=native,cueProvenance=cue,nativeDelivery=delivery,
             allChannelStates=clocks,sourceDACGateSHA256=gate_sha,sourceDAC=dac,dacFaultsRejected=dac_faults,
             wholeOriginalSoundROM=rom,originalSoundROMFaultsRejected=rom_faults,pcmHeaders=headers,dacHeaders=dac_headers,
             completeStereoFrames=waveform['comparedStereoFrames'],wholePCMSHA256=waveform['actualSHA256'],
             actualAudioRecordFaultsRejected=faults,inputHashes=pins,preservedExecutedFailure=str(capture.OUT/'failure.json'),
             sourceExactChainedMoveAudioAccepted=True,secondWinnerEOFAccepted=False,
             originalNativeBoundaryUnchanged=True,remaining=carrier['remaining'],goalStatus='active',
             newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,fullPortAcceptance=False,
             previousGoalTurnClassification='no progress: acknowledgement only; current files and live census revalidated',
             thisGoalTurnClassification='progress: whole natural CPU compound match source audio, packet delivery and distinct channel retirement qualified')
 OUT.mkdir();capture.prior.original.save(OUT/'waveform.json',waveform);capture.prior.original.save(OUT/'report.json',result)
 print(json.dumps(dict(passed=True,stereoFrames=result['completeStereoFrames'],delivery=delivery,channels=clocks)),flush=True)
 return result
