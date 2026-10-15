"""Successor fixes observer screen handle; preserve executed failed fixture."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_winner_visual_preparation'
out=sync.ROOT/'audit_current_sonya_winner_visual_screen_preparation'
assert not out.exists()
source=(old/'campaign.lua').read_text()
wrong="machine.screens[':screen']:snapshot('winner_'"
assert source.count(wrong)==1
source=source.replace(wrong,"screen:snapshot('winner_'")
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text().replace(old.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_winner_visual_runtime','audit_current_sonya_winner_visual_screen_runtime')
(out/'run.ps1').write_text(runner)
checker=(sync.ROOT/'tools/qualify_current_sonya_winner_visuals.py').read_text()
checker=checker.replace('audit_current_sonya_winner_visual_runtime','audit_current_sonya_winner_visual_screen_runtime').replace('audit_current_sonya_winner_visual_preparation','audit_current_sonya_winner_visual_screen_preparation').replace('audit_current_sonya_winner_visual_checked','audit_current_sonya_winner_visual_screen_checked')
(out/'qualify.py').write_text(checker)
print('Prepared corrected screen handle, unchanged controller and caps')
