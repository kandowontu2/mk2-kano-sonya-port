"""Native CPU weapon cue provenance, packet delivery, precise clip retirement.

Add to the complete source DAC/PCM/ROM result, not a substitute for it. Reuse
the original full packet/ADSP and sample-clock gates with only the already
completed selection clip as the pre-window channel0 state.
"""
import argparse,gzip,inspect,json,re,struct,subprocess,traceback,wave
from pathlib import Path
import verify_current_tomb_winner_mix_v5785 as old
import current_tomb_winner_mix_fault_model_v5789 as model
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
CASE=ROOT/'audit_v6368_current_cpu_blade_knife_audio_ram'
OUT=ROOT/'audit_v6371_current_cpu_blade_knife_audio_checked'


def packet_gate(text):
 source=inspect.getsource(old.gate)
 first=source.index(" packets=audio('PACKET');");last=source.index(' return dict(passed=True,',first)
 source='''def gate(text):
 records=old.inventory(text)
 audio=lambda tag:records.get('MK2_MAUDIO_'+tag,[])
 identity=17
 ends=audio('RESULT');need(len(ends)==1,'Single original audio terminal');end=ends[0]
'''+source[first:last]+'''
 return dict(packets=len(packets),portWrites=len(sounds),nativeDSPReads=len(delivery),trueWinnerMarkers=len(markers))
'''
 scope=dict(old.gate.__globals__,old=old)
 exec(compile(source,__file__+'::whole_original_native_packet_port_ADSP_chronology','exec'),scope)
 return scope['gate'](text)


def channel_gate(text,waveform,headers):
 source=inspect.getsource(old.channel_gate)
 before='return 0xffffffff,32000,endpoint'
 need(source.count(before)==1,'Only already completed selection clip differs before real winner marker')
 source=source.replace(before,'return 0xffffffff,18400,18400.0',1)
 scope=dict(old.channel_gate.__globals__)
 exec(compile(source,__file__+'::whole_original_precise_sample_clock_CPU_preselection_state','exec'),scope)
 return scope['channel_gate'](old.inventory(text),headers,dict(waveform=waveform),'kano')


def cue_gate(text,guest):
 routes=model.rows(text,'MK2_MAUDIO_ROUTE');offset=lambda at:(at-0xff800000)//8
 cases=[('FFF8CCC0',1871,0xc8,'010350A0','0106A370'),
        ('FFF900C0',1881,0x44,'01034E90','01068EA0'),
        ('FFFC38F0',2442,5,'010350A0','0106A370')]
 for caller,frame,command,actor,main in cases:
  rows=[r for r in routes if r['return_pc']==caller]
  need(len(rows)==1 and rows[0]['entry']=='FFA12530'and int(rows[0]['a0'],16)==command and
       rows[0]['frame']==str(frame)and rows[0]['id']=='17'and rows[0]['a8']==rows[0]['owner']==actor and rows[0]['a13']==main,
       'One real true-owner source weapon cue '+caller)
  at=offset(int(caller,16));instructions=struct.pack('<6H',0x09e0,command,0,0x0d5f,0x2530,0xffa1)
  need(guest[at-12:at]==instructions,'Whole actual MOVI/call weapon cue bytes '+caller)
 voice=[r for r in routes if r['return_pc']=='FFF90180']
 need([r['entry']for r in voice]==['FFA11FD0','FFA12220','FFA122D0','FFA123D0','FFA12530']and
      all(r['frame']=='1881'and r['a8']==r['owner']=='01034E90'and r['a13']=='01068EA0'and r['id']=='17'for r in voice),
      'Whole native actual-Kano victim grunt chain, no identity substitute')
 need(voice[1]['a0']==voice[2]['a0']=='00000002'and voice[1]['a1']==voice[2]['a1']=='32343638'and
      voice[2]['a2']=='00000011'and voice[3]['a2']==voice[4]['a2']=='00000001'and
      voice[3]['a1']==voice[4]['a1']==voice[4]['a0']=='00000032',
      'Original male selector uses actual victim17 and physical Main role1')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 need(guest[offset(0xffa12530):offset(0xffa13ed0)]==stock[offset(0xffa12530):offset(0xffa13ed0)],
      'Entire original fixed effect/queue/packet/handshake kernel unchanged')
 return dict(weaponCues=3,actualVictimVoiceRouteSteps=len(voice),actorIdentity=17,victimIdentity=17)


