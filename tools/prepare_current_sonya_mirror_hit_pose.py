"""Passive exact native hit-time pose observation; unchanged controller."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_neutral_recovery_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_hit_pose_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
anchor="     log('MIRROR_STANDING_DAMAGE',"
start=source.index(anchor)
end=source.index('\n',start)
extra="""
     if n==1 and other.action==771 and cpu.A8.value==other.actor and cpu.A13.value==other.main then
      log('MIRROR_CPU_HIT_POSE',string.format('before=%d after=%d cpu_actor=%08X cpu_main=%08X cpu_pose=%08X cpu_flags=%04X cpu_body=%d cpu_bank=%d human_pose=%08X human_action=%d human_flags=%04X gap=%d native_damage=%d',before,after,other.actor,other.main,other.pose,other.flags,other.body,other.bank,own.pose,own.action,own.flags,math.abs(own.x-other.x),cpu.A10.value))
     end"""
source=source[:end]+extra+source[end:]
assert source.count('maximum_fields=24000')==1
source=source.replace('frame>=24000','frame>=19500').replace('maximum_fields=24000','maximum_fields=19500')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_neutral_recovery_runtime','audit_current_sonya_mirror_hit_pose_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared19500fields; unchanged inputs; passive scalar hit poses; no media')
