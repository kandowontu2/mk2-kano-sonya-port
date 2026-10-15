"""Live startup to paid selection: complete original ordinary-play contract."""
import collections,hashlib,inspect,json,struct,wave
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
from pathlib import Path
import numpy as np
import qualify_launch_ko_round as prior
import qualify_current_challenger_boundary_v6489 as challenger
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
rows=prior.rows;clock=prior.mirror.old.audio

def physical_inventory(c):
 text=c['text'];first=int(prior.one(text,'MK2_MAUDIO_BEGIN')['frame']);last=int(prior.one(text,'MK2_JR_RESULT')['frame'])
 records=rows(text,'MK2_KO_FIELD');by={(int(r['frame']),int(r['slot'])):r for r in records}
 need(len(records)==len(by)==2*(last-first+1)and set(by)=={(f,s)for f in range(first,last+1)for s in(1,2)},'Every pre-task physical field through teardown/selection/new match/ordinary play')
 for f in range(first,last+1):
  need(by[f,1]['mode']==by[f,2]['mode']and all(by[f,s]['writes']=='0'and by[f,s]['assistance']=='none'for s in(1,2)), 'Both actual slots and one read-only native mode each callback')
 health=rows(text,'MK2_INTERRUPT_HEALTH');writes=collections.defaultdict(list)
 for r in health:
  pc=int(r['pc'],16);slot=int(r['slot']);before,after=int(r['before']),int(r['after'])
  need(r['mask']=='FFFF'and r['writes']=='0'and r['assistance']=='none'and int(r['at'],16)==(0x010602f0 if slot==1 else 0x01060ec0)and
       struct.unpack_from('<3H',c['guest'],(pc-48-0xff800000)//8)==tuple(int(r['op'+str(i)],16)for i in range(3)), 'Every native health store binds actual slot/PC/full opcode context')
  if pc==0xff836700:need(0<=after<before<=161,'Actual native collision damage and saturation')
  elif pc in(0xff825930,0xff825960):need(after==161,'Original full-health reset')
  elif pc in(0xff9dece0,0xff9ded10):need(before==161 and after==65535,'Original native fill sentinel')
  elif pc in(0xff9def40,0xff9def70):need((before==65535 and after==4)or(after==before+2 and 4<=before<160)or(before==160 and after==161),'Whole original native animated health fill')
  else:raise ValueError('Unqualified native health writer '+r['pc'])
  writes[int(r['frame']),slot].append(r)
 for f in range(first,last):
  for s in(1,2):
   hp=int(by[f,s]['hp'])
   for r in writes[f,s]:need(hp==int(r['before']),'Whole native health store chronology');hp=int(r['after'])
   need(hp==int(by[f+1,s]['hp']),'Every physical health transition explained by original stores')
 return dict(passed=True,continuousPhysicalFields=len(records),allNativeHealthWrites=len(health)),by

def pre_cpu_gate(text,events,side,own):
 by={(int(r['frame']),int(r['slot'])):r for r in rows(text,'MK2_KO_FIELD')}
 count=0;nulls=[]
 for f in range(events['coldMatch'],events['join']+1):
  for s in(1,2):
   r=by[f,s];need(r['mode']in('2','5','6','7')and r['state']==str(1 if s==side else 0)and(s!=side or r['roster']==str(own)),'Whole actual initial human/CPU ownership, including genuine intervening native round reset')
   if r['mode']=='6':need(r['actor']=='00000000'and r['id']=='-1','Native round-init unpublished actor, not invented proxy');nulls.append(dict(frame=f,slot=s))
   else:need(r['actor']==r['owner']and r['id']==r['roster'],'Every actual published initial human/CPU actor and Main owner')
   count+=1
 return dict(fields=count,nativeRoundInitNullPublications=nulls)

source=inspect.getsource(challenger.executed.gate)
start=source.index(" for frame in range(events['coldMatch']+1,events['join']+1):")
end=source.index(' highlights=rows',start)
source=source[:start]+" initial=pre_cpu_gate(text,events,side,own)\n"+source[end:]
changes=(
 ("events['join']==events['coldMatch']+600", "events['join']==int(rows(text,'MK2_JR_ACTUAL_LAUNCH')[0]['frame'])+1"),
 (" for button,at in (('Coin',10),('Coin',30),('Start',60)):", " for button,at in (('Coin',events['coldMatch']+80-events['join']),('Coin',events['coldMatch']+90-events['join']),('Start',0)):"),
 ("range(events['match']+1,events['terminal']+1)","range(events['match'],events['terminal'])"),
 ('len(tail)==601','len(tail)==600'),
 ('ordinaryTailFieldsPerSlot=601','ordinaryTailFieldsPerSlot=600'),
 ('originalCPUFields=600','originalCPUFields=initial[\'fields\'],nativeRoundInitNullPublications=initial[\'nativeRoundInitNullPublications\']'),
)
for before,after in changes:need(source.count(before)==1,'Whole original challenger/ordinary-play contract; exact physical launch and native round-init adaptation');source=source.replace(before,after,1)
scope=dict(vars(challenger.executed),pre_cpu_gate=pre_cpu_gate)
exec(compile(source,__file__+'::whole_original_joined_identity_highlight_six_hundred_field_combat_contract','exec'),scope)
gameplay_gate=scope['gate']

def source_events(c,pins):
 text=c['text'];side=c['side'];word='6B03'if c['move']=='ball'else'6B00';identity=17 if word=='6B03'else 18
 markers=[r for r in rows(text,'MK2_MAUDIO_SOUND')if r['word'].startswith('6B')];need(len(markers)==1 and markers[0]['word']==word,'One genuine physically launched startup before paid join')
 marker=markers[0];at=int(marker['frame']);fields={(int(r['frame']),int(r['slot'])):r for r in rows(text,'MK2_KO_FIELD')};field=fields[at,side]
 need(marker['pc']==('FFFFDEC0'if identity==17 else'FFFFCAC0')and marker['mask']=='FFFF'and marker['a8']==field['actor']==field['owner']and marker['a13']==field['main']and field['id']==field['roster']==str(identity),'Actual native action marker and true selected actor/Main/ID')
 boundary=next(f for f in sorted({f for f,s in fields})if f>at and fields[f,side]['mode']!='2');left,right=fields[boundary-1,side],fields[boundary,side]
 need(left['mode']=='2'and right['mode']=='14'and all(r['actor']==r['owner']==marker['a8']and r['main']==marker['a13']and r['id']==str(identity)and r['hp']==field['hp']for r in(left,right)),'Actual unchanged running owner enters native challenger teardown, not incoming-hit/EOF retirement')
 timer=int(Decimal(marker['seconds'])*clock.ATTO);period=clock.ATTO//60
 ticks=[timer+n*period for n in range(1,100)if int(Decimal(left['seconds'])*clock.ATTO)<timer+n*period<=int(Decimal(right['seconds'])*clock.ATTO)]
 need(len(ticks)==1,'Unique original60Hz noncombat guard tick in actual mode/owner bracket, no PCM clock fit');stop=ticks[0]
 asset=ROOT/prior.mirror.old.current.NAME/'samples/mk2ks/kano_ball_launch.wav'if identity==17 else ROOT/'samples/mk2ks/sonya_square_launch.wav'
 pins[str(asset)]=sha(asset)
 with wave.open(str(asset),'rb')as clip:
  need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,48000,55465 if identity==17 else 45512),'Whole original native startup asset')
  sample,positions=clock.sample_values(np.frombuffer(clip.readframes(clip.getnframes()),'<i2'),48000)
 start=clock.sample_clock(marker['seconds'],True)
 update=max([int(Decimal(h['seconds'])*clock.ATTO)for h in c['pcmHeaders']if int(Decimal(h['seconds'])*clock.ATTO)<stop]+[stop-period])
 generated=clock.sample_clock(str(Decimal(update)/clock.ATTO),True)-start
 need(0<generated<len(sample),'Actual noncombat interruption of audible partial startup, not an idle/EOF selection test')
 return [dict(marker=marker,slot=side,channel=10+2*(side-1),start=start,sample=sample,positions=positions,length=len(sample),generatedBeforeStop=generated,
  stopAttoseconds=stop,lastStreamUpdateAttoseconds=update,incoming=dict(reason='native challenger noncombat'),nativeBoundaryFrame=boundary)]

