"""Passive CPU throw-start writes and actual paired recovery/input geometry."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_retreat_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_throw_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='   local gap=math.abs(human.x-other.x)\n'
assert source.count(marker)==1
extra="""   if other.roster==5 and stage==10 then
    mt_taps=mt_taps or {}
    if not mt_taps[other.main] then
     local observed_main=other.main
     mt_taps[observed_main]=p:install_write_tap(observed_main+0x1f0,observed_main+0x1ff,'passive actual Mileena throw start',function(at,data,mask)
      if mask~=0xffff or data&0xffff~=1287 or p:read_u16(0x01061b30)~=10 then return end
      local h,c=sample(2),sample(1)
      if not h or not c or h.id~=17 or h.roster~=17 or c.id~=5 or c.roster~=5 or c.main~=observed_main or c.owner~=c.actor or h.owner~=h.actor then return end
      log('MILEENA_THROW_START',string.format('pc=%08X at=%08X a8=%08X a13=%08X cpu_actor=%08X cpu_main=%08X human_actor=%08X human_main=%08X gap=%d h_x=%d c_x=%d height=%d cpu_height=%d action=%d flags=%04X body=%04X cpu_flags=%04X cpu_body=%04X hardware=%04X health=%d,%d',cpu.PC.value,at,cpu.A8.value,cpu.A13.value,c.actor,c.main,h.actor,h.main,math.abs(h.x-c.x),h.x,c.x,h.floor-h.y,c.floor-c.y,h.action,h.flags,h.body,c.flags,c.body,p:read_u16(0x01600000),h.hp,c.hp))
     end)
     taps[#taps+1]=mt_taps[observed_main]
    end
   end
"""
source=source.replace(marker,marker+extra)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_retreat_counter_runtime','audit_current_kano_p2_mileena_throw_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Passive actual CPU1287 write scalar trace;unchanged controller;60000target/90sec/320MiB/10MiB/no media')
