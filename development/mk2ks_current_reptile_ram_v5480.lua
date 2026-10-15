-- Entire original887/904 controller and corrected owned art; passive display.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
dofile(root..'/mk2ks_current_reptile_ram_v5470.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local palette=manager.machine.palettes[':palette']
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local own=side==1 and 0x01060df0 or 0x01060220
local victim=side==1 and 0x01060220 or 0x01060df0
local native_frame,action_frame,latch=0,nil,nil
local vram,taps=nil,{}
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_local_videoram$')then assert(not vram);vram=emu.item(index)end
end end
assert(vram and vram.size==2 and vram.count>=512*512)
emu.register_frame(function()native_frame=native_frame+1 end)
taps[#taps+1]=p:install_read_tap(0xff8c81f0,0xff8c81ff,'passive actual Reptile display action epoch',function(at)
 if at~=0xff8c81f0 or action_frame or native_frame<=600 then return end
 local actor=p:read_u32(own);local other=p:read_u32(victim)
 if actor<0x01000000 or actor>=0x01100000 or other<0x01000000 or other>=0x01100000 then return end
 if cpu.A8.value~=actor or p:read_u16(actor+0x1f0)~=9 or p:read_u16(other+0x1f0)<17 then return end
 action_frame=native_frame
end)
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'passive actual native Reptile scene flip',function(at,data,mask)
 if at~=0xc0000090 or not action_frame then return end
 local age=native_frame-action_frame
 if age~=150 and age~=200 and age~=250 then return end
 latch={frame=native_frame,start=data&0xffff,control=p:read_u16(0xc0000080),tap=p:read_u16(0xc00001b0),
  pc=cpu.PC.value,mask=mask,raw=vram:read_block(0,512*512*2)}
end)
local original_snapshot=mk2_reptile_ram_snapshot
function mk2_reptile_ram_snapshot(filename)
 local age=assert(tonumber(filename:match('_(%d+)%.png$')))
 local colors={};for pen=0,32767 do colors[#colors+1]=string.pack('<I4',palette:pen_color(pen)&0xffffff)end
 local fields=string.format('filename=%s frame=%d age=%d',filename,native_frame,age)
 if age==150 or age==200 or age==250 then
  assert(latch and latch.frame==native_frame)
  fields=fields..string.format(' flip_frame=%d start=%04X control=%04X tap=%04X pc=%08X mask=%04X',
   latch.frame,latch.start,latch.control,latch.tap,latch.pc,latch.mask)
  mk2_reptile_ram_emit('VRAM',latch.raw,fields)
 end
 mk2_reptile_ram_emit('PALETTE',table.concat(colors),fields)
 original_snapshot(filename)
end
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
