"""Whole same-run two-human mirror recovery and independent startup lifetimes.

Original physical/body/FIFO gate retained. Source timer is shared between
slots: the earlier actual launch starts it, not each subsequent marker.
No all-arena, KO/reset/morph or full-port acceptance.
"""
import collections,hashlib,inspect,json,struct,subprocess,wave
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
from pathlib import Path
import numpy as np
import launch_interruption_model_v6689 as old
import qualify_native_close_recovery as close
import qualify_ground_input_delivery_v6712 as delivery
import qualify_launch_interruption_v6691 as qualifier
ROOT,need,sha=old.ROOT,old.need,old.sha
rows,num=old.rows,old.num

def physical_gate():
 source=inspect.getsource(old.physical.check)
 replacements=[
  ('ids={side:identity,3-side:4}','ids={side:identity,3-side:17}'),
  ('floors[3-side]==83','floors[3-side]==82'),
  ("need(victim_damage>=0 and num(before[c,side],'hp')==num(by[z,side],'hp')==161,'Actual passive victim damage, never own identity/health substitution')",
   "need(victim_damage>=0 and 0<num(by[z,side],'hp')<=num(before[c,side],'hp')<=161,'Both real mirror health ledgers remain independently source-accounted')"),
  ("need((victim_damage==0)if move=='square'else(victim_damage>0),'Observed stationary square whiff distinguished from genuine damaging moves')",
   "need(victim_damage>=0,'Either roll may be interrupted without outgoing contact; whole health ledger remains')"),
  ('and int(h[\'slot\'])==3-side','and int(h[\'slot\'])in(1,2)'),
  ("any(num(by[f,side],'action')==0x101 for f in range(followup+112,followup+140))",
   "(any(num(by[f,side],'action')==0x101 for f in range(followup+112,followup+140))or close.close_punch(by,side,followup,rows,guest))"),
 ]
 for before,after in replacements:
  need(source.count(before)==1,'Only true mirror identity/health or original close-punch adaptation');source=source.replace(before,after,1)
 scope=dict(vars(old.physical),native=old.current,close=close)
 exec(compile(source,__file__+'::whole5115_true_mirror_body_recovery','exec'),scope)
 return scope['check']

def whole_physical(carrier):
 code=old.source
 code=code[code.index('def phase(carrier):'):code.index(" health=rows(text,'MK2_INTERRUPT_HEALTH')")]+" return whole\n"
 scope=dict(vars(old),physical_gate=physical_gate)
 exec(compile(code,__file__+'::whole_native_phase_body_FIFOs','exec'),scope)
 return scope['phase'](carrier)

def sources(carrier,pins):
 text=carrier['text'];starts=rows(text,'MK2_INTERRUPT_ENTRY');markers=[r for r in rows(text,'MK2_MAUDIO_SOUND')if r['word']=='6B03']
 commands=rows(text,'MK2_HSPECIAL_COMMAND');need(len(starts)==len(markers)==4 and len(commands)==2,'Both original native roll launches in both real cycles')
 fields={(int(r['frame']),int(r['slot'])):r for r in rows(text,'MK2_HSPECIAL_FIELD')}
 asset=ROOT/old.current.NAME/'samples/mk2ks/kano_ball_launch.wav'
 need(sha(asset)==old.current.ASSET_SHA,'Exact complete original Kano launch waveform');pins[str(asset)]=sha(asset)
 with wave.open(str(asset),'rb')as clip:
  need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,48000,55465),'Full original latency/tail-preserving mono source')
  values=np.frombuffer(clip.readframes(55465),'<i2').copy()
 sample,positions=old.audio.sample_values(values,48000);events=[];period=old.audio.ATTO//60
 for command in commands:
  frame=int(command['frame']);pair=[r for r in starts if frame<int(r['frame'])<frame+100]
  need(len(pair)==2 and {r['slot']for r in pair}=={'1','2'}and len({r['frame']for r in pair})==1,'Actual simultaneous field launches, not invented same-time markers')
  timer=min(int(Decimal(r['seconds'])*old.audio.ATTO)for r in pair)
  for entry in pair:
   slot=int(entry['slot']);marker=next(r for r in markers if r['frame']==entry['frame']and r['a8']==entry['actor'])
   physical=fields[int(entry['frame']),slot]
   need(marker['pc']==entry['pc']=='FFFFDEC0'and marker['mask']=='FFFF'and marker['a13']==entry['main']==physical['main']and
        marker['a8']==entry['actor']==physical['actor']==physical['owner']and physical['id']==physical['roster']=='17','Every marker binds its actual physical mirror owner and source opcode')
   start=old.audio.sample_clock(marker['seconds'],True)
   incoming=[r for r in rows(text,'MK2_INTERRUPT_HEALTH')if int(r['slot'])==slot and int(entry['frame'])<int(r['frame'])<frame+200 and int(r['after'])<int(r['before'])]
   need(len(incoming)<=1,'Each finite roll has at most one actual incoming contact')
   if incoming:
    damage=int(Decimal(incoming[0]['seconds'])*old.audio.ATTO);n=(damage-timer+period-1)//period
    stop=timer+n*period;previous=stop-period
    earlier=[int(Decimal(h['seconds'])*old.audio.ATTO)for h in carrier['pcmHeaders']if int(Decimal(h['seconds'])*old.audio.ATTO)<stop]
    update=max(max(earlier),previous)
    cutoff=old.audio.sample_clock(str(Decimal(update)/old.audio.ATTO),True)
    generated=cutoff-start
    need(0<generated<len(sample),'Real shared-timer interrupted prefix, not silence or EOF')
   else:
    generated=len(sample);incoming=None
    n=1
    while old.audio.sample_clock(str(Decimal(timer+n*period)/old.audio.ATTO),True)-start<len(sample):n+=1
    stop=timer+n*period;update=None
   events.append(dict(marker=marker,slot=slot,channel=10+2*(slot-1),start=start,stopAttoseconds=stop,
                      sharedTimerOrigin=timer,lastStreamUpdateAttoseconds=update,generatedBeforeStop=generated,
                      incoming=incoming[0]if incoming else None,sample=sample,positions=positions,length=len(values)))
 need(sum(e['incoming']is not None for e in events)==2 and {e['slot']for e in events if e['incoming']}=={1},'Actual scheduler result: P1 interrupted twice, P2 retains both full tails')
 return events

