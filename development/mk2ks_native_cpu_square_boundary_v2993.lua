-- Unchanged physical v1997 inputs and complete original v2039 drawing observer.
-- Add independent real action-entry snapshots and every native collision branch.
-- No guest state, characters, RNG, HP, stage, registers or controls are written.
dofile('mk2ks_physical_p2_cpu_square_display_v2039.lua')
do
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,serial=0,0
local taps={}
local slots={{a=0x01060220,m=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {a=0x01060df0,m=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function owns()
 local a,m=p:read_u32(slots[2].a),p:read_u32(slots[2].m)
 return p:read_u16(0x010601d0)==2 and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==0 and
 valid(a)and valid(m)and cpu.A8.value==a and cpu.A13.value==m and p:read_u32(m+0xc0)==a and
 p:read_u16(a+0x1f0)==18 and p:read_u16(slots[2].id)==18
end
local function log(tag,text)
 print(string.format('MK2_SQUARE_BOUNDARY_%s frame=%d serial=%d %s writes=0 assistance=none',tag,frame,serial,text))
end
for _,item in ipairs({{0xffffca00,'entry'},{0xffffcef0,'collision_return'},{0xffffd1c0,'hit_entry'}})do
 local address,kind=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual Square entry/collision branch '..kind,function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or not owns()then return end
  if kind=='entry'then
   serial=serial+1
   for side,s in ipairs(slots)do
    local a,m=p:read_u32(s.a),p:read_u32(s.m)
    assert(valid(a)and valid(m),'Actual native Square entry has both physical actors')
    log('ENTRY_STATE',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d mode=%d hp=%d action=%04X pose=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X facing=%04X trail=%08X floor=%d stage_floor=%d stage=%d schedule=%08X',
      side,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(s.id),p:read_u16(s.state),p:read_u16(0x010601d0),p:read_u16(s.hp),
      p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20),
      p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u16(a+0xf0),p:read_u32(m+0x190),p:read_i16(m+0x200),p:read_i16(0x0105ecd0),p:read_u16(0x01061b30),p:read_u32(0x01061b10)))
   end
  end
  local values={}
  for n=0,14 do values[#values+1]=string.format('a%d=%08X',n,cpu['A'..n].value)end
  log('EVENT',string.format('kind=%s entry=%08X pc=%08X opcode=%04X mask=%04X status=%08X carry=%d ',kind,at,cpu.PC.value,data,mask,cpu.ST.value,(cpu.ST.value>>30)&1)..table.concat(values,' '))
 end)
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for _,range in ipairs({{0xffffd1c0,0xffffd340},{0xff831a60,0xff831bc0},{0xff876be0,0xff876e00}})do
   local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
end
