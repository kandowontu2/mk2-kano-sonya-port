-- Unchanged real coin/select/two-round/fatality inputs; extra read-only art evidence.
dofile('mk2ks_stock_head_victim_v913.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local gfx=manager.machine.memory.regions[':gfxrom']
local output=assert(os.getenv('MK2KS_REPTILE_AUDIT_DIR'))
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local frame,first,last,total=0,nil,nil,0
local queues,taps={},{}
local dma
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_dma_register$')then assert(not dma);dma=emu.item(index)end
end end
assert(dma)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_DEATH_ART_V897_%s frame=%d writes=0 assistance=none %s',tag,frame,text))
end
local function save(file,data)
 local f=assert(io.open(output..'/'..file,'wb'));f:write(data);f:close()
end
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'all native owned fatality FIFO sources',function(at)
 local start=rawget(_G,'MK2_STOCK_V913_ACTION_START')
 if not start or frame-start>300 or at~=0xff804410 or cpu.PC.value~=0xff804420 then return end
 local a=cpu.A0.value
 if not valid(a)or p:read_u16(a+0x1f0)~=(os.getenv('MK2KS_TEST_FIGHTER')=='kano'and 17 or 18)then return end
 log('ALL_FIFO',string.format('actor=%08X source=%08X pose=%08X cache=%08X id=%d bank=%04X x=%d y=%d size=%08X xy=%08X command=%04X cursor=%08X',
  a,cpu.A11.value,p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_u16(a+0x1f0),p:read_u16(a+0x140),
  p:read_i16(a+0x90),p:read_i16(a+0xb0),cpu.A9.value,cpu.A10.value,cpu.A12.value,cpu.A1.value))
end)
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'native custom death artwork FIFO',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 then return end
 local source=cpu.A11.value
 if source<0x0f600000 or source>=0x0f660260 then return end
 local a=cpu.A0.value;if not valid(a)then return end
 local field=side==1 and 0x01060220 or 0x01060df0
 local physical,main=p:read_u32(field),p:read_u32(field+0x40)
 if not valid(physical)or not valid(main)then return end
 local cache=p:read_u32(a+0x1a0)
 local q={actor=a,physical=physical,main=main,source=source,cursor=cpu.A1.value,
  pose=p:read_u32(a+0x1d0),id=p:read_u16(a+0x1f0),body=p:read_u16(a+0x160),
  bank=p:read_u16(a+0x140),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(main+0x200),
  size=cpu.A9.value,xy=cpu.A10.value,command=cpu.A12.value,palette=cpu.A6.value,
  stageY=p:read_i16(0x0105ecd0),displayY=p:read_i16(0x0105d060),cameraY=p:read_i16(0x0105d130)}
 queues[q.cursor]=q
 log('QUEUE',string.format('cursor=%08X source=%08X actor=%08X physical=%08X main=%08X owner=%08X id=%d pose=%08X cache=%08X body=%04X bank=%04X x=%d y=%d floor=%d size=%08X xy=%08X command=%08X palette=%08X stageY=%d displayY=%d cameraY=%d',
  q.cursor,source,a,physical,main,p:read_u32(main+0xc0),q.id,q.pose,cache,q.body,q.bank,q.x,q.y,q.floor,q.size,q.xy,q.command,q.palette,q.stageY,q.displayY,q.cameraY))
end)
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'actual custom death artwork native DMA',function(at,data,mask)
 local bank=((dma:read(15)or 0)>>5)&1
 local reg=mapping[bank+1][(at-0x01a80000)//16]
 local command=(dma:read(reg)&(~mask))|(data&mask)
 if reg~=1 or command&0x8000==0 or command&15~=2 then return end
 local source=dma:read(2)|(dma:read(3)<<16)
 if source<0x0f600000 or source>=0x0f660260 then return end
 local cursor=cpu.B14.value+192;local q=queues[cursor]
 first=first or frame;last=frame;total=total+1
 log('DMA',string.format('cursor=%08X source=%08X command=%04X palette=%04X x=%d y=%d width=%d height=%d fifo_actor=%08X fifo_physical=%08X fifo_main=%08X fifo_pose=%08X queue_match=%d',
  cursor,source,command,dma:read(8)&0x7f00,dma:read(4)&0x3ff,dma:read(5)&0x1ff,
  dma:read(6)&0x3ff,dma:read(7)&0x3ff,q and q.actor or 0,q and q.physical or 0,
  q and q.main or 0,q and q.pose or 0,q and q.source==source and 1 or 0))
end)
emu.register_frame(function()
 assert(#taps==3,'Retain native artwork observers')
 frame=frame+1
 if frame==1 then
  local f=assert(io.open(output..'/guest_maincpu.bin','wb'))
  for block=0,0xfffff,0x1000 do
   local bytes={}
   for at=0,0xfff do bytes[#bytes+1]=string.char(p:read_u8(0xff800000+(block+at)*8))end
   f:write(table.concat(bytes))
  end
  f:close()
  local count=0xc04c -- Exact v894 packed allocation, including alignment.
  local bytes={};for at=0, count-1 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1ec0000+at))end
  save('native_death_gfx.bin',table.concat(bytes))
  log('BOOT','guest_bytes=1048576 gfx_bytes='..count)
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('native_dma=%d first=%d last=%d',total,first or -1,last or -1))
end)
