"""Preserve productive route; only native Kung Lao context gets guarded leg inputs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_defensive_routes_preparation'
out=sync.ROOT/'audit_current_sonya_kunglao_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then\n')
end=source.index('   elseif (leg_tactic or strategy==',start)
branch=source[start:end].replace('   if leg_tactic and other.roster==18 then','   elseif leg_tactic and other.roster==0 then').replace('mg_','kg_')
branch=branch.replace('human.flags&0x18','human.flags&0x1c')
old='or (other.action>=1536 and other.action<=1551)'
assert branch.count(old)==1
branch=branch.replace(old,'or other.action==1792 or other.action==1793')
branch=branch.replace("    if other.action==4", "    safe=safe and other.flags&0x0c==0\n    if other.action==4")
branch=branch.replace('MIRROR_GUARD_ATTEMPT','KUNGLAO_GUARD_ATTEMPT')
source=source[:end]+branch+source[end:]
source="local kg_last,kg_leg,kg_retry,kg_upper,kg_guard=nil,nil,-1000,-1000,-1000\n"+source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_p1.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_defensive_routes_p1_runtime','audit_current_sonya_kunglao_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18000fields, guarded KungLao0 only; earlier current route untouched')
