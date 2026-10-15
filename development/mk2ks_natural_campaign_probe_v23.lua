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
assert(strategy=='uppercut' or strategy=='jumpkick' or strategy=='specials')
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
local command=nil
local reset_seen=nil
local draw_count=0
local cinematic_active=false
local pit_episode,episode_enter,episode_lookups=0,nil,0
local floor_origin,floor_pending=nil,nil
local floor_epoch,floor_snaps=0,0
local function log(tag,value)
 print(string.format('MK2_NAT_CAMPAIGN_%s frame=%d human_slot=%d fighter=%s writes=0 assistance=none %s',tag,frame,side,fighter,value or''))
end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a) or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),
  state=p:read_u16(s.state),hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),
  floor=p:read_i16(m+0x200),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),
  body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140),action=p:read_u16(m+0x1f0)}
end
-- Observe naturally reached arenas without changing the campaign's inputs.
-- All body/scenery/foreground DMA writes are retained during fixed windows;
-- no palette ownership is inferred from a fixed 0200/0300 slot assumption.
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
 local bank=((floor_regs[15]or 0)>>5)&1
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
 if floor_pre_frame~=frame then
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
 for n=1,2 do
  local a=sample(n)
  if a and a.owner==a.actor and a.bank&0x7f00==pal then
   owner_slot=n
   log('FLOOR_OWNER',string.format('epoch=%d event=%d source=%08X slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d cache=%08X pose=%08X bank=%04X body=%04X facing=%04X x=%d y=%d floor=%d action=%d stageY=%d displayY=%d cameraY=%d',floor_epoch,event,source,n,a.actor,a.main,a.owner,a.id,a.roster,p:read_u32(a.actor+0x1a0),a.pose,a.bank,a.body,p:read_u16(a.actor+0xf0),a.x,a.y,a.floor,a.action,p:read_i16(0x0105ecd0),p:read_i16(0x0105d060),p:read_i16(0x0105d130)))
  end
 end
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
 log('WIN',string.format('slot=%d stage=%d id=%d entry=%08X pc=%08X health=%d,%d',winner,p:read_u16(0x01061b30),(at-0xfffef800)//32,at,cpu.PC.value,p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)))
end)
for _,address in ipairs({0x010601d0,0x01061b00,0x010601f0,0x01060dc0})do
 taps[#taps+1]=p:install_write_tap(address,address+15,'native campaign transition provenance',function(at,data,mask)
  if not first_live or mask~=0xffff or p:read_u16(at)==data&0xffff then return end
  log('TRANSITION',string.format('at=%08X before=%d after=%d pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X sp=%08X callers=%08X,%08X,%08X mode=%d phase=%d',at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,cpu.SP.value,p:read_u32(cpu.SP.value),p:read_u32(cpu.SP.value+32),p:read_u32(cpu.SP.value+64),p:read_u16(0x010601d0),p:read_u16(0x01061b00)))
 end)
end
for _,address in ipairs({0xffffffe0,0xffa1e800,0xffa1e880,0xfffaae00,0xfffab200})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'native campaign reset or finish boundary',function(at)
  if not first_live or at~=address then return end
  if address~=0xffffffe0 and cpu.PC.value~=address+16 then return end
  log('BOUNDARY',string.format('entry=%08X pc=%08X a8=%08X a13=%08X mode=%d phase=%d stage=%d',address,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(0x010601d0),p:read_u16(0x01061b00),p:read_u16(0x01061b30)))
  if address==0xffffffe0 then reset_seen=reset_seen or frame end
 end)
end
-- Instruction and source provenance only. These taps never supply data or
-- change the guest, including the malformed group that is under investigation.
for _,address in ipairs({0xff838790,0xff83bb00,0xff85c420})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'Pit cinematic group provenance',function(at)
  if at~=address or cpu.PC.value~=address+16 or p:read_u16(0x010601d0)~=9 then return end
  draw_count=draw_count+1
  if draw_count>900 then return end
  local a,m=cpu.A8.value,cpu.A13.value
  local cells={}
  if valid(m)then for offset=0x100,0x350,0x10 do cells[#cells+1]=string.format('%03X:%08X',offset,p:read_u32(m+offset))end end
  log('DRAW',string.format('entry=%08X a0=%08X a1=%08X a5=%08X a8=%08X a9=%08X a13=%08X sp=%08X actor_id=%d pose=%08X cache=%08X flags=%04X x=%d y=%d bank=%04X task=%s',address,cpu.A0.value,cpu.A1.value,cpu.A5.value,a,cpu.A9.value,m,cpu.SP.value,valid(a)and p:read_u16(a+0x1f0)or -1,valid(a)and p:read_u32(a+0x1d0)or 0,valid(a)and p:read_u32(a+0x1a0)or 0,valid(a)and p:read_u16(a+0x160)or 0,valid(a)and p:read_i16(a+0x90)or -1,valid(a)and p:read_i16(a+0xb0)or -1,valid(a)and p:read_u16(a+0x140)or 0,table.concat(cells,',')))
 end)
