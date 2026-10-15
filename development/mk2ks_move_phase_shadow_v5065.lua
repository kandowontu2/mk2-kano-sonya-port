-- Ordinary two-human live round; only physical D,F,LP and post-thaw controls.
local file=assert(io.open('mk2ks_stock_fatality_v1021.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique ordinary-freeze source anchor')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('kung_lao=0,jax=11','kung_lao=0,jax=11,subzero=8')
replace([=[  if p:read_u16(0x01061b00)==0 and own.hp>0 and victim.hp>0 and frame-first_live>=180 then
   if gap>80 then press(winner_side,forward)
   else press(winner_side,'Down');if(frame-first_live)%42<4 then press(winner_side,'High Punch')end end
  end]=],[=[  if p:read_u16(0x01061b00)==0 and own.hp>0 and victim.hp>0 then
   local age=frame-first_live
   if age>=90 and age<93 then press(winner_side,'Down')end
   if age>=98 and age<101 then press(winner_side,forward)end
   if age>=106 and age<109 then press(winner_side,'Low Punch')end
   if age>=450 and age<466 then press(side,back)end
   if age>=510 and age<513 then press(side,'High Punch')end
   if age>=600 and age<603 then press(side,'Up')end
   if age>=710 and age<731 then press(side,'Down')end
   if age>=760 and age<763 then press(side,'High Kick')end
   if age>=810 and age<813 then press(side,'Low Kick')end
   if age>=850 and age<871 then press(side,'Block')end
   if age>=900 and age<903 then press(side,'Down');press(side,'High Punch')end
   if age>=950 and age<971 then press(side,back)end
  end]=])
replace('screen:snapshot(', 'MK2_NORMAL_FREEZE_SNAPSHOT_DISABLED(')
function MK2_NORMAL_FREEZE_SNAPSHOT_DISABLED(filename)
 print('MK2_NORMAL_FREEZE_REDUNDANT_IMAGE_SKIPPED filename='..filename..' writes=0 assistance=none')
end
assert(not source:find('screen:snapshot',1,true))
source=source..[==[

local native_gfx=assert(manager.machine.memory.regions[':gfxrom'])
local extra_taps={}
local marks={[60]='before',[145]='ice',[240]='wait',[580]='after_controls',
 [610]='air_rise',[625]='air_fall',[680]='landed',[720]='crouch',[735]='stand',
 [765]='high_kick',[815]='low_kick',[860]='block',[910]='uppercut',[960]='walk',[1040]='ready'}
local function normal_log(tag,extra)
 print(string.format('MK2_NORMAL_FREEZE_%s frame=%d victim=%s identity=%d side=%d writes=0 assistance=none %s',
  tag,frame,name,identity,side,extra or''))
end
for _,entry in ipairs({{0xff866630,'NORMAL_ICE_PARSE'},{0xff86f9d0,'ICE_REQUEST'},
 {0xff8a5900,'PROJECTILE_SETUP'},{0xff877590,'BUTTON_HISTORY'},
 {0xff838790,'BODY_CACHE'},{0xff83d2f0,'RESTORE_FLOOR'}})do
 local address,tag=entry[1],entry[2]
 extra_taps[#extra_taps+1]=p:install_read_tap(address,address+15,'readonly ordinary freeze branch',function(at,data,mask)
  if not first_live or at~=address or cpu.PC.value~=address+16 then return end
  local a,m=cpu.A8.value,cpu.A13.value
  if not valid(a)or not valid(m)or p:read_u32(m+0xc0)~=a then return end
  local id=p:read_u16(a+0x1f0)
  if id~=identity and id~=8 then return end
  normal_log(tag,string.format('age=%d entry=%08X pc=%08X value=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d action=%04X a0=%08X a7=%08X a9=%08X pose=%08X',
   frame-first_live,at,cpu.PC.value,data&0xffff,mask,a,m,p:read_u32(m+0xc0),id,p:read_u16(m+0x1f0),
   cpu.A0.value,cpu.A7.value,cpu.A9.value,p:read_u32(a+0x1d0)))
 end)
end
extra_taps[#extra_taps+1]=p:install_write_tap(0x01a80010,0x01a8001f,'readonly native scene DMA command',function(at,data,mask)
 if at~=0x01a80010 or not first_live or not marks[frame-first_live]then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 normal_log('DMA',string.format('stage=%s command=%04X mask=%04X pc=%08X actor_register=%08X main_register=%08X source=%08X x=%d y=%d width=%d height=%d palette=%04X color=%04X cache_row=%08X',
  marks[frame-first_live],data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,
  reg(2)|(reg(3)<<16),reg(4)&0x3ff,reg(5)&0x1ff,reg(6)&0x3ff,reg(7)&0x3ff,reg(8),reg(9),cpu.A9.value))
end)
emu.register_frame_done(function()
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  print('MK2_NORMAL_FREEZE_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02x',c:byte())end))
  local bytes={}
  for i=0,11943 do bytes[#bytes+1]=string.char(native_gfx:read_u8(0x1fa0000+i))end
  for i=0,7031 do bytes[#bytes+1]=string.char(native_gfx:read_u8(0x1fa4000+i))end
  raw=table.concat(bytes)
  print('MK2_NORMAL_FREEZE_GFX frame=1 bytes=18976 hex='..raw:gsub('.',function(c)return string.format('%02x',c:byte())end))
 end
 if first_live then
  local own,victim=sample(winner_side),sample(side)
  local age=frame-first_live
  if own and victim then
   normal_log('FIELD',string.format('age=%d mode=%d finish=%d own_actor=%08X own_main=%08X own_owner=%08X own_id=%d own_hp=%d victim_actor=%08X victim_main=%08X victim_owner=%08X victim_id=%d roster=%d state=%d hp=%d x=%d y=%d floor=%d action=%04X pose=%08X bank=%04X flags=%04X facing=%04X',
    age,p:read_u16(0x010601d0),p:read_u16(0x01061b00),own.actor,own.main,own.owner,own.id,own.hp,
    victim.actor,victim.main,victim.owner,victim.id,victim.roster,p:read_u16(slots[side].state),victim.hp,
    victim.x,victim.y,p:read_i16(victim.main+0x200),p:read_u16(victim.main+0x1f0),victim.pose,victim.bank,
    victim.flags,p:read_u16(victim.actor+0xf0)))
  else normal_log('INVALID_ACTOR','age='..age)end
  if marks[age]then
   local raw,width,height=screen:pixels();assert(width==400 and height==254 and #raw==406400)
   print(string.format('MK2_NORMAL_FREEZE_RGB frame=%d stage=%s width=%d height=%d bytes=%d hex=%s',
    frame,marks[age],width,height,#raw,raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))
  end
  if age>=1100 then normal_log('END','first_live='..first_live..' age='..age);manager.machine:exit()end
 elseif frame>=4300 then normal_log('NO_LIVE_ROUND','first_live=-1');manager.machine:exit()end
end)
emu.register_stop(function()
 for _,observer in ipairs(extra_taps)do observer:remove()end
end)
]==]

source=source..[==[
-- Observe owned cache components at the original direct shadow projection.
extra_taps[#extra_taps+1]=p:install_read_tap(0xff8012b0,0xff8012bf,'readonly direct ordinary freeze shadow projection',function(at,data,mask)
 if not first_live or not marks[frame-first_live]or at~=0xff8012b0 or cpu.PC.value~=0xff8012c0 then return end
 local row=cpu.A9.value
 for slot,info in ipairs(slots)do
  local actor,main=p:read_u32(info.actor),p:read_u32(info.main)
  if valid(actor)and valid(main)and p:read_u32(main+0xc0)==actor then
   local cache=p:read_u32(actor+0x1a0)
   local count=0
   if valid(cache)then
    while count<12 and p:read_u32(cache+count*112)~=0 do count=count+1 end
    assert(count<12,'Complete terminated owned native cache')
   end
   if valid(cache)and row>=cache and row<cache+count*112 and(row-cache)%112==0 then
    local graphic,width,height,command=p:read_u32(row),p:read_u16(row+0x20),p:read_u16(row+0x30),p:read_u16(row+0x40)
    local dx,dy=p:read_i16(row+0x50),p:read_i16(row+0x60)
    local world=((p:read_u16(actor+0xb0)&0xffff)<<16)|p:read_u16(actor+0x90)
    normal_log('PROJECTION',string.format('stage=%s slot=%d actor=%08X main=%08X owner=%08X id=%d pose=%08X cache=%08X row=%08X component=%d graphic=%08X width=%d height=%d command=%04X dx=%d dy=%d body=%04X facing=%04X world=%08X b1=%08X b2=%08X b4=%08X b7=%08X a5=%08X shadow_camera=%08X stageY=%d floor=%d pc=%08X value=%04X mask=%04X',
     marks[frame-first_live],slot,actor,main,actor,p:read_u16(actor+0x1f0),p:read_u32(actor+0x1d0),cache,row,(row-cache)//112,
     graphic,width,height,command,dx,dy,p:read_u16(actor+0x160),p:read_u16(actor+0xf0),world,
     cpu.B1.value,cpu.B2.value,cpu.B4.value,cpu.B7.value,cpu.A5.value,cpu.B1.value|p:read_u16(0x0105d350),
     p:read_i16(0x0105ecd0),p:read_i16(main+0x200),cpu.PC.value,data&0xffff,mask))
    -- Match the compiled video device's imported-source rebasing, not a guessed bitmap.
    local mapped=graphic
    if graphic>=0x10000000 and graphic<0x1a000000 then mapped=mapped-0x0a000000 end
    assert(mapped<0x10000000 and width>0 and height>0 and width<=200 and height<=200)
    local begin=mapped//8
    local count=(width*height*6+height*8+15)//8+4
    assert(begin+count<=native_gfx.size)
    local bytes={}
    for i=0,count-1 do bytes[#bytes+1]=string.char(native_gfx:read_u8(begin+i))end
    local raw=table.concat(bytes)
    print(string.format('MK2_NORMAL_FREEZE_PART frame=%d stage=%s slot=%d actor=%08X row=%08X graphic=%08X mapped=%08X width=%d height=%d command=%04X bytes=%d hex=%s',
     frame,marks[frame-first_live],slot,actor,row,graphic,mapped,width,height,command,#raw,
     raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))
   end
  end
 end
end)
]==]

assert(load(source,'@actual_move_phase_shadow_5065','t',_ENV))()


