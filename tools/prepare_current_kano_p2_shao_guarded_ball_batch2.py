"""Authorized batch2: Shao-only ball continuation and shorter physical retry."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_guarded_ball_batch1_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_guarded_ball_batch2_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('elseif other.hp<=55 and ready then')==1 and source.count('frame-sb_release>=60')==1
source=source.replace('elseif other.hp<=55 and ready then','elseif other.roster~=13 and other.hp<=55 and ready then').replace('frame-sb_release>=60','frame-sb_release>=(other.roster==13 and 24 or 60)')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_guarded_ball_batch1_runtime','audit_current_kano_p2_shao_guarded_ball_batch2_runtime')
(out/'run.ps1').write_text(runner)
print('Authorizedbatch2/3 Shaoonly ballthroughKO/retry24;180sec/320MiB/10MiB/no media')
