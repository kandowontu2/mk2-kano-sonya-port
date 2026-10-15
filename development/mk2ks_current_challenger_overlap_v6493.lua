-- Run the entire failed physical Sonya-P2 overlap unchanged. Add only
-- independent native transition-store/CPU/Main observations, never writes.
dofile('mk2ks_current_challenger_v6486.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame=0
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local taps={}
for _,address in ipairs({0x010601d0,0x010601f0,0x01060dc0})do
 taps[#taps+1]=p:install_write_tap(address,address+15,'challenger transition provenance '..address,function(at,data,mask)
  if frame<1450 then return end
  print(string.format('MK2_JO_STORE frame=%d at=%08X before=%04X after=%04X mask=%04X pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X writes=0 assistance=none',frame,at,p:read_u16(at),data&65535,mask,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value))
 end)
end
emu.register_frame_done(function()
 frame=frame+1
 if frame<2000 or frame>2600 and frame%60~=0 then return end
 print(string.format('MK2_JO_CPU frame=%d pc=%08X sp=%08X a8=%08X a13=%08X mode=%d p1state=%d p2state=%d p1hp=%d p2hp=%d input=%04X writes=0 assistance=none',
 frame,cpu.PC.value,cpu.SP.value,cpu.A8.value,cpu.A13.value,p:read_u16(0x010601d0),p:read_u16(0x010601f0),p:read_u16(0x01060dc0),p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(0x01600000)))
 for n,address in ipairs({0x01060260,0x01060e30})do
  local main=p:read_u32(address)
  if valid(main)then
   local words={};for off=0,0x2e0,0x20 do words[#words+1]=string.format('%08X',p:read_u32(main+off))end
   print(string.format('MK2_JO_MAIN frame=%d slot=%d main=%08X words=%s writes=0 assistance=none',frame,n,main,table.concat(words,',')))
  end
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