def owners(c,events):
 source=inspect.getsource(prior.mirror.owners)
 for before,after in (("rows(text,'MK2_HSPECIAL_READY')","rows(text,'MK2_MAUDIO_BEGIN')"),("rows(text,'MK2_HSPECIAL_RESULT')","rows(text,'MK2_JR_RESULT')"),("rows(text,'MK2_HSPECIAL_FIELD')","rows(text,'MK2_KO_FIELD')"),("r['id']=='17'","r['id']==('17'if carrier['move']=='ball'else'18')")):
  need(source.count(before)==1,'Whole original precise lifetime/retired-channel contract');source=source.replace(before,after,1)
 cached={}
 def inventory(text,tag):
  if tag not in cached:cached[tag]=rows(text,tag)
  return cached[tag]
 scope=dict(vars(prior.mirror),rows=inventory);exec(compile(source,__file__+'::whole_live_source_ownership_through_selection_and_rebuilt_pair','exec'),scope)
 return scope['owners'](c,events)

def predict(c,events,pins):
 headers=c['pcmHeaders'];text=c['text'];begin=prior.one(text,'MK2_MAUDIO_BEGIN');end=prior.one(text,'MK2_MAUDIO_RESULT')
 first=int((Decimal(begin['seconds'])*50).to_integral_value(rounding=ROUND_CEILING));last=int((Decimal(end['seconds'])*50).to_integral_value(rounding=ROUND_FLOOR))
 need([Decimal(h['seconds'])for h in headers]==[Decimal(n)/50 for n in range(first,last+1)]and headers==rows(text,'MK2_BBAUDIO_PCM_DIGEST')and c['dacHeaders']==rows(text,'MK2_NATIVE_DAC_RAM_DIGEST'),'Every original initial/cache/interior/terminal sound callback')
 pcm=np.frombuffer(b''.join(c['pcm']),'<i2').reshape(-1,2);dcs,clocks=clock.float_model()(c['dac'],c['dacHeaders']);need(pcm.shape==dcs.shape,'Whole native float DAC/cache/resampler')
 voices={i:np.zeros_like(dcs)for i in(0,10,12)};speech=[r for r in rows(text,'MK2_MAUDIO_SOUND')if r['pc']=='FFFF3DA0']
 need(len(speech)==2 and {r['word']for r in speech}=={'FFFB','FFFC'}and all(r['mask']=='FFFF'for r in speech),'Both actual native queued Sonya/Kano selection announcements')
 name_events=[]
 for i,marker in enumerate(speech):
  path=ROOT/'samples/mk2ks'/('kano_select.wav'if marker['word']=='FFFC'else'sonya_select.wav');pins[str(path)]=sha(path)
  with wave.open(str(path),'rb')as clip:
   need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,16000,18400),'Whole original16k selection source')
   sample,positions=clock.sample_values(np.frombuffer(clip.readframes(18400),'<i2'),16000)
  start=clock.sample_clock(marker['seconds'],True);limit=len(sample)
  if i+1<len(speech):limit=min(limit,clock.sample_clock(speech[i+1]['seconds'],True)-start)
  name_events.append(dict(marker=marker,channel=0,start=start,sample=sample,positions=positions,generatedBeforeStop=limit,gain=np.float32(np.float32(.70)*np.float32(.30))))
 for e in events+name_events:
  for i,h in enumerate(headers):
   tick=int(Decimal(h['seconds'])*50);at0=(tick-1)*960*(clock.ATTO//48000);s,f=divmod(at0,clock.ATTO)
   at=np.arange(s*48000+f//clock.PERIOD,s*48000+f//clock.PERIOD+960,dtype=np.int64)-e['start'];valid=(at>=0)&(at<e['generatedBeforeStop'])
   segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(e['sample'][at[valid]]*e.get('gain',np.float32(.70)));voices[e['channel']][i*960:(i+1)*960]+=segment[:,None]
 voice=np.float32(np.float32(voices[0]+voices[10])+voices[12]);convert=lambda v:(np.clip(v,-1,1).astype(np.float64)*32767.0).astype('<i2')
 predicted=convert(np.float32(dcs+voice));diff=np.argwhere(pcm!=predicted)
 faults=[]
 if not len(diff):
  for label,index in(('first PCM bit',0),('last PCM bit',len(pcm)-1)):
   bad=pcm.copy();bad[index,0]^=1;need(not np.array_equal(predicted,bad),'Actual changed boundary PCM rejected');faults.append(label)
  need(pcm[1:].shape!=predicted.shape and pcm[:-1].shape!=predicted.shape,'Whole first/cache/final shape checks');faults+=['first PCM frame omitted','last PCM frame omitted']
  for channel in(0,events[0]['channel']):
   bad=convert(np.float32(dcs+np.float32(voice-voices[channel])));need(not np.array_equal(bad,pcm),'Actual audible source channel omitted');faults.append('channel'+str(channel)+' omitted')
 return dict(passed=not len(diff),comparedStereoFrames=len(pcm),differentChannelSamples=len(diff),firstDifferences=diff[:12].tolist(),actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),actualWaveformFaultsRejected=faults,completeSourceClocks=clocks),name_events

def packet_gate(text):
 source=inspect.getsource(prior.mirror.qualifier.packet_gate)
 before='not markers and len(launches)in(2,4)';need(source.count(before)==1,'Whole original native sound delivery grammar')
 source=source.replace(before,"len(markers)==2 and {r['word']for r in markers}=={'FFFB','FFFC'}and all(r['pc']=='FFFF3DA0'and r['mask']=='FFFF'for r in markers)and len(launches)==1",1)
 source=source.replace('len(all_sounds)==len(sounds)+len(launches)and','len(all_sounds)==len(sounds)+len(launches)+len(markers)and',1)
 scope=dict(vars(prior.mirror.qualifier));exec(compile(source,__file__+'::whole_DCS_delivery_and_actual_selection_markers','exec'),scope)
 return scope['packet_gate'](text)

def qualify(c):
 out=ROOT/f"audit_launch_challenger_transition_checked_{c['move']}_p{c['side']}";need(not out.exists(),'Fresh complete same-terminal transition proof')
 need(c['report']['passed']and c['terminal']['nativeExit']==0 and not c['decodeErrors'],'Actual authoritative normal terminal')
 pins=dict(c['pins']);need(all(sha(p)==h for p,h in pins.items()),'Whole actual executed sources/candidate unchanged')
 state,by=physical_inventory(c);fighter='kano'if c['move']=='ball'else'sonya';game=gameplay_gate(c['text'],fighter,c['side']);events=source_events(c,pins);owned=owners(c,events)
 waveform,names=predict(c,events,pins);need(waveform['passed'],'Every complete startup/selection-announcer/DCS sample source-exact')
 gate,fault=prior.mirror.qualifier.source_audio.dac_models(len(c['pcmHeaders']));dac=dict(positive=gate(c['dac'],c['dacHeaders'],c['pcmHeaders']),faults=fault(c['dac'],c['dacHeaders'],c['pcmHeaders']))
 rg,rf=prior.mirror.qualifier.source_audio.host.models.rom_models(c['expectedROM']);rom=dict(positive=[rg(bytes(c['rom'][p]),p)for p in c['rom']],faults=[v for p in c['rom']for v in rf(bytes(c['rom'][p]),p)])
 packet=packet_gate(c['text'])
 for p in(Path(__file__),Path(prior.__file__),Path(challenger.__file__),Path(challenger.executed.__file__),ROOT/'mame-mkp/src/devices/sound/samples.cpp',*c['folder'].rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All exact source/evidence pins stable')
 report=dict(passed=True,candidate=prior.mirror.old.current.NAME,nativeTerminal=c['terminal'],completePhysicalAndHealthInventory=state,wholeOriginalJoinedGameplay=game,completeIndependentOwnership=owned,completeSourceWaveform=waveform,sourceDAC=dac,wholeSoundROM=rom,completeNativeDCSDelivery=packet,
  sourceEvents=[{k:v for k,v in e.items()if k not in('sample','positions')}for e in events],selectionNameEvents=[{k:v for k,v in e.items()if k not in('sample','positions','gain')}for e in names],
  fullCurrentUIRasterAcceptance=False,allSelectionMorphCoverageAccepted=False,fullPortAcceptance=False,goalStatus='active',inputHashes=pins,newBuilds=0,newRawMedia=0,newNativeBoots=0)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,move=c['move'],side=c['side'],physicalFields=state['continuousPhysicalFields'],stereoFrames=waveform['comparedStereoFrames'])),flush=True);return report
