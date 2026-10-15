"""Compact historical stock-specific input branches; no old recorder execution."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_mirror_guard_preparation'
out=sync.ROOT/'audit_current_sonya_stock_guard_tactics_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
historical=(sync.ROOT/'mk2ks_sonya_extended_guard_base_ram_v5201.lua').read_text()
start=historical.index('    -- Original block handlers use actions700/701')
end=historical.index("    log('GUARD_DECISION'",start)
policy=historical[start:end].replace('gp_','cg_')
logstart=policy.index("    log('GUARD_FIELD'")
logend=policy.index('    local reason\n',logstart)
policy=policy[:logstart]+policy[logend:]
policy=policy.replace('if other.action==4 or other.action==0xa or other.action==0x10 then', 'if other.action==4 or other.action==0xa or other.action==0x10 or (other.roster==8 and other.action==0x604)then')
policy=policy.replace('if cg_leg and frame-cg_leg<12 then', "if other.roster==11 and other.action==0x137 then cg_pound=frame+40 end\n    if other.roster==11 and frame<cg_pound and height<=8 then\n     cg_leg=nil;if frame-cg_jump>=4 then cg_jump=frame end\n     if frame-cg_jump<3 then press('Up');press(human.x<other.x and'Left'or'Right')end\n    elseif cg_leg and frame-cg_leg<(other.roster==8 and 26 or 12)then")
policy=policy.replace("if age<9 then press('Down')end", "if age<(other.roster==8 and 24 or 9)then press('Down')end")
policy=policy.replace("if age>=6 and age<9 then press('High Punch')end", "local punch_at=other.roster==8 and 10 or 6\n      if age>=punch_at and age<punch_at+3 then press('High Punch')end")
policy=policy.replace("reason='anti_air_attempt';press('High Punch');cg_upper=frame", "reason='anti_air_attempt';cg_move='uppercut';cg_leg=frame;cg_upper=frame")
prefix='''   if leg_tactic and (other.roster==4 or other.roster==8 or other.roster==11)then
    local forward=human.x<other.x and'Right'or'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    if not cg_last or frame-cg_last~=1 or cg_roster~=other.roster then
     cg_leg=nil;cg_move=nil;cg_last_leg=-1000;cg_upper=-1000;cg_guard=-1000;cg_pound=-1000;cg_jump=-1000
    end
    cg_last=frame;cg_roster=other.roster
'''
marker='   if leg_tactic and other.roster==18 then\n'
assert source.count(marker)==1
source=source.replace(marker,prefix+policy+"    if reason and reason:find('attempt',1,true)then log('STOCK_GUARD_ATTEMPT','cpu_roster='..other.roster..' reason='..reason..' gap='..gap)end\n   elseif leg_tactic and other.roster==18 then\n")
source="local cg_last,cg_roster,cg_leg,cg_move=nil,nil,nil,nil\nlocal cg_last_leg,cg_upper,cg_guard,cg_pound,cg_jump=-1000,-1000,-1000,-1000,-1000\n"+source
old='css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster))'
assert source.count(old)==1
source=source.replace(old,'css=frame;selections=selections+1;plan={}')
needle='  local age=frame-css\n'
assert source.count(needle)==1
source=source.replace(needle,needle+"  if age==56 then plan=route(p:read_u16(slots[side].roster));log('SELECT_INITIALIZED','target='..identity..' initial='..p:read_u16(slots[side].roster))end\n")
source=source.replace('frame>=30000','frame>=18000').replace('maximum_fields=30000','maximum_fields=18000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
for side in (1,2):
 text=runner.replace('audit_current_sonya_p2_mirror_guard_runtime',f'audit_current_sonya_stock_guard_tactics_p{side}_runtime')
 text=text.replace("$env:MK2KS_CAMPAIGN_SIDE='2'",f"$env:MK2KS_CAMPAIGN_SIDE='{side}'")
 (out/f'run_p{side}.ps1').write_text(text)
print('Prepared compact historical Kitana/Jax/SubZero physical policies, initialized selections, both slots')
