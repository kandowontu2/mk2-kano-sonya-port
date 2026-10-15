"""Full current Sonya Square KO/reset/rearm, body, owner and audio contracts."""
import collections,hashlib,inspect,json,struct,wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import qualify_launch_ko_round as prior
import verify_current_projectile_repeat_v5295 as floor_source
import qualify_native_close_recovery as close
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
rows,num=prior.rows,prior.num

source=inspect.getsource(prior.physical)
changes=[
 ("side=int(end['side'])", "side=int(end['side']);limit=5 if side==1 else 7;points=40 if side==1 else 26;ids={side:'18',3-side:'8'};floors={side:81,3-side:floor_source.subzero_floor(guest)}"),
 ("end['completed']==end['attempt']=='5'", "end['completed']==end['attempt']==str(limit+1)"),
 ("ko['p1HP']=='0'and ko['p2HP']=='161'", "ko['p'+str(side)+'HP']=='0'and ko['p'+str(3-side)+'HP']=='161'"),
 ("v['roster']=='17'", "v['roster']==ids[slot]"),
 ("v['floor']=='82'", "int(v['floor'])==floors[slot]"),
 ("v['id']=='17'", "v['id']==ids[slot]"),
 ("need([(v['slot'],int(v['before']),int(v['after']))for v in damage]==[('1',a,b)for a,b in((161,141),(141,117),(117,97),(97,73),(73,53),(53,29),(29,9),(9,0),(161,137))],\n      'Four actual low-kick/roll clashes earn KO; fresh post-reset roll damages only the genuine opponent')",
  "incoming=[v for v in damage if int(v['frame'])<k];want=[(str(side),max(0,161-i*points),max(0,161-(i+1)*points))for i in range(limit)]\n need([(v['slot'],int(v['before']),int(v['after']))for v in incoming]==want,'Every exact native40HP uppercut or26HP jump kick, including final KO saturation')\n for v in damage[limit:]:\n  need(int(v['frame'])>z and ((int(v['slot'])==side and int(v['before'])-int(v['after'])==points)or(int(v['slot'])==3-side and int(v['before'])-int(v['after'])==24 and int(v['frame'])==follow+120)),'Only actual post-reset original counter or commanded24HP close-punch contact')"),
 ("lethal=damage[7];need(int(lethal['frame'])==k-1 and by[k,1]['hp']=='0'and all(by[at,1]['hp']=='0'for at in range(k,int(next(v['frame']for v in health if v['pc']=='FF825930'))+1))",
  "lethal=damage[limit-1];need(int(lethal['frame'])==k-1 and by[k,side]['hp']=='0'and all(by[at,side]['hp']=='0'for at in range(k,int(next(v['frame']for v in health if v['pc']==('FF825930'if side==1 else'FF825960')))+1))"),
 ("int(by[at,side]['y'])<82", "int(by[at,side]['y'])<floors[side]"),
 ("any(int(by[at,side]['action'])==0x101 for at in range(follow+112,follow+140))", "(any(int(by[at,side]['action'])==0x101 for at in range(follow+112,follow+140))or close.close_punch({(at,s):by[at+1,s]for at,s in by if(at+1,s)in by},side,follow,{'MK2_HSPECIAL_HEALTH':rows(text,'MK2_HSPECIAL_HEALTH')},guest))"),
]
for before,after in changes:need(source.count(before)==1,'Exact true-ID/floor/attack/KO/counter adaptation');source=source.replace(before,after,1)
scope=dict(vars(prior),floor_source=floor_source,close=close);exec(compile(source,__file__+'::entire_native_KO_reset_health_input_contract_Sonya','exec'),scope)
physical=scope['physical']

