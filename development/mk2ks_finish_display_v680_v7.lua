-- The unchanged real two-round input scenario owns all controls.
-- This observer reads fighter/child ownership, original FIFO and native scanout.
dofile('mk2ks_unassisted_finish_v680_v2.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local gfx=manager.machine.memory.regions[':gfxrom']
local palette=manager.machine.palettes[':palette']
local output=assert(os.getenv('MK2KS_FLOOR_OUT'))
local side=tonumber(os.getenv('MK2_TRACE_NATIVE_FINISH_SIDE'))
assert(side==1 or side==2)
local frame,origin,event,snaps=0,nil,0,0
local taps,regs,emitted={},{},{}
local base,pre_frame,latch=nil,-1,nil
local queues={}
local retired={}
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
local function active()return origin and frame>=origin and frame<=origin+960 end
local function sampled(f)
 if not origin or f<origin+3 or f>origin+960 then return false end
 return (f-origin<=360 and f%2==0)or(f-origin>360 and f%12==0)
end
local function next_event()event=event+1;return event end
local function log(tag,value)
 print(string.format('MK2_NAT_CAMPAIGN_%s frame=%d human_slot=%d fighter=%s writes=0 assistance=none %s',tag,frame,side,os.getenv('MK2_TRACE_NATIVE_FINISH'),value or''))
end
for _,field in ipairs({0x01060220,0x01060df0})do
 taps[#taps+1]=p:install_write_tap(field,field+31,'native physical fighter pointer store',function(at,data,mask)
  if not active()then return end
  log('FLOOR_POINTER_STORE',string.format('field=%08X at=%08X value=%04X mask=%04X pc=%08X before=%08X',field,at,data,mask,cpu.PC.value,p:read_u32(field)))
 end)
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
 local physical=n==3 and side or n
 local field=physical==1 and 0x01060220 or 0x01060df0
 local a,m=p:read_u32(field),p:read_u32(field+0x40)
 if not valid(a)or not valid(m)then return end
 local parent=a
 if n>2 then
  a=p:read_u32(m+0x190)
  if not valid(a)then return end
 end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),
  parent=parent,kind=n>2 and 1 or 0,
  roster=p:read_u16(field+0x60),pose=p:read_u32(a+0x1d0),cache=p:read_u32(a+0x1a0),
  bank=p:read_u16(a+0x140),body=p:read_u16(a+0x160),facing=p:read_u16(a+0xf0),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),action=p:read_u16(m+0x1f0)}
