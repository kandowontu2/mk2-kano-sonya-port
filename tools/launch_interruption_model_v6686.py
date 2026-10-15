"""Complete two-cycle native hit/owner cleanup and whole source-audio model.

Keep the whole5115 physical/body/descriptor/FIFO gate; admit actual incoming
native damage through its same complete health ledger, not a passive-victim
assumption. Independent real uppercut, exact owner/ID retirement and source
timer/stream arithmetic distinguish exercised interruption from a miss.
No universal collision, KO, morph, selection or all-port acceptance.
"""
import collections,hashlib,inspect,json,re,struct,wave
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
from pathlib import Path
import numpy as np
import verify_special_repeat_v5115 as physical
import verify_current_projectile_repeat_v5295 as victim
import current_tomb_winner_mix_fault_model_v5789 as audio
import kano_ball_launch_context_v6642 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
rows,num=audio.rows,physical.num


def physical_gate():
 source=inspect.getsource(physical.check)
 changes={
  'ids={side:identity,3-side:4}':'ids={side:identity,3-side:8}',
  'floors[3-side]==83':'floors[3-side]==victim.subzero_floor(guest)',
  "need(victim_damage>=0 and num(before[c,side],'hp')==num(by[z,side],'hp')==161,'Actual passive victim damage, never own identity/health substitution')":
   "need(victim_damage>=0 and 0<num(by[z,side],'hp')<=num(before[c,side],'hp')<=161,'Actual incoming/outgoing damage accounted by whole native health ledger, never identity/health substitution')",
  "need((victim_damage==0)if move=='square'else(victim_damage>0),'Observed stationary square whiff distinguished from genuine damaging moves')":
   "need(victim_damage>=0,'An interrupted special need not complete its contact; every actual HP transition still requires a native source store')",
  "and int(h['slot'])==3-side":"and int(h['slot'])in(1,2)",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Exact whole original two-cycle interruption adaptation '+before)
  source=source.replace(before,after,1)
 scope=dict(physical.__dict__,native=current,victim=victim)
 exec(compile(source,__file__+'::whole5115_semantics_incoming_damage','exec'),scope)
 return scope['check']


def phase(carrier):
 text=carrier['text'];guest=carrier['guest'];side=carrier['side'];move=carrier['move']
 need(carrier['report']['passed']and guest==current.expected(),'Actual current whole guest and native transport terminal')
 data=collections.defaultdict(list)
 for line in text.splitlines():
  if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):
   data[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
 need(not data['MK2_HSPECIAL_FAILED'],'Original full controller reached both natural recoveries')
 terminal=data['MK2_HSPECIAL_RESULT'];need(len(terminal)==1,'Exactly one full real physical controller terminal')
 entries={int(r['frame'])for r in data['MK2_HSPECIAL_EVENT']if num(r,'entry')==physical.SPECS[move][1]}
 for tag in('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE'):
  data[tag]=[r for r in data[tag]if int(r['frame'])not in entries]
 scenes=[dict(frame=int(r['frame']),attempt=int(r['attempt']),stage=r['stage'],width=int(r['width']),height=int(r['height']),
              bytes=int(r['bytes']),sha256=r['sha256'],rawMediaFilesWritten=0)for r in carrier['rgb']]
 # These fields are independently bound by the captured actual kernel path,
 # unchanged EXE hash and every actual initialized guest/GFX byte, not by an
 # invented old capture result or rewritten report.
 report=dict(carrier['report'],nativeExit=carrier['terminal']['nativeExit'],executableSHA256=current.EXE_SHA,
             guestSHA256=current.GUEST_SHA,payloadSHA256=current.PAYLOAD_SHA,terminalResult=terminal[0],actualScenes=scenes)
 b=dict(move=move,side=side,rows=data,report=report)
 whole=physical_gate()(b,guest,(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes())
 health=rows(text,'MK2_INTERRUPT_HEALTH')
 for h in health:
  pc=int(h['pc'],16);need(pc==0xff836700 and h['mask']=='FFFF'and h['writes']=='0'and h['assistance']=='none'and
   int(h['at'],16)==(0x010602f0 if h['slot']=='1'else 0x01060ec0)and
   struct.unpack_from('<3H',guest,(pc-48-0xff800000)//8)==tuple(int(h['op'+str(i)],16)for i in range(3)),
   'Every real incoming/outgoing health store binds unchanged native instruction bytes')
 incoming=[h for h in health if int(h['slot'])==side and int(h['after'])<int(h['before'])]
 need(len(incoming)==2,'Two genuinely landed incoming hits; no acceptance for an unexercised input attempt')
 starts=rows(text,'MK2_INTERRUPT_ENTRY');uppercuts=rows(text,'MK2_INTERRUPT_UPPERCUT')
 need(len(starts)==len(uppercuts)==2,'Two source-owned real launches and two original opponent uppercut entries')
 first=int(terminal[0]['ready']);last=int(terminal[0]['frame']);fields=data['MK2_HSPECIAL_FIELD']
 before={(int(r['frame']),int(r['slot'])):r for r in fields}
 owner_rows=rows(text,'MK2_INTERRUPT_OWNER');owners={(int(r['frame']),int(r['slot'])):r for r in owner_rows}
 channel_rows=rows(text,'MK2_INTERRUPT_CHANNEL');channels={(int(r['frame']),int(r['channel'])):r for r in channel_rows}
 need(len(owners)==len(owner_rows)==(last-first+1)*2 and set(owners)=={(f,s)for f in range(first,last+1)for s in(1,2)}and
      len(channels)==len(channel_rows)==(last-first+1)*4 and set(channels)=={(f,c)for f in range(first,last+1)for c in range(10,14)},
      'Every actual video-frequency ownership/identity and all four battle source states')
 identity=physical.SPECS[move][0];base=10+2*(side-1);cycles=[]
 for index,(entry,hit,uppercut,c)in enumerate(zip(starts,incoming,uppercuts,whole['cycles'],strict=True)):
  start,at,end=int(entry['frame']),int(hit['frame']),c['recovered'];own=before[start,side];opponent=before[start,3-side]
  need(start==c['entry']and start<at<end and int(hit['before'])-int(hit['after'])==40 and
       int(hit['before'])==num(own,'hp')and int(hit['after'])==num(before[end,side],'hp'),
       'One real40-point incoming hit interrupts each already launched cycle; native ledger explains cumulative HP')
  need(uppercut['entry']=='FF870DC0'and uppercut['pc']=='FF870DD0'and uppercut['mask']=='FFFF'and
       int(uppercut['opcode'],16)==struct.unpack_from('<H',guest,(0xff870dc0-0xff800000)//8)[0]and
       uppercut['actor']==uppercut['owner']==opponent['actor']==hit['a8']and uppercut['main']==opponent['main']==hit['a13']and
       uppercut['id']=='8'and start<int(uppercut['frame'])<=at,
       'Actual unchanged original uppercut instruction and real physical opponent owns the incoming damage')
  hurt=[f for f in range(at+1,at+3)if num(before[f,side],'action')==0x503 and num(before[f,side],'gravity')==0x6000 and num(before[f,side],'vy')==0xfff40000]
  need(hurt,'Native uppercut hurt task reaches original airborne503/gravity/launch vector')
  for f in range(start+1,at+1):
   r=owners[f,side];need(r['actor']==own['actor']and r['main']==own['main']and int(r['health'])==int(hit['before'])and int(r['id'])==identity,
                       'Actual correct fighter/ID/health owns its running launch before incoming contact')
  recovered_stop={}
  lengths={base:55465 if move=='ball'else45512 if move=='square'else40720}
  if move=='bicycle':lengths[base+1]=66523
  for channel,length in lengths.items():
   stop=channels[at+1,channel]
   need(int(stop['length'])==length and 0<float(stop['position'])<length and stop['sample']=='4294967295',
        'Actual complete source played and stopped mid-cue, not a silence-only or EOF case')
   for f in range(at+1,end+1):
    r=channels[f,channel];need(r['bits']==stop['bits']and r['position']==stop['position']and r['sample']=='4294967295',
                              'Interrupted source clock freezes by first callback after damage and never resumes through recovery')
   recovered_stop[str(channel)]=dict(position=float(stop['position']),bits=stop['bits'])
  cycles.append(dict(serial=index+1,entry=start,hit=at,recovered=end,healthBefore=int(hit['before']),healthAfter=int(hit['after']),
                     uppercutEntry=int(uppercut['frame']),nativeHurtTask=min(hurt),stoppedPositions=recovered_stop))
 for f in range(first,last+1):
  active=next((c for c in cycles if c['entry']<f<=c['hit']),None)
  for s in(1,2):
   r=owners[f,s];need(r['writes']=='0'and r['assistance']=='none','Every ownership snapshot read-only')
   if s!=side or not active:
    need(r['actor']==r['main']=='00000000'and r['health']==r['id']=='0','Complete ownership and expected identity clear; opponent remains untouched')
  for channel in range(10,14):
   r=channels[f,channel];need(r['writes']==r['loop']==r['paused']=='0'and r['assistance']=='none','Finite passive battle source states')
   if channel not in lengths:need(r['length']=='0'and float(r['position'])==0 and r['sample']=='4294967295','All opponent and unused battle channels remain idle')
 return dict(passed=True,wholePhysicalAndSourceBodyContract=whole,actualInterruptedCycles=cycles,
             completeOwnershipFields=len(owner_rows),completeBattleChannelFields=len(channel_rows),
             fullInterruptionCoverageAccepted=False,fullPortAcceptance=False)


def source_events(carrier,pins):
 text=carrier['text'];side=carrier['side'];base=10+2*(side-1)
 mapping={'6B00':('sonya_square_launch',13,base),'6B01':('sonya_bicycle_launch',14,base),
          '6B02':('sonya_bicycle_cry',15,base+1),'6B03':('kano_ball_launch',16,base)}
 markers=[r for r in rows(text,'MK2_MAUDIO_SOUND')if r['word']in mapping]
 health=[r for r in rows(text,'MK2_INTERRUPT_HEALTH')if int(r['slot'])==side and int(r['after'])<int(r['before'])]
 need(len(health)==2,'Actual source-stop prediction requires both real incoming health transitions')
 events=[]
 for index,hit in enumerate(health):
  cycle=rows(text,'MK2_INTERRUPT_ENTRY')[index]
  onset=int(Decimal(cycle['seconds'])*audio.ATTO);damage=int(Decimal(hit['seconds'])*audio.ATTO);period=audio.ATTO//60
  n=(damage-onset+period-1)//period;stop=onset+n*period;previous=onset+(n-1)*period
  need(previous<damage<=stop,'Actual health change precedes first source-derived60Hz ownership tick')
  earlier=[int(Decimal(h['seconds'])*audio.ATTO)for h in carrier['pcmHeaders']if int(Decimal(h['seconds'])*audio.ATTO)<stop]
  need(earlier,'Whole native pre-entry sound callbacks present')
  for marker in markers:
   if marker['frame']!=cycle['frame']:continue
   name,sample_id,channel=mapping[marker['word']]
   path=(ROOT/current.NAME/'samples/mk2ks'/f'{name}.wav')if sample_id==16 else ROOT/'samples/mk2ks'/f'{name}.wav'
   pins[str(path)]=sha(path)
   if sample_id==16:need(sha(path)==current.ASSET_SHA,'Complete actual original Kano startup source')
   with wave.open(str(path),'rb')as clip:
    need(clip.getnchannels()==1 and clip.getsampwidth()==2 and clip.getcomptype()=='NONE','Whole original mono signed16 source asset')
    length,frequency=clip.getnframes(),clip.getframerate();values=np.frombuffer(clip.readframes(length),'<i2').copy()
   sample,positions=audio.sample_values(values,frequency)
   start=audio.sample_clock(marker['seconds'],True)
   # stop() clears the pointer without updating the stream. Main playing()
   # syncs at each preceding ownership tick; the auxiliary cry is not queried
   # while main playback short-circuits the native && expression.
   last_update=max(max(earlier),previous)if channel==base else max(earlier)
   cutoff=audio.sample_clock(str(Decimal(last_update)/audio.ATTO),True)
   count=max(0,min(len(sample),cutoff-start));need(0<count<len(sample),'Source-derived genuinely interrupted finite sample prefix')
   events.append(dict(marker=marker,start=start,cutoff=cutoff,stopAttoseconds=stop,lastStreamUpdateAttoseconds=last_update,
                      channel=channel,sample_id=sample_id,length=length,frequency=frequency,sample=sample,positions=positions,
                      generatedBeforeStop=count,sourceAsset=str(path),sourceAssetSHA256=sha(path)))
 need(len(events)==(4 if carrier['move']=='bicycle'else 2),'Every real launched source in both interrupted cycles accounted')
 return events


def predict(carrier,pins):
 headers=carrier['pcmHeaders'];text=carrier['text'];begin=rows(text,'MK2_MAUDIO_BEGIN');end=rows(text,'MK2_MAUDIO_RESULT')
 need(len(begin)==len(end)==1,'One complete actual audio admission and terminal')
 first=int((Decimal(begin[0]['seconds'])*50).to_integral_value(rounding=ROUND_CEILING))
 last=int((Decimal(end[0]['seconds'])*50).to_integral_value(rounding=ROUND_FLOOR))
 need([Decimal(h['seconds'])for h in headers]==[Decimal(n)/50 for n in range(first,last+1)]and
      headers==rows(text,'MK2_BBAUDIO_PCM_DIGEST')and carrier['dacHeaders']==rows(text,'MK2_NATIVE_DAC_RAM_DIGEST'),
      'Entire exact50Hz source window with every initial/cache/interior/final callback retained')
 pcm=np.frombuffer(b''.join(carrier['pcm']),'<i2').reshape(-1,2)
 dcs,clocks=audio.float_model()(carrier['dac'],carrier['dacHeaders']);need(pcm.shape==dcs.shape,'Whole native DAC/resampler and complete PCM')
 events=source_events(carrier,pins);voice=np.zeros_like(dcs);unstopped=np.zeros_like(dcs);gain=np.float32(.70)
 for event in events:
  for i,head in enumerate(headers):
   tick=int(Decimal(head['seconds'])*50);start=(tick-1)*960*(audio.ATTO//48000);s,f=divmod(start,audio.ATTO)
   view=s*48000+f//audio.PERIOD;at=np.arange(view,view+960,dtype=np.int64)-event['start']
   for target,limit in((voice,event['generatedBeforeStop']),(unstopped,len(event['sample']))):
    valid=(at>=0)&(at<limit);segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(event['sample'][at[valid]]*gain)
    target[i*960:(i+1)*960]+=segment[:,None]
 convert=lambda v:(np.clip(v,-1,1).astype(np.float64)*32767.0).astype('<i2')
 predicted=convert(np.float32(dcs+voice));different=np.argwhere(predicted!=pcm);faults=[]
 if not len(different):
  for label,n,c in(('first PCM bit',0,0),('last PCM bit',len(pcm)-1,1)):
   bad=pcm.copy();bad[n,c]^=1;need(not np.array_equal(bad,predicted),'Actual complete output bit fault rejected')
   faults.append(dict(fault=label,differentChannelSamples=int(np.count_nonzero(bad!=pcm))))
  for label,bad in(('first cached stereo frame omitted',pcm[1:]),('last stereo frame omitted',pcm[:-1])):
   need(bad.shape!=predicted.shape,'Complete shape rejects actual omitted stereo frame');faults.append(dict(fault=label,rejectedBy='whole source shape'))
  late=np.zeros_like(voice);late[1:]=voice[:-1]
  for label,bad in(('owned launch source omitted',convert(dcs)),('interrupted source keeps playing',convert(np.float32(dcs+unstopped))),
                    ('source one sample late',convert(np.float32(dcs+late))),('original route gain omitted',convert(np.float32(dcs+voice/gain)))):
   need(not np.array_equal(bad,pcm),'Audible nonvacuous original-source operation fault: '+label)
   faults.append(dict(fault=label,differentChannelSamples=int(np.count_nonzero(bad!=pcm))))
 return dict(passed=not len(different),comparedStereoFrames=len(pcm),differentChannelSamples=len(different),
             actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
             firstDifferences=[dict(stereoFrame=int(n),channel=int(c),expected=int(predicted[n,c]),actual=int(pcm[n,c]))for n,c in different[:12]],
             sourceEvents=[{k:v for k,v in e.items()if k not in('sample','positions')}for e in events],
             exactNativeSourceClocks=clocks,actualRawAndSourceFaultsRejected=faults,
             sourceStopsDerivedFromNativeTimerAndStreamOperations=True,fullInterruptionCoverageAccepted=False,fullPortAcceptance=False)
