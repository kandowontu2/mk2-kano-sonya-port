"""Physical response switch after first earned Baraka round, read-only wins."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_baraka_choke_route_preparation'
out=sync.ROOT/'audit_current_kano_p2_baraka_mixed_route_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="(other.roster==5 or other.roster==3) then"
new="(other.roster==5 or (other.roster==3 and (stage_wins[6]or 0)==0)) then"
assert source.count(old)==1
source=source.replace(old,new)
assert source.replace(new,old)==(base/'campaign.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_baraka_choke_route_runtime','audit_current_kano_p2_baraka_mixed_route_runtime')
(out/'run.ps1').write_text(runner)
print('CPU3 choke until first actual ownround, then existing ball/knife inputs;90sec/320MiB/10MiB/no media')
