"""Same native command against actual Baraka3 and Mileena5; no game edits."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_campaign_slim_health_preparation'
out=sync.ROOT/'audit_current_kano_p2_baraka_choke_route_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="   if fighter=='kano' and side==2 and other.roster==5 then"
new="   if fighter=='kano' and side==2 and (other.roster==5 or other.roster==3) then"
assert source.count(old)==1
source=source.replace(old,new)
for tag in ('LP_INPUT','PLAN'):
    original="log('MILEENA_CHOKE_"+tag+"',"
    replacement="log(other.roster==5 and 'MILEENA_CHOKE_"+tag+"' or 'BARAKA_CHOKE_"+tag+"',"
    assert source.count(original)==1
    source=source.replace(original,replacement)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_campaign_slim_health_runtime','audit_current_kano_p2_baraka_choke_route_runtime')
(out/'run.ps1').write_text(runner)
print('CPU3 Baraka physical D/F/LP counter;earlier route unchanged;80000target/90sec/320MiB/10MiB/no media')
