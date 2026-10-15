"""Reuse historical mirror physical guard/leg sequence, no dense observers."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_native_start_preparation'
out=sync.ROOT/'audit_current_sonya_p2_mirror_guard_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
needle="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(needle)==1
branch='''   if leg_tactic and other.roster==18 then
    local forward=human.x<other.x and'Right'or'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    if not mg_last or frame-mg_last~=1 then mg_leg=nil;mg_retry=-1000;mg_upper=-1000;mg_guard=-1000 end
    mg_last=frame
    local blocking=human.action==1792 or human.action==1793
    local ready=height<=8 and (blocking or human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==263)
      and human.flags&0x18==0 and (blocking or human.body&0x0c==0)
    local safe=other.action==0 or other.action==771 or other.action==770 or other.action==772 or other.action==263
      or (other.action>=1536 and other.action<=1551)
    if other.action==4 or other.action==10 or other.action==16 then mg_guard=frame+40 end
    if mg_leg and frame-mg_leg<12 then
     local age=frame-mg_leg
     if age<7 then press('Down')end
     if age>=3 and age<7 then press('Low Punch');press('Block')end
    elseif height>8 then
     press('Block');if gap<105 and frame%6<3 then press('High Kick')end
    elseif cpu_height>15 and gap<100 then
     press('Down')
     if ready and gap<78 and frame-mg_upper>=26 then press('High Punch');mg_upper=frame
     else press('Block')end
    elseif frame<mg_guard or (not safe and gap<125) then
     press('Down');press('Block')
    elseif ready and safe and gap<85 and frame-mg_retry>=32 then
     mg_leg=frame;mg_retry=frame;press('Down')
     log('MIRROR_GUARD_ATTEMPT',string.format('stage=%d gap=%d human_action=%d cpu_action=%d',stage,gap,human.action,other.action))
    elseif ready and safe and gap>75 and cpu_height<=8 then
     mg_leg=nil;press(forward)
    else
     press('Down');press('Block')
    end
   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then'''
source=source.replace(needle,branch)
source=source.replace('local guard_until=-1000','local guard_until=-1000\nlocal mg_last,mg_leg,mg_retry,mg_upper,mg_guard=nil,nil,-1000,-1000,-1000',1)
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_native_start_runtime','audit_current_sonya_p2_mirror_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared native mirror guarded LP+Block command;30k/no media/current caps')
