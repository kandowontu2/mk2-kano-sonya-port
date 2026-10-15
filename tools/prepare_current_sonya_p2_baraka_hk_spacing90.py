"""Widen Baraka-only physical HK spacing window; do not modify native range."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_hk_guard_ready_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_hk_spacing90_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='gap<((other.roster==2 or other.roster==0 or other.roster==9 or other.roster==3) and 100 or 90)'
new='gap<(other.roster==3 and 90 or ((other.roster==2 or other.roster==0 or other.roster==9) and 100 or 90))'
assert source.count(old)==1;source=source.replace(old,new)
assert source.count('frame>=60000')==1
source=source.replace('frame>=60000','frame>=120000').replace('maximum_fields=60000','maximum_fields=120000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_hk_guard_ready_runtime','audit_current_sonya_p2_baraka_hk_spacing90_runtime').replace("'-str','1250'","'-str','2500'").replace('TotalSeconds -gt 90','TotalSeconds -gt 180')
(out/'run.ps1').write_text(runner)
print('Barakaonlyphysicalspacing90;180sec/320MiB/10MiB/no media/guestwrites')
