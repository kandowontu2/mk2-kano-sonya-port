"""Observe exact native jump/kick Main writes on identical physical replay."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_event_jump_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_air_writers_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   elseif fighter=='kano' and side==2 and other.roster==3 then\n"
assert source.count(marker)==1
extra="""    sc_action_taps=sc_action_taps or {}
    if not sc_action_taps[human.main] then
     local own_main=human.main
     sc_action_taps[own_main]=p:install_write_tap(own_main+0x1f0,own_main+0x1ff,'passive own Scorpion fight air action stores',function(at,data,mask)
      if mask~=0xffff or p:read_u16(0x01061b30)~=6 then return end
      local h,c=sample(2),sample(1)
      if not h or not c or h.id~=17 or h.roster~=17 or c.id~=3 or h.main~=own_main or h.owner~=h.actor or cpu.A8.value~=h.actor or cpu.A13.value~=h.main then return end
      if cpu.PC.value~=0xff831360 and cpu.PC.value~=0xff871f50 then return end
      log('SCORPION_AIR_WRITE',string.format('at=%08X after=%d pc=%08X actor=%08X main=%08X owner=%08X a8=%08X a13=%08X gap=%d height=%d health=%d,%d',at,data&0xffff,cpu.PC.value,h.actor,h.main,h.owner,cpu.A8.value,cpu.A13.value,math.abs(h.x-c.x),h.floor-h.y,h.hp,c.hp))
     end)
     taps[#taps+1]=sc_action_taps[own_main]
    end
"""
source=source.replace(marker,marker+extra)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_event_jump_runtime','audit_current_kano_p2_scorpion_air_writers_runtime')
(out/'run.ps1').write_text(runner)
print('Passive native air action writes/geometry; unchanged physical replay;90sec/320MiB/10MiB/no media')
