"""Exact hit-time fighter actions and native helper ownership, passive only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kitana_ground_spacing_preparation'
out=sync.ROOT/'audit_current_kano_kitana_damage_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
needle="   log('HEALTH',string.format("
assert source.count(needle)==1
extra=r'''
   if p:read_u16(0x01061b30)==3 and cpu.PC.value==0xff836700 then
    local before,after=p:read_u16(at),data&0xffff
    if before<=161 and after<before then
     local own,other=sample(1),sample(2)
     local main=cpu.A13.value
     if own and other then
      log('KITANA_DAMAGE_DETAIL',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X helper_owner=%08X creator=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d heights=%d,%d gap=%d',n,before,after,cpu.A8.value,main,valid(main) and p:read_u32(main+0xc0) or 0,valid(main) and p:read_u32(main+0x230) or 0,own.actor,own.main,other.actor,other.main,own.id,other.id,own.action,other.action,own.floor-own.y,other.floor-other.y,math.abs(own.x-other.x)))
     end
    end
   end
'''
source=source.replace(needle,extra+needle)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_kitana_ground_spacing_runtime','audit_current_kano_kitana_damage_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18000field scalar hit-time observer, unchangedinputs,no media')
