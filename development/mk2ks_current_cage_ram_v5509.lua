-- Entire original921 controller and979 section observers; RAM-only evidence.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local function read(name)
 local f=assert(io.open(root..'/'..name,'rb'));local s=f:read('*a');f:close();return(s:gsub('\r\n','\n'))
end
local function replace_once(s,before,after)
 local first,last=assert(s:find(before,1,true));assert(not s:find(before,last+1,true))
 return s:sub(1,first-1)..after..s:sub(last+1)
end
function mk2_cage_ram_emit(tag,raw,fields)
 print('MK2_CURRENT_CAGE_RAM_'..tag..' '..fields..' bytes='..#raw..' hex='..
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
end
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local gfx=manager.machine.memory.regions[':gfxrom']
local pal=manager.machine.palettes[':palette']
local frame,serial,latch=0,0,nil
local queues,emitted,taps={},{},{}
local dma,vram
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_dma_register$')then assert(not dma);dma=emu.item(index)end
 if name:match('m_local_videoram$')then assert(not vram);vram=emu.item(index)end
end end
assert(dma and vram and vram.size==2 and vram.count>=512*512)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local function active()
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 return start and frame-start>=69 and frame-start<=141
end
function mk2_cage_ram_snapshot(filename)
 if filename:match('^torso_pose_')and active()then
  assert(latch and latch.frame==frame)
  local fields=string.format('filename=%s frame=%d age=%d flip_frame=%d start=%04X control=%04X tap=%04X pc=%08X mask=%04X',
   filename,frame,frame-rawget(_G,'MK2_STOCK_V921_ACTION_START'),latch.frame,latch.start,latch.control,latch.tap,latch.pc,latch.mask)
  local colors={};for i=0,32767 do colors[#colors+1]=string.pack('<I4',pal:pen_color(i)&0xffffff)end
  mk2_cage_ram_emit('VRAM',latch.raw,fields);mk2_cage_ram_emit('PALETTE',table.concat(colors),fields)
  print(string.format('MK2_CURRENT_CAGE_SCENE_CUTOFF filename=%s frame=%d age=%d serial=%d writes=0 assistance=none',
   filename,frame,frame-rawget(_G,'MK2_STOCK_V921_ACTION_START'),latch.serial))
 end
 local raw=manager.machine.video:snapshot_pixels()
 local w,h=manager.machine.video:snapshot_size()
 assert(w==400 and h==254 and #raw==w*h*4)
 mk2_cage_ram_emit('RGB',raw,string.format('filename=%s frame=%d width=%d height=%d',filename,frame,w,h))
end
-- Keep the complete physical controller; replace only its snapshot transport.
local controller=read('mk2ks_stock_head_victim_v921.lua')
controller=replace_once(controller,
 "screen:snapshot(string.format('stock_head_%d_%03d.png',action_start,frame-action_start))",
 "mk2_cage_ram_snapshot(string.format('stock_head_%d_%03d.png',action_start,frame-action_start))")
assert(load(controller,'@entire_original921_physical_controller_RAM_snapshot_sink','t',_ENV))()
local observer=read('mk2ks_cage_torso_display_v979.lua')
observer=replace_once(observer,"dofile('mk2ks_stock_head_victim_v921.lua')",'-- Complete original921 already registered.')
observer=replace_once(observer,"local f=assert(io.open(output..'/'..file,'wb'));f:write(data);f:close()",
 "mk2_cage_ram_emit('DATA',data,'filename='..file)")
observer=replace_once(observer,[=[  local f=assert(io.open(output..'/guest_maincpu.bin','wb'))
  for block=0,0xfffff,0x1000 do
   local bytes={}
   for at=0,0xfff do bytes[#bytes+1]=string.char(p:read_u8(0xff800000+(block+at)*8))end
   f:write(table.concat(bytes))
  end
  f:close()]=],[=[  local bytes={}
  for at=0,0xfffff do bytes[#bytes+1]=string.char(p:read_u8(0xff800000+at*8))end
  save('guest_maincpu.bin',table.concat(bytes))]=])
observer=replace_once(observer,'local count=0xc04c -- Exact v894 packed allocation, including alignment.',
 'local count=p:read_u32(0xff300040) -- Actual compiled current death allocation, passive header read.')
observer=replace_once(observer,"manager.machine.screens[':screen']:snapshot('torso_pose_'..item.key..'_'..frame..'.png')",
 "mk2_cage_ram_snapshot('torso_pose_'..item.key..'_'..frame..'.png')")
assert(load(observer,'@entire_original979_FIFO_palette_section_ground_retirement_RAM_sinks','t',_ENV))()
emu.register_frame(function()frame=frame+1 end)
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'passive complete native foreground FIFO',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 or not active()then return end
 local a=cpu.A0.value;if a<0x01000000 or a>=0x01100000 then return end
 queues[cpu.A1.value]={frame=frame,actor=a,source=cpu.A11.value,size=cpu.A9.value,xy=cpu.A10.value,
  command=cpu.A12.value,palette=cpu.A6.value,pose=p:read_u32(a+0x1d0),cache=p:read_u32(a+0x1a0),
  bank=p:read_u16(a+0x140),id=p:read_u16(a+0x1f0),body=p:read_u16(a+0x160)}
end)
local function observe_gfx(source,command,w,h)
 if command&15==12 or w==0 or h==0 then return end
 local key=string.format('%08X_%04X_%d_%d',source,command,w,h)
 if emitted[key]then return end;emitted[key]=true
 local offset=source
 if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000 end
 if offset>=0xf8000000 then offset=offset-0xf8000000 end
 local bpp=(command>>12)&7;if bpp==0 then bpp=8 end
 local first=offset//8
 local count=math.ceil((offset%8+w*h*bpp+(command&0x80~=0 and h*8 or 0))/8)+8
 assert(first>=0 and first<0x2000000)
 count=math.min(count,0x2000000-first)
 local bytes={};for i=first,first+count-1 do bytes[#bytes+1]=string.char(gfx:read_u8(i))end
 mk2_cage_ram_emit('GFX',table.concat(bytes),string.format('filename=%s offset=%d first=%d',key,offset,first))
end
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'passive ordered complete native foreground DMA',function(at,data,mask)
 local bank=(dma:read(15)>>5)&1
 local reg=mapping[bank+1][(at-0x01a80000)//16]
 local command=(dma:read(reg)&(~mask))|(data&mask)
 if reg~=1 or command&0x8000==0 or not active()then return end
 serial=serial+1
 local r={};for i=0,17 do r[i]=dma:read(i)end;r[1]=command
 local source=r[2]|(r[3]<<16);local w,h=r[6]&0x3ff,r[7]&0x3ff
 local cursor=cpu.B14.value+192;local q=queues[cursor]
 local match=q and q.frame==frame and q.source==source
 print(string.format('MK2_CURRENT_CAGE_SCENE_DMA frame=%d serial=%d source=%08X command=%04X palette=%04X color=%d x=%d y=%d width=%d height=%d scaleX=%d scaleY=%d left=%d right=%d top=%d bottom=%d skip=%d pc=%08X cursor=%08X queue_match=%d queue_frame=%d actor=%08X pose=%08X cache=%08X bank=%04X id=%d body=%04X queue_size=%08X queue_xy=%08X queue_command=%04X queue_palette=%04X writes=0 assistance=none',
  frame,serial,source,command,r[8]&0x7f00,r[9]&255,r[4]&0x3ff,r[5]&0x1ff,w,h,r[10],r[11],
  r[16]&0x3ff,r[17]&0x3ff,r[12]&0x1ff,r[13]&0x1ff,r[0],cpu.PC.value,cursor,match and 1 or 0,
  q and q.frame or -1,q and q.actor or 0,q and q.pose or 0,q and q.cache or 0,q and q.bank or 0,
  q and q.id or -1,q and q.body or 0,q and q.size or 0,q and q.xy or 0,q and q.command or 0,q and q.palette or 0))
 observe_gfx(source,command,w,h)
end)
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'passive actual section presentation flip',function(at,data,mask)
 if at~=0xc0000090 or not active()then return end
 latch={frame=frame,serial=serial,start=data&0xffff,control=p:read_u16(0xc0000080),tap=p:read_u16(0xc00001b0),
  pc=cpu.PC.value,mask=mask,raw=vram:read_block(0,512*512*2)}
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
