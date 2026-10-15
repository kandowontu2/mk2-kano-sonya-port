"""Full current mirror cue/identity/packet and all14 source-channel clocks.

Read only the same naturally terminal6395 capture and6403 exact source PCM
proof. No native run, gain/timing fitting, raw media or playable mutation.
"""
import gzip,inspect,json,re,struct,wave,subprocess
from bisect import bisect_right
from decimal import Decimal
from pathlib import Path
import numpy as np
import verify_current_cpu_ring_audio_v6386 as original
import finish_current_cpu_ring_mirror_audio_v6402 as model

ROOT,need,sha=original.ROOT,original.need,original.sha
CASE=model.OUT
CAPTURE=ROOT/'audit_v6395_current_cpu_ring_mirror_audio_ram'
OUT=ROOT/'audit_v6405_current_cpu_ring_mirror_audio_checked'


def channel_gate(text,waveform,headers,report):
 old=original.packets.old
 path=ROOT/'samples/mk2ks/sonya_select.wav'
 with wave.open(str(path),'rb')as clip:
  need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,16000,18400),'Whole actual preceding Sonya selection source')
  values=np.frombuffer(clip.readframes(clip.getnframes()),dtype='<i2').copy()
 _,positions=original.capture.mix.sample_values(values,16000)
 start=report['initialSquareSource']['sourceStartStreamIndex']
 times=[Decimal(r['seconds'])for r in headers]
 def square_state(clock):
  i=bisect_right(times,Decimal(clock))-1
  previous=headers[i]['seconds']if i>=0 else report['dacHeaders'][0]['previous_seconds']
  count=min(45512,max(0,original.capture.mix.sample_clock(previous,True)-start))
  sec,fraction=divmod(start,48000);upper=sec*10**18+fraction*original.capture.mix.PERIOD
  sec,fraction=divmod(start-1,48000);lower=sec*10**18+fraction*original.capture.mix.PERIOD
  now=int(Decimal(clock)*10**18);period=10**18//60
  earliest=max(0,(now-upper)//period);latest=max(0,(now-lower)//period)
  need(min(45512,earliest*800)==min(45512,latest*800),'Native source-clock interval gives unambiguous60Hz owner tick')
  return 0xffffffff,45512,float(max(count,min(45512,earliest*800)))
 source=inspect.getsource(old.channel_gate)
 changes={
  '  if channel:return 0xffffffff,0,0.0':"  if channel==12:return square_state(clock)\n  if channel:return 0xffffffff,0,0.0",
  'return 0xffffffff,32000,endpoint':'return 0xffffffff,18400,selection_endpoint',
  'allOtherChannelsIdle=True':'allOtherChannelsIdle=False,allOtherChannelsSourceQualified=True,initialSquareChannel=12',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Retain entire original repeated-double and14-channel clock gate '+before)
  source=source.replace(before,after,1)
 scope=dict(old.channel_gate.__globals__,square_state=square_state,selection_endpoint=positions[-1])
 exec(compile(source,__file__+'::whole_source_channel_clock_plus_native_Square_timer','exec'),scope)
 return scope['channel_gate'](old.inventory(text),headers,dict(waveform=waveform),'sonya')


def cue_gate(text,guest):
 capture=model.original.prior.original
 phase=capture.physical.physical.phase
 rows=original.capture.mix.rows
 fields=phase.pair.rows(text,'FIELD');first=fields[0]
 begin=rows(text,'MK2_MAUDIO_BEGIN')
 need(len(begin)==1 and begin[0]['frame']==begin[0]['origin']==str(first['frame'])=='1823' and
      int(begin[0]['a8'],16)==first['actor']==first['owner'] and int(begin[0]['a13'],16)==first['main'] and
      begin[0]['id']=='18' and first['id']==first['roster']==first['vid']==first['vroster']==18 and first['action']==0x207,
      'Whole first-live mirror sound belongs to actual initial CPU Square owner, not later Ring-only admission')
 events=phase.overlap.rows(text,'EVENT');parent=next(r for r in events if r['kind']=='ring')
 child=phase.overlap.rows(text,'CHILD')[0]
 field=next(r for r in fields if r['frame']==parent['frame']+1)
 routes=rows(text,'MK2_MAUDIO_ROUTE');offset=lambda at:(at-0xff800000)//8
 def exact(at,words,label):
  need(guest[offset(at):offset(at)+2*len(words)]==struct.pack('<'+'H'*len(words),*words),'Whole source instruction '+label)
 def owned(caller,frame,command,actor,main):
  actual=[r for r in routes if r['return_pc']==caller]
  need(len(actual)==1 and actual[0]['entry']=='FFA12530' and int(actual[0]['a0'],16)==command and
       actual[0]['frame']==str(frame) and actual[0]['id']=='18' and int(actual[0]['a8'],16)==int(actual[0]['owner'],16)==actor and
       int(actual[0]['a13'],16)==main and actual[0]['writes']=='0' and actual[0]['assistance']=='none','Actual true-owned mirror cue '+caller)
 owned('FFFC48F0',parent['frame'],5,parent['a8'],parent['a13'])
 owned('FF8B0010',2974,0x63,child['a8'],child['a13'])
 owned('FF8E9990',2974,0x16,field['vactor'],field['vmain'])
 need(not[r for r in routes if r['return_pc']=='FF8DE600' and r['frame']=='2974'],'Blocked Ring has no unblocked-hit victim grunt')
 exact(0xfffc48f0-96,(0x09e0,5,0,0x0d5f,0x2530,0xffa1),'Ring release MOVI/CALLA')
 exact(0xff8b0010-64,(0x09c0,0x62,0x0d3f,0x069a),'Ring impact base62 MOVI/CALLR')
 exact(0xff8b69b0,(0x4c52,0xca01,0x1020,0xc080,0x2530,0xffa1),'Native block-bit helper adds one before dispatch')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff8b0010-64,0xff8b0010),(0xff8b69b0,0xff8b6ac0),(0xff8e9800,0xff8e9a00),(0xffa12530,0xffa13ed0)):
  need(guest[offset(lo):offset(hi)]==stock[offset(lo):offset(hi)],'Whole original Ring impact/block/queue/packet kernel')
 female=bytes.fromhex('02b5f001420bfbff14ca420bfaff11ca80c00002ffff420bfeff08caa2b52000420bfeff01ca0125012d05c00126012d02c00127012d5f0de0ea80ff2014204010c0')
 need(guest[offset(0xffa12220):offset(0xffa12430)]==female,'Whole qualified original-role/native-Sonya female extension')
 voices=[]
 for index,row in enumerate(routes):
  if row['entry']!='FFA12220':continue
  chain=routes[index:index+4]
  need([r['entry']for r in chain]==['FFA12220','FFA123B0','FFA123D0','FFA12530'] and
       all(r['id']=='18' and r['a8']==r['owner']==row['a8'] and r['a13']==row['a13'] and
           r['return_pc']==row['return_pc'] and r['frame']==row['frame'] and r['writes']=='0' and r['assistance']=='none'for r in chain),
       'Every complete true-Sonya victim female dispatch chain, never Liu proxy')
  count=int(row['a0'],16);base=int(row['a1'],16)&255
  need(chain[1]['a0']==row['a0'] and chain[1]['a1']==row['a1'] and chain[1]['a2']=='00000012' and
       chain[2]['a2']==chain[3]['a2']=='00000012' and int(chain[2]['a1'],16)==int(chain[3]['a1'],16)==base and
       base<=int(chain[3]['a0'],16)<base+count and
       all(Decimal(a['seconds'])<Decimal(b['seconds'])for a,b in zip(chain,chain[1:])),
       'Whole female packed-byte/count/RNG sequence retains actual native18')
  voices.append(dict(frame=int(row['frame']),caller=row['return_pc'],base=base,count=count))
 need(voices and not[r for r in routes if r['entry']=='FFA122D0'],'Whole mirror has female routes and no male/role proxy dispatch')
 return dict(performerIdentity=18,victimIdentity=18,initialSquareOwner=first['actor'],initialSquareMain=first['main'],
  actualParent=parent['a8'],actualChild=child['a8'],release=parent['frame'],blockedImpact=2974,impactCommand=0x63,
  blockVictimCommand=0x16,completeFemaleVoiceChains=voices,unblockedRingHitGruntAbsent=True)


