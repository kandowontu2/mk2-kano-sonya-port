"""Controller-only guard after upper attempts, then actual native recovery release."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_upper_contact_bounded180_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_upper_recovery_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
branch=source[start:end]
old='     if gap>80 then\n'
assert branch.count(old)==1
new="     if su_pulse and frame-su_pulse<32 then\n      press('Down')\n      if frame-su_pulse<3 then press('High Punch')\n      else press('Block')end\n      su_down=nil\n     elseif gap>80 then\n"
branch=branch.replace(old,new)
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_upper_contact_bounded180_runtime','audit_current_kano_p2_shao_upper_recovery_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Physical upper guard32 thenrelease/crouchlead;180sec/320MiB/10MiB/no media/nativeHP observed')
