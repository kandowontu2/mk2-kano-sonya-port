"""Physical retreat during grounded close recovery; never change guest state."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_subzero_throw_onset_preparation'
out=sync.ROOT/'audit_current_sonya_p2_subzero_close_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='    if sr_start and frame-sr_start<64 then\n'
assert source.count(marker)==1
branch="""    if height<=8 and gap<90 and (not sh_start or frame-sh_start>=10) and (not sr_start or frame-sr_start>=15) then
     sh_start=nil;sr_start=nil
     press(human.x<other.x and 'Left' or 'Right')
    elseif sr_start and frame-sr_start<64 then
"""
source=source.replace(marker,branch)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_subzero_throw_onset_runtime','audit_current_sonya_p2_subzero_close_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('CPU8-only grounded back input gap<90 outside early attack/command;30k/90sec/320MiB/10MiB/no media')
