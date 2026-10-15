"""Source-exact real crouch-exit/Up timing and complete clean follow-up.
A no-activation diagnostic is accepted only as such, never credited as a jump.
This does not certify every move, arena, raster, sound, CPU fight or ending.
"""
import argparse,json,re,struct
from pathlib import Path
import verify_current_guard_uppercut_comparison_v2217 as check
import verify_current_crouch_jump_comparison_v2447 as prior
from verify_ball_register_source_v1837 import expected as current_expected
import verify_current_interrupt_v1870 as launch
ROOT=check.ROOT
SPECS={'jump_kano':17,'jump_sonya':18,'jump_liu':1,'jump_subzero':8}
def need(ok,label):
 if not ok:raise ValueError(label)
def restore_driver(text):
 baseline=ROOT/'mk2ks_crouch_jump_comparison_v2445.lua'
 need(launch.sha(baseline)=='869F5F4E066FBC2224711CD5CEDFDDECC976D94279CFC78F0BF90A745B42A4FE','Pinned complete previous crouch/jump physical driver')
 changed="    pulse(side,own.x<victim.x and'Left'or'Right',f,0,8);pulse(side,'Up',f,40,3);pulse(side,'High Punch',f,112,3)"
 original="    pulse(side,forward,f,0,8);pulse(side,'Up',f,40,3);pulse(side,'High Punch',f,112,3)"
 need(text.count(changed)==1,'One exact collision-free away-walk diagnostic follow-up')
 restored=text.replace(changed,original,1)
 need(restored==baseline.read_text().rstrip()+'\n','Only ordinary follow-up walk direction differs; complete cold selection/approach/command/observer/recovery code exact')
 prior.restore_driver(restored)
 return restored

