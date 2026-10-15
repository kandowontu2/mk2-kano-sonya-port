"""Use native knife at shorter range; retain earlier campaign unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_approved_180s_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_close_knife_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then\n',start)
branch=source[start:end];assert branch.count('elseif gap<140 then')==1
branch=branch.replace('elseif gap<140 then','elseif gap<80 then').replace('shao_knife_command_attempt','shao_close_knife_command_attempt')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_approved_180s_runtime','audit_current_kano_p2_shao_close_knife_runtime')
(out/'run.ps1').write_text(runner)
print('Knife gap80 instead140;180sec/320MiB/10MiB/no media/guestwrites')
