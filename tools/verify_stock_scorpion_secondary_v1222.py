"""Genuine Scorpion secondary activation/state gate; no full art acceptance.

Use two original stock controls, both true added victims in both slots,
independently reconstructed current guest, original held-HP release parser,
real collision KOs, native victim callbacks and original completion. Actual
images are pinned for separate review, not promoted to source/pixel fidelity.
"""
import hashlib,json,re,struct
from pathlib import Path
from PIL import Image
import verify_stock_fire_v1197 as state
import verify_native_headed_reaction_v1221 as headed
ROOT=state.ROOT
CASES=('control_kitana_p1','control_liu_p2','kano_p1','kano_p2','sonya_p1','sonya_p2')
OUT=ROOT/'audit_v1222_stock_secondary_state_checked'

def verify(texts=None,reconstructed=None,check_files=True):
 guest=(reconstructed if reconstructed is not None else headed.reconstruct())[0]
 errors=[];pins={};cases={};controls={}
 def need(ok,label):
  if not ok:errors.append(label)
 def pin(path,wanted=None):
  path=Path(path);actual=state.digest(path)
  need(wanted is None or actual==wanted,'Changed input '+str(path));pins[str(path)]=actual
 original_path=ROOT/'mk2/mk2-maincpu.bin';original=original_path.read_bytes();pin(original_path)
 def u32(data,at):return struct.unpack_from('<I',data,state.off(at))[0]
 for lo,hi in ((0xff814af0,0xff814b70),(0xff868700,0xff868930),
  (0xff876b40,0xff876be0),(0xff876f70,0xff877420),
  (0xff8775d0,0xff8779b0),(0xff878420,0xff8784f0),
  (0xff8bbfe0,0xff8bd040),(0xff841d10,0xff841e10)):
  need(guest[state.off(lo):state.off(hi)]==original[state.off(lo):state.off(hi)],'Original release/parser/victim/completion code '+hex(lo))
 need(u32(original,0xff814b00)==0xff863020 and u32(original,0xff863020)==0xff863140,
      'Original HP release input index zero')
 need(u32(original,0xff863190+10*32)==0xff868700 and
      u32(guest,u32(guest,0xff863150)+10*32)==0xff868700,
      'Original and relocated true Scorpion release dispatch')
 need(u32(original,0xff8ba390+10*32)==u32(guest,0xff8ba390+10*32)==0xff8bbfe0,
      'Native Scorpion second fatality action')
 need(struct.unpack_from('<13H',original,state.off(0xff878420))==(56,8,8,8,6,0,0,7,7,7,6,0,0),
      'Original reverse history: Down then three facing-relative forwards')
 build=json.loads((ROOT/headed.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 pin(ROOT/headed.CANDIDATE/'build-info.json')
 for file,wanted in build['input_hashes'].items():pin(file,wanted)
 for file in ('mk2ks_stock_scorpion_secondary_inputs_v1210.lua','mk2ks_stock_scorpion_secondary_display_v1210.lua'):
  source=(ROOT/file).read_text();pin(ROOT/file)
  need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',source),'No guest/CPU/graphics/save-state assistance '+file)
 for key in CASES:
  folder=ROOT/f'audit_v1220_secondary_{key}';label=' '+key
  result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));pin(folder/'result.json')
  name,side=result['player'],result['victim_slot'];identity={'kano':17,'sonya':18,'kitana':4,'liu_kang':1}[name];winner=3-side
  need(result['exit_code']==0 and result['seconds']==95 and result['candidate']==headed.CANDIDATE and result['executable_sha256']==build['executable_sha256'] and result['payload_sha256']==build['payload_sha256'],'Matched terminal build'+label)
  need(result['assistance']=='none' and result['cheats_enabled'] is False and result['killer']=='scorpion' and result['winner_slot']==winner and result['command']=='dfff_hp_release' and result['target_gap']==64,'Physical original release-command scenario'+label)
  if check_files:
   for file,wanted in result['input_hashes'].items():pin(file,wanted)
  text=texts[key] if texts is not None else (folder/'run.log').read_text(encoding='utf-8-sig');pin(folder/'run.log')
  need(not re.search(r'\[LUA ERROR\]|fatal error|stack traceback|access violation',text,re.I),'No runtime/observer error'+label)
  stock=state.rows(text,'MK2_STOCK_HEAD_V921');art=state.rows(text,'MK2_ROLLING_HEAD_V1003')
  need(all(r['writes']=='0' and r['assistance']=='none' for _,r in stock+art),'Read-only observations'+label)
  items=lambda tag:[r for t,r in stock if t==tag]
  action,wrap,stop,ready=(items(tag) for tag in ('ACTION','WRAP','RESULT','READY'))
  need(len(action)==len(wrap)==len(stop)==len(ready)==1,'One activation/finish/terminal/ready'+label)
  if not len(action)==len(wrap)==len(stop)==len(ready)==1:continue
  action,wrap,stop,ready=action[0],wrap[0],stop[0],ready[0];start=int(action['frame']);begin=int(ready['frame'])
  need(action['variant']=='2' and action['address']=='FF8BBFE0' and action['mode']=='2' and action['damage']=='322','True native secondary action'+label)
  live=items('FIRST_LIVE');need(len(live)==1 and live[0]['ids']==f'10,{identity}' and live[0]['own']==action['actor'] and live[0]['victim']==action['victim_actor'],'Real selected identities, no proxy'+label)
  need(ready['continuation']=='FFA17E10' and ready['victim_actor']==action['victim_actor'] and ready['victim_main']==action['victim_main'] and 60<=int(ready['gap'])<=69,'Natural dizzy state and close distance'+label)
  hp=161;damage=0;killed=0;chain=True
  collisions=[r for r in items('HEALTH') if r['pc']=='FF836700' and int(r['frame'])<=start]
  for r in collisions:
   before,after=int(r['before']),int(r['after']);chain=chain and before==hp and 0<=after<before<=161;hp=after;damage+=before-after
   if after==0:killed+=1;hp=161
  need(chain and len(collisions)==10 and damage==322 and killed==2 and len(items('WIN'))==2,'Two real collision KOs and native wins'+label)
  physical={(int(r['frame'])-begin,r['button']) for r in items('INPUT') if int(r['slot'])==winner and int(r['frame'])>=begin}
  forward='Left' if side==1 else 'Right'
  expected={(age,'Block') for age in range(50)}|{(age,'High_Punch') for age in range(5,50)}|{(age,'Down') for age in range(10,14)}|{(age,forward) for offset in (20,30,40) for age in range(offset,offset+4)}
  need(physical==expected and start==begin+52,'Exact Block lead-in, held HP and facing-relative Down F F F release'+label)
  gates=[r for t,r in art if t=='FIRE_GATE' and int(r['frame'])==start]
  distances=[r for r in items('GATE') if int(r['frame'])==start]
  need(len(distances)==1 and distances[0]['action']=='FF876B80' and distances[0]['limit']=='69' and 0<int(distances[0]['distance'])<=69 and distances[0]['actor']==action['actor'],'Original native distance gate'+label)
  need(any(r['entry']=='FF8687D0' and r['a1']=='0000002D' for r in gates) and any(r['entry']=='FF8688C0' and r['a1']=='0000700C' for r in gates) and any(r['entry']=='FF877160' and r['a0']=='FFA17E10' for r in gates) and any(r['entry']=='FF877350' and r['a7']=='FF876B80' for r in gates),'Original hold/history/dizzy/common gates'+label)
  need(wrap['age']=='96' and int(wrap['frame'])==start+96 and wrap['actor']==action['actor'] and wrap['main']==action['main'] and wrap['pc']=='FF8CDC50','Native 96-field completion'+label)
  need(stop['frame']=='5198' and stop['damage']=='322' and stop['wins']=='2' and int(stop['action'])==start and int(stop['wrap'])==start+96 and not items('CACHE_OVERWRITE') and any(r['mode']=='3' and int(r['frame'])>start+96 for r in items('MODE')),'Stable native continuation'+label)
  calls=[r for t,r in art if t=='FIRE_CALL'];signature=[]
  for entry,age in ((0xff8bbfe0,0),(0xff8bc810,27+side),(0xff8bca00,71+side),(0xff876650,71+side),(0xff8bc710,96),(0xff8cdc40,96)):
   found=[r for r in calls if int(r['entry'],16)==entry and int(r['age'])<=96]
   need(len(found)==1 and int(found[0]['age'])==age,'Original cooperative callback '+hex(entry)+label)
   if found:
    row=found[0];victim=entry in (0xff8bc810,0xff8bca00,0xff876650)
    need(row['actor']==action['victim_actor' if victim else 'actor'] and row['main']==action['victim_main' if victim else 'main'] and int(row['id'])==(identity if victim else 10),'True physical callback identity '+hex(entry)+label)
    signature.append((row['entry'],int(row['age'])))
  lookups=[r for r in items('LOOKUP') if int(r['age'])<=96]
  need([(r['index'],int(r['age'])) for r in lookups]==[('00000037',27+side),('00000039',71+side),('00000041',71+side)] and all(r['actor']==action['victim_actor'] and r['main']==action['victim_main'] for r in lookups),'Original headed reaction, upper torso and lower stump lookups'+label)
  states=[r for t,r in art if t=='FIRE_STATE' and 0<=int(r['age'])<=96]
  need(len(states)>=8,'Positive native physical-state coverage'+label)
  for r in states:
   victim=int(r['slot'])==side
   need(r['actor']==action['victim_actor' if victim else 'actor'] and r['main']==action['victim_main' if victim else 'main'] and r['id']==r['roster']==str(identity if victim else 10),'Actual physical actor/main/roster preserved'+label)
  if key.startswith('control_'):controls[side]=signature
  else:need(signature==controls[side],'Same-slot stock control chronology'+label)
  need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole independently reconstructed current guest'+label)
  display=items('DISPLAY');need([int(r['age']) for r in display]==list(range(0,601,10)),'Complete sampled physical-action timeline'+label)
  for r in display:
   path=folder/'snap'/f"stock_head_{start}_{int(r['age']):03d}.png";need(Image.open(path).size==(400,254),'Actual captured size'+label);pin(path)
  need(len(items('CONTINUE_DISPLAY'))==1 and items('CONTINUE_DISPLAY')[0]['frame']=='4080' and items('CONTINUE_DISPLAY')[0]['mode']=='3','Actual native continue capture'+label)
  pin(folder/'snap/continue_4080.png')
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
  cases[key]=dict(trueVictimID=identity,victimSlot=side,actionFrame=start,wrapAge=96,originalCallbackSignature=signature,actualPrimaryLookups=lookups,actualScenes=62)
 need(len(cases)==6 and len(controls)==2,'Four true added victims and both successful original controls')
 return dict(passed=not errors,errors=sorted(set(errors)),candidate=headed.CANDIDATE,cases=cases,inputHashes=pins,
  stockScorpionSecondaryNormalDeadPoolPhysicalStateAccepted=not errors,fullScreenDMAReplayAccepted=False,
  allFatalityArtAccepted=False,alternateCostumesAccepted=False,audioAccepted=False,allArenasAccepted=False,
  allFloorShadowsAccepted=False,fullPortAccepted=False,gameCodeChanged=False)

if __name__=='__main__':
 assert not OUT.exists(),'Never overwrite executed evidence'
 report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed'] else 1)
