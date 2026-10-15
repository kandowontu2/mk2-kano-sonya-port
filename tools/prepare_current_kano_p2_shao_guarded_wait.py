"""Let native boss approach; no unguarded forward walk at distance."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_active_attack_guard_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_guarded_wait_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="     elseif gap>80 then\n      su_down=nil;su_pulse=nil;press(forward)"
new="     elseif gap>80 then\n      su_down=nil;su_pulse=nil;press('Down');press('Block')"
assert source.count(old)==1
source=source.replace(old,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_active_attack_guard_runtime','audit_current_kano_p2_shao_guarded_wait_runtime')
(out/'run.ps1').write_text(runner)
print('Physicalguardedwait;180sec/320MiB/10MiB/no media/guestwrites')
