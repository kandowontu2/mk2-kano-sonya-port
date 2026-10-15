"""Physical guard during observed Baraka7 attack, not a stock AI change."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_own_ready_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_leg_attack_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='    if rl_start and frame-rl_start<12 then\n'
assert source.count(old)==1
source=source.replace(old,"    if other.action==7 then\n     rl_start=nil;press('Down');press('Block')\n    elseif rl_start and frame-rl_start<12 then\n")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_own_ready_leg_runtime','audit_current_sonya_p2_baraka_leg_attack_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Physical Down+Block guard during Baraka action7;90sec/320MiB/10MiB/no media')
