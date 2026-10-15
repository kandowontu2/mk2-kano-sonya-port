"""Grounded ordinary-HK mirror response, unchanged earlier earned Sonya route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_kunglao_guard_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_standing_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then')
end=source.index('   elseif leg_tactic and other.roster==0 then',start)
branch=r'''   if leg_tactic and other.roster==18 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    local stance=human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793
    local ready=height<=8 and human.flags&0x1c==0 and stance
    local safe=(other.action==0 or other.action==771 or other.action==772 or other.action==770) and other.flags&0x0c==0
    if not ms_last or frame-ms_last~=1 then ms_start=nil;ms_retry=-1000 end
    ms_last=frame
    if ms_start and frame-ms_start<32 then
     local age=frame-ms_start
     if age>=2 and age<6 then press('High Kick')end
     if age>=10 then press('Down');press('Block')end
    elseif ready and safe and cpu_height<=8 and gap<105 and frame-ms_retry>=32 then
     ms_start=frame;ms_retry=frame
     log('MIRROR_STANDING_COUNTER',string.format('gap=%d action=%d cpu_action=%d health=%d,%d',gap,human.action,other.action,human.hp,other.hp))
    elseif ready and safe and cpu_height<=8 and gap>=105 then
     ms_start=nil;press(forward)
    else
     ms_start=nil;press('Down');press('Block')
    end
'''
source='local ms_last,ms_start,ms_retry=nil,nil,-1000\n'+source[:start]+branch+source[end:]
source=source.replace('frame>=18000','frame>=24000').replace('maximum_fields=18000','maximum_fields=24000')
needle="   log('HEALTH',string.format(";assert source.count(needle)==1
extra=r'''
   if p:read_u16(0x01061b30)==5 and cpu.PC.value==0xff836700 then
    local before,after=p:read_u16(at),data&0xffff
    local own,other=sample(1),sample(2)
    if own and other and before<=161 and after<before then
     log('MIRROR_STANDING_DAMAGE',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d gap=%d',n,before,after,cpu.A8.value,cpu.A13.value,own.actor,own.main,other.actor,other.main,own.id,other.id,own.action,other.action,math.abs(own.x-other.x)))
    end
   end
'''
source=source.replace(needle,extra+needle)
source+=r'''
local ms_seen={}
emu.register_frame(function()
 if p:read_u16(0x01061b30)~=5 or p:read_u16(0x010601d0)~=2 then return end
 local own,other=sample(1),sample(2)
 if not own or not other or own.id~=18 or other.id~=18 or own.roster~=18 or other.roster~=18 then return end
 if ms_seen.main~=own.main or ms_seen.a~=own.action or ms_seen.b~=other.action then
  ms_seen.main=own.main;ms_seen.a=own.action;ms_seen.b=other.action
  log('MIRROR_STANDING_ACTION',string.format('p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d flags=%04X,%04X heights=%d,%d gap=%d counter_age=%d health=%d,%d',own.actor,own.main,other.actor,other.main,own.id,other.id,own.action,other.action,own.flags,other.flags,own.floor-own.y,other.floor-other.y,math.abs(own.x-other.x),ms_start and frame-ms_start or -1,own.hp,other.hp))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_kunglao_guard_runtime','audit_current_sonya_mirror_standing_counter_runtime')
assert runner.count("'-str','900'")==1
runner=runner.replace("'-str','900'","'-str','450'")
(out/'run.ps1').write_text(runner)
print('Prepared24000field Sonya mirror-only standingHK,90sec/320MiB,no media')
