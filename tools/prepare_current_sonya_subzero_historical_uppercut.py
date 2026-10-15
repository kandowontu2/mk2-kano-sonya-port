"""Compact physical Sub-Zero policy from historical guard controller, no dumps."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_mirror_guard_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_historical_uppercut_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then\n')
end=source.index('   elseif (leg_tactic or strategy==',start)
branch=source[start:end].replace('   if leg_tactic and other.roster==18 then','   elseif leg_tactic and other.roster==8 then').replace('mg_','sz_')
branch=branch.replace('human.flags&0x18','human.flags&0x1c')
branch=branch.replace('other.action==16 then','other.action==16 or other.action==1540 then')
branch=branch.replace("if age<7 then press('Down')end\n     if age>=3 and age<7 then press('Low Punch');press('Block')end","if age<9 then press('Down')end\n     if age>=6 and age<9 then press('High Punch')end")
branch=branch.replace('gap<85','gap<63').replace('gap>75','gap>58').replace('MIRROR_GUARD_ATTEMPT','SUBZERO_UPPERCUT_ATTEMPT')
source=source[:end]+branch+source[end:]
source="local sz_last,sz_leg,sz_retry,sz_upper,sz_guard=nil,nil,-1000,-1000,-1000\n"+source
old='css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster))'
assert source.count(old)==1
source=source.replace(old,'css=frame;selections=selections+1;plan={}')
needle='  local age=frame-css\n'
assert source.count(needle)==1
source=source.replace(needle,needle+"  if age==56 then plan=route(p:read_u16(slots[side].roster));log('SELECT_INITIALIZED','target='..identity..' initial='..p:read_u16(slots[side].roster))end\n")
source=source.replace('frame>=30000','frame>=18000').replace('maximum_fields=30000','maximum_fields=18000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_mirror_guard_runtime','audit_current_sonya_subzero_historical_uppercut_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared historical native Sub-Zero uppercut controls, post-init cursor routes, 18000 fields/no media')
