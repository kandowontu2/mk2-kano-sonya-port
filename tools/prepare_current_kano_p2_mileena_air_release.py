"""Physical landing guard release, same native air observation and AI."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_air_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_air_release_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   if fighter=='kano' and side==2 and other.roster==5 then")
end=source.index("   elseif fighter=='kano' and side==2 and (other.roster==18",start)
branch=source[start:end]
old='or human.action==1792 or human.action==3)'
new='or human.action==1792 or human.action==1793 or human.action==769 or human.action==3)'
assert branch.count(old)==1
branch=branch.replace(old,new)
oldguard="    else press('Down');press('Block')end"
assert branch.count(oldguard)==1
branch=branch.replace(oldguard,"    else ma_jump=nil end")
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_air_counter_runtime','audit_current_kano_p2_mileena_air_release_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only neutral landing fallback/1793+769ready;90sec/320MiB/10MiB/no media')
