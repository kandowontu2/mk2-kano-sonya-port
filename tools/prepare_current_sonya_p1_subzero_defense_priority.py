"""SubZero stage11 active-attack defense precedes unprotected retreat."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_subzero_guard_ready_preparation'
out=sync.ROOT/'audit_current_sonya_p1_subzero_defense_priority_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='    if height<=8 and gap<(other.roster==3 and 90 or ((other.roster==2 or other.roster==0 or other.roster==9) and 100 or 90))'
assert source.count(old)==1
new="""    local protected_hk=sh_start and frame-sh_start<6
    local protected_ring=sr_start and frame-sr_start<15
    if other.roster==8 and stage==11 and other.flags&0x10~=0 and not protected_hk and not protected_ring then
     sh_start=nil;sr_start=nil;press('Down');press('Block')
    elseif height<=8 and gap<(other.roster==3 and 90 or ((other.roster==2 or other.roster==0 or other.roster==9) and 100 or 90))"""
source=source.replace(old,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_subzero_guard_ready_runtime','audit_current_sonya_p1_subzero_defense_priority_runtime')
(out/'run.ps1').write_text(runner)
print('Stage11defenseprecedence/protectedcommandinputs;180sec/320MiB/10MiB/no media')