def owners(carrier,events):
 text=carrier['text'];first=int(rows(text,'MK2_HSPECIAL_READY')[0]['frame']);last=int(rows(text,'MK2_HSPECIAL_RESULT')[0]['frame'])
 records=rows(text,'MK2_INTERRUPT_OWNER');channels=rows(text,'MK2_INTERRUPT_CHANNEL')
 need(len(records)==2*(last-first+1)and {(int(r['frame']),int(r['slot']))for r in records}=={(f,s)for f in range(first,last+1)for s in(1,2)},'Every owner/ID/health snapshot in whole run')
 need(len(channels)==4*(last-first+1)and {(int(r['frame']),int(r['channel']))for r in channels}=={(f,c)for f in range(first,last+1)for c in range(10,14)},'All four complete battle source states')
 for r in records:
  time=int(Decimal(r['seconds'])*old.audio.ATTO);slot=int(r['slot'])
  active=[e for e in events if e['slot']==slot and int(Decimal(e['marker']['seconds'])*old.audio.ATTO)<time<e['stopAttoseconds']]
  need(len(active)<=1 and r['writes']=='0'and r['assistance']=='none','Source-owned finite lifetime and read-only record')
  if active:
   event=active[0];physical=next(f for f in rows(text,'MK2_HSPECIAL_FIELD')if f['frame']==event['marker']['frame']and f['slot']==r['slot'])
   need(r['actor']==event['marker']['a8']and r['main']==event['marker']['a13']and r['id']=='17'and r['health']==physical['hp'],'Every source-owned actor/Main/ID/HP until independent stop')
  else:need(r['actor']==r['main']=='00000000'and r['id']==r['health']=='0','Full owner retirement, no stale or cross-slot owner')
 for r in channels:
  need(r['loop']==r['paused']==r['writes']=='0'and r['assistance']=='none','Finite nonlooping unpaused battle source')
  if int(r['channel'])in(11,13):need(r['length']=='0'and r['position']=='0'and r['sample']=='4294967295','Unused aux channels stay genuinely idle')
  for event in events:
   if event['incoming']and int(r['channel'])==event['channel']and event['stopAttoseconds']<int(Decimal(r['seconds'])*old.audio.ATTO):
    later=any(e['channel']==event['channel']and e['start']>event['start']and Decimal(e['marker']['seconds'])<=Decimal(r['seconds'])for e in events)
    if not later:need(r['sample']=='4294967295'and float(r['position'])==event['positions'][event['generatedBeforeStop']-1],'Hit stops only its own channel at exact shared-timer stream prefix')
 return dict(passed=True,completeOwnerFields=len(records),completeBattleChannelFields=len(channels),independentHitAndEOFRetirement=True)

