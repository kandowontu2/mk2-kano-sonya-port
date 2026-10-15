-- Real cold P1 CPU/P2 human inputs are owned by the unchanged v7 scenario.
-- This observer only reads native display, sprite caches and graphics bytes.
dofile('mk2ks_cpu_recovery_probe_v7.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local gfx=manager.machine.memory.regions[':gfxrom']
local palette=manager.machine.palettes[':palette']
local output=assert(os.getenv('MK2KS_FLOOR_OUT'))
local frame,origin,event,snaps=0,nil,0,0
local taps,regs,emitted={},{},{}
local base,pre_frame,latch=nil,-1,nil
local vram,video_bank,dma_item=nil,nil,nil
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_local_videoram$')then assert(not vram);vram=emu.item(index)end
 if name:match('m_videobank_select$')then video_bank=emu.item(index)end
 if name:match('m_dma_register$')then dma_item=emu.item(index)end
end end
assert(vram and video_bank and dma_item and vram.size==2 and vram.count>=512*512)
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function active()return origin and frame>=origin and frame<=origin+240 end
local function next_event()event=event+1;return event end
local function log(tag,value)
 print(string.format('MK2_NAT_CAMPAIGN_%s frame=%d human_slot=2 fighter=%s writes=0 assistance=none %s',tag,frame,os.getenv('MK2KS_TEST_FIGHTER'),value or''))
end
local function save(file,raw)
 local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()
end
local function ensure_base()
 if base then return end
 base=true;save('display_base.bin',vram:read_block(0,512*512*2))
 log('FLOOR_BASE',string.format('epoch=1 event=%d file=display_base.bin phase=before_first_observed_write',event))
end
local function actor(n)
 local field=n==1 and 0x01060220 or 0x01060df0
 local a,m=p:read_u32(field),p:read_u32(field+0x40)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),
  roster=p:read_u16(field+0x60),pose=p:read_u32(a+0x1d0),cache=p:read_u32(a+0x1a0),
  bank=p:read_u16(a+0x140),body=p:read_u16(a+0x160),facing=p:read_u16(a+0xf0),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),action=p:read_u16(m+0x1f0)}
end
for _,address in ipairs({0xfff91400,0xfff80800})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'first actual CPU grab display window',function(at)
  local a=actor(1)
  if not origin and at==address and cpu.PC.value==address+16 and a and a.owner==a.actor and
     cpu.A8.value==a.actor and cpu.A13.value==a.main and p:read_u16(0x010601f0)==0 then
   origin=frame;log('FLOOR_BEGIN',string.format('epoch=1 origin=%d CPU=%d actor=%08X main=%08X',origin,a.id,a.actor,a.main))
  end
 end)
