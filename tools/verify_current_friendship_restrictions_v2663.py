"""Current-build physical Friendship wrong-command and no-punch restrictions.
Eight real cold negative cases cover both fighters and slots, original damage,
native wins, true IDs and normal next-screen return. This does not establish
complete positive scene pixels, floor shadows, audio or all-finisher acceptance.
"""
import argparse,copy,json,re,struct
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_friendship_dispatch_v778 as previous
import verify_ball_register_source_v1837 as current
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
CASES={f'{fighter}_{command_case}_p{side}':(fighter,side,command_case)for fighter in ('kano','sonya')for side in (1,2)for command_case in ('wrong_command','punch_used')}

def need(ok,label):
 if not ok:raise ValueError(label)

def check(rows,fighter,side,command_case):
 identity=17 if fighter=='kano'else 18
 control=previous.runtime(rows,fighter,side,command_case)
 selected=previous.select(rows,'SELECT_ID')
 need(all(int(r['target'])==(identity if int(r['slot'])==side else 35-identity)for r in selected),'Both actual native selected characters, no proxies')
 damage=previous.select(rows,'DAMAGE');expected=161;kos=[]
 for r in damage:
  before,after=int(r['before']),int(r['after'])
  need(before==expected and 0<=after<before<=161,'Complete ordered original health damage chain')
  expected=after
  if after==0:kos.append(int(r['frame']));expected=161
 need(len(kos)==2,'Two actual ordered combat KOs')
 wins=previous.select(rows,'WIN')
 need(len(wins)==2,'Two actual original winner-table dispatches')
 for index,r in enumerate(wins):
  need(int(r['slot'])==side and int(r['id'])==int(r['actor_id'])==int(r['roster'])==identity and
   r['owner']==r['actor'] and all(0x01000000<=int(r[k],16)<0x01100000 for k in ('actor','main')) and
   int(r['entry'],16)==0xfffef800+identity*32 and r['pc']=='FF8296B0','Actual true owned native winner identity and original dispatch')
  health=[int(h)for h in r['health'].split(',')]
  need(0<health[side-1]<=161 and health[2-side]==0,'Actual native winner has positive own health and KO victim')
  need(int(r['frame'])>=kos[index] and (index==0 or int(r['frame'])>int(wins[index-1]['frame'])),'Actual winner dispatch follows its ordered earned KO')
 return dict(**control,observedOriginalOwnWinnerDispatches=2,ownWinnerFrames=[int(r['frame'])for r in wins],
  originalKOFrames=kos,actualTrueFighterID=identity)

