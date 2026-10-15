-- Missing palette-cache stores only. The retained physical controller and
-- effect/FIFO/DMA observation remain unchanged; no game-state assistance.
dofile('mk2ks_native_selector_sonya_pressure_effects.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,serial=0,0
local taps={}
local base=0x0105bb30
local function log(kind,value)
 serial=serial+1
 print(string.format('MK2_PAL_%s frame=%d sequence=%d %s writes=0 assistance=none',kind,frame,serial,value))
end
local function cache(phase)
 local rows={}
 for i=0,59 do
  local at=base+i*64
  rows[#rows+1]=string.format('%08X:%04X:%04X',p:read_u32(at),p:read_u16(at+32),p:read_u16(at+48))
 end
 log('CACHE','phase='..phase..' entries='..table.concat(rows,','))
end
cache('initial')
taps[#taps+1]=p:install_write_tap(base,base+60*64-1,'complete native palette cache stores',function(at,data,mask)
 local index=(at-base)//64;local entry=base+index*64;local offset=at-entry
 local before=p:read_u16(at);local after=(before&(~mask))|(data&mask)
 log('WRITE',string.format('index=%d at=%08X offset=%d before=%04X data=%04X mask=%04X after=%04X source=%08X refs=%d stamp=%d pc=%08X a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X actor=%08X main=%08X returnPC=%08X',
  index,at,offset,before,data,mask,after&65535,p:read_u32(entry),p:read_u16(entry+32),p:read_u16(entry+48),
  cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A4.value,cpu.A8.value,cpu.A13.value,p:read_u32(cpu.SP.value)))
end)
-- Native actor bank assignment, including objects not currently published.
taps[#taps+1]=p:install_write_tap(0x0102d6f0,0x0105b94f,'native effect palette owner bank stores',function(at,data,mask)
 local displacement=at-0x0102d6f0
 if displacement%0x210~=0x140 then return end
 local actor=at-0x140;local before=p:read_u16(at)
 log('OWNER',string.format('actor=%08X before=%04X data=%04X mask=%04X after=%04X pc=%08X main=%08X returnPC=%08X',
  actor,before,data,mask,((before&(~mask))|(data&mask))&65535,cpu.PC.value,cpu.A13.value,p:read_u32(cpu.SP.value)))
end)
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()cache('frame_done')end)
emu.register_stop(function()
 cache('terminal')
 log('RESULT','terminalFrame='..frame)
 for _,tap in ipairs(taps)do tap:remove()end
end)
