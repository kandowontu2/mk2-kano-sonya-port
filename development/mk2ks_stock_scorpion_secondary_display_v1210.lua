-- Unchanged real coin/select/two-round/fatality inputs; extra read-only art evidence.
dofile('mk2ks_stock_scorpion_secondary_inputs_v1210.lua')
local killer_id=assert(({scorpion=10})[os.getenv('MK2KS_STOCK_KILLER')])
local victim_id=assert(({kano=17,sonya=18,liu_kang=1,kitana=4})[os.getenv('MK2KS_TEST_FIGHTER')])
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local gfx=manager.machine.memory.regions[':gfxrom']
local output=assert(os.getenv('MK2KS_REPTILE_AUDIT_DIR'))
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local frame,first,last,total=0,nil,nil,0
local queues,taps={},{}
local pending,seen={},{}
local palette_seen={}
local death_bytes=p:read_u32(0xff300040)
local dma
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_dma_register$')then assert(not dma);dma=emu.item(index)end
end end
assert(dma)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_ROLLING_HEAD_V1003_%s frame=%d writes=0 assistance=none %s',tag,frame,text))
end
local function save(file,data)
 local f=assert(io.open(output..'/'..file,'wb'));f:write(data);f:close()
end
-- Observe original secondary/victim choreography and sound requests. No
-- program, CPU-state, graphics or save-state writes are permitted here.
local fire_taps={}
for _,address in ipairs({0xff8bbfe0,0xff8bc810,0xff8bca00,0xff8bc710,
 0xff876650,0xff8b6450,0xff8cdc40,0xffa12530,0xff8386b0,0xff83ae20})do
 fire_taps[#fire_taps+1]=p:install_read_tap(address,address+15,'original fire choreography',function(at)
  local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
  if at~=address or not start or frame-start>650 then return end
  local actor=cpu.A8.value
  log('FIRE_CALL',string.format('age=%d entry=%08X actor=%08X main=%08X id=%d a0=%08X a1=%08X a9=%08X',
   frame-start,address,actor,cpu.A13.value,valid(actor)and p:read_u16(actor+0x1f0)or-1,
   cpu.A0.value,cpu.A1.value,cpu.A9.value))
 end)
end
local previous={}
local gate_taps={}
for _,address in ipairs({0xff868700,0xff8687d0,0xff868880,0xff8688a0,
 0xff8688c0,0xff8688e0,0xff876fc0,0xff8777f0,0xff8bbfe0,
 0xff876ff0,0xff877030,0xff877090,0xff8770d0,0xff877110,
 0xff877120,0xff877160,0xff877190,0xff8771d0,0xff8771f0,
 0xff877270,0xff8772f0,0xff877340,0xff877350,0xff877420})do
 gate_taps[#gate_taps+1]=p:install_read_tap(address,address+15,'native fire rejection diagnostic',function(at)
  if at~=address or frame<600 or p:read_u16(0x01061b00)~=3 then return end
  log('FIRE_GATE',string.format('entry=%08X actor=%08X main=%08X a0=%08X a1=%08X a3=%08X a7=%08X a9=%08X a10=%08X tick=%d',
   address,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A1.value,cpu.A3.value,cpu.A7.value,
   cpu.A9.value,cpu.A10.value,p:read_u16(0x0105d090)))
 end)
end
emu.register_frame(function()
 assert(#fire_taps==10 and #gate_taps==24,'Keep every native choreography/gate observer alive')
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if not start or frame-start>960 then return end
 for slot,field in ipairs({0x01060220,0x01060df0})do
  local actor,main=p:read_u32(field),p:read_u32(field+0x40)
  local state=string.format('slot=%d actor=%08X main=%08X',slot,actor,main)
  if valid(actor)and valid(main)then
   state=state..string.format(' id=%d roster=%d owner=%08X pose=%08X bank=%04X flags=%04X x=%d y=%d floor=%d attached=%08X',
    p:read_u16(actor+0x1f0),p:read_u16(field+0x60),p:read_u32(main+0xc0),
    p:read_u32(actor+0x1d0),p:read_u16(actor+0x140),p:read_u16(actor+0x160),
    p:read_i16(actor+0x90),p:read_i16(actor+0xb0),p:read_i16(main+0x200),p:read_u32(main+0x190))
  end
  if previous[slot]~=state then log('FIRE_STATE','age='..(frame-start)..' '..state);previous[slot]=state end
 end
end)
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'all native owned fatality FIFO sources',function(at)
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if not start or frame-start>650 or at~=0xff804410 or cpu.PC.value~=0xff804420 then return end
 local a=cpu.A0.value
 if not valid(a)then return end
 local id=p:read_u16(a+0x1f0)
 if id~=victim_id and id~=killer_id then return end
 log('ALL_FIFO',string.format('actor=%08X source=%08X pose=%08X cache=%08X id=%d bank=%04X x=%d y=%d size=%08X xy=%08X command=%04X cursor=%08X',
  a,cpu.A11.value,p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_u16(a+0x1f0),p:read_u16(a+0x140),
  p:read_i16(a+0x90),p:read_i16(a+0xb0),cpu.A9.value,cpu.A10.value,cpu.A12.value,cpu.A1.value))
end)
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'native custom death artwork FIFO',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 then return end
 local source=cpu.A11.value
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if not start or frame-start>650 then return end
 local a=cpu.A0.value;if not valid(a)then return end
 local id=p:read_u16(a+0x1f0)
 if id~=victim_id and id~=killer_id then return end
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
 local cursor=cpu.B14.value+192;local q=queues[cursor]
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if not start or frame-start>650 or not q or q.source~=source then return end
 if not palette_seen[source]then
  palette_seen[source]=true
  local bytes={};local pal=manager.machine.palettes[':palette'];local base=dma:read(8)&0x7f00
  for index=0,63 do bytes[#bytes+1]=string.pack('<I4',pal:pen_color(base+index)&0xffffff)end
  local file=string.format('death_palette_%08X_%d.bin',source,frame)
  save(file,table.concat(bytes))
  log('PALETTE_DUMP',string.format('source=%08X bank=%04X file=%s',source,base,file))
 end
 local key=string.format('%08X_%08X',q.actor,q.source)
 if not seen[key] then seen[key]=true;pending[#pending+1]={frame=frame+1,key=key,source=source}end
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
  local count=death_bytes -- Header-bound extended packed allocation.
  local bytes={};for at=0, count-1 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1ec0000+at))end
  save('native_death_gfx.bin',table.concat(bytes))
  log('BOOT','guest_bytes=1048576 gfx_bytes='..count)
 end
end)
-- Only AFTER native screen presentation, not at the beginning of the field.
emu.register_frame_done(function()
 for index=#pending,1,-1 do
  local item=pending[index]
  if item.frame<=frame then
   manager.machine.screens[':screen']:snapshot('head_pose_'..item.key..'_'..frame..'.png')
   log('POSE_SNAPSHOT',string.format('actor_pose=%s source=%08X queued_frame=%d',item.key,item.source,item.frame-1))
   table.remove(pending,index)
  end
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('native_dma=%d first=%d last=%d',total,first or -1,last or -1))
end)
