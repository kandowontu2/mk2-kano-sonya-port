-- Original controller retained; observe ordered native foreground operations.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_reptile_ram_v5483.lua','rb'))
local source=f:read('*a');f:close()
assert(load(source,'@original_reptile_controller_and_actual_scanout','t',_ENV))()
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local gfx=manager.machine.memory.regions[':gfxrom']
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local own=side==1 and 0x01060df0 or 0x01060220
local victim=side==1 and 0x01060220 or 0x01060df0
local frame,origin,serial=0,nil,0
local taps,queues,emitted={},{},{}
local flip_serial={}
local dma=nil
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_dma_register$')then assert(not dma);dma=emu.item(index)end
end end
assert(dma)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function active()
 if not origin then return false end
 local age=frame-origin
 return age==149 or age==150 or age==199 or age==200 or age==249 or age==250
end
emu.register_frame(function()frame=frame+1 end)
taps[#taps+1]=p:install_read_tap(0xff8c81f0,0xff8c81ff,'passive overlap action epoch',function(at)
 if at~=0xff8c81f0 or origin or frame<=600 then return end
 local a,b=p:read_u32(own),p:read_u32(victim)
 if valid(a)and valid(b)and cpu.A8.value==a and p:read_u16(a+0x1f0)==9 and
    p:read_u16(b+0x1f0)>=17 then origin=frame end
end)
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'passive all native foreground FIFO',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 or not active()then return end
 local a=cpu.A0.value;if not valid(a)then return end
 queues[cpu.A1.value]={frame=frame,actor=a,source=cpu.A11.value,
  size=cpu.A9.value,xy=cpu.A10.value,command=cpu.A12.value,palette=cpu.A6.value,
  pose=p:read_u32(a+0x1d0),cache=p:read_u32(a+0x1a0),bank=p:read_u16(a+0x140),
  id=p:read_u16(a+0x1f0),body=p:read_u16(a+0x160)}
end)
local function observe_gfx(source,command,w,h)
 if command&15==12 or w==0 or h==0 then return end
 local key=string.format('%08X_%04X_%d_%d',source,command,w,h)
 if emitted[key]then return end;emitted[key]=true
 local offset=source
 if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000 end
 if offset>=0xf8000000 then offset=offset-0xf8000000 end
 local bits=(command>>12)&7;if bits==0 then bits=8 end
 local first=offset//8
 local count=math.ceil((offset%8+w*h*bits+(command&0x80~=0 and h*8 or 0))/8)+8
 assert(first>=0 and first<0x2000000)
 count=math.min(count,0x2000000-first)
 local bytes={};for i=first,first+count-1 do bytes[#bytes+1]=string.char(gfx:read_u8(i))end
 mk2_reptile_ram_emit('GFX',table.concat(bytes),string.format('filename=%s offset=%d first=%d',key,offset,first))
end
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'passive ordered native foreground DMA',function(at,data,mask)
 local bank=(dma:read(15)>>5)&1
 local reg=mapping[bank+1][(at-0x01a80000)//16]
 local command=(dma:read(reg)&(~mask))|(data&mask)
 if reg~=1 or command&0x8000==0 or not active()then return end
 serial=serial+1
 local r={};for i=0,17 do r[i]=dma:read(i)end;r[1]=command
 local source=r[2]|(r[3]<<16);local w,h=r[6]&0x3ff,r[7]&0x3ff
 local cursor=cpu.B14.value+192;local q=queues[cursor]
 local matched=q and q.frame==frame and q.source==source
 print(string.format('MK2_CURRENT_REPTILE_SCENE_DMA frame=%d serial=%d source=%08X command=%04X palette=%04X color=%d x=%d y=%d width=%d height=%d scaleX=%d scaleY=%d left=%d right=%d top=%d bottom=%d skip=%d pc=%08X cursor=%08X queue_match=%d queue_frame=%d actor=%08X pose=%08X cache=%08X bank=%04X id=%d body=%04X queue_size=%08X queue_xy=%08X queue_command=%04X queue_palette=%04X writes=0 assistance=none',
  frame,serial,source,command,r[8]&0x7f00,r[9]&255,r[4]&0x3ff,r[5]&0x1ff,w,h,r[10],r[11],
  r[16]&0x3ff,r[17]&0x3ff,r[12]&0x1ff,r[13]&0x1ff,r[0],cpu.PC.value,cursor,matched and 1 or 0,
  q and q.frame or -1,q and q.actor or 0,q and q.pose or 0,q and q.cache or 0,q and q.bank or 0,
  q and q.id or -1,q and q.body or 0,q and q.size or 0,q and q.xy or 0,q and q.command or 0,q and q.palette or 0))
 observe_gfx(source,command,w,h)
end)
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'passive exact native foreground cutoff',function(at)
 if at==0xc0000090 and active()then flip_serial[frame]=serial end
end)
local snapshot=mk2_reptile_ram_snapshot
function mk2_reptile_ram_snapshot(filename)
 local age=assert(tonumber(filename:match('_(%d+)%.png$')))
 if age==150 or age==200 or age==250 then
  assert(flip_serial[frame])
  print(string.format('MK2_CURRENT_REPTILE_SCENE_CUTOFF filename=%s frame=%d age=%d serial=%d writes=0 assistance=none',filename,frame,age,flip_serial[frame]))
 end
 snapshot(filename)
end
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
