"""Continuous-Down close uppercut preparation, native physical controls only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kunglao_early_counter_preparation'
out=sync.ROOT/'audit_current_kano_kunglao_crouch_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if identity==17 and other.roster==0 then')
end=source.index('   elseif identity==17 and other.roster==4 then',start)
branch=r'''   if identity==17 and other.roster==0 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    local stance=human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793
    local ready=height<=8 and human.flags&0x1c==0 and stance
    local safe=(other.action==0 or other.action==771 or other.action==772 or other.action==770 or other.action==1792 or other.action==1793) and other.flags&0x0c==0
    if not ku_last or frame-ku_last~=1 then ku_start=nil end
    ku_last=frame
    if gap<105 and height<=8 and (ready or human.action==263) then
     if not ku_start or frame-ku_start>=36 then ku_start=frame end
     local age=frame-ku_start
     press('Down')
     if age<10 or age>=24 then press('Block')end
     if age>=13 and age<24 and age%6<3 then press('High Punch')end
     if age==13 then log('KANO_KUNGLAO_CROUCH_COUNTER',string.format('stage=%d gap=%d action=%d cpu_action=%d health=%d,%d',stage,gap,human.action,other.action,human.hp,other.hp))end
    elseif ready and safe and gap>=105 and other.floor-other.y<=8 then
     ku_start=nil;press(forward)
    else
     ku_start=nil;press('Down');press('Block')
    end
'''
source='local ku_last,ku_start=nil,nil\n'+source[:start]+branch+source[end:]
source+=r'''
taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'owned KungLao crouch counter uppercut',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=0xff870dd0 or p:read_u16(0x01061b30)~=4 then return end
 local own=sample(side)
 if own and own.id==17 and own.roster==17 and own.owner==own.actor and cpu.A8.value==own.actor and cpu.A13.value==own.main then
  log('KANO_KUNGLAO_NATIVE_UPPER',string.format('actor=%08X main=%08X owner=%08X id=%d pc=%08X',own.actor,own.main,own.owner,own.id,cpu.PC.value))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kunglao_early_counter_runtime','audit_current_kano_kunglao_crouch_counter_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000field continuous-Down physical upper tactic,90sec/320MiB,no media')
