"""Physical close-range backward retreat only against actual CPU5."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_approach_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_retreat_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="    elseif other.flags&0x10~=0 then kp_start=nil;press('Down');press('Block')"
assert source.count(old)==1
new="""    elseif other.roster==5 and gap<70 and height<=8 then
     kp_start=nil;press(forward=='Right' and 'Left' or 'Right')
    elseif other.flags&0x10~=0 then kp_start=nil;press('Down');press('Block')"""
source=source.replace(old,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_approach_runtime','audit_current_kano_p2_mileena_retreat_counter_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only physical retreat gap<70/grounded;60000target/90sec/320MiB/10MiB/no media')
