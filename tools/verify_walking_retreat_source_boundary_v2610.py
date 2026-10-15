"""Exact stage16 physical-only standing-retreat successor; not whole-port acceptance."""
import argparse,json,re
from pathlib import Path
import verify_current_boss_shao_walking_retreat_v2609 as current
ROOT=current.ROOT;launch=current.current_launch

def need(ok,label):
 if not ok:raise ValueError(label)

def verify():
 path=ROOT/'mk2ks_natural_campaign_boss_shao_walking_retreat_v2607.lua'
 text=path.read_text().rstrip()+'\n'
 current.restore_shao_walking_retreat_policy(text)
 need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',text),'No guest/register/state writes')
 runner=ROOT/'tools/run_current_boss_shao_walking_retreat_v2608.ps1'
 previous=ROOT/'tools/run_current_boss_shao_standing_retreat_v2577.ps1'
 restored=runner.read_text().replace('mk2ks_natural_campaign_boss_shao_walking_retreat_v2607','mk2ks_natural_campaign_boss_shao_standing_retreat_v2576').replace('shao_walking_retreat','shao_standing_retreat')
 need(restored.rstrip()+'\n'==previous.read_text().rstrip()+'\n','Whole original launcher inverse')
 mutations={
  'removed_walk0_eligibility':text.replace('(human.action==0 or human.action==0x303 or human.action==0x304)','(human.action==0x303 or human.action==0x304)',1),
  'changed_jump_distance':text.replace('standing and gap<220','standing and gap<221',1),
  'shortened_jump_hold':text.replace('if frame-boss_last_jump<16 then','if frame-boss_last_jump<15 then',1),
  'changed_jump_direction':text.replace('boss_jump_direction=back','boss_jump_direction=forward',1),
  'removed_native_state_gate':text.replace('human.flags&0x1c==0','human.flags&0x0c==0',1),
  'changed_own_identity':text.replace('kano=17,sonya=18','kano=1,sonya=18',1),
  'changed_ordinary_HP_timing':text.replace("if frame-last_uppercut>=22 then press('High Punch')","if frame-last_uppercut>=21 then press('High Punch')",1),
  'added_guest_write':text+"p:write_u16(0x010602f0,161)\n",
 }
 rejected=[]
 for name,changed in mutations.items():
  need(changed!=text,'Non-vacuous source mutation '+name)
  try:current.restore_shao_walking_retreat_policy(changed)
  except AssertionError:rejected.append(name)
  else:raise ValueError('Changed source boundary accepted '+name)
 current.restore_shao_walking_retreat_policy(text)
 guest,old,payload=current.current_source.expected()
 need(guest==(ROOT/'audit_v2515_current_sonya_p1_shao_duck_wait_campaign/guest_maincpu.bin').read_bytes(),'Whole unchanged current guest')
 need(payload==(ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata').read_bytes(),'Whole unchanged current payload')
 pins=launch.source_pins()
 recovery_path=ROOT/'audit_v2548_dynamic_native_source_dependencies_recovered/report.json'
 recovery=json.loads(recovery_path.read_text());need(recovery['passed'],'Actual required historical dependencies recovered')
 for file,wanted in recovery['inputHashes'].items():need(launch.sha(file)==wanted,'Exact retained/recovered dependency');pins[file]=wanted
 for p in(path,runner,previous,recovery_path,ROOT/'mk2ks_natural_campaign_boss_shao_guard_walk_v2540.lua',ROOT/'tools/verify_current_boss_shao_guard_walk_v2542.py',ROOT/'mk2ks_natural_campaign_boss_shao_standing_retreat_v2576.lua',ROOT/'tools/verify_current_boss_shao_standing_retreat_v2578.py',Path(__file__).resolve()):pins[str(p)]=launch.sha(p)
 launch.module_pins(pins)
 return dict(passed=True,fullSourceInverse=True,wholeLauncherInverse=True,wholeGuestAndPayloadReconstructed=True,rejectedSpecificSourceCounterexamples=rejected,inputHashes=pins,gameChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable source-boundary proof')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
