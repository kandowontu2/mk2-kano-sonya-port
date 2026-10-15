"""Stage12 physical short leg controller, preserving proven Sub-Zero route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_subzero_short_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p1_liukang_short_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='sonya' and side==1 and other.roster==8 and stage==11 then")
end=source.index("   elseif fighter=='sonya' and side==1 and (other.roster==8",start+1)
branch=source[start:end].replace("other.roster==8 and stage==11","other.roster==1 and stage==12").replace("log('SONYA_SETTLED_LEG_PLAN'","log('SONYA_LIUKANG_LEG_PLAN'")
marker="   elseif leg_tactic and (other.roster==0 or (side==1 and other.roster==1)) then"
assert source.count(marker)==1
source=source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_subzero_short_leg_runtime','audit_current_sonya_p1_liukang_short_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Stage12 only: physical short leg Down7 LP+Block3..7 retry48; 180sec/320MiB/10MiB; no media')
