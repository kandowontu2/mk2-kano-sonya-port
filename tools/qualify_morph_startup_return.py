"""Actual Shang roster6, real form17/18, late special and native return."""
import inspect,json,wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import qualify_launch_challenger_transition as original
import verify_morph_adversity_v3235 as morph
ROOT,need,sha=original.ROOT,original.need,original.sha
rows=original.rows;clock=original.clock

def physical(c):
 text=c['text'];side=c['side'];identity=17 if c['move']=='ball'else 18;target='kano'if identity==17 else'sonya'
 source=inspect.getsource(original.physical_inventory)
 need(source.count("'MK2_JR_RESULT'")==1,'Whole native health ledger changes only its terminal tag')
 source=source.replace("'MK2_JR_RESULT'","'MK2_HUMAN_SHANG_RESULT'",1)
 scope=dict(vars(original));exec(compile(source,__file__+'::complete_native_physical_and_health_inventory','exec'),scope)
 inventory,by=scope['physical_inventory'](c)
 first=int(original.prior.one(text,'MK2_MAUDIO_BEGIN')['frame']);end=original.prior.one(text,'MK2_HUMAN_SHANG_RESULT');last=int(end['frame'])
 match=original.prior.one(text,'MK2_HUMAN_SHANG_MATCH');stores=rows(text,'MK2_HUMAN_SHANG_STORE');reverse=rows(text,'MK2_HUMAN_SHANG_RESTORE_BEGIN')
 need(first==int(match['frame'])==int(end['match']) and last==first+2400 and end['forms']==end['restores']=='1'and end['errors']=='0'and len(stores)==2,'Whole actual cold human morph and 2400-field ordinary tail')
 formed,restored=stores;f,z=int(formed['frame']),int(restored['frame'])
 own=by[first,side];other=by[first,3-side]
 need(formed['old']=='6'and formed['id']==str(identity)and formed['pc']=='FF86E670'and int(formed['a9'],16)==identity and restored['old']==str(identity)and restored['id']=='6'and restored['pc']=='FFA16700'and restored['a0']=='00000006','Original native forward and reverse identity writes, never a proxy roster')
 need(reverse and int(reverse[0]['frame'])==f+512 and z==int(reverse[-1]['frame'])+12,'Original timed return starts at512 and genuine final return completes after12 fields; retries retained')
 for r in stores:need(r['actor']==own['actor']and r['main']==own['main']and r['side']==str(side)and r['target']==target and r['writes']=='0','True current own actor/Main native identity stores')
 pairs=rows(text,'MK2_HUMAN_SHANG_PAIR');need(len(pairs)==len(by)and not rows(text,'MK2_HUMAN_SHANG_PAIR_MISSING'),'Every independent old-driver physical publication retained')
 for r in pairs:
  state=by[int(r['frame']),int(r['slot'])]
  need(all(r[k]==state[k]for k in('actor','main','owner','state','roster','id','hp','pose','x','y','floor','vx','vy','gravity','flags','body','trail'))and int(r['action'],16)==int(state['action']),'Every independently observed original driver field equals full pre-task physical state')
 for at in range(first,last+1):
  for slot in(1,2):
   r=by[at,slot];initial=own if slot==side else other;expected=identity if slot==side and f<at<=z else 6 if slot==side else 17
   need(r['mode']=='2'and r['state']=='1'and r['roster']==str(6 if slot==side else 17)and r['id']==str(expected)and r['actor']==r['owner']==initial['actor']and r['main']==initial['main']and r['floor']==str({6:87,17:82,18:81}[expected]),'Every actual human ownership/identity/floor through form, special, return and ordinary controls')
 expected=morph.expected_own_inputs(target,side,'formed','added')
 if identity==17:
  for at in range(f+400,f+484):expected[at-first]='Low_Kick'
 else:
  forward='Right'if side==1 else'Left';back='Left'if side==1 else'Right'
  for n in range(484,493):
   commands=[]
   if 484<=n<487:commands.append(forward)
   if 489<=n<492:commands.append(back)
   if 490<=n<493:commands.append('High_Punch')
   if commands:expected[f+n-first]=','.join(commands)
 inputs=rows(text,'MK2_HUMAN_SHANG_INPUT');need(len(inputs)==len(expected)and{int(r['age']):r['buttons']for r in inputs}==expected,'Every original morph/ordinary input plus exact late special command')
 need(not rows(text,'MK2_HUMAN_SHANG_ATTACK')and all(r['button']in('Left','Right')for r in rows(text,'MK2_HUMAN_SHANG_OPINPUT')),'Opponent closes using real directions only; no forced interruption')
 for at in range(first+1100,first+1110):need(by[at+1,side]['x']!=by[at,side]['x'],'Restored Shang actually walks under ordinary input')
 need(any(int(by[at,side]['y'])<int(by[at,side]['floor'])for at in range(first+1140,first+1190)),'Restored Shang actually jumps')
 need(len({by[at,side]['pose']for at in range(first+1250,first+1290)})>1,'Restored Shang ordinary punch has genuine pose progression')
 tail=by[last,side];need(tail['id']=='6'and tail['y']==tail['floor']and tail['vx']==tail['vy']==tail['gravity']==tail['trail']=='00000000'and int(tail['flags'],16)&0x1c==0,'Final restored Shang grounded and responsive, no retained special effect')
 inventory.update(originalForwardStoreFrame=f,originalReturnStoreFrame=z,originalReturnEntries=[int(r['frame'])for r in reverse],nativeRosterRemainsShang=True,actualOrdinaryControlsAfterReturnAccepted=True,physicalInputs=len(inputs))
 return inventory,by