def main(preflight=False):
 need(not OUT.exists(),'Immutable complete native audio qualification')
 case=ROOT/'audit_v6366_current_cpu_blade_knife_audio_ram'if preflight else CASE
 terminal=json.loads((case/'native_terminal.json').read_text())
 need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors'],'Actual same native process terminal, never a timeout')
 with gzip.open(case/'run.log.gz','rt',encoding='utf-8')as reader:text=reader.read()
 guest=current.expected();cue=cue_gate(text,guest);packet=packet_gate(text)
 headers=model.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 marker=next(r for r in model.rows(text,'MK2_MAUDIO_SOUND')if r['pc']=='FFFB7140')
 with wave.open(str(ROOT/'samples/mk2ks/kano_select.wav'),'rb')as clip:
  need(clip.getnframes()==18400,'Actual complete initial selection source length')
 if preflight:
  clocks=channel_gate(text,dict(sourceMarker=marker,sourceStartStreamIndex=model.sample_clock(marker['seconds'],True)),headers)
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,cue=cue,packet=packet,preciseStates=clocks['preciseSourceChannelStates'])),flush=True);return
 report=json.loads((case/'report.json').read_text());waveform=json.loads((case/'waveform.json').read_text())
 need(report['passed']and report['samplesEnabled']and report['nativeDCSWaveformAccepted']and report['sourceWinnerMixAccepted']and
      waveform['passed']and waveform['differentChannelSamples']==0 and
      waveform['actualSHA256']==waveform['predictedSHA256']and
      all(sha(p)==h for p,h in report['inputHashes'].items()),'Entire current source-native DAC/PCM/winner/ROM proof unchanged')
 need(headers==report['pcmHeaders']and model.rows(text,'MK2_NATIVE_DAC_RAM_DIGEST')==report['dacHeaders'],
      'Every actual persisted callback digest binds the full accepted RAM waveform')
 clocks=channel_gate(text,waveform,headers)
 faults=[]
 def reject(label,bad,gate):
  need(bad!=text,'Actual counterexample changes a real observed field')
  try:gate(bad)
  except(ValueError,KeyError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted real native sound fault '+label)
 def alter(tag,key,value,where):
  line=next(s for s in text.splitlines()if s.startswith(tag+' ')and where in s)
  changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and changed!=line,'Real actual field altered');return text.replace(line,changed,1)
 for label,tag,key,value,where,gate in [
  ('wrong blade cue','MK2_MAUDIO_ROUTE','a0','000000C9','return_pc=FFF8CCC0',lambda value:cue_gate(value,guest)),
  ('wrong knife owner','MK2_MAUDIO_ROUTE','id','1','return_pc=FFFC38F0',lambda value:cue_gate(value,guest)),
  ('wrong victim identity','MK2_MAUDIO_ROUTE','a2','00000001','entry=FFA122D0',lambda value:cue_gate(value,guest)),
  ('wrong native packet','MK2_MAUDIO_PACKET','a3','000000BE','frame=1871',packet_gate),
  ('wrong sound port word','MK2_MAUDIO_SOUND','word','FF01','frame=1871',packet_gate),
  ('wrong DSP delivery','MK2_MAUDIO_DELIVERY','word','0001','frame=1871',packet_gate),
  ('wrong real channel position','MK2_TOMB_MIX_CHANNEL','bits','000000000000F03F','channel=0',lambda value:channel_gate(value,waveform,headers)),
  ('looped retained winner','MK2_TOMB_MIX_CHANNEL','loop','1','channel=0',lambda value:channel_gate(value,waveform,headers)),
 ]:reject(label,alter(tag,key,value,where),gate)
 need(cue_gate(text,guest)==cue and packet_gate(text)==packet and channel_gate(text,waveform,headers)==clocks,
      'Entire unmodified positive restored after actual faults')
 pins=dict(report['inputHashes'])
 for path in(case/'report.json',case/'waveform.json',case/'run.log.gz',case/'native_terminal.json',Path(__file__),Path(old.__file__),ROOT/'samples/mk2ks/kano_select.wav'):
  pins[str(path.resolve())]=sha(path)
 result=dict(passed=True,currentCPUBladeKnifeSourceAudioAccepted=True,nativeTerminal=terminal,cueProvenance=cue,
             nativeDelivery=packet,wholePreciseWinnerClockAndRetirement=clocks,sourceDAC=report['dacProof'],
             completeStereoFrames=waveform['comparedStereoFrames'],wholePCMSHA256=waveform['actualSHA256'],
             actualAudioFaultsRejected=faults,rawWaveformFaultsRejected=waveform['actualMixedRawPCMByteFaultsRejected'],
             sourceWaveformFaultsRejected=waveform['actualMixedSourceOperationFaultsRejected'],
             inputHashes=pins,remaining=report['remaining'],newNativeBoots=0,newBuilds=0,newRawMedia=0,fullPortAcceptance=False,goalStatus='active')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact proof losslessly compressed')
 print(json.dumps(dict(passed=True,completeStereoFrames=result['completeStereoFrames'],nativePackets=packet['packets'],actualAudioFaultsRejected=len(faults))),flush=True)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
