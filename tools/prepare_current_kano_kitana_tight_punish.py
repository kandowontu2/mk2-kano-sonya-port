"""Shorter physical HP window, earlier guard after actual crouch preparation."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kitana_close_guard_preparation'
out=sync.ROOT/'audit_current_kano_kitana_tight_punish_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
for old,new in (("if age<10 or age>=24 then press('Block')end","if age<10 or age>=17 then press('Block')end"),("if age>=13 and age<24 and age%6<3 then press('High Punch')end","if age>=13 and age<17 and age%6<3 then press('High Punch')end")):
    assert source.count(old)==1;source=source.replace(old,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kitana_close_guard_runtime','audit_current_kano_kitana_tight_punish_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18000field tightphysicalpunish test,no media,90sec/320MiB')