def events(c,pins,by):
 markers=[r for r in rows(c['text'],'MK2_MAUDIO_SOUND')if r['word'].startswith('6B')];need(len(markers)==1,'One actual late native startup')
 marker=markers[0];identity=17 if c['move']=='ball'else 18;side=c['side'];at=int(marker['frame']);r=by[at,side]
 need(marker['word']==('6B03'if identity==17 else'6B00')and marker['pc']==('FFFFDEC0'if identity==17 else'FFFFCAC0')and marker['mask']=='FFFF'and marker['a8']==r['actor']==r['owner']and marker['a13']==r['main']and r['id']==str(identity)and r['roster']=='6','Real native form identity executes its own special while underlying selection remains Shang6')
 path=ROOT/original.prior.mirror.old.current.NAME/'samples/mk2ks/kano_ball_launch.wav'if identity==17 else ROOT/'samples/mk2ks/sonya_square_launch.wav';pins[str(path)]=sha(path)
 with wave.open(str(path),'rb')as clip:
  need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,48000,55465 if identity==17 else 45512),'Whole original donor launch asset')
  sample,positions=clock.sample_values(np.frombuffer(clip.readframes(clip.getnframes()),'<i2'),48000)
 start=clock.sample_clock(marker['seconds'],True);origin=int(Decimal(marker['seconds'])*clock.ATTO);period=clock.ATTO//60;n=1
 while clock.sample_clock(str(Decimal(origin+n*period)/clock.ATTO),True)-start<len(sample):n+=1
 stop=origin+n*period
 # Source-driven EOF is not adjusted to the observed PCM or return timestamp.
 active=[v for v in rows(c['text'],'MK2_INTERRUPT_OWNER')if v['slot']==str(side)and origin<int(Decimal(v['seconds'])*clock.ATTO)<stop]
 need(active and all(v['id']==str(identity)and v['health']==r['hp']and v['actor']==r['actor']and v['main']==r['main']for v in active),'Whole source-owned form remains valid until original EOF timer')
 return [dict(marker=marker,slot=side,channel=10+2*(side-1),start=start,stopAttoseconds=stop,sharedTimerOrigin=origin,lastStreamUpdateAttoseconds=None,generatedBeforeStop=len(sample),incoming=None,sample=sample,positions=positions,length=55465 if identity==17 else 45512)]

