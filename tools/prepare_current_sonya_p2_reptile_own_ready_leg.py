"""Physical leg attempts gated by actual human readiness, not inferred CPU idle."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_reptile_damage_trace_preparation'
out=sync.ROOT/'audit_current_sonya_p2_reptile_own_ready_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='   elseif leg_tactic and (other.roster==0 or (side==2 and (other.roster==1 or other.roster==9))) then\n'
assert source.count(marker)==1
branch="""   elseif fighter=='sonya' and side==2 and other.roster==9 then
    local height=human.floor-human.y
    local blocking=human.action==1792 or human.action==1793
    local ready=height==0 and p:read_u32(human.actor+0x60)==0 and human.flags&0x1c==0
     and (blocking or human.body&0x0c==0) and (blocking or human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==263)
    if not rl_last or frame-rl_last~=1 then rl_start=nil;rl_retry=-1000 end
    rl_last=frame
    if rl_start and frame-rl_start<12 then
     local age=frame-rl_start
     if age<7 then press('Down')end
     if age>=3 and age<7 then press('Low Punch');press('Block')end
    elseif ready and gap<115 and frame-rl_retry>=32 and other.floor-other.y<=8 then
     rl_start=frame;rl_retry=frame;press('Down')
     log('REPTILE_LEG_PLAN',string.format('gap=%d human_action=%d cpu_action=%d cpu_flags=%04X',gap,human.action,other.action,other.flags))
    elseif ready and gap>105 then
     press(human.x<other.x and 'Right' or 'Left')
    else
     press('Down');press('Block')
    end
"""
source='local rl_last,rl_start,rl_retry=nil,nil,-1000\n'+source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_reptile_damage_trace_runtime','audit_current_sonya_p2_reptile_own_ready_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Reptile physical leg gated by own native readiness;90sec/320MiB/10MiB/no media')