def source_events(carrier,pins):
 text=carrier['text'];side=carrier['side'];fields={(int(r['frame']),int(r['slot'])):r for r in rows(text,'MK2_KO_FIELD')}
 starts=rows(text,'MK2_INTERRUPT_ENTRY');markers=[r for r in rows(text,'MK2_MAUDIO_SOUND')if r['word']=='6B00']
 limit=5 if side==1 else 7;need(len(starts)==len(markers)==limit+1,'Every real pre-KO launch plus fresh native post-reset Square launch')
 proof_path=ROOT/'audit_v5379_current_cpu_square_audio_ram_checked/report.json';proof=json.loads(proof_path.read_text());asset=ROOT/'samples/mk2ks/sonya_square_launch.wav'
 need(proof['passed']and proof['inputHashes'][str(asset)]==sha(asset),'Exact original source-qualified full Sonya Square waveform');pins[str(asset)]=sha(asset);pins[str(proof_path)]=sha(proof_path)
 with wave.open(str(asset),'rb')as clip:
  need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,48000,45512),'Entire original mono signed16/48k Square source')
  values=np.frombuffer(clip.readframes(45512),'<i2').copy()
 audio=prior.mirror.old.audio;sample,positions=audio.sample_values(values,48000);events=[];period=audio.ATTO//60
 damage=[r for r in rows(text,'MK2_INTERRUPT_HEALTH')if r['pc']=='FF836700'and int(r['slot'])==side]
 for index,(entry,marker)in enumerate(zip(starts,markers,strict=True)):
  at=int(entry['frame']);field=fields[at,side]
  need(entry['frame']==marker['frame']and entry['slot']==str(side)and entry['id']=='18'and entry['command']=='6B00'and entry['pc']==marker['pc']=='FFFFCAC0'and
       marker['mask']=='FFFF'and marker['a8']==entry['actor']==field['actor']==field['owner']and marker['a13']==entry['main']==field['main']and field['id']==field['roster']=='18', 'Every actual Square opcode, physical owner/Main and true selected Sonya identity')
  timer=int(Decimal(marker['seconds'])*audio.ATTO);start=audio.sample_clock(marker['seconds'],True)
  incoming=[r for r in damage if at<int(r['frame'])<at+120]
  need(len(incoming)<=1 and(index>=limit or len(incoming)==1),'All original pre-KO launches are actually interrupted, including lethal contact')
  if incoming:
   hit=incoming[0];clock=int(Decimal(hit['seconds'])*audio.ATTO);n=(clock-timer+period-1)//period;stop=timer+n*period
   earlier=[int(Decimal(h['seconds'])*audio.ATTO)for h in carrier['pcmHeaders']if int(Decimal(h['seconds'])*audio.ATTO)<stop];need(earlier,'Whole initial native PCM cache included')
   update=max(max(earlier),stop-period);generated=audio.sample_clock(str(Decimal(update)/audio.ATTO),True)-start
   need(0<generated<len(sample),'Real interrupted prefix, not silence or assumed EOF')
  else:
   hit=None;generated=len(sample);update=None;n=1
   while audio.sample_clock(str(Decimal(timer+n*period)/audio.ATTO),True)-start<len(sample):n+=1
   stop=timer+n*period
  events.append(dict(marker=marker,slot=side,channel=10+2*(side-1),start=start,stopAttoseconds=stop,sharedTimerOrigin=timer,
                     lastStreamUpdateAttoseconds=update,generatedBeforeStop=generated,incoming=hit,sample=sample,positions=positions,length=len(values)))
 return events

def owners(carrier,events):
 source=inspect.getsource(prior.mirror.owners)
 source=source.replace("rows(text,'MK2_HSPECIAL_FIELD')","rows(text,'MK2_KO_FIELD')")
 source=source.replace("r['id']=='17'","r['id']=='18'")
 before="  if int(r['channel'])in(11,13):need(r['length']=='0'and r['position']=='0'and r['sample']=='4294967295','Unused aux channels stay genuinely idle')"
 after="  if int(r['channel'])!=10+2*(carrier['side']-1):need(r['length']=='0'and r['position']=='0'and r['sample']=='4294967295','All unused/opponent battle channels stay genuinely idle')"
 need(source.count(before)==1,'Whole four-channel scope remains explicit');source=source.replace(before,after,1)
 # Cache complete parsed immutable tag inventories, not gameplay or acceptance.
 cached={};parse=rows
 def inventory(text,tag):
  if tag not in cached:cached[tag]=parse(text,tag)
  return cached[tag]
 scope=dict(vars(prior.mirror),rows=inventory);exec(compile(source,__file__+'::whole_actual_Sonya_source_owner_lifetimes','exec'),scope)
 return scope['owners'](carrier,events)

