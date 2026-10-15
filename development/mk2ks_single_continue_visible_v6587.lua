-- On paid P2 continue, mode4 can still contain the prior valid character ID
-- before its new cursor is initialized. Route only once native CSS is drawn.
-- Header pixels are read-only, exactly the established challenger criterion.
-- Extra passive scenes show the actual ladder, not the previous CSS buffer
-- sampled on the very callback when the mode first changes.
local f=assert(io.open('mk2ks_single_continue_controls_v6579.lua','rb'))
local wrapper=f:read('*a');f:close()
-- Extend the source transformations before the preserved wrapper loads them.
local marker="assert(load(source,'@mk2ks_single_continue_v6567.lua::physical_actual_control_observer'))()"
local insert=[[
replace('a8=%08X a13=%08X',
 'a8=%08X a13=%08X ctxOwner=%08X parent=%08X ctxID=%d pairActor=%08X pairMain=%08X pairAction=%d caller=%08X')
replace('cpu.A8.value,cpu.A13.value))',
 [=[cpu.A8.value,cpu.A13.value,
 valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0xc0)or 0,
 valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0x230)or 0,
 valid(cpu.A8.value)and p:read_u16(cpu.A8.value+0x1f0)or -1,
 valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0x140)or 0,
 valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0x170)or 0,
 valid(cpu.A13.value)and valid(p:read_u32(cpu.A13.value+0x170))and p:read_u16(p:read_u32(cpu.A13.value+0x170)+0x1f0)or -1,
 p:read_u32(cpu.SP.value)))]=])
replace("local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Coin',age,270,5);pulse('Start',age,310,5)",
 [=[local age=frame-continueAt
  if side==2 then pulse('Coin',age,20,5);pulse('Coin',age,50,5);pulse('Start',age,80,5)
  else pulse('Coin',age,20,5);pulse('Coin',age,270,5);pulse('Start',age,310,5)end]=])
replace('if frame>=14000 then',
 'if recover and frame>=recover+180 then manager.machine:exit()end\n if frame>=14000 then')
replace('local adjacency={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}',[=[local function css_visible()
 local yellow=0
 for y=0,24,2 do for x=40,360,2 do
  local c=string.unpack('<I4',pixels,(y*width+x)*4+1)
  if (c>>16)&255>175 and (c>>8)&255>140 and c&255<100 then yellow=yellow+1 end
 end end
 return yellow>=400 and yellow<=430
end
local adjacency={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}]=])
replace('if mode==4 and state==3 and p:read_u16(slots[side].roster)<=18 then reselect=frame;',
 'if mode==4 and state==3 and p:read_u16(slots[side].roster)<=18 and css_visible()then reselect=frame;')
replace('if reselectExit and not reLive and mode==2 and owned(own,ids[target])',
 [=[if reselectExit and not reLive and (frame==reselectExit+30 or frame==reselectExit+90 or frame==reselectExit+180)then snap('actual_continue_ladder')end
 if reselectExit and not reLive and mode==2 and owned(own,ids[target])]=])
]]
local first,last=assert(wrapper:find(marker,1,true));assert(not wrapper:find(marker,last+1,true))
wrapper=wrapper:sub(1,first-1)..insert..wrapper:sub(first)
assert(load(wrapper,'@mk2ks_single_continue_controls_v6579.lua::native_visible_cursor'))()
