"""Remove controller no-attack gap, without touching native gameplay."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_reptile_crouch_counter_long_preparation'
out=sync.ROOT/'audit_current_sonya_reptile_counter_gap_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if gap>105 then press(human.x<other.x and'Right'or'Left')"
assert source.count(old)==1
source=source.replace(old,"if gap>85 then press(human.x<other.x and'Right'or'Left')")
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_reptile_crouch_counter_long_runtime','audit_current_sonya_reptile_counter_gap_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared20k real counter inputs: approach85 instead105; same native game/caps/no media')
