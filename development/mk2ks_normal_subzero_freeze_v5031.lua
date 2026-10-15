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
  end]=])
replace('screen:snapshot(', 'MK2_NORMAL_FREEZE_SNAPSHOT_DISABLED(')
function MK2_NORMAL_FREEZE_SNAPSHOT_DISABLED(filename)
 print('MK2_NORMAL_FREEZE_REDUNDANT_IMAGE_SKIPPED filename='..filename..' writes=0 assistance=none')
end
assert(not source:find('screen:snapshot',1,true))
source=source..[==[

local native_gfx=assert(manager.machine.memory.regions[':gfxrom'])
local extra_taps={}
local marks={[60]='before',[145]='ice',[240]='wait',[580]='after_controls'}
local function normal_log(tag,extra)
 print(string.format('MK2_NORMAL_FREEZE_%s frame=%d victim=%s identity=%d side=%d writes=0 assistance=none %s',
  tag,frame,name,identity,side,extra or''))
end
for _,entry in ipairs({{0xff866630,'NORMAL_ICE_PARSE'},{0xff86bb80,'ICE_REQUEST'},
 {0xff86bab0,'PROJECTILE_SETUP'},{0xff877590,'BUTTON_HISTORY'},
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
 normal_log('DMA',string.format('stage=%s command=%04X mask=%04X pc=%08X actor_register=%08X main_register=%08X source=%08X x=%d y=%d width=%d height=%d palette=%04X',
  marks[frame-first_live],data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,
  reg(2)|(reg(3)<<16),reg(4)&0x3ff,reg(5)&0x1ff,reg(6)&0x3ff,reg(7)&0x3ff,reg(8)))
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
  if age>=700 then normal_log('END','first_live='..first_live..' age='..age);manager.machine:exit()end
 elseif frame>=4300 then normal_log('NO_LIVE_ROUND','first_live=-1');manager.machine:exit()end
end)
emu.register_stop(function()
 for _,observer in ipairs(extra_taps)do observer:remove()end
end)
]==]
assert(load(source,'@actual_normal_subzero_freeze_5031','t',_ENV))()
