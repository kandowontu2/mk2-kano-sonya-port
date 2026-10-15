-- Actual compiled owned frozen-body data/graphics and native0616 instance; not full shatter acceptance.
local file=assert(io.open('mk2ks_stock_fatality_v1021.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local start,stop=source:find(before,1,true);assert(start and not source:find(before,stop+1,true),'Unique stock source anchor')
 source=source:sub(1,start-1)..after..source:sub(stop+1)
end
replace('kung_lao=0,jax=11','kung_lao=0,jax=11,subzero=8')
replace('local sequence=assert(commands[command])',"commands.ffd_hk={'Forward','Forward','Down','High Kick'}\nlocal sequence=assert(commands[command])")
replace('screen:snapshot(', 'MK2KS_SUBZERO_REDUNDANT_SNAPSHOT(')
function MK2KS_SUBZERO_REDUNDANT_SNAPSHOT(filename)
 print('MK2_SUBZERO_REDUNDANT_IMAGE_SKIPPED filename='..filename..' writes=0 assistance=none')
end
assert(not source:find('screen:snapshot',1,true))
assert(load(source,'@stock1021_native_SubZero_physical_inputs','t',_ENV))()

local p=manager.machine.devices[':maincpu'].spaces.program
local gfx=assert(manager.machine.memory.regions[':gfxrom'])
local screen=manager.machine.screens[':screen']
local cpu=manager.machine.devices[':maincpu'].state
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
local winner=3-side
local identity=assert(({kano=17,sonya=18})[os.getenv('MK2KS_TEST_FIGHTER')])
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local buttons=manager.machine.ioport.ports[':IN0'].fields
local frame,deep,uppercut,completed,native_main=0,nil,nil,nil,nil
local shatter={'Forward','Down','Forward','Forward','High Punch'}
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,extra)
 print(string.format('MK2_EARNED_SUBZERO_%s frame=%d identity=%d side=%d writes=0 assistance=none %s',tag,frame,identity,side,extra or''))
end
local function sample()
 local s=slots[side];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return a,m,p:read_u16(a+0x1f0),p:read_u16(m+0x1f0)
end
for _,entry in ipairs({{0xff8c2320,'DEEP_TASK'},{0xff906090,'MAIN_LOOKUP'},
 {0xff838790,'CACHE_BEGIN'},{0xff8c26b0,'BODY_LOOKUP'}})do
 local address,tag=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'readonly earned SubZero native victim',function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 then return end
  local a,m,id,action=sample()
  if id~=identity or cpu.A8.value~=a or not valid(cpu.A13.value)or p:read_u32(cpu.A13.value+0xc0)~=a then return end
  if tag=='DEEP_TASK'then deep=deep or frame;native_main=cpu.A13.value end
  if not deep then return end
  log(tag,string.format('entry=%08X pc=%08X value=%04X mask=%04X actor=%08X main=%08X owner=%08X hp=%d roster=%d action=%04X a0=%08X a1=%08X a9=%08X pose=%08X',
   at,cpu.PC.value,data&0xffff,mask,a,cpu.A13.value,p:read_u32(cpu.A13.value+0xc0),p:read_u16(slots[side].hp),p:read_u16(slots[side].id),p:read_u16(cpu.A13.value+0x1f0),cpu.A0.value,cpu.A1.value,cpu.A9.value,p:read_u32(a+0x1d0)))
 end)
end
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 if frame==1 then
  local bytes={}
  for at=0,11943 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa0000+at))end
  local raw=table.concat(bytes)
  print('MK2_EARNED_SUBZERO_GFX frame=1 bytes=11944 hex='..raw:gsub('.',function(c)return string.format('%02x',c:byte())end))

  local bytes=p:read_range(0xff800000,0xffffffff,8,8)
  assert(#bytes==1048576)
  print('MK2_EARNED_SUBZERO_GUEST frame=1 bytes=1048576 hex='..bytes:gsub('.',function(c)return string.format('%02x',c:byte())end))
 end
 if deep and frame-deep==100 then
  local raw,width,height=screen:pixels();assert(width==400 and height==254 and #raw==400*254*4)
  print(string.format('MK2_EARNED_SUBZERO_RGB frame=%d width=%d height=%d bytes=%d hex=%s',frame,width,height,#raw,raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))
 end
 if deep then
  local a,m,id,action=sample();assert(id==identity)
  if native_main and p:read_u32(native_main+0xc0)==a then m=native_main;action=p:read_u16(m+0x1f0)end
  log('FIELD',string.format('actor=%08X main=%08X owner=%08X roster=%d state=%d hp=%d action=%04X pose=%08X',
   a,m,p:read_u32(m+0xc0),p:read_u16(slots[side].id),p:read_u16(slots[side].state),p:read_u16(slots[side].hp),action,p:read_u32(a+0x1d0)))
 end
 if (deep and frame-deep>=400)or frame>=7000 then
  log('HOST_EXIT',string.format('deep=%d uppercut=%d completed=%d',deep or-1,uppercut or-1,completed or-1))
  manager.machine:exit()
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('deep=%d uppercut=%d completed=%d',deep or-1,uppercut or-1,completed or-1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