end
taps[#taps+1]=p:install_read_tap(0xff840b60,0xff840b6f,'actual native single-frame update',function(at)
 if at~=0xff840b60 or cpu.PC.value~=0xff840b70 or not active()then return end
 local m=cpu.A13.value
 if not valid(m)then return end
 local a=p:read_u32(m+0x190);if not valid(a)then return end
 local parent=cpu.A8.value
 local value={};for _,offset in ipairs({0xf0,0x140,0x160,0x1a0,0x1d0})do
  value[#value+1]=string.format('word_%X=%08X',offset,p:read_u32(a+offset))end
 value[#value+1]=string.format('actor=%08X main=%08X parent=%08X x=%d y=%d frame_table=%08X',a,m,parent,p:read_i16(a+0x90),p:read_i16(a+0xb0),cpu.A11.value)
 log('FLOOR_CHILD_UPDATE',table.concat(value,' '))
end)
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'original body FIFO publication',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 or not active()then return end
 local slot=0
 for n=1,3 do local a=actor(n);if a and a.actor==cpu.A0.value then slot=n end end
 if slot==0 then return end
 local a=actor(slot)
 local row=cpu.A3.value-112
 -- A7 comes from actor+160: bit1 selects the native multipart branch.
 -- actor+F0 is the pixel command; its bit1 is not a sprite-type flag.
 local multipart=a.body&2~=0
 if multipart then assert(row>=a.cache and row<a.cache+12*112 and(row-a.cache)%112==0,'Original current cache iterator')end
 local q={slot=slot,actor=a.actor,main=a.main,owner=a.owner,id=a.id,roster=a.roster,pose=a.pose,cache=a.cache,
  bank=a.bank,body=a.body,facing=a.facing,x=a.x,y=a.y,floor=a.floor,action=a.action,
  parent=a.parent,kind=a.kind,multipart=multipart and 1 or 0,
  source=cpu.A11.value,size=cpu.A9.value,xy=cpu.A10.value,command=cpu.A12.value,palette=cpu.A6.value,
  cursor=cpu.A1.value,row=multipart and row or 0,part=multipart and(row-a.cache)//112 or 0,frame=frame}
 queues[q.cursor]=q
 local value={}
 for _,key in ipairs({'actor','main','owner','parent','pose','cache','bank','body','facing','source','size','xy','command','palette','cursor','row'})do
  value[#value+1]=string.format('%s=%08X',key,q[key])
 end
 for _,key in ipairs({'slot','id','roster','x','y','floor','action','part','kind','multipart'})do value[#value+1]=string.format('%s=%d',key,q[key])end
 value[#value+1]='pc=FF804420'
 log('FLOOR_QUEUE',table.concat(value,' '))
 if not multipart then
  local raw={};for offset=0,0x200,0x10 do raw[#raw+1]=string.format('%04X',p:read_u16(a.actor+offset))end
  log('FLOOR_SINGLE',string.format('cursor=%08X slot=%d actor=%08X pose=%08X words=%s',q.cursor,slot,a.actor,a.pose,table.concat(raw,',')))
  local hex={};for offset=0,31 do hex[#hex+1]=string.format('%02X',p:read_u8(a.cache+offset*8))end
  log('FLOOR_SINGLE_DESCRIPTOR',string.format('cursor=%08X slot=%d actor=%08X descriptor=%08X bytes=32 data=%s',q.cursor,slot,a.actor,a.cache,table.concat(hex)))
 end
 for i=0,multipart and 11 or -1 do
  local ptr=a.cache+i*112;local source=p:read_u32(ptr);if source==0 then break end
  log('FLOOR_QUEUE_PART',string.format('cursor=%08X slot=%d part=%d source=%08X width=%d height=%d command=%04X dx=%d dy=%d',
   q.cursor,slot,i,source,p:read_u16(ptr+0x20),p:read_u16(ptr+0x30),p:read_u16(ptr+0x40),p:read_i16(ptr+0x50),p:read_i16(ptr+0x60)))
 end
end)
for _,address in ipairs({0xfffaae00,0xfffab200})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'first actual individual fatality display window',function(at)
  local a=actor(side)
  if not origin and at==address and cpu.PC.value==address+16 and a and a.owner==a.actor and
     cpu.A8.value==a.actor and cpu.A13.value==a.main and(a.id==17 or a.id==18)then
   origin=frame;log('FLOOR_BEGIN',string.format('epoch=1 origin=%d id=%d entry=%08X actor=%08X main=%08X',origin,a.id,address,a.actor,a.main))
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
 if pre_frame~=frame and sampled(frame+1)then
  pre_frame=frame;local file=string.format('display_pre_%d.bin',frame)
  save(file,vram:read_block(0,512*512*2))
  log('FLOOR_PRE_FRAME',string.format('epoch=1 event=%d file=%s phase=before_first_frame_dma',next_event(),file))
 end
 local e=next_event();local command=regs[1]
 local source=regs[2]|(regs[3]<<16);local pal=regs[8]&0x7f00
 local w,h=regs[6]&0x3ff,regs[7]&0x3ff;local slot=0
 local b14=cpu.B14.value
 local q=queues[b14+192]
 log('FLOOR_DMA_REGS',string.format('event=%d b14=%08X a0=%08X a1=%08X a3=%08X a7=%08X b10=%08X source=%08X command=%04X',
  e,b14,cpu.A0.value,cpu.A1.value,cpu.A3.value,cpu.A7.value,cpu.B10.value,source,command))
 if q and command&15==2 and q.source==source then
  slot=q.slot
  log('FLOOR_QUEUE_DISPATCH',string.format('event=%d cursor=%08X queue_frame=%d slot=%d actor=%08X main=%08X source=%08X',
   e,q.cursor,q.frame,slot,q.actor,q.main,source))
 end
 for n=1,2 do
  local a=actor(n)
  if a and a.owner==a.actor and a.bank&0x7f00==pal then
   -- Palette observation is not authoritative body ownership: native effects
   -- can share this bank. Only the exact original FIFO cursor identifies it.
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
 if not active()then return end
 local a1,a2=p:read_u32(0x01060220),p:read_u32(0x01060df0)
 log('FLOOR_STATE',string.format('mode=%d p1=%08X p2=%08X main1=%08X main2=%08X roster1=%d roster2=%d state1=%d state2=%d winner=%d health1=%d health2=%d',
 p:read_u16(0x010601d0),a1,a2,p:read_u32(0x01060260),p:read_u32(0x01060e30),p:read_u16(0x01060280),p:read_u16(0x01060e50),p:read_u16(0x010601f0),p:read_u16(0x01060dc0),p:read_u16(0x01061b00),p:read_u16(0x010602f0),p:read_u16(0x01060ec0)))
 if a1==0 and a2==0 and not retired.frame then
  retired.frame=frame;log('FLOOR_RETIRED',string.format('mode=%d p1=%08X p2=%08X winner=%d victim_health=%d',p:read_u16(0x010601d0),a1,a2,p:read_u16(0x01061b00),p:read_u16(side==1 and 0x01060ec0 or 0x010602f0)))
 end
 if not sampled(frame)then return end
 local modeled=latch and latch.frame==frame and pre_frame==frame-1
 snaps=snaps+1
 local file=string.format('display_%d.png',frame);screen:snapshot(file)
 local vfile=string.format('display_vram_%d.bin',frame)
 save(vfile,modeled and latch.raw or vram:read_block(0,512*512*2))
 local colors={};for pen=0,32767 do colors[#colors+1]=string.pack('<I4',palette:pen_color(pen)&0xffffff)end
 local pfile=string.format('display_palette_%d.bin',frame);save(pfile,table.concat(colors))
 log('FLOOR_DISPLAY',string.format('epoch=1 start=%04X control=%04X tap=%04X palette_file=%s',p:read_u16(0xc0000090),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),pfile))
 if modeled then
  log('FLOOR_LATCH',string.format('epoch=1 event=%d snapshot=%d flip_frame=%d start=%04X control=%04X tap=%04X file=%s',latch.event,frame,latch.frame,latch.start,latch.control,latch.tap,vfile))
 else
  log('FLOOR_HELD',string.format('epoch=1 event=%d snapshot=%d last_flip=%d pre_frame=%d start=%04X control=%04X tap=%04X file=%s reason=no_current_flip_or_prior_DMA',next_event(),frame,latch and latch.frame or -1,pre_frame,p:read_u16(0xc0000090),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),vfile))
 end
 log('FLOOR_SNAP',string.format('epoch=1 selection=1 arena=%d origin=%d age=%d phase=frame_done file=%s',p:read_u16(0x01061ac0),origin,frame-origin,file))
end)
emu.register_stop(function()
 log('FLOOR_RESULT',string.format('origin=%d snapshots=%d schema=1 scope=sampled_actual_individual_fatality_display_not_all_finishers_victims_or_audio',origin or -1,snaps))
 for _,tap in ipairs(taps)do tap:remove()end
end)
