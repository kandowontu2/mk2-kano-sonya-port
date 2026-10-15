"""Authorized batch3: best guarded retry60, Shao knife handoff55to20 only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_guarded_ball_batch1_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_guarded_ball_batch3_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='elseif other.hp<=55 and ready then'
assert source.count(old)==1
source=source.replace(old,'elseif other.hp<=(other.roster==13 and 20 or 55) and ready then')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_guarded_ball_batch1_runtime','audit_current_kano_p2_shao_guarded_ball_batch3_runtime')
(out/'run.ps1').write_text(runner)
print('Authorizedbatch3/3 Shaoonly knifehandoff20/retry60;180sec/320MiB/10MiB/no media')