end
taps[#taps+1]=p:install_write_tap(0,0x001fffff,'actual CPU VRAM writes',function(at,data,mask)
 if not active()then return end
 ensure_base();local index=(at//16)*2
 assert(index>=0 and index+1<512*512)
 log('FLOOR_CPU',string.format('epoch=1 event=%d at=%08X value=%04X mask=%04X video_bank=%d palette=%04X index=%d before0=%04X before1=%04X pc=%08X',
  next_event(),at,data,mask,video_bank:read(0),dma_item:read(8),index,vram:read(index),vram:read(index+1),cpu.PC.value))
end)
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'actual native display flip',function(at,data,mask)
 if at~=0xc0000090 or not active()then return end
 latch={frame=frame,event=next_event(),start=data&0xffff,control=p:read_u16(0xc0000080),
  tap=p:read_u16(0xc00001b0),raw=vram:read_block(0,512*512*2)}
 log('FLOOR_FLIP',string.format('epoch=1 event=%d at=%08X value=%04X mask=%04X control=%04X tap=%04X pc=%08X',
  latch.event,at,latch.start,mask,latch.control,latch.tap,cpu.PC.value))
end)
local function observe_gfx(source,command,w,h)
 if command&15==12 or w==0 or h==0 then return end
 local key=string.format('%08X_%04X_%d_%d',source,command,w,h)
 if emitted[key]then return end
 emitted[key]=true
 local offset=source
 if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000 end
 if offset>=0xf8000000 then offset=offset-0xf8000000 end
 local bits=(command>>12)&7;if bits==0 then bits=8 end
 local first=offset//8
 local count=math.ceil((offset%8+w*h*bits+(command&0x80~=0 and h*8 or 0))/8)+8
 assert(first>=0 and first<0x2000000)
 count=math.min(count,0x2000000-first)
 local hex={};for i=first,first+count-1 do hex[#hex+1]=string.format('%02X',gfx:read_u8(i))end
 log('FLOOR_GFX',string.format('key=%s offset=%d first=%d bytes=%d data=%s',key,offset,first,count,table.concat(hex)))
end
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'native body/scenery/foreground DMA',function(at,data,mask)
 local bank=((dma_item:read(15)or 0)>>5)&1
 local reg=mapping[bank+1][(at-0x01a80000)//16]
 local merged=(dma_item:read(reg)&(~mask))|(data&mask)
 if reg~=1 or merged&0x8000==0 or not active()then return end
 for i=0,17 do regs[i]=dma_item:read(i)end;regs[1]=merged
 ensure_base()
 -- Save only the exact passes displayed by fixed even-frame samples.
 if pre_frame~=frame and frame%2==1 then
  pre_frame=frame;local file=string.format('display_pre_%d.bin',frame)
  save(file,vram:read_block(0,512*512*2))
  log('FLOOR_PRE_FRAME',string.format('epoch=1 event=%d file=%s phase=before_first_frame_dma',next_event(),file))
 end
 local e=next_event();local command=regs[1]
 local source=regs[2]|(regs[3]<<16);local pal=regs[8]&0x7f00
 local w,h=regs[6]&0x3ff,regs[7]&0x3ff;local slot=0
 for n=1,2 do
  local a=actor(n)
  if a and a.owner==a.actor and a.bank&0x7f00==pal then
   slot=n
   log('FLOOR_OWNER',string.format('epoch=1 event=%d source=%08X slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d cache=%08X pose=%08X bank=%04X body=%04X facing=%04X x=%d y=%d floor=%d action=%d stageY=%d displayY=%d cameraY=%d',
    e,source,n,a.actor,a.main,a.owner,a.id,a.roster,a.cache,a.pose,a.bank,a.body,a.facing,a.x,a.y,a.floor,a.action,p:read_i16(0x0105ecd0),p:read_i16(0x0105d060),p:read_i16(0x0105d130)))
   if command&15==2 and valid(a.cache)then
    for i=0,11 do
     local row=a.cache+i*112;local value=p:read_u32(row)
     if value==0 then break end
     log('FLOOR_CACHE_PART',string.format('event=%d slot=%d part=%d source=%08X width=%d height=%d command=%04X dx=%d dy=%d',
      e,n,i,value,p:read_u16(row+0x20),p:read_u16(row+0x30),p:read_u16(row+0x40),p:read_i16(row+0x50),p:read_i16(row+0x60)))
    end
   end
  end
 end
 log('FLOOR_DMA',string.format('epoch=1 event=%d selection=1 arena=%d mode=%d source=%08X command=%04X palette=%04X slot=%d color=%d x=%d y=%d width=%d height=%d scaleX=%d scaleY=%d left=%d right=%d top=%d bottom=%d skip=%d pc=%08X',
  e,p:read_u16(0x01061ac0),p:read_u16(0x010601d0),source,command,pal,slot,regs[9]&255,regs[4]&0x3ff,regs[5]&0x1ff,w,h,regs[10],regs[11],regs[16],regs[17],regs[12],regs[13],regs[0],cpu.PC.value))
 observe_gfx(source,command,w,h)
end)
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 if not active()or frame<origin+3 or frame%2~=0 then return end
 assert(latch and latch.frame==frame and pre_frame==frame-1,'Exact saved prior pass and current flip')
 snaps=snaps+1
 local file=string.format('display_%d.png',frame);screen:snapshot(file)
 local vfile=string.format('display_vram_%d.bin',frame);save(vfile,latch.raw)
 local colors={};for pen=0,32767 do colors[#colors+1]=string.pack('<I4',palette:pen_color(pen)&0xffffff)end
 local pfile=string.format('display_palette_%d.bin',frame);save(pfile,table.concat(colors))
 log('FLOOR_DISPLAY',string.format('epoch=1 start=%04X control=%04X tap=%04X palette_file=%s',p:read_u16(0xc0000090),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),pfile))
 log('FLOOR_LATCH',string.format('epoch=1 event=%d snapshot=%d flip_frame=%d start=%04X control=%04X tap=%04X file=%s',latch.event,frame,latch.frame,latch.start,latch.control,latch.tap,vfile))
 log('FLOOR_SNAP',string.format('epoch=1 selection=1 arena=%d origin=%d age=%d phase=frame_done file=%s',p:read_u16(0x01061ac0),origin,frame-origin,file))
end)
emu.register_stop(function()
 log('FLOOR_RESULT',string.format('origin=%d snapshots=%d schema=1 scope=sampled_actual_CPU_pair_display_not_all_moves_or_audio',origin or -1,snaps))
 for _,tap in ipairs(taps)do tap:remove()end
end)
