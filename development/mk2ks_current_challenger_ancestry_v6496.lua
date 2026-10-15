-- Exact physical failed Sonya-P2 case, passive native error ancestry only.
dofile('mk2ks_current_challenger_v6486.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame=0
local taps,counts={},{}
local function words(address,count)
 if address<0x01000000 or address+count*32>=0x01100000 then return 'outside_ram' end
 local out={};for i=0,count-1 do out[#out+1]=string.format('%08X',p:read_u32(address+i*32))end
 return table.concat(out,',')
end
for _,entry in ipairs({0xffa1d860,0xffa1e7b0,0xffa1e800,0xffa4c0c0,0xff83f520,0xff817d30,0xff80e0e0,0xff8096f0,0xff80d5f0,0xff80d6c0,0xff80d810})do
 counts[entry]=0
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'challenger native ancestry '..entry,function(at,data,mask)
  if frame<2100 or counts[entry]>=16 then return end
  counts[entry]=counts[entry]+1
  local registers={};for i=0,14 do registers[#registers+1]=string.format('%08X',cpu['A'..i].value)end
  print(string.format('MK2_JA_ENTRY frame=%d at=%08X pc=%08X ordinal=%d sp=%08X registers=%s stack=%s task=%s mode=%d writes=0 assistance=none',frame,at,cpu.PC.value,counts[entry],cpu.SP.value,table.concat(registers,','),words(cpu.SP.value,24),words(cpu.A13.value,24),p:read_u16(0x010601d0)))
 end)
end
emu.register_frame_done(function()frame=frame+1 end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
