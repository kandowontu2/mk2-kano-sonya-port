-- Reuse the complete physical v18 loss/continue/reselect driver unchanged.
-- Only its snapshot sink changes: full pixels go to host RAM, never PNGs.
local getenv=os.getenv
os.getenv=function(key)
 if key=='MK2KS_GROUND_FIGHTER' then return getenv('MK2PORT_CONTINUE_FIGHTER') end
 if key=='MK2KS_GROUND_SIDE' then return getenv('MK2PORT_CONTINUE_SIDE') end
 return getenv(key)
end
local file=assert(io.open('mk2ks_continue_cross_v18_probe.lua','rb'))
local source=file:read('*a');file:close()
local count
source,count=source:gsub('screen:snapshot%(file%)',"current_continue_rgb(file,frame)")
assert(count==1,'Only original snapshot output changes')
local screen=manager.machine.screens[':screen']
local program=manager.machine.devices[':maincpu'].spaces.program
local gfx=manager.machine.memory.regions[':gfxrom']
local function hex(raw) return raw:gsub('.',function(c)return string.format('%02x',c:byte())end) end
current_continue_rgb=function(filename,frame)
 local raw,width,height=screen:pixels()
 assert(width==400 and height==254 and #raw==406400)
 print(string.format('MK2_CR_RGB frame=%d filename=%s bytes=%d hex=%s',frame,filename,#raw,hex(raw)))
end
assert(load(source,'@mk2ks_continue_cross_v18_probe.lua::RAM_snapshot_sink'))()
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame=0
local function valid(a) return a>=0x01000000 and a<0x01100000 end
emu.register_frame_done(function()
 frame=frame+1
 if frame==1 then
  local raw=program:read_range(0xff800000,0xffffffff,8,8)
  assert(#raw==1048576)
  print('MK2_CR_GUEST frame=1 bytes=1048576 hex='..hex(raw))
  local bytes={}
  for i=0,11943 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa0000+i)) end
  for i=0,7031 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa4000+i)) end
  raw=table.concat(bytes)
  print('MK2_CR_GFX frame=1 bytes=18976 hex='..hex(raw))
 end
 for n,s in ipairs(slots) do
  local a,m=program:read_u32(s.actor),program:read_u32(s.main)
  if valid(a) and valid(m) then
   print(string.format('MK2_CR_FIELD frame=%d slot=%d mode=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d x=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X flags=%04X writes=0 assistance=none',
    frame,n,program:read_u16(0x010601d0),a,m,program:read_u32(m+0xc0),program:read_u16(a+0x1f0),
    program:read_u16(s.id),program:read_u16(s.state),program:read_u16(s.hp),program:read_i16(a+0x90),
    program:read_i16(a+0xb0),program:read_i16(m+0x200),program:read_u32(a+0x40),program:read_u32(a+0x60),
    program:read_u32(a+0x20),program:read_u16(m+0x210)))
  end
 end
end)