def main():
 need(not OUT.exists() and not original.capture.process_tools.census(),'Fresh independent host check, no native process/replay')
 report=json.loads((CASE/'report.json').read_text());waveform=json.loads((CASE/'waveform.json').read_text())
 need(report['passed'] and report['nativeTerminal']['nativeExit']==0 and not report['nativeTerminal']['hostDecodeErrors'] and
      waveform['passed'] and waveform['differentChannelSamples']==0 and waveform['actualSHA256']==waveform['predictedSHA256'] and
      all(sha(p)==h for p,h in report['inputHashes'].items()),'Entire actual full current source PCM/DAC/ROM positive remains immutable')
 with gzip.open(CAPTURE/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 guest=original.capture.original.current.expected();headers=original.capture.mix.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(headers==report['pcmHeaders'] and original.capture.mix.rows(text,'MK2_NATIVE_DAC_RAM_DIGEST')==report['dacHeaders'],'Every actual callback digest matches complete RAM source proof')
 cue=cue_gate(text,guest);packet=original.packet_gate(text);channels=channel_gate(text,waveform,headers,report)
 faults=[]
 def alter(tag,key,value,where):
  line=next(s for s in text.splitlines()if s.startswith(tag+' ')and where in s)
  bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and bad!=line,'Nonvacuous actual mirror audio record fault');return text.replace(line,bad,1)
 for label,tag,key,value,where,gate in [
  ('wrong initial true identity','MK2_MAUDIO_BEGIN','id','1','origin=1823',lambda t:cue_gate(t,guest)),
  ('wrong Ring release','MK2_MAUDIO_ROUTE','a0','00000006','return_pc=FFFC48F0',lambda t:cue_gate(t,guest)),
  ('unblocked impact substituted','MK2_MAUDIO_ROUTE','a0','00000062','return_pc=FF8B0010',lambda t:cue_gate(t,guest)),
  ('child given parent owner','MK2_MAUDIO_ROUTE','a8',format(cue['actualParent'],'08X'),'return_pc=FF8B0010',lambda t:cue_gate(t,guest)),
  ('female selector given Liu identity','MK2_MAUDIO_ROUTE','a2','00000001','entry=FFA123B0',lambda t:cue_gate(t,guest)),
  ('wrong actual packet','MK2_MAUDIO_PACKET','a3','000000BE','frame=2945',original.packet_gate),
  ('wrong actual port byte','MK2_MAUDIO_SOUND','word','FF01','frame=2945',original.packet_gate),
  ('wrong ADSP delivery','MK2_MAUDIO_DELIVERY','word','0001','frame=2945',original.packet_gate),
  ('wrong winner marker','MK2_MAUDIO_SOUND','word','FFFE','pc=FFFB7140',original.packet_gate),
  ('wrong Square double position','MK2_TOMB_MIX_CHANNEL','bits','000000000000F03F','channel=12',lambda t:channel_gate(t,waveform,headers,report)),
  ('wrong initial timer video state','MK2_MAUDIO_CHANNEL','pos','0.00000000','channel=12',lambda t:channel_gate(t,waveform,headers,report)),
  ('looped winner','MK2_TOMB_MIX_CHANNEL','loop','1','channel=0',lambda t:channel_gate(t,waveform,headers,report)),
 ]:
  try:gate(alter(tag,key,value,where))
  except(ValueError,KeyError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual mirror audio fault accepted '+label)
 need(cue_gate(text,guest)==cue and original.packet_gate(text)==packet and channel_gate(text,waveform,headers,report)==channels,'Entire native positive restored after all actual faults')
 pins=dict(report['inputHashes'])
 for p in(CASE/'report.json',CASE/'waveform.json',Path(__file__),Path(original.__file__),ROOT/'samples/mk2ks/sonya_select.wav'):
  pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,currentMirrorBlockedRingSourceAudioAccepted=True,nativeTerminal=report['nativeTerminal'],
  completeStereoFrames=waveform['comparedStereoFrames'],wholePCMSHA256=waveform['actualSHA256'],cueProvenance=cue,
  nativeDelivery=packet,wholeSourceChannelClocks=channels,actualRecordFaultsRejected=faults,inputHashes=pins,
  remaining=report['remaining'],newNativeBoots=0,newBuilds=0,newRawMedia=0,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact proof losslessly compressed')
 print(json.dumps(dict(passed=True,stereoFrames=result['completeStereoFrames'],packets=packet,channels=channels,actualFaults=len(faults))),flush=True)


if __name__=='__main__':main()
