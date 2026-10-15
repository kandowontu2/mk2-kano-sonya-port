"""Exact physical-only successor boundary; no game acceptance from test-source checks."""
import argparse,json
from pathlib import Path
import verify_current_boss_shao_guard_walk_v2542 as current
import verify_current_boss_shao_duck_wait_v2514 as previous
ROOT=current.ROOT;launch=current.current_launch

def need(ok,label):
 if not ok:raise ValueError(label)

def verify():
 source=ROOT/'mk2ks_natural_campaign_boss_shao_guard_walk_v2540.lua'
 baseline=ROOT/'mk2ks_natural_campaign_boss_shao_duck_wait_v2494.lua'
 actual=source.read_text().rstrip()+'\n';old=baseline.read_text().rstrip()+'\n'
 need(current.restore_shao_guard_walk_policy(actual)==previous.restore_shao_crouch_exit_policy(old),'Full accepted ordinary/Kintaro/native-observer chain exactly preserved')
 runner=ROOT/'tools/run_current_boss_shao_guard_walk_v2541.ps1'
 old_runner=ROOT/'tools/run_current_boss_shao_duck_wait_v2513.ps1'
 restored=runner.read_text().replace('mk2ks_natural_campaign_boss_shao_guard_walk_v2540','mk2ks_natural_campaign_boss_shao_duck_wait_v2494').replace('shao_guard_walk','shao_duck_wait')
 need(restored.rstrip()+'\n'==old_runner.read_text().rstrip()+'\n','Whole physical launcher exact inverse')
 mutations={
  'changed_walk_range':actual.replace('(walk_pose and gap<95)','(walk_pose and gap<96)',1),
  'removed_guard_fallback':actual.replace("     else\n      boss_walk_last_x=nil;press('Down');press('Block')\n     end\n    elseif quiet", "     else\n      boss_walk_last_x=nil;press('Down')\n     end\n    elseif quiet",1),
  'shortened_block_release':actual.replace("frame-boss_walk_last_x>=12 and opening","frame-boss_walk_last_x>=10 and opening",1),
  'changed_true_identity':actual.replace('kano=17,sonya=18','kano=1,sonya=18',1),
  'changed_ordinary_command':actual.replace("if frame-last_uppercut>=22 then press('High Punch')","if frame-last_uppercut>=21 then press('High Punch')",1),
 }
 rejected=[]
 for name,changed in mutations.items():
  need(changed!=actual,'Non-vacuous physical source mutation '+name)
  try:current.restore_shao_guard_walk_policy(changed)
  except AssertionError:rejected.append(name)
  else:raise ValueError('Changed physical boundary accepted '+name)
 need(current.restore_shao_guard_walk_policy(actual)==previous.restore_shao_crouch_exit_policy(old),'Final untouched complete source control')
 expected,pins=current.current_source.expected()
 pins.update(launch.source_pins())
 for file in (source,baseline,runner,old_runner,Path(__file__).resolve()):pins[str(file)]=launch.sha(file)
 launch.module_pins(pins)
 return dict(passed=True,rejectedSpecificSourceCounterexamples=rejected,fullSourceInverse=True,wholeLauncherInverse=True,inputHashes=pins,gameChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable boundary proof')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
