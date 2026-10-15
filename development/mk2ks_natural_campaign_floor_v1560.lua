-- Cold campaign, genuine losses/paid continues. Inputs only, no guest writes.
if rawget(_G,'MK2_NATURAL_CAMPAIGN_ACTIVE')then
 print('MK2_NAT_CAMPAIGN_REENTRY duplicate_callbacks_prevented=true writes=0 assistance=none')
 return
end
rawset(_G,'MK2_NATURAL_CAMPAIGN_ACTIVE',true)
for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_CPU_HEALTH',
 'MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_P1_REGEN','MK2_P2_TOWER_HEALTH_ASSIST'})do
 assert(not os.getenv(key),'No campaign assistance: '..key)
end
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local identity=assert(({kano=17,sonya=18})[fighter])
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
assert(side==1 or side==2)
local opponent=3-side
local boot=tonumber(os.getenv('MK2KS_TEST_BOOT_FRAME')or'600')
local strategy=os.getenv('MK2KS_CAMPAIGN_STRATEGY')or'uppercut'
assert(strategy=='uppercut' or strategy=='jumpkick' or strategy=='reactive' or strategy=='zoning'or strategy=='leg'or strategy=='defensive_leg'or strategy=='lowkick'or strategy=='throw')
local leg_tactic=strategy=='leg'or strategy=='defensive_leg'
assert(not leg_tactic or fighter=='sonya','Leg tactic is Sonya only')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local high,system,low=manager.machine.ioport.ports[':IN0'].fields,
 manager.machine.ioport.ports[':IN1'].fields,manager.machine.ioport.ports[':IN2'].fields
local buttons={}
for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[key]=high['P'..side..' '..key]end
buttons['Low Punch']=low['P'..side..' Low Punch'];buttons['Low Kick']=low['P'..side..' Low Kick']
buttons.Coin=system['Coin '..side];buttons.Start=system[side==1 and '1 Player Start' or '2 Players Start']
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,selections,losses,wins,live_fields=0,0,0,0,0
local css,css_exit,loss_at,plan=nil,nil,nil,nil
local last_state,first_live,last_fight,ending=nil,nil,nil,nil
local seen,taps={},{}
local jump_start,last_jump,last_uppercut=nil,-1000,-1000
local previous_y=nil
local projectile_start,projectile_direction=nil,nil
local close_start,last_close=nil,-1000
local guard_until=-1000
local stage_wins,picture_reads,text_reads={},{0,0},{0,0}
local ending_completed=nil
local pending_pages,id_taps={},{}
local function log(tag,value)
 print(string.format('MK2_NAT_CAMPAIGN_%s frame=%d human_slot=%d fighter=%s writes=0 assistance=none %s',tag,frame,side,fighter,value or''))
end
-- Native ending/table/store observers only. The ending is entered only after
-- actual owned boss victories and the original native actor retirement.
for page=0,1 do
 local entry=0xff800000+0xf4900*8+(50+(identity-17)*2+page)*32
 taps[#taps+1]=p:install_read_tap(entry,entry+31,'own native ending picture',function(at,data,mask)
  if at~=entry or not first_live or p:read_u16(0x01061b30)~=16 or
   p:read_u16(slots[side].roster)~=identity or p:read_u16(0x01061b00)~=side then return end
  picture_reads[page+1]=picture_reads[page+1]+1
  log('PICTURE',string.format('page=%d entry=%08X value=%04X mask=%04X pc=%08X roster=%d',page+1,at,data&0xffff,mask,cpu.PC.value,p:read_u16(slots[side].roster)))
  pending_pages[frame+60]='ending_page'..(page+1)..'_'..frame
  pending_pages[frame+180]='ending_page'..(page+1)..'_late_'..frame
 end)
 local table_base=0xff800000+(page==0 and 0xf4a00 or 0xf4b00)*8
 local first=table_base+identity*3*32
 taps[#taps+1]=p:install_read_tap(first,first+3*32-1,'own native ending text',function(at,data,mask)
  if(at-first)%32~=0 or not first_live or p:read_u16(0x01061b30)~=16 or
   p:read_u16(slots[side].roster)~=identity or p:read_u16(0x01061b00)~=side then return end
  text_reads[page+1]=text_reads[page+1]+1
  log('TEXT',string.format('page=%d segment=%d entry=%08X value=%04X mask=%04X pc=%08X roster=%d',page+1,(at-first)//32,at,data&0xffff,mask,cpu.PC.value,p:read_u16(slots[side].roster)))
 end)
end
emu.register_frame_done(function()
 if pending_pages[frame]then
  screen:snapshot(pending_pages[frame]..'.png')
  log('PAGE_SNAP','file='..pending_pages[frame]..'.png');pending_pages[frame]=nil
 end
end)
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a) or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),
  state=p:read_u16(s.state),hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),
  floor=p:read_i16(m+0x200),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),
  body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140),action=p:read_u16(m+0x1f0)}
