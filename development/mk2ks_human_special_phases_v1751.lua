-- The immutable v3 scenario owns every physical input. Only observe here.
-- Consecutive full-size scene captures, actual native fighter FIFO parts,
-- and end-of-field actor state; no guest, AI, difficulty or position writes.
local original_print=print
local origin,recovery,frame,snaps=nil,nil,0,0
print=function(...)
 local values={...}
 for _,line in ipairs(values)do
  if type(line)=='string' then
   local command=line:match('^MK2_HSPECIAL_COMMAND frame=(%d+) ')
   local recovered=line:match('^MK2_HSPECIAL_RECOVERED frame=(%d+) ')
   if command then assert(not origin);origin=tonumber(command)end
   if recovered then assert(not recovery);recovery=tonumber(recovered)end
  end
 end
 original_print(...)
end
dofile('mk2ks_human_special_matrix_v3.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local move=assert(os.getenv('MK2KS_HUMAN_SPECIAL_MOVE'))
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local slots={0x01060220,0x01060df0}
local function active()return origin and frame>=origin and frame<=origin+416 and(not recovery or frame<=recovery+12)end
local function log(tag,value)
 original_print(string.format('MK2_HPHASE_%s frame=%d move=%s side=%d writes=0 assistance=none %s',tag,frame,move,side,value or''))
end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local tap=p:install_read_tap(0xff804410,0xff80441f,'actual special-phase physical FIFO',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 or not active()then return end
 for slot,field in ipairs(slots)do
  local a,m=p:read_u32(field),p:read_u32(field+0x40)
  if a==cpu.A0.value and valid(a)and valid(m)then
   local cache=p:read_u32(a+0x1a0);local row=cpu.A3.value-112
   assert(valid(cache)and row>=cache and row<cache+12*112 and(row-cache)%112==0)
   log('QUEUE',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d pose=%08X cache=%08X part=%d row=%08X source=%08X size=%08X xy=%08X command=%08X palette=%08X pc=%08X',
    slot,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(field+0x60),p:read_u32(a+0x1d0),cache,(row-cache)//112,row,cpu.A11.value,cpu.A9.value,cpu.A10.value,cpu.A12.value,cpu.A6.value,cpu.PC.value))
  end
 end
end)
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 if not active()then return end
 local file=string.format('phase_%05d.png',frame);screen:snapshot(file);snaps=snaps+1
 log('SNAP',string.format('file=%s age=%d recovery=%d',file,frame-origin,recovery or-1))
 for slot,field in ipairs(slots)do
  local a,m=p:read_u32(field),p:read_u32(field+0x40);assert(valid(a)and valid(m))
  log('ACTOR',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d hp=%d pose=%08X cache=%08X x=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X action=%d body=%04X flags=%04X stageY=%d arena=%d',
   slot,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(field+0x60),p:read_u16(field+0xd0),p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_i16(a+0x90),p:read_i16(a+0xb0),p:read_i16(m+0x200),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20),p:read_u16(m+0x1f0),p:read_u16(a+0x160),p:read_u16(m+0x210),p:read_i16(0x0105ecd0),p:read_u16(0x01061ac0)))
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('origin=%d recovery=%d snaps=%d fullPortAcceptance=false rasterAcceptance=false',origin or-1,recovery or-1,snaps))
 tap:remove();print=original_print
end)