def verify_log(text,meta):
 side=meta['side'];identity=SPECS[meta['move']];lead=meta['lead'];hold=meta['hold']
 need(side in(1,2)and lead in(0,12)and hold in(3,16),'Declared physical comparison')
 need(meta['profile']=='crouch_release'and meta['victim']=='sub_zero'and not meta['air'],'Actual native two-human crouch comparison')
 need(not re.search(r'LUA ERROR|Lua error|fatal error|access violation',text,re.I),'No observer/runtime error')
 need(not check.rows(text,'FAILED'),'No lost pair or stuck/unfinished native recovery')
 for line in text.splitlines():
  if not line.startswith('MK2_HSPECIAL_'):continue
  scope=dict(re.findall(r'(\w+)=([^\s]+)',line))
  need(scope.get('move')==meta['move']and scope.get('side')==str(side)and scope.get('profile')=='crouch_release'and scope.get('lead')==str(lead)and scope.get('hold')==str(hold)and scope.get('writes')=='0'and scope.get('assistance')=='none','Every recorded row exact true comparison scope')
 finals=check.rows(text,'RESULT');need(len(finals)==1,'Unique actual terminal comparison')
 r=finals[0];need(r['fullPortAcceptance']=='false','Bounded comparison only')
 for tag,key in(('CSS','css'),('LIVE','live'),('READY','ready'),('COMMAND','command'),('RECOVERED','recovered'),('FINAL','frame')):
  events=check.rows(text,tag);need(len(events)==1 and events[0]['frame']==r[key],'Actual single '+tag)
 need(700<=r['css']<r['live']<r['ready']<=r['command']<r['recovered']<r['followup']<r['frame'],'Complete cold genuine match/command/recovery chronology')
 need(r['followup']==r['recovered']+16 and r['frame']==r['followup']+160,'Entire ordinary follow-up interval')
 need(r['recovered']>=r['command']+120+lead+hold+60,'Complete physical input and neutral retirement interval')
 fields=check.rows(text,'FIELD');by={(f['frame'],f['slot']):f for f in fields}
 wanted={(frame,n)for frame in range(r['ready'],r['frame']+1)for n in(1,2)}
 need(len(by)==len(fields)==len(wanted)and set(by)==wanted,'Every consecutive paired native field')
 owners={n:(by[r['ready'],n]['actor'],by[r['ready'],n]['main'])for n in(1,2)}
 floors={n:by[r['ready'],n]['floor']for n in(1,2)}
 for f in fields:
  ident=identity if f['slot']==side else 8
  need(f['mode']==2 and f['state']==1 and f['id']==f['roster']==ident and f['owner']==f['actor']and(f['actor'],f['main'])==owners[f['slot']],'True selected IDs and stable native Main/actor, never proxies')
  need(f['floor']==floors[f['slot']]and 0<=f['hp']<=161,'Stable actual character-owned floor and native health')
 need(all(check.clean(by[r['ready'],n])and by[r['ready'],n]['hp']==161 for n in(1,2)),'Real full-health grounded match')
 need(all(check.clean(by[r['recovered'],n])and check.clean(by[r['frame'],n])for n in(1,2)),'Both humans retire and finish naturally clean on own floors')
 inputs=check.rows(text,'INPUT');keys={(i['frame'],i['slot'],i['button'])for i in inputs}
 need(len(keys)==len(inputs),'Unique physical inputs')
 need(not any(r['command']-120<=i['frame']<r['command']for i in inputs),'Original120field neutral approach retirement')
 command=check.rows(text,'COMMAND')[0];forward=command['forward']
 need(command['expectedEntry']==0xff831360 and forward in('Left','Right'),'Actual horizontal jump target and direction')
 planned={(r['command']+at,side,'Down')for at in range(120)}
 planned|={(r['command']+at,side,button)for at in range(120+lead,120+lead+hold)for button in('Up',forward)}
 need({k for k in keys if r['command']<=k[0]<r['followup']}==planned,'Exact physical Down release and Up/direction duration; no conflicting Down/Block/HP')
 follow=r['followup']
 away='Left'if by[follow,side]['x']<by[follow,3-side]['x']else'Right'
 expected_follow={(follow+at,side,button)for button,start,duration in((away,0,8),('Up',40,3),('High_Punch',112,3))for at in range(start,start+duration)}
 need({k for k in keys if k[0]>=follow}==expected_follow,'Exact complete ordinary walk/jump/punch follow-up')
 for event in check.rows(text,'EVENT')+check.rows(text,'HANDLER'):
  need(event['id']==identity and(event['actor'],event['main'])==owners[side]and event['a8']==event['actor']and event['a13']==event['main']and event['pc']==event['entry']+16,'Own actual native instruction/ID/Main/register provenance')
 command_entries=[e for e in check.rows(text,'EVENT')if e['entry']==0xff831360 and r['command']<=e['frame']<r['recovered']]
 need(len(command_entries)<=1,'One physical command cannot claim repeated independent jumps')
 jump_fields=[by[f,side]for f in range(r['command'],r['recovered'])if by[f,side]['y']<floors[side]and by[f,side]['vy']!=0]
 if command_entries:
  need(r['entry']==command_entries[0]['frame']and r['command']+120+lead<=r['entry']<r['command']+120+lead+hold+32,'Actual original horizontal jump entry follows real held Up')
  need(jump_fields and any(f['action']==0x308 for f in jump_fields),'Actual human308 airborne jump, not an Up plan or victim hurt')
  need(not any(f['action']in(0x503,0x107)for f in jump_fields),'No uppercut/hurt credited as a jump')
  need(any(e['entry']==0xff861350 and r['entry']<e['frame']<=r['recovered']for e in check.rows(text,'EVENT')),'Original individual ready handoff after measured jump')
 else:
  need(r['entry']==-1 and not jump_fields,'No-activation recording never fabricated entry or airborne motion')
 exit_fields=[by[f,side]for f in range(r['command']+120,r['recovered'])if by[f,side]['action']==0x301]
 exits=[e for e in check.rows(text,'HANDLER')if e['entry']==0xff82fd70 and r['command']<=e['frame']<r['recovered']]
 need(exits and exit_fields and all(e['action']==0x302 for e in exits),'Observed original302 to301 crouch-exit retirement')
 health=check.rows(text,'HEALTH')
 for h in health:
  need(h['slot']==3-side and h['pc']==0xff836700 and h['mask']==0xffff and 0<=h['after']<=h['before']<=161,'Only original own ordinary follow-up collision damage')
 need(not any(h['frame']<r['followup']for h in health),'Command jump cannot fabricate contact or healing')
 for n in(1,2):
  for f in range(r['ready'],r['frame']):
   stores=[h for h in health if h['frame']==f and h['slot']==n]
   if stores:
    need(stores[0]['before']==by[f,n]['hp']and stores[-1]['after']==by[f+1,n]['hp']and all(a['after']==b['before']for a,b in zip(stores,stores[1:])),'Original ordered health stores explain adjacent fields')
   else:need(by[f,n]['hp']==by[f+1,n]['hp'],'No unexplained native health change')
 need(all(f['hp']==161 for f in fields if f['slot']==side),'Passive opponent cannot harm own human')
 sign=1 if away=='Right'else -1
 walker=by[follow,side];opponent=by[follow,3-side];toward=(opponent['x']-walker['x'])*sign>0
 need(not toward,'Follow-up physically moves away from actual opponent; no body-push collision')
 speed=0x20000
 need(all(by[f,side]['vx']==(speed*sign)&0xffffffff and by[f,side]['y']==floors[side]for f in range(follow+3,follow+9)),'Real native collision-free back walking after crouch/jump')
 need(any(by[f,side]['y']<floors[side]and by[f,side]['vy']!=0 for f in range(follow+42,follow+65)),'Real ordinary follow-up jump responds')
 need(any(by[f,side]['action']==0x101 for f in range(follow+114,follow+140)),'Real ordinary high punch after landing')
 return dict(nativeCommandJumpObserved=bool(command_entries),actualNativeJumpEntry=r['entry'],
  actualCrouchExitEntryFrames=[e['frame']for e in exits],actualCrouchExitFieldFrames=[f['frame']for f in exit_fields],
  actualAirborneCommandFields=len(jump_fields),native308AirborneCommandFields=sum(f['action']==0x308 for f in jump_fields),
  completeRecoveryAndOrdinaryFollowup=True,noActivationNeverPromotedToJump=True,pairedFields=len(fields),
  command=r['command'],recovered=r['recovered'],followup=r['followup'],final=r['frame'])

