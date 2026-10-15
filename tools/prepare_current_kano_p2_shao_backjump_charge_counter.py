"""One physical opening backjump, then observed crouch charge counter."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_crouch_charge_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_backjump_charge_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='    if stage==16 then\n     if human.action==263 or human.action==1539 then'
assert source.count(old)==1
source=source.replace(old,"""    if stage==16 then
     if frame-boss_live_begin<16 then
      press('Up');press(back)
     elseif height>0 and frame-boss_live_begin<64 then
      press(back)
     elseif human.action==263 or human.action==1539 then""")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_crouch_charge_counter_runtime','audit_current_kano_p2_shao_backjump_charge_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Physicalopeningbackjump+counter;180sec/320MiB/10MiB/no media/guestwrites')
