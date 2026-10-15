-- Cold two-human selection, real mobility inputs, read-only presentation data.
local fighter = assert(os.getenv('MK2KS_GROUND_FIGHTER'))
local side = assert(tonumber(os.getenv('MK2KS_GROUND_SIDE')))
local boot = tonumber(os.getenv('MK2KS_GROUND_BOOT') or '604')
local ids = {kano=17, sonya=18, sub_zero=8, kitana=4}
assert(ids[fighter] and fighter~='kitana' and (side==1 or side==2))
local names = side==1 and {fighter,'kitana'} or {'kitana',fighter}
local routes = {
 {kano={'Left'},sonya={'Right','Right','Right','Right'},sub_zero={'Down'},kitana={'Right','Right','Down'}},
 {kano={'Left','Left','Left','Left'},sonya={'Right'},sub_zero={'Left','Left','Left','Down'},kitana={'Left','Down'}}}
local slots = {{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local p = manager.machine.devices[':maincpu'].spaces.program
local cpu = manager.machine.devices[':maincpu'].state
local screen = manager.machine.screens[':screen']
local gfx = manager.machine.memory.regions[':gfxrom']
local palette = manager.machine.palettes[':palette']
local high,system = manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local fields = {{},{}}
for n=1,2 do
 for _,button in ipairs({'High Punch','Left','Right','Up','Down'}) do fields[n][button]=high['P'..n..' '..button] end
 fields[n].Coin=system['Coin '..n]
 fields[n].Start=system[n==1 and '1 Player Start' or '2 Players Start']
end
local frame,css,live,ready = 0,nil,nil,nil
local dma_event=0
local regs,taps,emitted = {},{},{}
local pending=nil
local pre_frame=-1
local vram,dma_item=nil,nil
for _,device in pairs(manager.machine.devices)do
 for name,index in pairs(device.items)do
  if name:match('m_local_videoram$')then vram=emu.item(index)end
  if name:match('m_dma_register$')then dma_item=emu.item(index)end
 end
end
assert(vram and dma_item and vram.size==2 and vram.count>=512*512,'Actual native video items')
local output=assert(os.getenv('MK2KS_GROUND_OUT'))
local latch=nil
local function valid(a) return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 print(string.format('MK2_GROUND_%s frame=%d fighter=%s side=%d writes=0 assistance=none %s',tag,frame,fighter,side,value or ''))
end
local function pulse(n,button,age,first,hold)
 if age>=first and age<first+(hold or 4) then
  fields[n][button]:set_value(1)
  log('INPUT',string.format('slot=%d button=%s age=%d',n,button:gsub(' ','_'),age))
 end
end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a) or not valid(m) then return nil end
 return {actor=a,main=m,id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),state=p:read_u16(s.state),
  hp=p:read_u16(s.hp),owner=p:read_u32(m+0xc0),pose=p:read_u32(a+0x1d0),cache=p:read_u32(a+0x1a0),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
  vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),
  action=p:read_u16(m+0x1f0),body=p:read_u16(a+0x160),flags=p:read_u16(m+0x210),
  bank=p:read_u16(a+0x140),facing=p:read_u16(a+0xf0)}
end
local function live_pair(a,b)
 return p:read_u16(0x010601d0)==2 and a and b and a.id==ids[names[1]] and b.id==ids[names[2]]
  and a.roster==a.id and b.roster==b.id and a.state==1 and b.state==1 and a.owner==a.actor and b.owner==b.actor
end
local function clean(a)
 return a.hp==161 and a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0
end
local function capture_age(age)
 return age%8==0 and(age>=16 and age<=96 or age>=128 and age<=192 or age>=248 and age<=312 or
  age>=368 and age<=392 or age>=432 and age<=456 or age==480)
