"""Passive action changes and exact damage callback; controller byte unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kunglao_stance_counter_preparation'
out=sync.ROOT/'audit_current_kano_kunglao_counter_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
needle="   log('HEALTH',string.format("
assert source.count(needle)==1
extra=r'''
   if p:read_u16(0x01061b30)==4 and cpu.PC.value==0xff836700 then
    local before,after=p:read_u16(at),data&0xffff
    local own,other=sample(1),sample(2)
    if before<=161 and after<before and own and other then
     log('KUNGLAO_DAMAGE_DETAIL',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d heights=%d,%d gap=%d',n,before,after,cpu.A8.value,cpu.A13.value,own.actor,own.main,other.actor,other.main,own.id,other.id,own.action,other.action,own.floor-own.y,other.floor-other.y,math.abs(own.x-other.x)))
    end
   end
'''
source=source.replace(needle,extra+needle).replace('frame>=24000','frame>=19500').replace('maximum_fields=24000','maximum_fields=19500')
source+=r'''
local kl_seen={}
emu.register_frame(function()
 if p:read_u16(0x01061b30)~=4 then return end
 local own,other=sample(1),sample(2)
 if not own or not other or own.id~=17 or own.roster~=17 or other.id~=0 or other.roster~=0 then return end
 if kl_seen.main~=own.main or kl_seen.a~=own.action or kl_seen.b~=other.action then
  kl_seen.main=own.main;kl_seen.a=own.action;kl_seen.b=other.action
  log('KUNGLAO_ACTION_CHANGE',string.format('p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d flags=%04X,%04X heights=%d,%d gap=%d counter_age=%d health=%d,%d',own.actor,own.main,other.actor,other.main,own.id,other.id,own.action,other.action,own.flags,other.flags,own.floor-own.y,other.floor-other.y,math.abs(own.x-other.x),kl_start and frame-kl_start or -1,own.hp,other.hp))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kunglao_stance_counter_runtime','audit_current_kano_kunglao_counter_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared19500field unchanged-input trace,90sec/320MiB,no media')
