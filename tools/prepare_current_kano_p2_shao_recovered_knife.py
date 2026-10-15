"""Schedule physical commands from observed recovery, not fixed cadence."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_close_knife_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_recovered_knife_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
branch=source[start:end]
old='     if projectile_start and frame-projectile_start<64 then'
assert branch.count(old)==1
branch=branch.replace(old,"""     local knife_ready=height==0 and human.flags&0x1c==0 and
      (human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793)
     if projectile_start and (frame-projectile_start<16 or not knife_ready) then""")
branch=branch.replace('shao_close_knife_command_attempt','shao_recovered_knife_command_attempt')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_close_knife_runtime','audit_current_kano_p2_shao_recovered_knife_runtime')
(out/'run.ps1').write_text(runner)
print('Recoverygatedphysicalknife;180sec/320MiB/10MiB/no media/guestwrites')
