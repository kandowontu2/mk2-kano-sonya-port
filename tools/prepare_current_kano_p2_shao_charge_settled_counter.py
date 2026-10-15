"""Wait for observed native crouch loop, not early action770 pose."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_charge_guard_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_charge_settled_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local cg_loop,cg_loop_main=nil,nil\n'+source
old="      if can_crouch and frame-cg_down>=4 and(not cg_pulse or frame-cg_pulse>=26)then"
assert source.count(old)==1
source=source.replace(old,"      if can_crouch and human.action==770 and cg_loop and cg_loop_main==human.main and cg_loop>=cg_down and frame-cg_loop<=2 and frame-cg_down>=4 and(not cg_pulse or frame-cg_pulse>=26)then")
old="      log('BOSS_ACTION',string.format"
assert source.count(old)==1
source=source.replace(old,"      if current_stage==16 and data&0xffff==770 and cpu.PC.value==0xff82fa80 then cg_loop=frame;cg_loop_main=observed_main end\n"+old)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_charge_guard_counter_runtime','audit_current_kano_p2_shao_charge_settled_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Actualnativecrouchloopgatedcounter;180sec/320MiB/10MiB/no media/guestwrites')
