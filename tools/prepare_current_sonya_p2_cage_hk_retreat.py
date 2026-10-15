"""Extend physical Sonya kick/retreat controller to native Cage ID2 only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_subzero_close_retreat_preparation'
out=sync.ROOT/'audit_current_sonya_p2_cage_hk_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   elseif fighter=='sonya' and side==2 and other.roster==8 then"
assert source.count(marker)==1
source=source.replace(marker,"   elseif fighter=='sonya' and side==2 and (other.roster==8 or other.roster==2) then")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_subzero_close_retreat_runtime','audit_current_sonya_p2_cage_hk_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('CPU2-only policy extension; earlier inputs unchanged;30k/90sec/320MiB/10MiB/no media')
