"""Release physical crouch/guard after landing, preserve actual close airkick."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_close_air_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_release_air_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="elseif ready and gap>70 then press(forward)\n    else press('Down');press('Block')end"
assert source.count(old)==1
new="""elseif ready and gap>70 then press(forward)
    elseif height<=8 and (human.action==770 or human.action==769 or human.action==1792 or human.action==1793) then
     -- Neutral physical input releases held crouch/guard; no state modification.
    else press('Down');press('Block')end"""
source=source.replace(old,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_close_air_runtime','audit_current_kano_p2_scorpion_release_air_runtime')
(out/'run.ps1').write_text(runner)
print('Physical landing guard release;32000fields/90sec/320MiB/10MiB/no media')