def predict(carrier,events):
 headers=carrier['pcmHeaders'];text=carrier['text'];begin,end=rows(text,'MK2_MAUDIO_BEGIN'),rows(text,'MK2_MAUDIO_RESULT')
 need(len(begin)==len(end)==1,'One complete audio window')
 first=int((Decimal(begin[0]['seconds'])*50).to_integral_value(rounding=ROUND_CEILING));last=int((Decimal(end[0]['seconds'])*50).to_integral_value(rounding=ROUND_FLOOR))
 need([Decimal(h['seconds'])for h in headers]==[Decimal(n)/50 for n in range(first,last+1)]and headers==rows(text,'MK2_BBAUDIO_PCM_DIGEST')and
      carrier['dacHeaders']==rows(text,'MK2_NATIVE_DAC_RAM_DIGEST'),'Whole exact scheduled sound window, every cache/interior/tail callback')
 pcm=np.frombuffer(b''.join(carrier['pcm']),'<i2').reshape(-1,2);dcs,clocks=old.audio.float_model()(carrier['dac'],carrier['dacHeaders'])
 need(dcs.shape==pcm.shape,'Entire original DAC/float/cache/resampler output')
 voices={c:np.zeros_like(dcs)for c in(10,12)}
 for event in events:
  for i,head in enumerate(headers):
   tick=int(Decimal(head['seconds'])*50);start=(tick-1)*960*(old.audio.ATTO//48000);s,f=divmod(start,old.audio.ATTO)
   at=np.arange(s*48000+f//old.audio.PERIOD,s*48000+f//old.audio.PERIOD+960,dtype=np.int64)-event['start']
   valid=(at>=0)&(at<event['generatedBeforeStop']);segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(event['sample'][at[valid]]*np.float32(.70))
   voices[event['channel']][i*960:(i+1)*960]+=segment[:,None]
 voice=np.float32(voices[10]+voices[12]);convert=lambda v:(np.clip(v,-1,1).astype(np.float64)*32767.0).astype('<i2')
 predicted=convert(np.float32(dcs+voice));diff=np.argwhere(pcm!=predicted)
 faults=[]
 if not len(diff):
  for channel in(10,12):
   bad=convert(np.float32(dcs+voices[22-channel]));need(not np.array_equal(bad,pcm),'Actual audible independent channel omitted')
   faults.append(dict(fault=f'channel{channel} omitted',differentChannelSamples=int(np.count_nonzero(bad!=pcm))))
  for label,index in [('first PCM bit',0),('last PCM bit',len(pcm)-1)]:
   bad=pcm.copy();bad[index,0]^=1;need(not np.array_equal(bad,predicted),'Actual boundary PCM bit fault');faults.append(dict(fault=label))
  for label,bad in [('first frame omitted',pcm[1:]),('last frame omitted',pcm[:-1])]:
   need(bad.shape!=predicted.shape,'Whole shape rejects boundary trim');faults.append(dict(fault=label))
 return dict(passed=not len(diff),comparedStereoFrames=len(pcm),differentChannelSamples=len(diff),firstDifferences=diff[:12].tolist(),
             actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
             actualWaveformFaultsRejected=faults,completeOriginalSourceClocks=clocks)

def qualify(carrier):
 out=ROOT/f"audit_launch_dual_roll_checked_p{carrier['side']}";need(not out.exists(),'Fresh same-terminal proof')
 need(carrier['terminal']['nativeExit']==0 and not carrier['decodeErrors']and carrier['report']['passed'],'Actual normal native terminal')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'All executed inputs intact')
 whole=whole_physical(carrier);inputs=delivery.delivered(carrier['text']);events=sources(carrier,pins)
 ownership=owners(carrier,events);audio=predict(carrier,events);need(audio['passed'],'Every complete output sample matches independent source model')
 gate,fault=qualifier.source_audio.dac_models(len(carrier['pcmHeaders']));dac=gate(carrier['dac'],carrier['dacHeaders'],carrier['pcmHeaders']);dac_faults=fault(carrier['dac'],carrier['dacHeaders'],carrier['pcmHeaders'])
 rg,rf=qualifier.source_audio.host.models.rom_models(carrier['expectedROM']);rom=[rg(bytes(carrier['rom'][p]),p)for p in carrier['rom']];rom_faults=[f for p in carrier['rom']for f in rf(bytes(carrier['rom'][p]),p)]
 packet=qualifier.packet_gate(carrier['text'])
 for path in [Path(__file__),Path(close.__file__),Path(delivery.__file__),Path(qualifier.__file__),ROOT/'tools/launch_interruption_model_v6686.py',Path(old.__file__),ROOT/'tools/verify_special_repeat_v5115.py',ROOT/'mame-mkp/src/devices/sound/samples.cpp',*carrier['folder'].rglob('*')]:
  if path.is_file():pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'Whole sources and actual evidence unchanged')
 proof=dict(passed=True,candidate=old.current.NAME,nativeTerminal=carrier['terminal'],wholePhysicalAndBodyContract=whole,physicalInputDelivery=inputs,
            completeIndependentOwnership=ownership,completeSourceWaveform=audio,sourceEvents=[{k:v for k,v in e.items()if k not in('sample','positions')}for e in events],
            sourceDAC=dac,actualDACFaultsRejected=dac_faults,entireOriginalSoundROM=rom,actualSoundROMFaultsRejected=rom_faults,completeNativeSoundDelivery=packet,
            inputHashes=pins,newNativeBoots=0,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,fullPortAcceptance=False,fullRasterAcceptance=False,
            fullOverlapCoverageAccepted=False,goalStatus='active')
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(proof,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Lossless exact proof')
 print(json.dumps(dict(passed=True,report=str(path),stereoFrames=audio['comparedStereoFrames'],differentChannelSamples=audio['differentChannelSamples'])),flush=True)
 return proof
