"""Exact source/guest delta and actual both-slot grab sound requests/behavior.

Adds MKII equivalents of original-game cues, not original MK3 sample playback.
No all-move audio/perceptual/CPU/full-game acceptance is implied.
"""
import json,re,struct,sys
from pathlib import Path
import numpy as np
import verify_ring_native_lookup_v1342 as prior
import verify_human_special_matrix as human
import inspect_current_move_audio_v1408 as media

ROOT=prior.ROOT;NAME='diagnostic_v1411_native_grab_audio';OUT=ROOT/'audit_v1415_native_grab_audio_checked'
SOURCE_ADDITIONS=(
 '\t// Original FFA2BF80 plays the shared swing at leg-grab startup.\n\t// Use MKII\'s ordinary unvoiced swing, not a donor fighter\'s voice.\n\tleg_call(0xffa11d30);\n',
 '\t// Original FFA2C340/FFA2C380: one contact impact and actual victim grunt.\n\tleg_call(0xffa11ea0);\n\tleg_movi(0,0xffa11fd0); leg_call(0xff842be0);\n',
 '\t// Original FFA2F490 requests the held victim\'s pain voice once on contact,\n\t// not at every damage pulse. Native callback keeps both real actor/Main IDs.\n\tleg_movi(0,0xffa11fd0); leg_call(0xff842be0);\n')

def need(test,message):
 if not test:raise ValueError(message)

def call(target):return struct.pack('<3H',0x0d5f,target&65535,target>>16)
def movi(reg,value):return struct.pack('<3H',0x09e0+reg,value&65535,value>>16)

def inserted_routine(old,start,limit,insertions):
 """Relocate only declared original absolute branch operands around additions."""
 blob=old[start:limit];end=(len(blob.rstrip(b'\xff'))+1)//2*2
 blob=bytearray(blob[:end]);points=[]
 for marker,addition in insertions:
  at=bytes(blob).find(marker);need(at>=0 and bytes(blob).count(marker)==1,'Unique original native instruction anchor')
  points.append((at+len(marker),addition))
 points.sort();low=0xff800000+start*8;high=low+len(blob)*8;branches=[]
 for at in range(0,len(blob)-3,2):
  target=struct.unpack_from('<I',blob,at)[0]
  if low<=target<high:
   need(at>=2 and struct.unpack_from('<H',blob,at-2)[0] in (0xc080,0xca80,0xcb80,0xc880,0xc980),'Only independently identified internal absolute branches may relocate')
   destination=(target-low)//8
   need(all(destination!=point for point,extra in points),'Insertion must not ambiguously replace a native branch label')
   translated=target+sum(len(extra)*8 for point,extra in points if point<destination)
   struct.pack_into('<I',blob,at,translated);branches.append(dict(original=f'{target:08X}',relocated=f'{translated:08X}'))
 rebuilt=b'';cursor=0
 for point,extra in points:rebuilt+=bytes(blob[cursor:point])+extra;cursor=point
 rebuilt+=bytes(blob[cursor:]);need(len(rebuilt)<=limit-start,'Existing owned native code allocation')
 return rebuilt+b'\xff'*(limit-start-len(rebuilt)),branches

def expected_guest():
 old,_,_,payload=prior.reconstruct();expected=bytearray(old)
 face=movi(0,0xff83cd50)+call(0xff842be0)
 leg,leg_branches=inserted_routine(old,0xf0100,0xf0400,[(movi(1,0x110)+call(0xff877ba0),call(0xffa11d30)),(face,call(0xffa11ea0)+movi(0,0xffa11fd0)+call(0xff842be0))])
 choke,choke_branches=inserted_routine(old,0xf2280,0xf2600,[(face,movi(0,0xffa11fd0)+call(0xff842be0))])
 expected[0xf0100:0xf0400]=leg;expected[0xf2280:0xf2600]=choke
 return bytes(expected),dict(leg=leg_branches,choke=choke_branches),payload

