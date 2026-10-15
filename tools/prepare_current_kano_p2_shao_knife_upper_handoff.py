"""At low boss health, guard until close rather than queue another knife."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_knife_upper_finish_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_knife_upper_handoff_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='     elseif other.hp<=35 and gap<=90 and height==0 then'
assert source.count(old)==1
source=source.replace(old,'     elseif other.hp<=35 and height==0 then')
old="      if human.action==263 or human.action==1539 then"
assert source.count(old)==1
source=source.replace(old,"""      if not ku_last or frame-ku_last>1 then decision('shao_low_health_guard_handoff')end
      if gap>90 then
       press('Down');press('Block');ku_down=nil
      elseif human.action==263 or human.action==1539 then""")
# Log entry before updating last field, leaving actual reset behavior intact.
source=source.replace("      ku_last=frame\n      if not ku_last or frame-ku_last>1 then decision('shao_low_health_guard_handoff')end", "      if not ku_last or frame-ku_last>1 then decision('shao_low_health_guard_handoff')end\n      ku_last=frame")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_knife_upper_finish_runtime','audit_current_kano_p2_shao_knife_upper_handoff_runtime')
(out/'run.ps1').write_text(runner)
print('Lowhealthphysicalguardhandoff;180sec/320MiB/10MiB/no media/guestwrites')
