"""Current full-hit Ring cue sources, ADSP delivery and exact clip retirement.

Add to the whole actual source-native DAC/resampler/PCM/ROM proof, not replace
it. Preserve original packet and sample-clock contracts; the performer is
true Sonya18, the child has its own actual owner, and the victim is Kano17.
"""
import argparse,gzip,inspect,json,re,struct,subprocess,traceback
from pathlib import Path
import capture_current_cpu_ring_audio_v6384 as capture
import verify_current_cpu_blade_knife_audio_v6370 as packets
import verify_current_cpu_blade_knife_audio_v6372 as clocks
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.OUT
OUT=ROOT/'audit_v6387_current_cpu_ring_audio_checked'


def packet_gate(text):
 source=inspect.getsource(packets.packet_gate)
 need(source.count('identity=17')==1,'Only actual native winner identity changes')
 source=source.replace('identity=17','identity=18',1)
 scope=dict(packets.packet_gate.__globals__)
 exec(compile(source,__file__+'::whole_original_native_packet_ADSP_delivery_Sonya_winner','exec'),scope)
 return scope['packet_gate'](text)


def channel_gate(text,waveform,headers):
 source=inspect.getsource(clocks.channel_gate)
 need(source.count("'kano'")==1,'Only actual winner changes; prior human Kano selection source stays')
 source=source.replace("'kano'","'sonya'",1)
 scope=dict(clocks.channel_gate.__globals__)
 exec(compile(source,__file__+'::whole_original_precise_clock_Kano_selection_Sonya_winner','exec'),scope)
 return scope['channel_gate'](text,waveform,headers)


def cue_gate(text,guest):
 phase=capture.physical.phase
 events=phase.overlap.rows(text,'EVENT')
 parent=next(r for r in events if r['kind']=='ring')
 child=phase.overlap.rows(text,'CHILD')[0]
 field=next(r for r in phase.pair.rows(text,'FIELD')if r['frame']==parent['frame']+1)
 victim,vmain=field['vactor'],field['vmain']
 starts=capture.mix.rows(text,'MK2_MAUDIO_BEGIN')
 need(len(starts)==1 and int(starts[0]['a8'],16)==parent['a8'] and int(starts[0]['a13'],16)==parent['a13'] and
      starts[0]['id']=='18' and starts[0]['frame']==str(parent['frame']),
      'Audio begins at actual native true Sonya parent, not proxy or recycled child')
 routes=capture.mix.rows(text,'MK2_MAUDIO_ROUTE');offset=lambda at:(at-0xff800000)//8
 def exact(at,words,label):
  need(guest[offset(at):offset(at)+2*len(words)]==struct.pack('<'+'H'*len(words),*words),'Entire source instruction '+label)
 def owned(caller,frame,command,actor,main):
  rows=[r for r in routes if r['return_pc']==caller]
  need(len(rows)==1 and rows[0]['entry']=='FFA12530' and int(rows[0]['a0'],16)==command and
       rows[0]['frame']==str(frame) and rows[0]['id']=='18' and int(rows[0]['a8'],16)==int(rows[0]['owner'],16)==actor and
       int(rows[0]['a13'],16)==main and rows[0]['writes']=='0' and rows[0]['assistance']=='none',
       'One real true-owned native Ring cue '+caller)
 owned('FFFC48F0',parent['frame'],5,parent['a8'],parent['a13'])
 exact(0xfffc48f0-96,(0x09e0,5,0,0x0d5f,0x2530,0xffa1),'authored Ring release MOVI/CALLA')
 timeline=phase.ring_contract.verify(text,guest,'kano')['acceptedRings'][0]
 owned('FF8B0010',timeline['hit'],0x62,child['a8'],child['a13'])
 exact(0xff8b0010-64,(0x09c0,0x62,0x0d3f,0x069a),'original impact MOVI/CALLR')
 need(0xff8b0010+0x069a*16==0xff8b69b0,'Original signed CALLR reaches actual effect sound helper')
 exact(0xff8b69b0,(0x4c52,0xca01,0x1020,0xc080,0x2530,0xffa1),'original priority/helper dispatch jump')
 voice=[r for r in routes if r['return_pc']=='FF8DE600']
 need([r['entry']for r in voice]==['FFA11FD0','FFA12220','FFA122D0','FFA123D0','FFA12530'] and
      all(r['frame']==str(timeline['hit']) and int(r['a8'],16)==int(r['owner'],16)==victim and
          int(r['a13'],16)==vmain and r['id']=='17' and r['writes']=='0' and r['assistance']=='none'for r in voice),
      'Complete actual native Ring-hit Kano victim voice chain, no Liu proxy')
 need(voice[1]['a0']==voice[2]['a0']=='00000002' and voice[1]['a1']==voice[2]['a1']=='32343638' and
      voice[2]['a2']=='00000011' and voice[3]['a2']==voice[4]['a2']=='00000001' and
      voice[3]['a1']==voice[4]['a1']=='00000032' and int(voice[4]['a0'],16)in(0x32,0x33),
      'Original packed count2/base32 selects actual victim17 and physical Main role1')
 exact(0xff8de600-48,(0x0d5f,0x1fd0,0xffa1),'original victim voice CALLA')
 exact(0xffa11fd0,(0x1840,0x09e1,0x3638,0x3234,0xc020),'original count2/role/female packed selector')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff8b0010-64,0xff8b0010),(0xff8b69b0,0xff8b6ac0),(0xff8de000,0xff8de700),(0xffa12530,0xffa13ed0)):
  need(guest[offset(lo):offset(hi)]==stock[offset(lo):offset(hi)],'Entire original Ring impact/voice/queue/packet kernel unchanged')
 return dict(releaseCues=1,impactCues=1,actualVictimVoiceRouteSteps=len(voice),performerIdentity=18,childIdentity=18,
             victimIdentity=17,actualParent=parent['a8'],actualChild=child['a8'],actualVictim=victim,sourceHitFrame=timeline['hit'])