end
local components=0
taps[#taps+1]=p:install_read_tap(0xff8387f0,0xff8387ff,'Pit component source provenance',function(at)
 if at~=0xff8387f0 or cpu.PC.value~=0xff838800 or p:read_u16(0x010601d0)~=9 then return end
 components=components+1
 if components>150 then return end
 local source=cpu.A0.value
 log('COMPONENT',string.format('source=%08X value=%08X dst=%08X a8=%08X a9=%08X a13=%08X',source,p:read_u32(source),cpu.A1.value,cpu.A8.value,cpu.A9.value,cpu.A13.value))
end)
local pit_table=p:read_u32(0xff85c330)
assert(pit_table==p:read_u32(0xff85c4a0),'Both actual scene operands must agree')
local pit_lookups,pit_enter,pit_exit=0,nil,nil
taps[#taps+1]=p:install_read_tap(pit_table,pit_table+19*32-1,'actual native Pit victim table lookup',function(at,data,mask)
 if cpu.PC.value~=0xff83b850 or (at-pit_table)%32~=0 then return end
 local a,m=cpu.A8.value,cpu.A13.value
 if not cinematic_active then
  pit_episode=pit_episode+1;episode_enter=frame;episode_lookups=0
 end
 cinematic_active=true
 episode_lookups=episode_lookups+1
 pit_lookups=pit_lookups+1;pit_enter=pit_enter or frame
 log('PIT_LOOKUP',string.format('at=%08X value=%08X mask=%08X pc=%08X a8=%08X a13=%08X id=%d a1=%08X table_slot=%d mode=%d episode=%d',at,data,mask,cpu.PC.value,a,m,p:read_u16(a+0x1f0),cpu.A1.value,(at-pit_table)//32,p:read_u16(0x010601d0),pit_episode))
end)
-- Observe the original constructor's arguments and actual palette load.
-- A2=0 is the stock Pit call, so even an alternate-costume victim is
-- reconstructed using the normal table. No palette/flag writes are supplied.
for _,address in ipairs({0xff906ef0,0xff85bc10})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'Pit original palette constructor provenance',function(at)
  if at~=address or cpu.PC.value~=address+16 or p:read_u16(0x010601d0)~=9 then return end
  local a=cpu.A8.value
  log('PIT_CONSTRUCTOR',string.format('episode=%d entry=%08X pc=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X id=%d body=%04X bank=%04X',pit_episode+1,address,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,a,cpu.A13.value,valid(a)and p:read_u16(a+0x1f0)or -1,valid(a)and p:read_u16(a+0x160)or 0,valid(a)and p:read_u16(a+0x140)or 0))
 end)
end
local palette_observing=false
for variant,address in ipairs({0xfffec000,0xfffec400})do
 taps[#taps+1]=p:install_read_tap(address,address+19*32-1,'Pit actual character palette table '..variant,function(at,data,mask)
  if palette_observing or cpu.PC.value~=0xff9071a0 or (at-address)%32~=0 or p:read_u16(0x010601d0)~=9 then return end
  palette_observing=true
  local pointer=p:read_u32(at);local count=p:read_u16(pointer);local colors={}
  if count==65 then for index=0,64 do colors[#colors+1]=string.format('%04X',p:read_u16(pointer+16+index*16))end end
  log('PIT_PALETTE',string.format('episode=%d table=%08X at=%08X value=%08X mask=%08X pc=%08X variant=%d id=%d pointer=%08X count=%d colors=%s a8=%08X a13=%08X',pit_episode+1,address,at,data,mask,cpu.PC.value,variant-1,(at-address)//32,pointer,count,table.concat(colors,','),cpu.A8.value,cpu.A13.value))
  palette_observing=false
 end)
end
local moves={knife=0xffffb000,ring=0xffffb400,choke=0xfff91400,leg=0xfff80800,
 blade=0xfff8cc00,ball=0xffffde00,bicycle=0xfff9a400,square=0xffffca00}
for move,address in pairs(moves)do
 taps[#taps+1]=p:install_read_tap(address,address+15,'natural campaign action '..move,function(at)
  if at~=address or cpu.PC.value~=address+16 then return end
  local own=sample(side)
  if own and own.actor==cpu.A8.value and own.main==cpu.A13.value and own.state==1 and own.id==identity then
   log('SPECIAL',string.format('move=%s entry=%08X pc=%08X actor=%08X main=%08X id=%d stage=%d',move,address,cpu.PC.value,own.actor,own.main,own.id,p:read_u16(0x01061b30)))
  end
 end)
end
emu.register_frame(function()
 frame=frame+1
 for _,field in pairs(buttons)do field:clear_value()end
 if frame==1 then
  log('BOOT','schema=23 strategy='..strategy..' boot='..boot)
  log('PIT_OPERANDS',string.format('first=%08X second=%08X',p:read_u32(0xff85c330),p:read_u32(0xff85c4a0)))
  local coordinates=p:read_u32(0xff85bd40)
  log('PIT_COORDINATES',string.format('operand=%08X kano=%08X sonya=%08X',coordinates,p:read_u32(coordinates+17*32),p:read_u32(coordinates+18*32)))
  for id=0,18 do log('PIT_ROM',string.format('id=%d value=%08X',id,p:read_u32(pit_table+id*32)))end
  local rom_table=p:read_u32(0xff8a11f0)
  for order=0,5 do
   local list=p:read_u32(rom_table+order*32);local ids={}
   for stage=0,16 do ids[#ids+1]=p:read_u16(list+stage*16)end
   log('ROM',string.format('table=%08X order=%d list=%08X ids=%s',rom_table,order,list,table.concat(ids,',')))
  end
 end
 if frame>=300 and frame<304 then press('High Punch')end
 local mode=p:read_u16(0x010601d0);local state=p:read_u16(slots[side].state)
 if cinematic_active and mode~=9 then
  cinematic_active=false
  pit_exit=frame
  log('PIT_EXIT',string.format('enter=%d lookups=%d mode=%d states=%d,%d health=%d,%d episode=%d total_lookups=%d',episode_enter,episode_lookups,mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),pit_episode,pit_lookups))
  screen:snapshot('campaign_pit_exit_'..frame..'.png')
 end
 local stage=p:read_u16(0x01061b30);local schedule=p:read_u32(0x01061b10)
 local winner=p:read_u16(0x01061b00)
 local key=string.format('%d:%d:%d:%d:%08X:%d:%d:%08X:%08X',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),stage,schedule,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor))
 if key~=last_state or frame%120==0 then
  log('STATE',string.format('mode=%d states=%d,%d stage=%d schedule=%08X roster=%d,%d actors=%08X,%08X health=%d,%d winner=%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),stage,schedule,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),winner))
  last_state=key
 end
 if first_live and mode==9 and last_state==key then
  if frame%30==0 then
   log('NINE',string.format('pc=%08X phase=%d stage=%d a8=%08X a13=%08X',cpu.PC.value,winner,stage,cpu.A8.value,cpu.A13.value))
   screen:snapshot('campaign_mode9_'..frame..'.png')
  end
 end
 if cinematic_active and mode==9 and frame%3==0 then screen:snapshot('campaign_pit_'..frame..'.png')end
 if pit_exit and frame<=pit_exit+240 and frame%3==0 then screen:snapshot('campaign_pit_post_'..frame..'.png')end
 if reset_seen and frame>=reset_seen+240 then manager.machine:exit()end
 if first_live and not loss_at and mode==3 and state==2 and p:read_u16(slots[side].hp)==0 and p:read_u32(slots[side].actor)==0 then
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
 local selection_roster=p:read_u16(slots[side].roster)
 if not css and frame>700 and mode==4 and state==3 and selection_roster<=18 then
  plan=route(selection_roster);css=frame;selections=selections+1
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
 if mode==2 and state==1 and p:read_u16(slots[opponent].state)==0 and human and other and human.owner==human.actor and other.owner==other.actor then
  if not first_live then first_live=frame end
  local fight_key=string.format('%d:%d:%08X:%08X',selections,stage,human.actor,other.actor)
  if fight_key~=last_fight then
   last_fight=fight_key;loss_at=nil;command=nil
   floor_origin=frame;floor_epoch=floor_epoch+1
   log('FLOOR_BEGIN',string.format('epoch=%d selection=%d arena=%d human=%d:%d cpu=%d:%d',floor_epoch,selections,p:read_u16(0x01061ac0),human.roster,human.id,other.roster,other.id))
   log('FIGHT',string.format('selection=%d stage=%d schedule=%08X human=%d:%d cpu=%d:%d actors=%08X,%08X',selections,stage,schedule,human.roster,human.id,other.roster,other.id,human.actor,other.actor))
   screen:snapshot(string.format('campaign_fight_selection%d_stage%d.png',selections,stage))
  end
  if frame-floor_origin>=216 and frame-floor_origin<=336 and frame%8==0 then floor_pending=true end
  local seen_key=stage..':'..schedule
  if not seen[seen_key]then seen[seen_key]=true;log('STAGE','stage='..stage..' schedule='..string.format('%08X',schedule))end
  live_fields=live_fields+1
  if live_fields<300 or frame%30==0 then
   log('BODY',string.format('selection=%d human=%d:%d cpu=%d:%d actors=%08X,%08X bodies=%04X,%04X banks=%04X,%04X',selections,human.roster,human.id,other.roster,other.id,human.actor,other.actor,human.body,other.body,human.bank,other.bank))
   log('LIVE',string.format('selection=%d stage=%d schedule=%08X human=%d:%d cpu=%d:%d health=%d,%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X hpos=%d,%d hfloor=%d cpos=%d,%d cfloor=%d poses=%08X,%08X actions=%d,%d flags=%04X,%04X banks=%04X,%04X',selections,stage,schedule,human.roster,human.id,other.roster,other.id,human.hp,other.hp,human.actor,human.main,other.actor,other.main,human.x,human.y,human.floor,other.x,other.y,other.floor,human.pose,other.pose,human.action,other.action,human.flags,other.flags,human.bank,other.bank))
  end
  if winner==0 and human.hp>0 and other.hp>0 then
   local gap=math.abs(human.x-other.x)
   if strategy=='uppercut' then
    if gap>65 then press(human.x<other.x and'Right'or'Left')
    else press('Down');if frame%22<4 then press('High Punch')end end
   elseif strategy=='jumpkick' then
    if gap>80 then press(human.x<other.x and'Right'or'Left')end
    if frame%56<4 then press('Up')end
    if frame%56>=12 and frame%56<20 then press('High Kick')end
   else
    if command and (command.actor~=human.actor or command.main~=human.main or frame-command.frame>=110)then command=nil end
    if not command and human.y==human.floor and human.flags&0x1c==0 then
     if gap>150 or gap<=58 then
      local forward=human.x<other.x and'Right'or'Left'
      command={frame=frame,actor=human.actor,main=human.main,forward=forward,
       back=forward=='Right'and'Left'or'Right',move=gap>150 and(fighter=='kano'and'knife'or'ring')or(fighter=='kano'and'choke'or'leg')}
      log('COMMAND','move='..command.move..' gap='..gap..' forward='..forward)
     else press(human.x<other.x and'Right'or'Left')end
    end
    if command then
     local age=frame-command.frame;local move=command.move
     if move=='leg' then
      if age<7 then press('Down')end
      if age>=3 and age<7 then press('Low Punch');press('Block')end
     else
      if age<3 then press('Down')end
      if age>=5 and age<8 then press(move=='knife'and command.back or command.forward)end
      if age>=6 and age<9 then press(move=='knife'and'High Punch'or'Low Punch')end
     end
    end
   end
  end
 end
 if first_live and stage==16 and mode==11 and winner==side and p:read_u16(slots[side].roster)==identity then
  ending=ending or frame
  if (frame-ending)%120==0 then screen:snapshot('campaign_ending_'..(frame-ending)..'.png');log('ENDING','age='..(frame-ending))end
 end
end)
emu.register_stop(function()
 local count=0;for _ in pairs(seen)do count=count+1 end
 log('RESULT',string.format('schema=23 selections=%d losses=%d native_win_reads=%d first_live=%d live_fields=%d seen_stages=%d ending=%d reset=%d pit_lookups=%d pit_enter=%d pit_exit=%d pit_episodes=%d floor_epochs=%d floor_snaps=%d scope=unassisted_campaign_observation_independent_verification_pending',selections,losses,wins,first_live or -1,live_fields,count,ending or -1,reset_seen or -1,pit_lookups,pit_enter or -1,pit_exit or -1,pit_episode,floor_epoch,floor_snaps))
 for _,tap in ipairs(taps)do tap:remove()end
end)