end
local function part(n,a)
 local data={string.format('slot=%d age=%d stage=%d stageY=%d cameraX=%d displayY=%d cameraY=%d',n,frame-ready,p:read_u16(0x01061ac0),p:read_i16(0x0105ecd0),p:read_i16(0x0105d120),p:read_i16(0x0105d060),p:read_i16(0x0105d130))}
 for _,key in ipairs({'actor','main','owner','pose','cache','vx','vy','gravity','body','flags','bank','facing'}) do data[#data+1]=string.format('%s=%08X',key,a[key]) end
 for _,key in ipairs({'id','roster','state','hp','x','y','floor','action'}) do data[#data+1]=string.format('%s=%d',key,a[key]) end
 log('FIELD',table.concat(data,' '))
 if not valid(a.cache) then return end
 for i=0,11 do
  local at=a.cache+i*0x70;local source=p:read_u32(at)
  if source==0 then break end
  log('PART',string.format('slot=%d age=%d part=%d source=%08X width=%d height=%d xoff=%d yoff=%d',
   n,frame-ready,i,source,p:read_u16(at+0x20),p:read_u16(at+0x30),p:read_i16(at+0x50),p:read_i16(at+0x60)))
 end
end
local mapping = {{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'exact idle/mobility display flip',function(at,data,mask)
 if at~=0xc0000090 or not ready or not capture_age(frame-ready)then return end
 latch={frame=frame,start=data&0xffff,control=p:read_u16(0xc0000080),tap=p:read_u16(0xc00001b0),raw=vram:read_block(0,512*512*2)}
end)
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'ground actual DMA observation',function(at,data,mask)
 local bank=((dma_item:read(15) or 0)>>5)&1;local reg=mapping[bank+1][(at-0x01a80000)//16]
 local command=(dma_item:read(reg)&(~mask))|(data&mask)
 if reg~=1 or (command&0x8000)==0 or not ready then return end
 for index=0,17 do regs[index]=dma_item:read(index)end
 regs[reg]=command
 local age=frame-ready
 if pre_frame~=frame and capture_age(age+1)then
  pre_frame=frame
  local file=string.format('pre_%d.bin',frame)
  local dump=assert(io.open(output..'/'..file,'wb'));dump:write(vram:read_block(0,512*512*2));dump:close()
  log('PRE',string.format('age=%d file=%s phase=before_first_dma',age,file))
 end
 local source=(regs[2] or 0)|((regs[3] or 0)<<16)
 local command=regs[1];local color=(regs[9] or 0)&255;local pal=(regs[8] or 0)&0x7f00
 local w,h=(regs[6] or 0)&0x3ff,(regs[7] or 0)&0x3ff
 dma_event=dma_event+1
 log('DMA',string.format('age=%d source=%08X command=%04X palette=%04X color=%d x=%d y=%d width=%d height=%d scaleX=%d scaleY=%d left=%d right=%d top=%d bottom=%d skip=%d pc=%08X',
  age,source,command,pal,color,(regs[4] or 0)&0x3ff,(regs[5] or 0)&0x1ff,w,h,regs[10] or 0,regs[11] or 0,
  regs[16] or 0,regs[17] or 0,regs[12] or 0,regs[13] or 0,regs[0] or 0,cpu.PC.value)..' event='..dma_event)
 if command&15==8 and source>=0x10000000 and source<0x1a000000 then
  local actor,row=cpu.A8.value,cpu.A9.value
  local n=actor==p:read_u32(slots[1].actor)and 1 or actor==p:read_u32(slots[2].actor)and 2 or nil
  assert(n,'Actual native projected actor is one physical fighter')
  local a=assert(sample(n));assert(a.id==ids[names[n]]and a.owner==actor and valid(a.cache))
  local component=(row-a.cache)//0x70;assert(row==a.cache+component*0x70 and component>=0 and component<12)
  local first_source=p:read_u32(row);local fullw,fullh=p:read_u16(row+0x20),p:read_u16(row+0x30)
  local descriptor_command=p:read_u16(row+0x40)
  log('SHADOW_COMPONENT',string.format('event=%d slot=%d id=%d actor=%08X main=%08X owner=%08X cache=%08X row=%08X component=%d first_source=%08X width=%d height=%d command=%04X xoff=%d yoff=%d',
   dma_event,n,a.id,actor,a.main,a.owner,a.cache,row,component,first_source,fullw,fullh,descriptor_command,p:read_i16(row+0x50),p:read_i16(row+0x60)))
  -- Capture the full compressed source independently, even if this cache pose
  -- differs from the body drawn in the same field. This never alters a pose.
  local full_command=descriptor_command|0x8002
  local full_key=string.format('%08X_%04X_%d_%d',first_source,full_command,fullw,fullh)
  if not emitted[full_key]then
   emitted[full_key]=true
   local offset=first_source-0x0a000000;local first=offset//8
   local bytes=math.ceil((offset%8+fullw*fullh*((full_command>>12)&7)+(full_command&0x80~=0 and fullh*8 or 0))/8)+8
   assert(first>=0 and first+bytes<=0x2000000,'Full owned shadow source inside graphics region')
   local dump={};for i=first,first+bytes-1 do dump[#dump+1]=string.format('%02X',gfx:read_u8(i))end
   log('GFX',string.format('key=%s offset=%d first=%d bytes=%d data=%s',full_key,offset,first,bytes,table.concat(dump)))
  end
 end
 if command&15==2 and(pal==0x200 or pal==0x300)then
  local n=pal==0x200 and 1 or 2;local a=sample(n)
  assert(a and a.owner==a.actor,'Actual body ownership')
  log('OWNER',string.format('slot=%d source=%08X actor=%08X owner=%08X id=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X action=%d pose=%08X stageY=%d displayY=%d cameraY=%d',n,source,a.actor,a.owner,a.id,a.y,a.floor,a.vx,a.vy,a.gravity,a.action,a.pose,p:read_i16(0x0105ecd0),p:read_i16(0x0105d060),p:read_i16(0x0105d130)))
 end
 if command&15==2 and source>=0x10000000 and source<0x1a000000 then
  for n=1,2 do
   local a=sample(n)
   if a and valid(a.cache) then
    local sources={}
    for part=0,11 do
     local at=a.cache+part*0x70;local value=p:read_u32(at)
     if value==0 then break end
     sources[#sources+1]=string.format('%08X',value)
    end
    log('DMA_CACHE',string.format('age=%d slot=%d source=%08X actor=%08X main=%08X owner=%08X id=%d cache=%08X sources=%s y=%d floor=%d stageY=%d a8=%08X a13=%08X',
     age,n,source,a.actor,a.main,a.owner,a.id,a.cache,table.concat(sources,','),a.y,a.floor,p:read_i16(0x0105ecd0),cpu.A8.value,cpu.A13.value)..string.format(' cameraXY=%08X worldXY=%08X world2=%08X',p:read_u32(0x0105d050),p:read_u32(0x0105d120),p:read_u32(0x0105d140)))
   end
  end
 end
 local key=string.format('%08X_%04X_%d_%d',source,command,w,h)
 if emitted[key] or w==0 or h==0 or command&15==12 then return end
 emitted[key]=true
 local offset=source
 if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000 end
 if offset>=0xf8000000 then offset=offset-0xf8000000 end
 local first=offset//8
 local bytes=math.ceil((offset%8+w*h*((command>>12)&7)+(command&0x80~=0 and h*8 or 0))/8)+8
 assert(first>=0 and first<0x2000000,'Actual stock/imported graphics bounds')
 bytes=math.min(bytes,0x2000000-first)
 local dump={}
 for i=first,first+bytes-1 do dump[#dump+1]=string.format('%02X',gfx:read_u8(i)) end
 log('GFX',string.format('key=%s offset=%d first=%d bytes=%d data=%s',key,offset,first,bytes,table.concat(dump)))
end)
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(fields[n]) do field:clear_value() end end
 if frame>=300 and frame<304 then fields[1]['High Punch']:set_value(1) end
 local pixels,width=screen:pixels();assert(width==400 and #pixels>=400*254*4)
 local yellow,early=0,0
 for y=0,24,2 do for x=40,360,2 do
  local c=string.unpack('<I4',pixels,(y*width+x)*4+1);local r,g,b=(c>>16)&255,(c>>8)&255,c&255
  if r>175 and g>140 and b<100 then yellow=yellow+1;if y==4 then early=early+1 end end
 end end
 if not css and frame>=boot then local age=(frame-boot)%300;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(1,'Start',age,20) end
 if not css and frame>700 and yellow>=400 and yellow<=430 and early>=10 then css=frame;log('CSS','yellow='..yellow..' early='..early) end
 if css and not live then
  local age=frame-css;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(2,'Start',age,20)
  for n=1,2 do
   for i,direction in ipairs(routes[n][names[n]]) do pulse(n,direction,age,n==1 and (12+(i-1)*12) or (132+(i-1)*16)) end
   pulse(n,'High Punch',age,n==1 and 96 or 220,8)
  end
 end
 local a,b=sample(1),sample(2)
 if not live and frame>1200 and live_pair(a,b) then live=frame;log('LIVE') end
 if live and not ready and frame%30==0 and a and b then
  log('WAIT',string.format('mode=%d aID=%d bID=%d aHP=%d bHP=%d aY=%d bY=%d aFloor=%d bFloor=%d aVX=%08X bVX=%08X aVY=%08X bVY=%08X aGravity=%08X bGravity=%08X aAction=%d bAction=%d aFlags=%04X bFlags=%04X',p:read_u16(0x010601d0),a.id,b.id,a.hp,b.hp,a.y,b.y,a.floor,b.floor,a.vx,b.vx,a.vy,b.vy,a.gravity,b.gravity,a.action,b.action,a.flags,b.flags))
 end
 if live and not ready and frame>=live+180 and live_pair(a,b) and clean(a) and clean(b) then
  ready=frame;log('READY')
  for _,bank in ipairs({0,0x200,0x300}) do
   local colors={};for pen=0,63 do colors[#colors+1]=string.format('%06X',palette:pen_color(bank+pen)&0xffffff) end
   log('PALETTE',string.format('bank=%04X colors=%s',bank,table.concat(colors,',')))
  end
 end
 if ready then
  local age=frame-ready
  pulse(side,'Up',age,120,3);pulse(3-side,'Up',age,240,3)
  pulse(1,'Down',age,360,24);pulse(2,'Down',age,360,24)
  pulse(1,'Right',age,420,12);pulse(2,'Left',age,420,12)
  if live_pair(a,b) then part(1,a);part(2,b) else log('INVALID','age='..age) end
  if capture_age(age) then pending=age end
  if age>=480 then manager.machine:exit() end
 end
end)
emu.register_frame_done(function()
 if not pending then return end
 assert(latch and latch.frame==frame,'Exactly current native display latch, no best-buffer selection')
 local file=string.format('ground_%04d.png',frame);screen:snapshot(file)
 local vram_file=string.format('vram_%d.bin',frame)
 local dump=assert(io.open(output..'/'..vram_file,'wb'));dump:write(latch.raw);dump:close()
 local colors={};for pen=0,32767 do colors[#colors+1]=string.pack('<I4',palette:pen_color(pen)&0xffffff)end
 local palette_file=string.format('palette_%d.bin',frame)
 dump=assert(io.open(output..'/'..palette_file,'wb'));dump:write(table.concat(colors));dump:close()
 log('SNAP',string.format('age=%d file=%s vram_file=%s palette_file=%s flip_frame=%d start=%04X control=%04X tap=%04X phase=frame_done',pending,file,vram_file,palette_file,latch.frame,latch.start,latch.control,latch.tap))
 pending=nil
end)
emu.register_stop(function()
 log('RESULT',string.format('css=%d live=%d ready=%d terminalAge=%d scope=two_human_ground_jump_crouch_walk_not_all_arenas',css or -1,live or -1,ready or -1,ready and frame-ready or -1))
 for _,tap in ipairs(taps) do tap:remove() end
end)