def body_publication(text,guest,by):
 source=inspect.getsource(prior.body_publication);before='ids={1:17,2:17}'
 need(source.count(before)==1,'Complete original descriptor/clip/FIFO binding')
 side=int(prior.one(text,'MK2_HSPECIAL_RESULT')['side']);scope=dict(vars(prior),body_ids={side:18,3-side:8})
 exec(compile(source.replace(before,'ids=body_ids'),__file__+'::entire_native_body_publication_Sonya_SubZero','exec'),scope)
 return scope['body_publication'](text,guest,by)

def predict(carrier,events,pins):
 source=inspect.getsource(prior.mirror.old.predict);before='events=source_events(carrier,pins);voice='
 need(source.count(before)==1,'Entire previous whole native float/PCM/source predictor')
 source=source.replace('def predict(carrier,pins):','def predict(carrier,pins,events):').replace(before,'voice=',1)
 scope=dict(vars(prior.mirror.old));exec(compile(source,__file__+'::whole_native_DCS_Square_source_mix_KO_reset','exec'),scope)
 return scope['predict'](carrier,pins,events)

def packet_gate(text):
 source=inspect.getsource(prior.mirror.qualifier.packet_gate)
 before='len(launches)in(2,4)';need(source.count(before)==1,'Original complete native packet grammar')
 source=source.replace(before,"len(launches)==(6 if audio('BEGIN')[0]['slot']=='1' else 8)")
 scope=dict(vars(prior.mirror.qualifier),prior=prior);exec(compile(source,__file__+'::whole_native_DCS_delivery_six_or_eight_Square_starts','exec'),scope)
 return scope['packet_gate'](text)

def qualify(carrier):
 out=ROOT/f"audit_sonya_launch_ko_round_checked_p{carrier['side']}";need(not out.exists(),'Fresh whole same-terminal current proof')
 need(carrier['report']['passed']and carrier['terminal']['nativeExit']==0 and not carrier['decodeErrors'],'Actual natural terminal and whole transport')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'All executed source/candidate pins stable')
 semantic,by=physical(carrier['text'],carrier['guest']);inputs=prior.mirror.delivery.delivered(carrier['text']);body=body_publication(carrier['text'],carrier['guest'],by)
 events=source_events(carrier,pins);owned=owners(carrier,events);audio=predict(carrier,events,pins);need(audio['passed'],'Whole actual native Square/DCS audio source-exact through KO and reset')
 dac_gate,dac_fault=prior.mirror.qualifier.source_audio.dac_models(len(carrier['pcmHeaders']));dac=dict(positive=dac_gate(carrier['dac'],carrier['dacHeaders'],carrier['pcmHeaders']),faults=dac_fault(carrier['dac'],carrier['dacHeaders'],carrier['pcmHeaders']))
 rg,rf=prior.mirror.qualifier.source_audio.host.models.rom_models(carrier['expectedROM']);rom=dict(positive=[rg(bytes(carrier['rom'][p]),p)for p in carrier['rom']],faults=[v for p in carrier['rom']for v in rf(bytes(carrier['rom'][p]),p)])
 packets=packet_gate(carrier['text'])
 for path in(Path(__file__),Path(prior.__file__),Path(floor_source.__file__),Path(close.__file__),Path(prior.mirror.__file__),ROOT/'tools/launch_interruption_model_v6686.py',ROOT/'tools/launch_interruption_model_v6689.py',ROOT/'tools/verify_special_repeat_v5115.py',ROOT/'mame-mkp/src/devices/sound/samples.cpp',*carrier['folder'].rglob('*')):
  if path.is_file():pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'Entire actual source/evidence unchanged')
 report=dict(passed=True,candidate=prior.mirror.old.current.NAME,nativeTerminal=carrier['terminal'],physicalKOResetRearm=semantic,wholeNativeInputDelivery=inputs,
             completeIndependentOwnership=owned,sampledNativeBodyDescriptorClipFIFO=body,completeSourceWaveform=audio,sourceDAC=dac,wholeSoundROM=rom,completeNativeDCSDelivery=packets,
             sourceEvents=[{k:v for k,v in e.items()if k not in('sample','positions')}for e in events],inputHashes=pins,newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,
             fullRasterAcceptance=False,allKOResetMorphCoverageAccepted=False,fullPortAcceptance=False,goalStatus='active')
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,side=carrier['side'],physicalFields=semantic['continuousPhysicalFields'],stereoFrames=audio['comparedStereoFrames'],differentChannelSamples=audio['differentChannelSamples'])),flush=True);return report