def main(preflight=False):
 need(not OUT.exists() and not capture.process_tools.census(),'Fresh independent proof, no live native game or new replay')
 report=json.loads((CASE/'report.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 waveform=json.loads((CASE/'waveform.json').read_text())
 need(report['passed'] and report['samplesEnabled'] and report['sourceWinnerMixAccepted'] and
      report['nativeDCSWaveformAccepted'] and terminal['nativeExit']==0 and not terminal['hostDecodeErrors'] and
      waveform['passed'] and waveform['differentChannelSamples']==0 and waveform['actualSHA256']==waveform['predictedSHA256'] and
      all(sha(p)==h for p,h in report['inputHashes'].items()),'Complete current source-native DAC/PCM/winner/ROM proof unchanged')
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 guest=capture.original.current.expected();physical=capture.state(text,'sonya',2,guest)
 headers=capture.mix.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(headers==report['pcmHeaders'] and capture.mix.rows(text,'MK2_NATIVE_DAC_RAM_DIGEST')==report['dacHeaders'],
      'Every actual callback digest binds accepted full RAM waveform')
 cue=cue_gate(text,guest);delivery=packet_gate(text);channels=channel_gate(text,waveform,headers)
 if preflight:
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,cue=cue,delivery=delivery,preciseStates=channels['preciseSourceChannelStates'])),flush=True);return
 faults=[]
 def alter(tag,key,value,where):
  line=next(s for s in text.splitlines()if s.startswith(tag+' ')and where in s)
  changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and changed!=line,'Real actual audio field changed');return text.replace(line,changed,1)
 for label,tag,key,value,where,gate in [
  ('wrong release command','MK2_MAUDIO_ROUTE','a0','00000006','return_pc=FFFC48F0',lambda t:cue_gate(t,guest)),
  ('wrong parent identity','MK2_MAUDIO_BEGIN','id','1','origin=2077',lambda t:cue_gate(t,guest)),
  ('impact given parent owner','MK2_MAUDIO_ROUTE','a8',format(cue['actualParent'],'08X'),'return_pc=FF8B0010',lambda t:cue_gate(t,guest)),
  ('wrong native victim selector','MK2_MAUDIO_ROUTE','a2','00000001','entry=FFA122D0',lambda t:cue_gate(t,guest)),
  ('wrong actual packet','MK2_MAUDIO_PACKET','a3','000000BE','frame=2077',packet_gate),
  ('wrong actual port byte','MK2_MAUDIO_SOUND','word','FF01','frame=2077',packet_gate),
  ('wrong actual ADSP delivery','MK2_MAUDIO_DELIVERY','word','0001','frame=2077',packet_gate),
  ('wrong winner marker','MK2_MAUDIO_SOUND','word','FFFE','pc=FFFB7140',packet_gate),
  ('wrong exact channel position','MK2_TOMB_MIX_CHANNEL','bits','000000000000F03F','channel=0',lambda t:channel_gate(t,waveform,headers)),
  ('looped retired winner','MK2_TOMB_MIX_CHANNEL','loop','1','channel=0',lambda t:channel_gate(t,waveform,headers)),
 ]:
  bad=alter(tag,key,value,where)
  try:gate(bad)
  except(ValueError,KeyError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted actual native Ring audio fault '+label)
 need(cue_gate(text,guest)==cue and packet_gate(text)==delivery and channel_gate(text,waveform,headers)==channels,
      'Entire native audio positive restored after all actual faults')
 pins=dict(report['inputHashes'])
 for path in(CASE/'report.json',CASE/'waveform.json',CASE/'run.log.gz',CASE/'native_terminal.json',Path(__file__),
             Path(packets.__file__),Path(clocks.__file__),ROOT/'samples/mk2ks/kano_select.wav'):
  pins[str(path.resolve())]=sha(path)
 result=dict(passed=True,currentCPUFullRingHitSourceAudioAccepted=True,nativeTerminal=terminal,wholeNativePhysicalPhase=physical,
             cueProvenance=cue,nativeDelivery=delivery,wholePreciseWinnerClockAndRetirement=channels,sourceDAC=report['dacProof'],
             completeStereoFrames=waveform['comparedStereoFrames'],wholePCMSHA256=waveform['actualSHA256'],
             actualAudioFaultsRejected=faults,rawWaveformFaultsRejected=waveform['actualRawMixedPCMFaultsRejected'],
             sourceWaveformFaultsRejected=waveform['actualMixedSourceOperationFaultsRejected'],inputHashes=pins,
             remaining=report['remaining'],newNativeBoots=0,newBuilds=0,newRawMedia=0,fullPortAcceptance=False,goalStatus='active')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,
      'Exact finite proof losslessly compressed')
 print(json.dumps(dict(passed=True,completeStereoFrames=result['completeStereoFrames'],nativePackets=delivery['packets'],actualAudioFaultsRejected=len(faults))),flush=True)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