def verify():
 pins={}
 def pin(path,wanted=None):
  path=Path(path);key=str(path)
  if key not in pins:pins[key]=prior.digest(path)
  need(wanted is None or pins[key]==wanted,'Changed executed evidence '+key)
 folder=ROOT/NAME;compiled=json.loads((folder/'build-info.json').read_text(encoding='utf-8-sig'));pin(folder/'build-info.json')
 need(compiled['name']==NAME and compiled['prior_candidate']==prior.CANDIDATE and compiled['executable_sha256']=='01EF3950691A890BAA41723D99935E44A28B09A7431EA78EC5DBF8E0E90630C3','Matched new source-built candidate')
 for p,h in compiled['input_hashes'].items():pin(p,h)
 pin(folder/'mkport_candidate.exe',compiled['executable_sha256']);pin(folder/'roms/mk2ks/mk2ks.mdata',compiled['payload_sha256'])
 oldsource=ROOT/prior.CANDIDATE/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 source=folder/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 text=source.read_text()
 for block in SOURCE_ADDITIONS:need(text.count(block)==1,'Exactly one declared source addition');text=text.replace(block,'')
 need(text==oldsource.read_text(),'Whole compiled source differs only by three original-grounded cue additions')
 for name in ('midtunit.cpp','midtunit.h','midtunit_v.cpp','midtunit_v.h','mk2ks_native_picture.h'):
  a=folder/'input_sources/mame-mkp/src/mame/midway'/name;b=ROOT/prior.CANDIDATE/'input_sources/mame-mkp/src/mame/midway'/name
  pin(a);pin(b);need(a.read_bytes()==b.read_bytes(),'Unchanged driver/art/other native source')
 sourceproof=ROOT/'audit_v1342_native_ring_lookup_checked/report.json';base=json.loads(sourceproof.read_text());pin(sourceproof)
 need(base['passed'] and base['nativeROMAuditAccepted'],'Original whole native guest proof')
 for p,h in base['inputHashes'].items():pin(p,h)
 guest,branches,payload=expected_guest();need((folder/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Unchanged exact payload')
 prior_audio_path=ROOT/'audit_v1408_current_move_audio_checked/report.json';prior_audio=json.loads(prior_audio_path.read_text());pin(prior_audio_path)
 need(prior_audio['passed'] and prior_audio['candidate']==prior.CANDIDATE,'Complete prior real-input audio inventory')
 for p,h in prior_audio['inputHashes'].items():pin(p,h)
 originals={}
 for family in ('choke','leg','bicycle'):
  original=ROOT/f'audit_v1407_original_audio_{family}';launch=json.loads((original/'result.json').read_text(encoding='utf-8-sig'))
  need(launch['exit_code']==0 and launch['family']==family and launch['assistance']=='none' and launch['writes']==0,'Unassisted original-game reference')
  for p,h in launch['input_hashes'].items():pin(p,h)
  src=(ROOT/f'mk3_{family if family!="leg" else "leggrab"}_reference.lua').read_text()
  adapted=(ROOT/f'mk3_{family if family!="leg" else "leggrab"}_reference_v1406.lua').read_text()
  need(adapted==src.replace('emu.add_machine_frame_notifier','emu.register_frame').replace('emu.add_machine_stop_notifier','emu.register_stop'),'Original controls and state observation unchanged; only notifier API spelling adapted')
  log=(original/'run.log').read_text(encoding='utf-8-sig');need(not re.search('LUA ERROR|fatal error|stack traceback|access violation',log,re.I),'Original reference runtime')
  sounds=media.records(log,'MK3_SPECIAL_AUDIO_SOUND');terminal=media.records(log,'MK3_SPECIAL_AUDIO_RESULT')
  need(len(terminal)==1 and terminal[0]['frame']=='4651' and sounds,'Original complete actual sound interval')
  need(len(sounds)%2==0,'Whole original DCS byte pairs')
  commands=[]
  for high,low in zip(sounds[::2],sounds[1::2]):
   need(high['pc']=='FFAA88B0' and low['pc']=='FFAA8920' and high['frame']==low['frame'] and high['a8']==low['a8'],'Actual original native DCS pair')
   commands.append(dict(frame=int(high['frame']),seconds=float(high['seconds']),command=high['byte']+low['byte'],actor=high['a8']))
  if family=='choke':
   need('MK3_CHOKE_SELECTED p1=0 p2=1 target=near' in log and any(q['command']=='0816' for q in commands),'Original catch victim pain cue')
  elif family=='leg':
   states=media.records(log,'MK3_LEG_STATE');live=[q for q in states if q['frame']=='3900']
   need(len(live)==2 and [q['id'] for q in live]==['1','0'],'True original Sonya/Kano pair')
   need(commands[0]['command']=='009B' and any(q['command']=='006F' for q in commands) and any(q['command']=='13D0' for q in commands),'Original shared swing, impact and true victim pain cues')
  else:need('MK3_BICYCLE_REFERENCE_RESULT pass=true target=near' in log,'Actual original bicycle execution')
  for path in original.rglob('*'):
   if path.is_file():pin(path)
  originals[family]=dict(commands=commands,scope='Actual original MK3 reference; native MKII equivalents are deliberately not numerical MK3 command IDs')
 cases=[]
 for move in ('choke','leg','bicycle'):
  for side in (1,2):
   case=ROOT/f'audit_v1414_human_audio_{move}_p{side}';launch=json.loads((case/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((case/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
   need(launch['exit_code']==0 and launch['candidate']==NAME and launch['executable_sha256']==compiled['executable_sha256'] and launch['payload_sha256']==compiled['payload_sha256'] and launch['move']==move and launch['side']==side and launch['victim']=='sub_zero' and not launch['air'] and not launch['cheats_enabled'] and launch['assistance']=='none','Actual matched new audio fixture')
   need(before==launch['input_hashes'] and all(before.get(p)==h for p,h in compiled['input_hashes'].items()),'Complete executed manifest')
   for p,h in before.items():
    pin(p,h)
    if Path(p).suffix in('.lua','.ps1','.json'):pin(case/'input_sources'/Path(p).name,h)
   need((case/'guest_maincpu.bin').read_bytes()==guest,'Entire actual native guest equals independently relocated original plus declared cues')
   log=(case/'run.log').read_text(encoding='utf-8-sig');state=human.verify_log(log,move,side)
   old=ROOT/f'audit_v1398_human_audio_{move}_p{side}'
   events=lambda data:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',line)for line in data.splitlines()if line.startswith('MK2_HSPECIAL_')]
   need(events(log)==events((old/'run.log').read_text(encoding='utf-8-sig')),'Every original native input/state/pose/contact/damage/recovery event remains exact')
   for name in ('special_before.png','special_recovered.png','special_final.png'):need((case/'snap'/name).read_bytes()==(old/'snap'/name).read_bytes(),'Original actual full scenes remain byte-exact')
   requests=[q for q in media.records(log,'MK2_GRAB_AUDIO_REQUEST') if state['entry']<=int(q['frame'])<=state['recovered']]
   fields=human.rows(log,'FIELD');by={(q['frame'],q['slot']):q for q in fields}
   for q in requests:
    at=int(q['frame']);actor=int(q['actor'],16);main=int(q['main'],16);entry=int(q['entry'],16)
    physical=[n for n in (1,2) if actor==int(q[f'p{n}'],16) and main==int(q[f'p{n}main'],16)]
    need(len(physical)==1 and actor==int(q['owner'],16) and q['writes']=='0' and q['assistance']=='none' and int(q['pc'],16)==entry+16,'Actual physical actor/Main sound request; no proxy')
    need(by[at,physical[0]]['id']==int(q['id']),'Native sound lookup sees actual own/victim ID')
   contact=human.rows(log,'HEALTH')[0]['frame']
   expected=[(0xffa11fd0,contact,3-side)] if move=='choke' else [(0xffa11d30,state['entry'],side),(0xffa11ea0,contact,side),(0xffa11fd0,contact,3-side)] if move=='leg' else [(0xffa11ea0,int(q['frame']),side) for q in requests]
   actual=[(int(q['entry'],16),int(q['frame']),1 if q['actor']==q['p1'] else 2) for q in requests]
   need(actual==expected and (move!='bicycle' or len(actual)>=7),'Exactly timed requested cue inventory; no repeated choke grunts or false victim voice')
   rate,channels,mix=media.pcm(case/'game_mix.wav');terminal=media.records(log,'MK2_HAUDIO_RESULT')
   need((rate,channels)==(48000,2) and len(terminal)==1 and len(mix)/rate>=float(terminal[0]['seconds'])-.05,'Complete synchronized actual native PCM')
   sounds=media.records(log,'MK2_HAUDIO_SOUND');commands=[];pending=None
   for q in sounds:
    if q['pc']=='FFA13C90':need(pending is None,'Whole native command pair');pending=q
    elif q['pc']=='FFA13D60':
     need(pending is not None and pending['frame']==q['frame'],'Same actual DCS command field')
     commands.append(dict(frame=int(q['frame']),seconds=float(pending['seconds']),command=pending['word'][-2:]+q['word'][-2:]));pending=None
   need(pending is None,'No incomplete native sound command')
   interval=[q for q in commands if state['entry']<=q['frame']<=state['recovered']]
   if move in ('choke','leg'):
    native_contact=[q for q in interval if q['frame']==contact]
    need(len(native_contact)==(1 if move=='choke' else 2),'New actual contact commands reach native DCS')
    before_rate,_,before_mix=media.pcm(old/'game_mix.wav');need(before_rate==rate,'Matched PCM sampling')
    start=int(native_contact[0]['seconds']*rate);end=start+int(.35*rate)
    need(end<=len(mix) and end<=len(before_mix),'Actual contact waveform interval retained')
    delta=mix[start:end]-before_mix[start:end]
    need(np.count_nonzero(delta)>1000 and np.sqrt(np.mean(delta*delta))>1,'New contact cue changes actual PCM, not just sound-port logging')
    contact_pcm=dict(start=start/rate,duration=.35,changedSamples=int(np.count_nonzero(delta)),differenceRMS=float(np.sqrt(np.mean(delta*delta))),scope='Actual additional native sound energy; not isolated-waveform/perceptual equivalence')
   else:contact_pcm=None
   cases.append(dict(case=case.name,move=move,side=side,state=state,requests=requests,nativeCommands=interval,contactPCM=contact_pcm,everyPriorNativeHumanEventMatched=True,priorActualFullScreensByteMatched=3,wholeGuestExact=True))
   for path in case.rglob('*'):
    if path.is_file():pin(path)
 for module in tuple(sys.modules.values()):
  file=getattr(module,'__file__',None)
  if file and Path(file).resolve().is_relative_to(ROOT/'tools') and Path(file).suffix=='.py':pin(file)
 return dict(passed=True,candidate=NAME,cases=cases,originalReferences=originals,relocatedOriginalBranches=branches,
  inputHashes=pins,wholeGuestIndependentlyReconstructed=True,sourceDeltaOnlyDeclaredNativeGrabCues=True,
  bothSlotGrabContactRequestsAndPCMChangeAccepted=True,everyPriorNativeHumanEventMatched=True,exactPriorActualFullScreensMatched=18,
  noActorIDProxy=True,allMoveAudioAccepted=False,CPUAccepted=False,launcherPromoted=False,fullPortAccepted=False,
  scope='Original-grounded MKII native leg swing/contact and choke/leg actual victim pain requests, real PCM change, exact six human state/full-screen regressions; not full audio fidelity, all victims, defensive/KO/CPU cases, or release acceptance')

if __name__=='__main__':
 need(not OUT.exists(),'Never overwrite evidence')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),cases=len(report.get('cases',[]))),indent=2),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