end
-- Read-only native drawing observer, layered over the byte-exact v850 input policy.
local floor_origin,floor_pending=nil,nil
local floor_epoch,floor_snaps=0,0
local floor_queues={}
local function floor_actor(n)
 local a=sample(n);if not a then return end
 a.cache=p:read_u32(a.actor+0x1a0);a.facing=p:read_u16(a.actor+0xf0)
 return a
end
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'original body FIFO publication',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 or not floor_origin or frame-floor_origin<208 or frame-floor_origin>344 then return end
 local slot=0
 for n=1,2 do local a=floor_actor(n);if a and a.actor==cpu.A0.value then slot=n end end
 if slot==0 then return end
 local a=floor_actor(slot);local row=cpu.A3.value-112
 assert(row>=a.cache and row<a.cache+12*112 and(row-a.cache)%112==0,'Original current cache iterator')
 local q={slot=slot,actor=a.actor,main=a.main,owner=a.owner,id=a.id,roster=a.roster,pose=a.pose,cache=a.cache,
  bank=a.bank,body=a.body,facing=a.facing,x=a.x,y=a.y,floor=a.floor,action=a.action,
  source=cpu.A11.value,size=cpu.A9.value,xy=cpu.A10.value,command=cpu.A12.value,palette=cpu.A6.value,
  cursor=cpu.A1.value,row=row,part=(row-a.cache)//112,frame=frame}
 floor_queues[q.cursor]=q
 local value={}
 for _,key in ipairs({'actor','main','owner','pose','cache','bank','body','facing','source','size','xy','command','palette','cursor','row'})do
  value[#value+1]=string.format('%s=%08X',key,q[key])
 end
 for _,key in ipairs({'slot','id','roster','x','y','floor','action','part'})do value[#value+1]=string.format('%s=%d',key,q[key])end
 value[#value+1]='pc=FF804420'
 log('FLOOR_QUEUE',table.concat(value,' '))
 for i=0,11 do
  local ptr=a.cache+i*112;local source=p:read_u32(ptr);if source==0 then break end
  log('FLOOR_QUEUE_PART',string.format('cursor=%08X slot=%d part=%d source=%08X width=%d height=%d command=%04X dx=%d dy=%d',
   q.cursor,slot,i,source,p:read_u16(ptr+0x20),p:read_u16(ptr+0x30),p:read_u16(ptr+0x40),p:read_i16(ptr+0x50),p:read_i16(ptr+0x60)))
 end
end)
local floor_regs,floor_gfx,floor_palettes={},{},{}
local floor_palette_count=0
local floor_mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local floor_region=manager.machine.memory.regions[':gfxrom']
local floor_palette=manager.machine.palettes[':palette']
local floor_vram,floor_video_bank,floor_dma_item=nil,nil,nil
for tag,device in pairs(manager.machine.devices)do
 for name,index in pairs(device.items)do
  if name:match('m_local_videoram$')then
   assert(not floor_vram,'One actual T-unit VRAM item')
   floor_vram=emu.item(index)
  end
  if name:match('m_videobank_select$')then floor_video_bank=emu.item(index)end
  if name:match('m_dma_register$')then floor_dma_item=emu.item(index)end
 end
end
assert(floor_vram and floor_vram.size==2 and floor_vram.count>=512*512,'Actual read-only T-unit VRAM item')
assert(floor_video_bank and floor_dma_item and floor_dma_item.count>=18,'Actual native CPU VRAM write controls')
local floor_output=assert(os.getenv('MK2KS_FLOOR_OUT'))
local floor_latches={}
local shadow_row_reads=0
taps[#taps+1]=p:install_read_tap(0x12000000,0x1bffffff,'actual native imported shadow row scan',function(at,data,mask)
 if not floor_origin or frame-floor_origin<208 or frame-floor_origin>344 or cpu.PC.value~=0xff8016a0 then return end
 shadow_row_reads=shadow_row_reads+1
 if shadow_row_reads>500 then return end
 log('SHADOW_ROW_READ',string.format('ordinal=%d at=%08X value=%04X mask=%04X pc=%08X source=%08X cache=%08X width=%d pre_shift=%d post_shift=%d command=%04X',shadow_row_reads,at,data,mask,cpu.PC.value,cpu.A10.value,cpu.A9.value,cpu.A11.value,cpu.A4.value,cpu.A1.value,cpu.A14.value))
end)
local floor_event,floor_base_epoch,floor_pre_frame=0,0,-1
local function floor_next()
 floor_event=floor_event+1
 return floor_event
end
local function floor_base()
 if floor_base_epoch==floor_epoch then return end
 floor_base_epoch=floor_epoch
 local file=string.format('floor_base_epoch%d_%d.bin',floor_epoch,frame)
 local raw=floor_vram:read_block(0,512*512*2)
 local dump=assert(io.open(floor_output..'/'..file,'wb'));dump:write(raw);dump:close()
 log('FLOOR_BASE',string.format('epoch=%d event=%d file=%s bytes=%d phase=before_first_observed_write',floor_epoch,floor_event,file,#raw))
end
-- Original CPU writes can erase a component after a queued DMA copy. Observe
-- them with the actual native video-bank and full palette register; no writes
-- to RAM, save items or device state are supplied by this diagnostic.
taps[#taps+1]=p:install_write_tap(0x00000000,0x001fffff,'actual native CPU VRAM write provenance',function(at,data,mask)
 if not floor_origin or frame-floor_origin<208 or frame-floor_origin>344 then return end
 floor_base()
 local index=(at//16)*2
 assert(index>=0 and index+1<512*512,'Visible native VRAM write bounds')
 log('FLOOR_CPU',string.format('epoch=%d event=%d at=%08X value=%04X mask=%04X video_bank=%d palette=%04X index=%d before0=%04X before1=%04X pc=%08X',floor_epoch,floor_next(),at,data,mask,floor_video_bank:read(0),floor_dma_item:read(8),index,floor_vram:read(index),floor_vram:read(index+1),cpu.PC.value))
end)
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'actual TMS display start provenance',function(at,data,mask)
 if at~=0xc0000090 or not floor_origin or frame-floor_origin<208 or frame-floor_origin>344 then return end
 local latch={frame=frame,event=floor_next(),start=data&0xffff,control=p:read_u16(0xc0000080),tap=p:read_u16(0xc00001b0),raw=floor_vram:read_block(0,512*512*2)}
 floor_latches[#floor_latches+1]=latch
 if #floor_latches>4 then table.remove(floor_latches,1)end
 log('FLOOR_FLIP',string.format('epoch=%d event=%d time=%.9f at=%08X value=%04X mask=%04X control=%04X tap=%04X pc=%08X',floor_epoch,latch.event,emu.time(),at,latch.start,mask,latch.control,latch.tap,cpu.PC.value))
end)
local function observe_floor_gfx(source,command,w,h)
 if command&15==12 or w==0 or h==0 then return end
 local key=string.format('%08X_%04X_%d_%d',source,command,w,h)
 if floor_gfx[key]then return end
 local offset=source
 if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000 end
 if offset>=0xf8000000 then offset=offset-0xf8000000 end
 local bits=(command>>12)&7;if bits==0 then bits=8 end
 local first=offset//8
 local count=math.ceil((offset%8+w*h*bits+(command&0x80~=0 and h*8 or 0))/8)+8
 assert(first>=0 and first<0x2000000,'Bounded actual graphics observation')
 count=math.min(count,0x2000000-first)
 local hex={};for i=first,first+count-1 do hex[#hex+1]=string.format('%02X',floor_region:read_u8(i))end
 log('FLOOR_GFX',string.format('key=%s offset=%d first=%d bytes=%d data=%s',key,offset,first,count,table.concat(hex)))
 floor_gfx[key]=true
end
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'natural arena read-only floor DMA',function(at,data,mask)
 local bank=((floor_dma_item:read(15)or 0)>>5)&1
 local reg=floor_mapping[bank+1][(at-0x01a80000)//16]
 local before=floor_dma_item:read(reg)
 local merged=(before&(~mask))|(data&mask)
 floor_regs[reg]=((floor_regs[reg]or 0)&(~mask))|(data&mask)
 if reg~=1 or not floor_origin then return end
 local age=frame-floor_origin
 if age<208 or age>344 then return end
 log('FLOOR_COMMAND',string.format('epoch=%d at=%08X value=%04X mask=%04X before=%04X after=%04X pc=%08X',floor_epoch,at,data,mask,before,merged,cpu.PC.value))
 if merged&0x8000==0 then return end
 -- Use the actual register state. DMA completion clears its busy/start bit
 -- independently of CPU writes, so a local write-only mirror is insufficient.
 for index=0,17 do floor_regs[index]=floor_dma_item:read(index)end
 floor_regs[reg]=merged
 floor_base()
 -- Every fixed screenshot displays the preceding field's completed pass.
 -- Save that pass's initial VRAM, not 137 unneeded full buffers per arena.
 if floor_pre_frame~=frame and frame%8==7 then
  floor_pre_frame=frame
  local file=string.format('floor_pre_frame_%d.bin',frame)
  local raw=floor_vram:read_block(0,512*512*2)
  local dump=assert(io.open(floor_output..'/'..file,'wb'));dump:write(raw);dump:close()
  log('FLOOR_PRE_FRAME',string.format('epoch=%d event=%d file=%s bytes=%d phase=before_first_frame_dma',floor_epoch,floor_next(),file,#raw))
 end
 local event=floor_next()
 local command=floor_regs[1];local source=(floor_regs[2]or 0)|((floor_regs[3]or 0)<<16)
 local pal=(floor_regs[8]or 0)&0x7f00;local colors={}
 for pen=0,255 do colors[#colors+1]=string.format('%06X',floor_palette:pen_color(pal+pen)&0xffffff)end
 local palette_key=string.format('%04X_%s',pal,table.concat(colors,','))
 if not floor_palettes[palette_key]then
  floor_palette_count=floor_palette_count+1;floor_palettes[palette_key]=floor_palette_count
  log('FLOOR_PALETTE',string.format('ref=%d bank=%04X colors=%s',floor_palette_count,pal,table.concat(colors,',')))
 end
 local w,h=(floor_regs[6]or 0)&0x3ff,(floor_regs[7]or 0)&0x3ff
 local owner_slot=0
 local q=floor_queues[cpu.B14.value+192]
 if q and command&15==2 and q.source==source then owner_slot=q.slot end
 for n=1,2 do
  local a=sample(n)
  if a and a.owner==a.actor and owner_slot==n then
   log('FLOOR_OWNER',string.format('epoch=%d event=%d source=%08X slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d cache=%08X pose=%08X bank=%04X body=%04X facing=%04X x=%d y=%d floor=%d action=%d stageY=%d displayY=%d cameraY=%d',floor_epoch,event,source,n,a.actor,a.main,a.owner,a.id,a.roster,p:read_u32(a.actor+0x1a0),a.pose,a.bank,a.body,p:read_u16(a.actor+0xf0),a.x,a.y,a.floor,a.action,p:read_i16(0x0105ecd0),p:read_i16(0x0105d060),p:read_i16(0x0105d130)))
   log('FLOOR_QUEUE_DISPATCH',string.format('event=%d cursor=%08X queue_frame=%d slot=%d actor=%08X main=%08X source=%08X',event,q.cursor,q.frame,n,q.actor,q.main,source))
  end
 end
 log('FLOOR_DMA_REGS',string.format('event=%d b14=%08X a0=%08X a1=%08X a3=%08X a7=%08X b10=%08X source=%08X command=%04X',event,cpu.B14.value,cpu.A0.value,cpu.A1.value,cpu.A3.value,cpu.A7.value,cpu.B10.value,source,command))
 log('FLOOR_DMA',string.format('epoch=%d event=%d selection=%d arena=%d mode=%d source=%08X command=%04X palette=%04X palref=%d slot=%d color=%d x=%d y=%d width=%d height=%d scaleX=%d scaleY=%d left=%d right=%d top=%d bottom=%d skip=%d pc=%08X',floor_epoch,event,selections,p:read_u16(0x01061ac0),p:read_u16(0x010601d0),source,command,pal,floor_palettes[palette_key],owner_slot,(floor_regs[9]or 0)&255,(floor_regs[4]or 0)&0x3ff,(floor_regs[5]or 0)&0x1ff,w,h,floor_regs[10]or 0,floor_regs[11]or 0,floor_regs[16]or 0,floor_regs[17]or 0,floor_regs[12]or 0,floor_regs[13]or 0,floor_regs[0]or 0,cpu.PC.value))
 -- v635 lets the original row engine read and project the real imported rows.
 -- Retain the actual cached component and owned actor for each shadow copy.
 if source>=0x10000000 and source<0x1a000000 and command&15==8 then
  local row=cpu.A9.value
  for n=1,2 do
   local a=sample(n)
   if a and a.owner==a.actor then
    local cache=p:read_u32(a.actor+0x1a0)
    if row>=cache and row<cache+112*12 and(row-cache)%112==0 then
     log('SHADOW_COMPONENT',string.format('event=%d slot=%d actor=%08X main=%08X owner=%08X id=%d row=%08X cache=%08X component=%d first_source=%08X width=%d height=%d xoff=%d yoff=%d command=%04X x=%d y=%d floor=%d stageY=%d displayY=%d cameraY=%d',event,n,a.actor,a.main,a.owner,a.id,row,cache,(row-cache)//112,p:read_u32(row),p:read_u16(row+0x20),p:read_u16(row+0x30),p:read_i16(row+0x50),p:read_i16(row+0x60),p:read_u16(row+0x40),a.x,a.y,a.floor,p:read_i16(0x0105ecd0),p:read_i16(0x0105d060),p:read_i16(0x0105d130)))
     -- Observe the entire original component now, even if the body copy falls
     -- just beyond this fixed window. This only reads the graphics region.
     observe_floor_gfx(p:read_u32(row),p:read_u16(row+0x40)|0x8002,p:read_u16(row+0x20),p:read_u16(row+0x30))
    end
   end
  end
 end
 if command&15==12 or w==0 or h==0 then return end
 local key=string.format('%08X_%04X_%d_%d',source,command,w,h)
 if floor_gfx[key]then return end
 local offset=source
 if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000 end
 if offset>=0xf8000000 then offset=offset-0xf8000000 end
 local bits=(command>>12)&7;if bits==0 then bits=8 end
 local first=offset//8
 local count=math.ceil((offset%8+w*h*bits+(command&0x80~=0 and h*8 or 0))/8)+8
 assert(first>=0 and first<0x2000000,'Bounded actual graphics observation')
 -- A stock transparent shadow row can point to the last graphics bytes.
 -- The raw upper-bound estimate includes decoding padding, not bytes that
 -- the native skip header necessarily consumes. Retain only real ROM bytes;
 -- the independent decoder still rejects actual exhaustion.
 count=math.min(count,0x2000000-first)
 local dump={};for i=first,first+count-1 do dump[#dump+1]=string.format('%02X',floor_region:read_u8(i))end
 log('FLOOR_GFX',string.format('key=%s offset=%d first=%d bytes=%d data=%s',key,offset,first,count,table.concat(dump)))
 floor_gfx[key]=true
end)
emu.register_frame_done(function()
 if not floor_pending then return end
 floor_snaps=floor_snaps+1
 local file=string.format('floor_epoch%d_%d.png',floor_epoch,frame)
 screen:snapshot(file)
 local colors={};for pen=0,32767 do colors[#colors+1]=string.pack('<I4',floor_palette:pen_color(pen)&0xffffff)end
 local palette_file=string.format('floor_palette_%d.bin',frame)
 local palette_dump=assert(io.open(floor_output..'/'..palette_file,'wb'))
 palette_dump:write(table.concat(colors));palette_dump:close()
 log('FLOOR_DISPLAY',string.format('epoch=%d time=%.9f start=%04X address=%04X control=%04X tap=%04X palette_file=%s',floor_epoch,emu.time(),p:read_u16(0xc0000090),p:read_u16(0xc00001e0),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),palette_file))
 for index=math.max(1,#floor_latches-1),#floor_latches do
  local latch=floor_latches[index]
  local latch_file=string.format('floor_vram_snap%d_flip%d_%d.bin',frame,latch.frame,index)
  local dump=assert(io.open(floor_output..'/'..latch_file,'wb'));dump:write(latch.raw);dump:close()
  log('FLOOR_LATCH',string.format('epoch=%d event=%d snapshot=%d flip_frame=%d start=%04X control=%04X tap=%04X file=%s bytes=%d',floor_epoch,latch.event,frame,latch.frame,latch.start,latch.control,latch.tap,latch_file,#latch.raw))
 end
 log('FLOOR_SNAP',string.format('epoch=%d selection=%d arena=%d origin=%d age=%d phase=frame_done file=%s',floor_epoch,selections,p:read_u16(0x01061ac0),floor_origin,frame-floor_origin,file))
 floor_pending=nil
end)

local adjacency={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
local function route(start)
 local queue={{start,{}}};local visited={[start]=true};local cursor=1
 while queue[cursor]do
  local current=queue[cursor];cursor=cursor+1
  if current[1]==identity then return current[2]end
  for _,button in ipairs({'Left','Right','Down'})do
   local next_id=p:read_u16(adjacency[button]+current[1]*16)
   if next_id<=18 and not visited[next_id]then
    local steps={};for _,step in ipairs(current[2])do steps[#steps+1]=step end
    steps[#steps+1]=button;queue[#queue+1]={next_id,steps};visited[next_id]=true
   end
  end
 end
 error('No native selection route to actual character')
end
local function press(button)
 buttons[button]:set_value(1)
 log('INPUT','button='..button:gsub(' ','_')..' selection='..selections)
end
-- Observe actual own special entries independently of intended button plans.
-- Same cold campaign, no actor/health/difficulty/ladder assistance.
local own_moves=fighter=='kano'and{{'knife',0xffffb000},{'ball',0xffffde00},{'blade',0xfff8cc00},{'choke',0xfff91400}}
 or{{'ring',0xffffb400},{'square',0xffffca00},{'bicycle',0xfff9a400},{'leg',0xfff80800}}
for _,move in ipairs(own_moves)do
local move_name,move_entry=move[1],move[2]
taps[#taps+1]=p:install_read_tap(move_entry+16,move_entry+31,'owned natural special '..move_name,function(at)
 if at~=move_entry+16 or not first_live then return end
 local a,m=p:read_u32(slots[side].actor),p:read_u32(slots[side].main)
 if not valid(a)or not valid(m)or cpu.A8.value~=a or cpu.A13.value~=m or
  p:read_u16(a+0x1f0)~=identity or p:read_u16(slots[side].roster)~=identity then return end
 log('SPECIAL',string.format('move=%s entry=%08X at=%08X pc=%08X actor=%08X main=%08X a8=%08X a13=%08X id=%d roster=%d stage=%d',
  move_name,move_entry,at,cpu.PC.value,a,m,cpu.A8.value,cpu.A13.value,
  p:read_u16(a+0x1f0),p:read_u16(slots[side].roster),p:read_u16(0x01061b30)))
end)
end
for n,slot in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'natural campaign native health '..n,function(at,data,mask)
  if mask==0xffff and first_live then
   log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d pc=%08X a8=%08X a13=%08X',n,at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value))
  end
 end)
end
taps[#taps+1]=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,'natural campaign native winner',function(at)
 if not first_live or (at-0xfffef800)%32~=0 then return end
 local winner=p:read_u16(0x01061b00)
 if winner~=1 and winner~=2 then return end
 wins=wins+1
 if winner==side then stage_wins[p:read_u16(0x01061b30)]=(stage_wins[p:read_u16(0x01061b30)]or 0)+1 end
 log('WIN',string.format('slot=%d stage=%d id=%d entry=%08X pc=%08X health=%d,%d',winner,p:read_u16(0x01061b30),(at-0xfffef800)//32,at,cpu.PC.value,p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)))
end)
emu.register_frame(function()
 frame=frame+1
 for _,field in pairs(buttons)do field:clear_value()end
 if frame==1 then
  log('BOOT','schema=30 strategy='..strategy..' boot='..boot)
  assert(p:read_u16(0xff86e650)==0xb128 and p:read_u16(0xff86e660)==0x1f0)
  assert(p:read_u16(0xffa166e0)==0xb008 and p:read_u16(0xffa166f0)==0x1f0)
  log('MORPH_ROM','morph=FF86E650:B128,01F0 restore=FFA166E0:B008,01F0')
  local rom_table=p:read_u32(0xff8a11f0)
  for order=0,5 do
   local list=p:read_u32(rom_table+order*32);local ids={}
   for stage=0,16 do ids[#ids+1]=p:read_u16(list+stage*16)end
   log('ROM',string.format('table=%08X order=%d list=%08X ids=%s',rom_table,order,list,table.concat(ids,',')))
  end
 end
 if frame>=300 and frame<304 then press('High Punch')end
 local mode=p:read_u16(0x010601d0);local state=p:read_u16(slots[side].state)
 local stage=p:read_u16(0x01061b30);local schedule=p:read_u32(0x01061b10)
 local winner=p:read_u16(0x01061b00)
 local key=string.format('%d:%d:%d:%d:%08X:%d:%d:%08X:%08X',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),stage,schedule,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor))
 if key~=last_state or frame%120==0 then
  log('STATE',string.format('mode=%d states=%d,%d stage=%d schedule=%08X roster=%d,%d actors=%08X,%08X health=%d,%d winner=%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),stage,schedule,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),winner))
  last_state=key
 end
 if first_live and not loss_at and mode==3 and state==2 and winner==opponent and p:read_u32(slots[side].actor)==0 then
  losses=losses+1;loss_at=frame;css=nil;css_exit=nil
  log('LOSS','number='..losses..' stage='..stage)
  screen:snapshot(string.format('campaign_loss_%d.png',losses))
 end
 if loss_at and not css then
  local age=frame-loss_at
  if age>=20 and age<25 or age>=270 and age<275 then press('Coin')end
  if age>=310 and age<315 then press('Start')end
 end
 if selections==0 and not css and frame>=boot then
  local age=(frame-boot)%300
  if age<4 then press('Coin')end
  if age>=20 and age<24 then press('Start')end
 end
 if not css and frame>700 and mode==4 and state==3 and p:read_u16(slots[side].roster)<=18 then
  css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster))
  log('SELECT',string.format('number=%d initial=%d target=%d path=%s continue=%d stage=%d schedule=%08X',selections,p:read_u16(slots[side].roster),identity,table.concat(plan,','),loss_at or -1,stage,schedule))
 end
 if css and not css_exit then
  local age=frame-css
  for index,direction in ipairs(plan)do
   local at=56+(index-1)*12
   if age>=at and age<at+4 then press(direction)end
  end
  if age==130 or age==146 then
   log('SELECT_ID',string.format('number=%d roster=%d state=%d',selections,p:read_u16(slots[side].roster),state))
   screen:snapshot(string.format('campaign_selection_%d_%d.png',selections,age))
  end
  if age>=148 and age<156 then press('High Punch')end
  if age>148 and mode~=4 then css_exit=frame;log('SELECT_EXIT','number='..selections)end
 end
 local human,other=sample(side),sample(opponent)
 if stage==14 and other and other.roster==6 and not id_taps[other.actor]then
  local actor=other.actor
  id_taps[actor]=p:install_write_tap(actor+0x1f0,actor+0x1ff,'original CPU Shang ID provenance',function(at,data,mask)
   if p:read_u32(slots[opponent].actor)~=actor or p:read_u16(slots[opponent].roster)~=6 or
    p:read_u16(0x01061b30)~=14 then return end
   log('CPU_ID',string.format('actor=%08X before=%d after=%d pc=%08X a0=%08X a9=%08X a8=%08X a13=%08X mask=%04X',actor,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A0.value,cpu.A9.value,cpu.A8.value,cpu.A13.value,mask))
  end)
 end
 if mode==2 and state==1 and p:read_u16(slots[opponent].state)==0 and human and other and human.owner==human.actor and other.owner==other.actor then
  if not first_live then first_live=frame end
  local fight_key=string.format('%d:%d:%08X:%08X',selections,stage,human.actor,other.actor)
  if fight_key~=last_fight then
   floor_origin=frame;floor_epoch=floor_epoch+1;floor_latches={};floor_queues={}
   log('FLOOR_BEGIN',string.format('epoch=%d selection=%d arena=%d human=%d:%d cpu=%d:%d',floor_epoch,selections,p:read_u16(0x01061ac0),human.roster,human.id,other.roster,other.id))
   last_fight=fight_key;loss_at=nil;jump_start=nil;previous_y=nil;projectile_start=nil;close_start=nil;last_close=-1000;guard_until=-1000
   log('FIGHT',string.format('selection=%d stage=%d schedule=%08X human=%d:%d cpu=%d:%d actors=%08X,%08X',selections,stage,schedule,human.roster,human.id,other.roster,other.id,human.actor,other.actor))
   screen:snapshot(string.format('campaign_fight_selection%d_stage%d.png',selections,stage))
  end
  if frame-floor_origin>=216 and frame-floor_origin<=336 and frame%8==0 then floor_pending=true end
  local seen_key=stage..':'..schedule
  if not seen[seen_key]then seen[seen_key]=true;log('STAGE','stage='..stage..' schedule='..string.format('%08X',schedule))end
  live_fields=live_fields+1
  if live_fields<300 or frame%30==0 then
   log('LIVE',string.format('selection=%d stage=%d schedule=%08X human=%d:%d cpu=%d:%d health=%d,%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X hpos=%d,%d hfloor=%d cpos=%d,%d cfloor=%d poses=%08X,%08X actions=%d,%d flags=%04X,%04X banks=%04X,%04X',selections,stage,schedule,human.roster,human.id,other.roster,other.id,human.hp,other.hp,human.actor,human.main,other.actor,other.main,human.x,human.y,human.floor,other.x,other.y,other.floor,human.pose,other.pose,human.action,other.action,human.flags,other.flags,human.bank,other.bank))
  end
  if winner==0 and human.hp>0 and other.hp>0 then
   local gap=math.abs(human.x-other.x)
   if leg_tactic or strategy=='lowkick'or strategy=='throw'then
    local forward=human.x<other.x and'Right'or'Left'
    local height=human.floor-human.y
    local cpu_height=other.floor-other.y
    -- Native Sub-Zero's visible freeze launch is action 604 (intro 10).
    -- Physical crouch-block holds through projectile travel, then approach.
    if strategy=='defensive_leg'and other.roster==8 and gap>100 and
     (other.action==0x604 or other.action==0x10)then guard_until=frame+40 end
    if close_start and frame-close_start<12 then
     local age=frame-close_start
     if leg_tactic then
      if age<7 then press('Down')end
      if age>=3 and age<7 then press('Low Punch');press('Block')end
     elseif strategy=='lowkick'then
      press('Down');if age<4 then press('Low Kick')end
     else
      if age<4 then press('Low Punch');press(forward)end
     end
    elseif strategy=='defensive_leg'and frame<guard_until and gap>90 then
     press('Down');press('Block')
    elseif height>8 then
     if gap<100 and frame%6<3 then press('High Kick')end
    elseif cpu_height>15 and gap<80 then
     press('Down')
     if frame-last_uppercut>=22 then press('High Punch');last_uppercut=frame
     else press('Block')end
    elseif gap<(strategy=='throw'and 42 or leg_tactic and 85 or 70)then
     if frame-last_close>=24 and human.flags&0x1c==0 and human.body&0x0c==0 then
      close_start=frame;last_close=frame
      log('DECISION',string.format('move=%s gap=%d human_action=%d cpu_action=%d',strategy,gap,human.action,other.action))
      if leg_tactic then press('Down')
      elseif strategy=='lowkick'then press('Down');press('Low Kick')
      else press('Low Punch');press(forward)end
     end
    else
     close_start=nil;press(forward)
    end
   elseif strategy=='uppercut' then
    if gap>65 then press(human.x<other.x and'Right'or'Left')
    else press('Down');if frame%22<4 then press('High Punch')end end
   elseif strategy=='jumpkick' then
    if gap>80 then press(human.x<other.x and'Right'or'Left')end
    if frame%56<4 then press('Up')end
    if frame%56>=12 and frame%56<20 then press('High Kick')end
   elseif strategy=='zoning' and other.roster==12 then
    -- Native boss stomp tracks the last grounded location. Evade by walking
    -- during the visible ascent rather than holding block under that spot.
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    local cpu_height=other.floor-other.y
    local height=human.floor-human.y
    if cpu_height>12 then
     press(back)
    elseif height>8 then
     if frame%6<3 then press('High Kick')end
    elseif gap<100 then
     if frame-last_jump>=40 then press('Up');last_jump=frame
     elseif frame-last_jump<4 then press('Up')end
    else
     press(forward)
    end
   elseif strategy=='zoning' then
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    local height=human.floor-human.y
    if projectile_start and frame-projectile_start<64 then
     local age=frame-projectile_start
     -- Preserve the direct-tested native commands: Kano D,B,HP;
     -- Sonya D,F,LP. F,B,HP belongs to Sonya's square-wave, not ring.
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(projectile_direction)end
     if age>=8 and age<12 then press(fighter=='kano'and'High Punch'or'Low Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif height>8 then
     if frame%6<3 then press('High Kick')end
    elseif gap<80 then
     projectile_start=nil
     if frame-last_jump>=40 then press('Up');press(back);last_jump=frame
     elseif frame-last_jump<4 then press('Up');press(back)
     else press('Down');press('Block')end
    else
     projectile_start=frame;projectile_direction=fighter=='kano'and back or forward
     log('DECISION',string.format('move=projectile gap=%d direction=%s',gap,projectile_direction))
    end
   else
    -- Read-only feedback: jump from actual grounded state, kick during the
    -- actual flight, and anti-air an approaching airborne CPU. No fixed
    -- health, action, position, schedule or difficulty changes are supplied.
    local forward=human.x<other.x and'Right'or'Left'
    local height=human.floor-human.y
    local cpu_height=other.floor-other.y
    local airborne=height>8
    if airborne then
     jump_start=jump_start or frame
     local age=frame-jump_start
     local descending=previous_y and human.y>previous_y
     if gap<115 and height<90 and(age>=9 or descending)then
      if age%6<3 then press('High Kick')end
     end
    else
     jump_start=nil
     if frame-last_jump<4 then
      press('Up');press(forward)
     elseif cpu_height>12 and gap<105 then
      press('Down')
      if gap<78 and frame-last_uppercut>=22 then
       press('High Punch');last_uppercut=frame
      else press('Block')end
     elseif gap<47 then
      press('Down')
      if frame-last_uppercut>=22 then
       press('High Punch');last_uppercut=frame
      else press('Block')end
     elseif frame-last_jump>=38 then
      press('Up');press(forward);last_jump=frame
      log('DECISION',string.format('move=jump gap=%d human_height=%d cpu_height=%d',gap,height,cpu_height))
     else
      press('Down');press('Block')
     end
    end
    previous_y=human.y
   end
  end
 end
 if first_live and stage==16 and mode==11 and winner==side and p:read_u16(slots[side].roster)==identity and
  p:read_u16(slots[opponent].hp)==0 and p:read_u16(slots[side].hp)>0 and
  p:read_u32(slots[1].actor)==0 and p:read_u32(slots[2].actor)==0 and(stage_wins[16]or 0)>0 then
  if not ending then ending=frame;log('ENDING_START',string.format('stage=%d winner=%d health=%d,%d actors=00000000,00000000 roster=%d',stage,winner,p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),identity))end
  if (frame-ending)%120==0 then screen:snapshot('campaign_ending_'..(frame-ending)..'.png');log('ENDING','age='..(frame-ending))end
 end
 if ending and not ending_completed and frame-ending>1200 and mode==11 and
  p:read_u16(slots[side].roster)~=identity and math.min(table.unpack(picture_reads))>0 and
  math.min(table.unpack(text_reads))>0 then
  ending_completed=frame
  log('ENDING_COMPLETED',string.format('age=%d mode=%d roster=%d,%d pictures=%d,%d texts=%d,%d',frame-ending,mode,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),picture_reads[1],picture_reads[2],text_reads[1],text_reads[2]))
  screen:snapshot('ending_return_to_attract.png')
 end
 if ending_completed and frame-ending_completed>=300 then manager.machine:exit()end
end)
emu.register_stop(function()
 log('FLOOR_RESULT',string.format('schema=1 epochs=%d snapshots=%d scope=native_campaign_saved_pass_all_observed_arenas_not_all_move_phases',floor_epoch,floor_snaps))
 local count=0;for _ in pairs(seen)do count=count+1 end
 log('RESULT',string.format('schema=30 selections=%d losses=%d native_win_reads=%d first_live=%d live_fields=%d seen_stages=%d ending=%d ending_completed=%d pictures=%d,%d texts=%d,%d scope=unassisted_campaign_observation_independent_verification_pending',selections,losses,wins,first_live or -1,live_fields,count,ending or -1,ending_completed or -1,picture_reads[1],picture_reads[2],text_reads[1],text_reads[2]))
 for _,tap in ipairs(taps)do tap:remove()end
end)
