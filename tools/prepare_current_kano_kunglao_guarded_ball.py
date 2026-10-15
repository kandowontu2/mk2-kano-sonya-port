"""Verified guarded-LK charge physical tactic, native KungLao context only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kunglao_early_counter_preparation'
out=sync.ROOT/'audit_current_kano_kunglao_guarded_ball_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if identity==17 and other.roster==0 then')
end=source.index('   elseif identity==17 and other.roster==4 then',start)
branch=r'''   if identity==17 and other.roster==0 then
    local height=human.floor-human.y
    local stance=human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793
    local ready=height<=8 and human.flags&0x1c==0 and stance
    if not kb_last or frame-kb_last~=1 then kb_start=nil;kb_release=-1000 end
    kb_last=frame
    if kb_start then
     local age=frame-kb_start
     if age<84 or not ready then
      press('Low Kick');press('Down');press('Block')
     else
      kb_start=nil;kb_release=frame
      log('KANO_KUNGLAO_BALL_RELEASE',string.format('stage=%d gap=%d age=%d action=%d cpu_action=%d health=%d,%d',stage,gap,age,human.action,other.action,human.hp,other.hp))
     end
    elseif ready and frame-kb_release>=60 then
     kb_start=frame;press('Low Kick');press('Down');press('Block')
     log('KANO_KUNGLAO_BALL_CHARGE',string.format('stage=%d gap=%d action=%d cpu_action=%d',stage,gap,human.action,other.action))
    elseif human.action~=531 and frame-kb_release>=12 then
     press('Down');press('Block')
    end
'''
source='local kb_last,kb_start,kb_release=nil,nil,-1000\n'+source[:start]+branch+source[end:]
source+=r'''
taps[#taps+1]=p:install_read_tap(0xffffde00,0xffffde0f,'owned campaign guarded ball entry',function(at)
 if at~=0xffffde00 or p:read_u16(0x01061b30)~=4 then return end
 local own=sample(side)
 if own and own.id==17 and own.roster==17 and own.owner==own.actor and cpu.A8.value==own.actor and cpu.A13.value==own.main then
  log('KANO_KUNGLAO_NATIVE_BALL',string.format('actor=%08X main=%08X owner=%08X id=%d pc=%08X',own.actor,own.main,own.owner,own.id,cpu.PC.value))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kunglao_early_counter_runtime','audit_current_kano_kunglao_guarded_ball_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000field KungLao-only physical guarded ball,90sec/320MiB,no media')
