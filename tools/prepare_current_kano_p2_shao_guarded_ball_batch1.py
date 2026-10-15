"""Authorized batch test1: extend proven physical guarded ball to Shao13 only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_approved_180s_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_guarded_ball_batch1_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="elseif fighter=='kano' and side==2 and other.roster==3 then"
assert source.count(old)==1
source=source.replace(old,"elseif fighter=='kano' and side==2 and (other.roster==3 or other.roster==13) then")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_approved_180s_runtime','audit_current_kano_p2_shao_guarded_ball_batch1_runtime')
(out/'run.ps1').write_text(runner)
print('Authorizedbatch1/3 guardedball Shao13;180sec/320MiB/10MiB/no media/no guestwrites')
