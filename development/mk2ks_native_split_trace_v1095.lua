-- Same real inputs and display observer; native split register trace only.
dofile('mk2ks_stock_fatality_display_v1021.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,taps=0,{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function words(a)
 if a<0xfe800000 or a>=0xfffffff0 then return 'none' end
 local items={}
 for n=0,3 do items[#items+1]=string.format('%08X',p:read_u32(a+n*32))end
 return table.concat(items,',')
end
for _,address in ipairs({0xff8cecb0,0xff8cece0,0xff8cede0,0xff8cef00,
 0xff8cefb0,0xff8cf030,0xff842630,0xff842650,0xff842690,0xff8426b0})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'read-only original split state',function(at)
  local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
  if at~=address or cpu.PC.value~=address+16 or not start or frame-start>230 then return end
  local actor,other=cpu.A8.value,cpu.A10.value
  print(string.format('MK2_SPLIT_V1095_STATE frame=%d age=%d at=%08X actor=%08X id=%d other=%08X other_id=%d a0=%08X a9=%08X a11=%08X main=%08X sp=%08X st=%08X flags=%04X other_flags=%04X words9=%s words11=%s writes=0 assistance=none',
   frame,frame-start,address,actor,valid(actor)and p:read_u16(actor+0x1f0)or-1,
   other,valid(other)and p:read_u16(other+0x1f0)or-1,cpu.A0.value,cpu.A9.value,
   cpu.A11.value,cpu.A13.value,cpu.SP.value,cpu.ST.value,
   valid(actor)and p:read_u16(actor+0xf0)or 0,valid(other)and p:read_u16(other+0xf0)or 0,
   words(cpu.A9.value),words(cpu.A11.value)))
 end)
end
emu.register_frame(function()frame=frame+1 end)