def verify(case):
 fighter,side,command_case=CASES[case];folder=ROOT/f'audit_v2660_current_{fighter}_friendship_{command_case}_p{side}'
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(meta['exit_code']==0 and meta['candidate']==current.NAME and meta['winner']==fighter and meta['side']==side and
  meta['command_case']==command_case and meta['samples_enabled'] and meta['guest_writes']==0 and meta['assistance']=='none' and
  meta['executable_sha256']==build['executable_sha256'] and meta['payload_sha256']==build['payload_sha256'] and
  before==meta['input_hashes'],'Complete matched current-build terminal physical case')
 pins={}
 def pin(path,wanted=None):
  path=str(path);actual=launch.sha(path)
  need(wanted is None or actual==wanted,'Unchanged actual executed input '+path)
  pins[path]=actual
 for path,wanted in before.items():
  pin(path,wanted)
  if Path(path).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(path).name,wanted)
 need(all(before.get(p)==h for p,h in build['input_hashes'].items()),'Every actual compiled input is the same current matched build')
 for name,wanted in (
  ('mk2ks_native_friendship_probe_v784.lua','7B8F9CB538175410B93AF1D98783A25878A9E28A1CB7E94066F0F4EB1D553450'),
  ('mk2ks_native_friendship_audio_v790.lua','8D461B5BC7C100C207E1C7F0082747CE77B5A11274FFBACBE48477E05679DA73'),
  ('tools/verify_native_friendship_dispatch_v778.py','F2AC088DBAE1C228820D1501E89E1F8E4B09798C9409AAB7CF74A1FE65A69139')):pin(ROOT/name,wanted)
 for name in ('mk2ks_native_friendship_probe_v784.lua','mk2ks_native_friendship_audio_v790.lua','mk2ks_current_friendship_wins_v2651.lua'):
  need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',(ROOT/name).read_text()),'No guest/register/loaded-state writes')
 runner=(ROOT/'tools/run_current_friendship_v2650.ps1').read_text()
 need('-nocheat'in runner and '-noautoframeskip -frameskip 0'in runner and 'mk2ks_current_friendship_wins_v2651.lua'in runner,'Cold physical, no-cheat, every native frame runner')
 guest,_,payload=current.expected()
 need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole actual current guest and payload independently reconstructed')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();off=lambda address:(address-0xff800000)//8
 need(guest[0xf98a0:0xf98a0+17*4]==stock[off(0xff880a70):off(0xff880a70)+17*4] and
  guest[0xf98f0:0xf98f0+17*4]==stock[off(0xff880d90):off(0xff880d90)+17*4],'All seventeen original Friendship command/action rows unchanged')
 text=(folder/'run.log').read_text(encoding='utf-8-sig')
 need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),'No native or observer runtime errors')
 rows=previous.parse(folder/'run.log');control=check(rows,fighter,side,command_case)
 index=lambda tag,predicate=lambda r:True:next(i for i,(t,r)in enumerate(rows)if t==tag and predicate(r))
 win=index('WIN');damage=index('DAMAGE');final=index('RESULT');window=index('WINDOW')
 field=max(i for i,(tag,r)in enumerate(rows)if tag=='FIELD')
 mutations=[
  ('proxy_selected_own_character',index('SELECT_ID',lambda r:int(r['slot'])==side),'actual','1','Native selection did not construct actual IDs'),
  ('wrong_original_damage_route',damage,'pc','FF836710','Not two genuine native round wins'),
  ('missing_native_win',win,None,None,'Two actual original winner-table dispatches'),
  ('wrong_native_win_identity',win,'id','1','Actual true owned native winner identity'),
  ('positive_health_victim_on_win',win,'health','161,161','Actual native winner has positive own health'),
  ('false_Friendship_activation',final,'action',str(int(rows[window][1]['frame'])+78),'Ineligible/wrong command activated scene'),
  ('missing_native_next_screen',field,'mode','2','Finish window did not cleanly leave for next screen')]
 if command_case=='punch_used':
  mutations.append(('masked_actual_winning_round_HP_counter',window,'hp_counters','0,0','Actual winning-round HP restriction not exercised'))
 else:
  mutations.append(('proxy_actual_own_identity',index('BOOT'),'own_id','1','Wrong character ownership'))
 outcomes=[]
 for name,at,key,value,label in mutations:
  changed=copy.deepcopy(rows)
  if key is None:changed.pop(at)
  else:changed[at][1][key]=value
  need(changed!=rows,'Non-vacuous actual Friendship restriction corruption '+name)
  try:check(changed,fighter,side,command_case)
  except ValueError as error:
   need(label in str(error),'Intended native invariant, not incidental failure '+str(error));outcomes.append(dict(name=name,rejectedBy=str(error)))
  else:raise ValueError('Malformed current Friendship restriction accepted '+name)
 need(check(rows,fighter,side,command_case)==control,'Final untouched actual restriction control')
 for name in ('run.log','result.json','inputs_before.json','guest_maincpu.bin','native_mix.wav'):pin(folder/name)
 pin(Path(__file__).resolve());launch.module_pins(pins)
 return dict(passed=True,case=case,**{k:v for k,v in control.items()if k!='scope'},commandCase=command_case,
  currentWholeGuestAndPayloadReconstructed=True,originalFriendshipRowsPreserved=17,
  rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes,finalUnmodifiedControlPassed=True,
  actualPhysicalFriendshipRestrictionAccepted=True,actualUnwantedActivation=False,
  gameChanged=False,fullFinisherAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',choices=CASES);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable current physical restriction proof')
 try:r=verify(a.case)
 except Exception as error:
  import traceback
  r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in ('inputHashes','outcomes')},indent=2),flush=True)
 raise SystemExit(0 if r['passed']else 1)
