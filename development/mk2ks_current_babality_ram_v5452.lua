-- Native single-frame FIFO/DMA/display binding; unchanged original controller.
local file=assert(io.open('mk2ks_current_babality_ram_v5446.lua','rb'))
local wrapper=file:read('*a');file:close()
local before="assert(load(transport..source,'@entire_original_babality_controller_RAM_sinks_only','t',_ENV))()"
local after=[====[
replace_once('for index=0,31 do colors[#colors+1]', 'for index=0,63 do colors[#colors+1]')
local observe=[==[
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local palette=manager.machine.palettes[':palette']
local native_frame=0
emu.register_frame(function()native_frame=native_frame+1 end)
local dma,vram
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_local_videoram$')then assert(not vram);vram=emu.item(index)end
 if name:match('m_dma_register$')then assert(not dma);dma=emu.item(index)end
end end
assert(vram and dma and vram.size==2 and vram.count>=512*512)
local function emit(tag,raw,fields)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print('MK2_BRAM_'..tag..' '..fields..' bytes='..#raw..' hex='..hex)
end
local tables={[0xfffcb400]=true,[0xfffcb500]=true,[0xffb1c960]=true}
local queues,last_dma,taps={},{},{}
local latch
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'passive baby native FIFO',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 then return end
 local actor=cpu.A0.value
 if actor<0x01000000 or actor>=0x01100000 then return end
 local cache=p:read_u32(actor+0x1a0)
 if not tables[cache]then return end
 local q={frame=native_frame,actor=actor,cache=cache,cursor=cpu.A1.value,source=cpu.A11.value,size=cpu.A9.value,xy=cpu.A10.value,
  world=((p:read_i16(actor+0xb0)&0xffff)<<16)|(p:read_i16(actor+0x90)&0xffff),camera=cpu.A4.value,
  body=cpu.A7.value,command=cpu.A12.value,palette=cpu.A6.value}
 queues[q.cursor]=q
 print(string.format('MK2_BRAM_QUEUE frame=%d actor=%08X cache=%08X cursor=%08X source=%08X size=%08X xy=%08X world=%08X camera=%08X body=%08X command=%08X palette=%08X pc=%08X writes=0 assistance=none',
  q.frame,q.actor,q.cache,q.cursor,q.source,q.size,q.xy,q.world,q.camera,q.body,q.command,q.palette,cpu.PC.value))
end)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'passive baby native hardware DMA',function(at,data,mask)
 local bank=((dma:read(15)or 0)>>5)&1
 local reg=mapping[bank+1][(at-0x01a80000)//16]
 local command=(dma:read(reg)&(~mask))|(data&mask)
 if reg~=1 or command&0x8000==0 or command&15~=2 then return end
 local q=queues[cpu.B14.value+192]
 local source=dma:read(2)|(dma:read(3)<<16)
 if not q or q.source~=source then return end
 local row={frame=native_frame,queue=q,x=dma:read(4)&1023,y=dma:read(5)&511,width=dma:read(6)&1023,height=dma:read(7)&1023,
  command=command,palette=dma:read(8)&0x7f00,pc=cpu.PC.value}
 last_dma[q.cache]=row
 print(string.format('MK2_BRAM_DMA frame=%d queue_frame=%d actor=%08X cache=%08X cursor=%08X source=%08X x=%d y=%d width=%d height=%d command=%04X palette=%04X pc=%08X writes=0 assistance=none',
  row.frame,q.frame,q.actor,q.cache,q.cursor,source,row.x,row.y,row.width,row.height,row.command,row.palette,row.pc))
end)
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'passive actual native display latch',function(at,data,mask)
 if at~=0xc0000090 then return end
 latch={frame=native_frame,start=data&0xffff,control=p:read_u16(0xc0000080),tap=p:read_u16(0xc00001b0),
  pc=cpu.PC.value,mask=mask,raw=vram:read_block(0,512*512*2),dma={}}
 for key,value in pairs(last_dma)do latch.dma[key]=value end
end)
local function native_baby_observe_snapshot(filename,frame)
 if filename~='babality_160.png'and filename~='babality_200.png'and filename~='babality_240.png'then return end
 assert(latch and latch.frame==frame and native_frame==frame)
 local colors={};for pen=0,32767 do colors[#colors+1]=string.pack('<I4',palette:pen_color(pen)&0xffffff)end
 local fields=string.format('frame=%d filename=%s flip_frame=%d start=%04X control=%04X tap=%04X pc=%08X mask=%04X',
  frame,filename,latch.frame,latch.start,latch.control,latch.tap,latch.pc,latch.mask)
 emit('VRAM',latch.raw,fields);emit('PALETTE',table.concat(colors),fields)
 for key,row in pairs(latch.dma)do
  print(string.format('MK2_BRAM_DISPLAY_DMA frame=%d filename=%s dma_frame=%d queue_frame=%d actor=%08X cache=%08X cursor=%08X source=%08X x=%d y=%d width=%d height=%d pc=%08X writes=0 assistance=none',
   frame,filename,row.frame,row.queue.frame,row.queue.actor,key,row.queue.cursor,row.queue.source,row.x,row.y,row.width,row.height,row.pc))
 end
end
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
]==]
local before_snapshot="local function ram_snapshot(filename,frame)"
local index,last=assert(transport:find(before_snapshot,1,true));assert(not transport:find(before_snapshot,last+1,true))
transport=transport:sub(1,index-1)..before_snapshot.."\n native_baby_observe_snapshot(filename,frame)"..transport:sub(last+1)
assert(load(observe..transport..source,'@original_babality_with_passive_full_palette_FIFO_DMA_scanout','t',_ENV))()
]====]
local first,last=assert(wrapper:find(before,1,true));assert(not wrapper:find(before,last+1,true))
wrapper=wrapper:sub(1,first-1)..after..wrapper:sub(last+1)
assert(load(wrapper,'@original_babality_RAM_transport_native_scanout_observer','t',_ENV))()