def owners(c,events):
 source=inspect.getsource(original.owners)
 before="'MK2_JR_RESULT'";need(source.count(before)==1,'Whole ownership gate terminal-only adaptation');source=source.replace(before,"'MK2_HUMAN_SHANG_RESULT'",1)
 scope=dict(vars(original));exec(compile(source,__file__+'::whole_ownership_through_morph_and_return','exec'),scope)
 return scope['owners'](c,events)

def predict(c,events,pins):
 source=inspect.getsource(original.predict)
 before="len(speech)==2 and {r['word']for r in speech}=={'FFFB','FFFC'}and all(r['mask']=='FFFF'for r in speech)"
 need(source.count(before)==1,'Complete source mix in a no-selection-in-combat window');source=source.replace(before,'not speech',1)
 before="for channel in(0,events[0]['channel']):";need(source.count(before)==1,'Only actual audible source omission tested');source=source.replace(before,"for channel in(events[0]['channel'],):",1)
 scope=dict(vars(original));exec(compile(source,__file__+'::whole_DAC_and_form_startup_source_mix','exec'),scope)
 return scope['predict'](c,events,pins)[0]

def packets(text):
 source=inspect.getsource(original.prior.mirror.qualifier.packet_gate)
 before='len(launches)in(2,4)';need(source.count(before)==1,'Whole original DCS packet/ADSP grammar, one startup');source=source.replace(before,'len(launches)==1',1)
 scope=dict(vars(original.prior.mirror.qualifier));exec(compile(source,__file__+'::all_native_DCS_delivery','exec'),scope)
 return scope['packet_gate'](text)

def qualify(c):
 out=ROOT/f"audit_morph_startup_return_checked_{c['move']}_p{c['side']}";need(not out.exists(),'Fresh same-terminal morph integration proof')
 need(c['report']['passed']and c['terminal']['nativeExit']==0 and not c['decodeErrors'],'Actual normal native terminal')
 pins=dict(c['pins']);need(all(sha(p)==h for p,h in pins.items()),'All actual compiled/controller sources stable')
 state,by=physical(c);sources=events(c,pins,by);ownership=owners(c,sources);audio=predict(c,sources,pins);need(audio['passed'],'Entire actual PCM equals complete native DAC and original launch source')
 gate,fault=original.prior.mirror.qualifier.source_audio.dac_models(len(c['pcmHeaders']));dac=dict(positive=gate(c['dac'],c['dacHeaders'],c['pcmHeaders']),faults=fault(c['dac'],c['dacHeaders'],c['pcmHeaders']))
 rg,rf=original.prior.mirror.qualifier.source_audio.host.models.rom_models(c['expectedROM']);rom=dict(positive=[rg(bytes(c['rom'][p]),p)for p in c['rom']],faults=[v for p in c['rom']for v in rf(bytes(c['rom'][p]),p)])
 delivery=packets(c['text'])
 for p in(Path(__file__),Path(original.__file__),Path(morph.__file__),ROOT/'mame-mkp/src/devices/sound/samples.cpp',*c['folder'].rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Whole exact executed proof sources stable')
 report=dict(passed=True,candidate=original.prior.mirror.old.current.NAME,nativeTerminal=c['terminal'],completePhysicalAndHealthInventory=state,completeIndependentOwnership=ownership,completeSourceWaveform=audio,sourceDAC=dac,wholeSoundROM=rom,completeNativeDCSDelivery=delivery,sourceEvents=[{k:v for k,v in e.items()if k not in('sample','positions')}for e in sources],inputHashes=pins,allMorphContextsAccepted=False,fullRasterAcceptance=False,fullPortAcceptance=False,goalStatus='active',newNativeBoots=0,newBuilds=0,newRawMedia=0)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,move=c['move'],side=c['side'],physicalFields=state['continuousPhysicalFields'],stereoFrames=audio['comparedStereoFrames'])),flush=True);return report
