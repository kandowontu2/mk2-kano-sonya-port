"""Same observed charge counter, physical crouching rather than standing guard."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_charge_settled_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_crouch_charge_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
branch=source[start:end]
assert branch.count("press('Block')")==2
branch=branch.replace("press('Block')","press('Down');press('Block')")
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_charge_settled_counter_runtime','audit_current_kano_p2_shao_crouch_charge_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Crouchguard/observedchargecounter;180sec/320MiB/10MiB/no media/guestwrites')
