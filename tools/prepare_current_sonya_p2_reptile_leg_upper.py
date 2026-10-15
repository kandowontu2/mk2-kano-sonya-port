"""Physical native uppercut at low CPU HP; preserve earlier qualified route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_own_ready_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_leg_upper_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='sonya' and side==2 and other.roster==9 then\n")
end=source.index('   elseif leg_tactic and ',start)
branch=source[start:end]
old='    if rl_start and frame-rl_start<12 then\n'
assert branch.count(old)==1
branch=branch.replace(old,"    if ru_start and frame-ru_start<8 then\n     local age=frame-ru_start\n     if age<6 then press('Down')end\n     if age>=2 and age<6 then press('High Punch')end\n    elseif rl_start and frame-rl_start<12 then\n")
old='    elseif ready and gap<115 and frame-rl_retry>=32 and other.floor-other.y<=8 then\n'
assert branch.count(old)==1
branch=branch.replace(old,"    elseif ready and other.hp<=60 and gap<105 and frame-ru_retry>=32 and other.floor-other.y<=8 then\n     ru_start=frame;ru_retry=frame;rl_start=nil;press('Down')\n     log('REPTILE_UPPER_PLAN',string.format('gap=%d cpu_hp=%d human_hp=%d',gap,other.hp,human.hp))\n"+old)
source='local ru_start,ru_retry=nil,-1000\n'+source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_own_ready_leg_runtime','audit_current_sonya_p2_reptile_leg_upper_runtime')
(out/'run.ps1').write_text(runner)
print('Physical lowHP uppercut plus own-ready leg;90sec/320MiB/10MiB/no media')
