"""Actual collision-earned KO, native health-fill/reset, rearm and recovery.

Keep complete physical/health/input/owned-body publication and source clocks.
P1's closed noninteractive host cannot prove its lost PCM; that gap is explicit.
P2's still-held native buffers additionally prove the whole winner/roll/DCS mix.
"""
import collections,gzip,hashlib,inspect,json,struct
from pathlib import Path
import numpy as np
import qualify_launch_dual_roll as mirror
import current_tomb_winner_mix_fault_model_v5789 as winner
ROOT,need,sha=mirror.ROOT,mirror.need,mirror.sha
rows,num=mirror.rows,mirror.num

def one(text,tag):
 records=rows(text,tag);need(len(records)==1,'One actual '+tag);return records[0]

def physical(text,guest):
 ready=int(one(text,'MK2_HSPECIAL_READY')['frame']);end=one(text,'MK2_HSPECIAL_RESULT');last=int(end['frame']);side=int(end['side'])
 ko=one(text,'MK2_HSPECIAL_KO');reset=one(text,'MK2_HSPECIAL_ROUND_RESET');rearm=one(text,'MK2_HSPECIAL_REARM_COMMAND');recovered=one(text,'MK2_HSPECIAL_REARM_RECOVERED');final=one(text,'MK2_HSPECIAL_KO_FINAL')
 k,z,c,r,f=(int(v['frame'])for v in(ko,reset,rearm,recovered,final));follow=int(final['followup'])
 need(ready<k<z<c<r<follow<f==last-1 and c==z+32 and follow==r+16 and f==follow+160 and end['completed']==end['attempt']=='5'and
      ko['p1HP']=='0'and ko['p2HP']=='161'and reset['p1HP']==reset['p2HP']=='161','Actual collision KO, native reset, fresh command/recovery and terminal control chronology')
 need(not rows(text,'MK2_HSPECIAL_FAILED'),'No controller failure or missing real boundary')
 records=rows(text,'MK2_KO_FIELD');by={(int(v['frame']),int(v['slot'])):v for v in records}
 need(len(by)==len(records)==2*(last-ready+1)and set(by)=={(at,s)for at in range(ready,last+1)for s in(1,2)},'Every continuous physical boundary field in both slots')
 publications={s:{key:by[ready,s][key]for key in('actor','main','owner')}for s in(1,2)}
 modes=[]
 for at in range(ready,last+1):
  mode=by[at,1]['mode'];need(mode==by[at,2]['mode'],'One actual native mode for each field')
  if not modes or modes[-1]!=mode:modes.append(mode)
  for slot in(1,2):
   v=by[at,slot];initial=publications[slot]
   need(v['writes']=='0'and v['assistance']=='none'and v['stage']=='0'and v['state']=='1'and v['roster']=='17'and
        v['main']==initial['main']and v['owner']==initial['owner']and v['floor']=='82','Actual stable true native roster/Main/floor throughout collision and native transition')
   if mode=='6':need(v['actor']=='00000000'and v['id']=='-1','Native round-init unpublished actor, not a proxy')
   else:need(v['actor']==v['owner']==initial['actor']and v['id']=='17','Actual genuine owned Kano before/after round recreation')
 need(modes==['2','5','6','7','2'],'Entire original combat/winner/round-init/precombat/combat mode ordering')
 health=rows(text,'MK2_INTERRUPT_HEALTH');sites={'FF825930','FF825960','FF836700','FF9DECE0','FF9DED10','FF9DEF40','FF9DEF70'}
 need({v['pc']for v in health}==sites,'All original damage/reset/sentinel/animated-health-fill sites actually observed')
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff836650,0xff836750),(0xff8258b0,0xff8259a0),(0xff9decb0,0xff9defa0)):
  a,b=(lo-0xff800000)//8,(hi-0xff800000)//8;need(guest[a:b]==original[a:b],'Entire original native damage/reset/animated refill instruction interval')
 writes=collections.defaultdict(list)
 for v in health:
  pc=int(v['pc'],16);slot=int(v['slot']);before,after=int(v['before']),int(v['after'])
  need(v['mask']=='FFFF'and v['writes']=='0'and v['assistance']=='none'and int(v['at'],16)==(0x010602f0 if slot==1 else 0x01060ec0)and
       struct.unpack_from('<3H',guest,(pc-48-0xff800000)//8)==tuple(int(v['op'+str(i)],16)for i in range(3)), 'Every native health store binds its actual slot/PC/opcode/mask')
  if pc==0xff836700:need(0<=after<before<=161,'Actual collision damage, including native KO saturation')
  elif pc in(0xff825930,0xff825960):need(after==161,'Original native round reset restores full health')
  elif pc in(0xff9dece0,0xff9ded10):need(before==161 and after==65535,'Original refill initialization sentinel, not damage')
  else:need((before==65535 and after==4)or(after==before+2 and 4<=before<160)or(before==160 and after==161),'Entire original two-step health fill, including first and last values')
  writes[int(v['frame']),slot].append(v)
 for at in range(ready,last):
  for slot in(1,2):
   hp=int(by[at,slot]['hp'])
   for v in writes[at,slot]:need(hp==int(v['before']),'Every native health-write chronology');hp=int(v['after'])
   need(hp==int(by[at+1,slot]['hp']),'Every actual physical HP transition fully explained by native stores')
 damage=[v for v in health if v['pc']=='FF836700']
 need([(v['slot'],int(v['before']),int(v['after']))for v in damage]==[('1',a,b)for a,b in((161,141),(141,117),(117,97),(97,73),(73,53),(53,29),(29,9),(9,0),(161,137))],
      'Four actual low-kick/roll clashes earn KO; fresh post-reset roll damages only the genuine opponent')
 lethal=damage[7];need(int(lethal['frame'])==k-1 and by[k,1]['hp']=='0'and all(by[at,1]['hp']=='0'for at in range(k,int(next(v['frame']for v in health if v['pc']=='FF825930'))+1)),
                         'Actual lethal contact reaches and retains KO until native reset')
 need(by[z,1]['hp']==by[z,2]['hp']=='161'and all(mirror.old.physical.clean(by[at,s])for at in(z,r,f,last)for s in(1,2)),'Native reset and rearm recovery/final leave both actual fighters clean')
 inputs=rows(text,'MK2_HSPECIAL_INPUT');want=[(follow+i,side,'Right'if int(by[follow,side]['x'])<int(by[follow,3-side]['x'])else'Left')for i in range(8)]+[(follow+i,side,'Up')for i in range(40,43)]+[(follow+i,side,'High_Punch')for i in range(112,115)]
 need([(int(v['frame']),int(v['slot']),v['button'])for v in inputs if int(v['frame'])>=follow]==want,'Entire actual post-reset walk/jump/punch input sequence')
 need(any(by[at,side]['x']!=by[follow,side]['x']for at in range(follow+1,follow+16))and
      any(int(by[at,side]['y'])<82 for at in range(follow+40,follow+85))and
      any(int(by[at,side]['action'])==0x101 for at in range(follow+112,follow+140)), 'Walk, jump and original standing punch actually activate after round reset')
 return dict(passed=True,continuousPhysicalFields=len(records),allNativeHealthWrites=len(health),actualCollisionDamageWrites=len(damage),nativeModeSequence=modes,
             koFrame=k,lethalHealthStore=lethal,fullHealthResetFrame=z,rearmCommand=c,rearmRecovered=r,ordinaryFollowup=follow,finalDraw=f,terminalFrame=last,
             actualPostResetWalkJumpPunchAccepted=True),by

def events(carrier,pins):
 source=inspect.getsource(mirror.sources)
 changes=[("commands=rows(text,'MK2_HSPECIAL_COMMAND');need(len(starts)==len(markers)==4 and len(commands)==2", "commands=rows(text,'MK2_HSPECIAL_COMMAND')+rows(text,'MK2_HSPECIAL_REARM_COMMAND');need(len(starts)==len(markers)==10 and len(commands)==5"),
          ("rows(text,'MK2_HSPECIAL_FIELD')","rows(text,'MK2_KO_FIELD')"),
          ("sum(e['incoming']is not None for e in events)==2","sum(e['incoming']is not None for e in events)==5"),
          ('Actual scheduler result: P1 interrupted twice, P2 retains both full tails','Actual P1 source stops at each collision, including KO and rearm; P2 retains all independent tails')]
 for before,after in changes:need(source.count(before)==1,'Exact extended five-cycle same-source clock contract');source=source.replace(before,after,1)
 scope=dict(vars(mirror));exec(compile(source,__file__+'::whole_shared_timer_events_through_KO_reset','exec'),scope)
 return scope['sources'](carrier,pins)

def owners(carrier,events):
 source=inspect.getsource(mirror.owners);before="rows(text,'MK2_HSPECIAL_FIELD')";need(source.count(before)==1,'Entire source-owned lifetime uses actual continuous boundary fields')
 scope=dict(vars(mirror));exec(compile(source.replace(before,"rows(text,'MK2_KO_FIELD')"),__file__+'::whole_owner_lifetimes_through_native_reset','exec'),scope)
 return scope['owners'](carrier,events)

def body_publication(text,guest,by):
 physical=mirror.old.physical;source=inspect.getsource(physical.check)
 start=source.index(" frames={s['frame']for s in scenes}");finish=source.index(' return dict(move=move',start)
 block=source[start:finish]
 starts=rows(text,'MK2_INTERRUPT_ENTRY');entry_frames=sorted({int(v['frame'])for v in starts})
 data={tag:rows(text,tag)for tag in('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE')}
 for tag in data:data[tag]=[v for v in data[tag]if int(v['frame'])not in entry_frames]
 scenes=rows(text,'MK2_HPHASE_RGB_DIGEST');scenes=[dict(v,frame=int(v['frame']))for v in scenes]
 publications={s:(num(by[min(at for at,slot in by),s],'actor'),num(by[min(at for at,slot in by),s],'main'))for s in(1,2)}
 code='def check():\n'+block+" return dict(sourceBoundBodyCandidates=len(candidates),nativePublishedBodyParts=len(queues),nativeClippedParts=clipped,entryBodyPublicationUnobservedFrames=sorted(entry_frames))\n"
 scope=dict(vars(physical),guest=guest,payload=(ROOT/mirror.old.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),scenes=scenes,rows=data,owners=publications,ids={1:17,2:17},cycle_results=[dict(entry=f)for f in entry_frames])
 exec(compile(code,__file__+'::entire_original_native_descriptor_clip_FIFO_contract','exec'),scope);return scope['check']()

def packet_gate(text):
 source=inspect.getsource(mirror.qualifier.packet_gate)
 before="need(not markers and len(launches)in(2,4)and all(r['mask']=='FFFF'for r in launches)and"
 after="need(len(markers)==1 and markers[0]['word']=='FFFE'and markers[0]['mask']=='FFFF'and len(launches)==10 and all(r['mask']=='FFFF'for r in launches)and"
 need(source.count(before)==1,'Whole original DCS packet grammar with actual round winner and ten startups')
 source=source.replace(before,after).replace('len(all_sounds)==len(sounds)+len(launches)and','len(all_sounds)==len(sounds)+len(launches)+len(markers)and')
 scope=dict(vars(mirror.qualifier));exec(compile(source,__file__+'::whole_original_DCS_delivery_with_round_winner','exec'),scope);return scope['packet_gate'](text)

def predict(carrier,events,pins):
 # Whole existing DAC/cache/roll predictor; add original winner source inside
 # the separate voice speaker, in native ascending mixer input order0,10,12.
 source=inspect.getsource(mirror.predict)
 before=" voice=np.float32(voices[10]+voices[12]);convert=lambda v:(np.clip(v,-1,1).astype(np.float64)*32767.0).astype('<i2')"
 after=""" marker=[r for r in rows(text,'MK2_MAUDIO_SOUND')if r['pc']=='FFFB7140']
 need(len(marker)==1 and marker[0]['word']=='FFFE','One actual native Kano round-winner source')
 values,frequency=winner.read_winner('kano',pins);sample,positions=winner.sample_values(values,frequency)
 start=winner.sample_clock(marker[0]['seconds'],True);win=np.zeros_like(dcs);gain=np.float32(np.float32(.70)*np.float32(.30))
 for i,head in enumerate(headers):
  tick=int(Decimal(head['seconds'])*50);at0=(tick-1)*960*(winner.ATTO//48000);s,f=divmod(at0,winner.ATTO)
  at=np.arange(s*48000+f//winner.PERIOD,s*48000+f//winner.PERIOD+960,dtype=np.int64)-start
  valid=(at>=0)&(at<len(sample));segment=np.zeros(960,dtype='<f4');segment[valid]=np.float32(sample[at[valid]]*gain);win[i*960:(i+1)*960]=segment[:,None]
 voice=np.float32(np.float32(win+voices[10])+voices[12]);convert=lambda v:(np.clip(v,-1,1).astype(np.float64)*32767.0).astype('<i2')"""
 need(source.count(before)==1,'Full original native float/DAC/cache/roll loop retained')
 source=source.replace(before,after).replace('def predict(carrier,events):','def predict(carrier,events,pins):')
 # Existing fault omits either actual roll channel; keep winner in that copy.
 source=source.replace("bad=convert(np.float32(dcs+voices[22-channel]))","bad=convert(np.float32(dcs+np.float32(win+voices[22-channel])))")
 scope=dict(vars(mirror),winner=winner,one=one);exec(compile(source,__file__+'::whole_native_roll_winner_DCS_mix','exec'),scope)
 return scope['predict'](carrier,events,pins)

def qualify(carrier,audio=True):
 out=ROOT/f"audit_launch_ko_round_checked_p{carrier['side']}";need(not out.exists(),'Fresh immutable actual terminal proof')
 terminal=json.loads((carrier['folder']/'native_terminal.json').read_text());need(carrier['report']['passed']and terminal==carrier['terminal']and terminal['nativeExit']==0 and not terminal['hostDecodeErrors'],'Actual current naturally terminal transport')
 pins=dict(carrier.get('pins',carrier['report']['inputHashes']));need(all(sha(p)==h for p,h in pins.items()),'Whole actual executed inputs stable')
 guest=carrier['guest'];need(hashlib.sha256(guest).hexdigest().upper()==mirror.old.current.GUEST_SHA,'Independently reconstructed exact guest matches both actual inventory digests')
 for v in rows(carrier['text'],'MK2_HPHASE_GUEST_DIGEST')+rows(carrier['text'],'MK2_MAUDIO_GUEST_DIGEST'):need(v['sha256']==mirror.old.current.GUEST_SHA,'Every actual complete guest inventory retained')
 semantic,by=physical(carrier['text'],guest);inputs=mirror.delivery.delivered(carrier['text']);body=body_publication(carrier['text'],guest,by);packets=packet_gate(carrier['text'])
 full_audio=None;ownership=None;source_events=None;dac=None;rom=None
 if audio:
  source_events=events(carrier,pins);ownership=owners(carrier,source_events);full_audio=predict(carrier,source_events,pins);need(full_audio['passed'],'Every whole actual native roll/winner/DCS PCM sample source-exact')
  gate,fault=mirror.qualifier.source_audio.dac_models(len(carrier['pcmHeaders']));dac=dict(positive=gate(carrier['dac'],carrier['dacHeaders'],carrier['pcmHeaders']),actualFaultsRejected=fault(carrier['dac'],carrier['dacHeaders'],carrier['pcmHeaders']))
  rg,rf=mirror.qualifier.source_audio.host.models.rom_models(carrier['expectedROM']);rom=dict(positive=[rg(bytes(carrier['rom'][p]),p)for p in carrier['rom']],actualFaultsRejected=[v for p in carrier['rom']for v in rf(bytes(carrier['rom'][p]),p)])
 for path in(Path(__file__),Path(mirror.__file__),Path(winner.__file__),Path(mirror.old.physical.__file__),Path(mirror.delivery.__file__),Path(mirror.qualifier.__file__),ROOT/'mame-mkp/src/emu/disound.cpp',ROOT/'mame-mkp/src/emu/speaker.cpp',ROOT/'mame-mkp/src/devices/sound/samples.cpp',*carrier['folder'].rglob('*')):
  if path.is_file():pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All whole current source/evidence pins preserved')
 report=dict(passed=True,candidate=mirror.old.current.NAME,nativeTerminal=terminal,physicalKOResetRearm=semantic,wholeNativeInputDelivery=inputs,
             sampledNativeBodyDescriptorClipFIFO=body,wholeNativeDCSDelivery=packets,completeIndependentOwnership=ownership,completeSourceWaveform=full_audio,
             sourceEvents=[{k:v for k,v in e.items()if k not in('sample','positions')}for e in source_events]if source_events else None,
             sourceDAC=dac,originalSoundROM=rom,inputHashes=pins,completeAudioAccepted=audio,fullRasterAcceptance=False,
             firstHostPCMReleasedBeforeQualification=not audio,fullPortAcceptance=False,allKOResetMorphCoverageAccepted=False,goalStatus='active',
             newBuilds=0,newROMCopies=0,newRawMedia=0,newNativeBoots=0)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,physicalFields=semantic['continuousPhysicalFields'],audioAccepted=audio,stereoFrames=full_audio['comparedStereoFrames']if full_audio else None)),flush=True);return report

def load_first():
 folder=ROOT/'audit_launch_ko_round_ball_p1_delay1';report=json.loads((folder/'report.json').read_text());text=gzip.open(folder/'run.log.gz','rt').read()
 return dict(folder=folder,side=1,move='ball',text=text,guest=mirror.old.current.expected(),report=report,terminal=report['nativeTerminal'])
