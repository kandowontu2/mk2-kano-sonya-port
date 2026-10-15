"""Wait for observed standing pose after blocked/crouched start, native inputs only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_standing_counter_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_confirmed_stance_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then')
end=source.index('   elseif leg_tactic and other.roster==0 then',start)
branch=source[start:end]
before='if not ms_last or frame-ms_last~=1 then ms_start=nil;ms_retry=-1000 end'
assert branch.count(before)==1
branch=branch.replace(before,'if not ms_last or frame-ms_last~=1 then ms_start=nil;ms_retry=-1000;ms_prepare=nil;ms_fast=false end')
before='    if ms_start and frame-ms_start<32 then'
assert branch.count(before)==1
branch=branch.replace(before,r'''    local standing=human.action==0 or human.action==771 or human.action==772
    if ms_prepare then
     if height>8 or human.flags&0x1c~=0 or frame-ms_prepare>=20 then
      log('MIRROR_STAND_CANCEL',string.format('age=%d action=%d flags=%04X',frame-ms_prepare,human.action,human.flags))
      ms_prepare=nil;press('Down');press('Block')
     elseif standing then
      local prep_age=frame-ms_prepare
      ms_prepare=nil;ms_start=frame;ms_retry=frame;ms_fast=true;press('High Kick')
      log('MIRROR_STAND_ACCEPTED',string.format('age=%d action=%d gap=%d flags=%04X',prep_age,human.action,gap,human.flags))
      log('MIRROR_STANDING_COUNTER',string.format('gap=%d action=%d cpu_action=%d health=%d,%d',gap,human.action,other.action,human.hp,other.hp))
     end
    elseif ms_start and frame-ms_start<32 then''')
before="if age>=2 and age<6 then press('High Kick')end"
assert branch.count(before)==1
branch=branch.replace(before,"if (ms_fast and age<4) or (not ms_fast and age>=2 and age<6) then press('High Kick')end")
before="     ms_start=frame;ms_retry=frame\n     log('MIRROR_STANDING_COUNTER',string.format('gap=%d action=%d cpu_action=%d health=%d,%d',gap,human.action,other.action,human.hp,other.hp))"
assert branch.count(before)==1
branch=branch.replace(before,r'''     if standing then
      ms_start=frame;ms_retry=frame;ms_fast=false
      log('MIRROR_STANDING_COUNTER',string.format('gap=%d action=%d cpu_action=%d health=%d,%d',gap,human.action,other.action,human.hp,other.hp))
     else
      ms_prepare=frame;ms_start=nil
      log('MIRROR_STAND_PREPARE',string.format('action=%d gap=%d flags=%04X',human.action,gap,human.flags))
     end''')
source='local ms_prepare,ms_fast=nil,false\n'+source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_standing_counter_runtime','audit_current_sonya_mirror_confirmed_stance_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared24000fields; confirm native standing after block,90sec/320MiB,no media')
