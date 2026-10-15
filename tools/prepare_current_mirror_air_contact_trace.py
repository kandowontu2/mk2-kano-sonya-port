"""Native attack entry and actual damage writer, unchanged confirmed-jump inputs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_mirror_confirmed_jump_preparation'
out=sync.ROOT/'audit_current_mirror_air_contact_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='for n,slot in ipairs(slots)do\n'
assert source.count(marker)==1
extra=r'''
taps[#taps+1]=p:install_read_tap(0xff8718a0,0xff8718af,'native action270 attack entry',function(at)
 if at~=0xff8718a0 or cpu.PC.value~=0xff8718b0 or p:read_u16(0x01061b30)~=5 then return end
 for slot=1,2 do
  local own=sample(slot);local other=sample(3-slot)
  if own and other and cpu.A8.value==own.actor and cpu.A13.value==own.main and own.id==18 and own.roster==18 then
   log('AIR_NATIVE_ENTRY',string.format('slot=%d actor=%08X main=%08X height=%d gap=%d health=%d,%d pc=%08X',slot,own.actor,own.main,own.floor-own.y,math.abs(own.x-other.x),own.hp,other.hp,cpu.PC.value))
  end
 end
end)
'''
source=source.replace(marker,extra+'\n'+marker)
needle="   log('HEALTH',string.format("
assert source.count(needle)==1
extra=r'''
   if p:read_u16(0x01061b30)==5 and cpu.PC.value==0xff836700 then
    local before,after=p:read_u16(at),data&0xffff
    if before<=161 and after<before then
     local own=sample(1);local other=sample(2)
     if own and other then
      log('AIR_NATIVE_DAMAGE',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X actions=%d,%d heights=%d,%d gap=%d',n,before,after,cpu.A8.value,cpu.A13.value,own.actor,own.main,other.actor,other.main,own.action,other.action,own.floor-own.y,other.floor-other.y,math.abs(own.x-other.x)))
     end
    end
   end
'''
source=source.replace(needle,extra+needle)
source=source.replace('frame>=21000','frame>=18500').replace('maximum_fields=21000','maximum_fields=18500')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_mirror_confirmed_jump_runtime','audit_current_mirror_air_contact_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18500field native attack/damage observations,no media,90sec/320MiB')