def verify_case(folder):
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/check.current_source.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(meta['candidate']==build['name']==check.current_source.NAME and meta['exit_code']==0 and not meta['cheats_enabled']and meta['assistance']=='none','Current terminal unassisted capture')
 need(before==meta['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Complete actual build inputs frozen')
 need(meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256'],'Matched current EXE/payload')
 pins={}
 for file,wanted in before.items():
  need(launch.sha(file)==wanted,'Unchanged executed input '+file);pins[file]=wanted
  if Path(file).suffix in('.lua','.ps1','.json'):
   frozen=folder/'input_sources'/Path(file).name;need(launch.sha(frozen)==wanted,'Unchanged frozen executed input');pins[str(frozen)]=wanted
 driver=(folder/'input_sources/mk2ks_crouch_jump_comparison_v2450.lua').read_text()
 need(not re.search(r':write_|write_u\d+|load_?state|\bdofile\s*\(|\.value\s*=(?!=)',driver),'No forced guest/task/position/health/RNG/ID state')
 restore_driver(driver)
 runner=(folder/'input_sources/run_current_crouch_jump_comparison_v2451.ps1').read_text()
 need('-nocheat'in runner and '-noautoframeskip -frameskip 0'in runner,'Original no-cheat/full-field run')
 guest=(folder/'guest_maincpu.bin').read_bytes();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 need(guest==current_expected()[0],'Whole actual initialized guest independently reconstructed')
 for a,b in((0xff82f9f0,0xff82fe00),(0xff831360,0xff831510),(0xff83c430,0xff83c5b0)):
  need(guest[(a-0xff800000)//8:(b-0xff800000)//8]==original[(a-0xff800000)//8:(b-0xff800000)//8],'Original crouch retirement/jump/animation routine unchanged')
 result=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),meta)
 for file in folder.rglob('*'):
  if file.is_file():pins[str(file.resolve())]=launch.sha(file)
 for file in(Path(__file__),ROOT/'mk2ks_guard_uppercut_comparison_v2212.lua'):
  pins[str(file.resolve())]=launch.sha(file)
 pins.update(launch.source_pins());launch.module_pins(pins)
 return dict(passed=True,**result,move=meta['move'],side=meta['side'],lead=meta['lead'],hold=meta['hold'],
  inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable real crouch/jump proof')
 try:r=verify_case(a.folder)
 except Exception as error:
  import traceback
  r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in('inputHashes','actualCrouchExitFieldFrames')},indent=2),flush=True)
 raise SystemExit(0 if r['passed']else 1)
