-- Normal physical v1997 inputs and complete source-derived native render only.
-- Both true CPU mobility entries, initial stores and native collision branches.
dofile('mk2ks_native_cpu_bicycle_display_v3105.lua')
do
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,serial,start,move=0,0,-1000,'none'
local taps,bound={},{}
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
 print(string.format('MK2_MOBILITY_%s frame=%d serial=%d move=%s %s writes=0 assistance=none',tag,frame,serial,move,text))
end
local function bind(side,s,a,main)
 for _,kind in ipairs({'action','body','flags'})do
  local address=kind=='body'and a+0x160 or main+(kind=='action'and 0x1f0 or 0x210)
  local key=string.format('%d:%s:%08X',side,kind,address)
  if not bound[key]then
   bound[key]=true
   taps[#taps+1]=p:install_write_tap(address,address+15,'native mobility state provenance '..key,function(at,value,mask)
    if at~=address or serial==0 or frame>start+120 or p:read_u16(0x010601d0)~=2 or
     p:read_u32(s.a)~=a or p:read_u32(s.m)~=main then return end
    log('FLAG',string.format('slot=%d kind=%s at=%08X before=%04X after=%04X mask=%04X pc=%08X a8=%08X a13=%08X op0=%04X op1=%04X actor=%08X main=%08X owner=%08X id=%d state=%d',
     side,kind,at,p:read_u16(at),value&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,
     p:read_u16(cpu.PC.value-32),p:read_u16(cpu.PC.value-16),a,main,p:read_u32(main+0xc0),p:read_u16(a+0x1f0),p:read_u16(s.state)))
   end)
  end
 end
end
for _,item in ipairs({{0xffffca00,'square_entry'},{0xffffcef0,'square_collision'},{0xffffd1c0,'square_hit'},
 {0xfff9a400,'bicycle_entry'},{0xfff9aa30,'bicycle_collision'},{0xfff9acf0,'bicycle_contact'},
 {0xff876660,'native_fall'}})do
 local address,kind=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual native mobility '..kind,function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or not owns()then return end
  local action=p:read_u16(cpu.A13.value+0x1f0)
  if kind=='native_fall'and action~=0x611 and action~=0x207 then return end
  if kind=='square_entry'or kind=='bicycle_entry'then
   serial=serial+1;start=frame;move=kind=='square_entry'and'square'or'bicycle'
   for side,s in ipairs(slots)do
    local a,m=p:read_u32(s.a),p:read_u32(s.m)
    assert(valid(a)and valid(m)and p:read_u32(m+0xc0)==a,'Both actual mobility entry owners')
    log('ENTRY_STATE',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d mode=%d hp=%d action=%04X pose=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X facing=%04X trail=%08X floor=%d stage_floor=%d stage=%d schedule=%08X',
     side,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(s.id),p:read_u16(s.state),p:read_u16(0x010601d0),p:read_u16(s.hp),
     p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20),
     p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u16(a+0xf0),p:read_u32(m+0x190),p:read_i16(m+0x200),p:read_i16(0x0105ecd0),p:read_u16(0x01061b30),p:read_u32(0x01061b10)))
    bind(side,s,a,m)
   end
  end
  local values={};for n=0,14 do values[#values+1]=string.format('a%d=%08X',n,cpu['A'..n].value)end
  log('EVENT',string.format('kind=%s entry=%08X pc=%08X opcode=%04X mask=%04X status=%08X carry=%d actor=%08X main=%08X owner=%08X id=18 action=%04X ',
   kind,at,cpu.PC.value,data,mask,cpu.ST.value,(cpu.ST.value>>30)&1,cpu.A8.value,cpu.A13.value,p:read_u32(cpu.A13.value+0xc0),action)..table.concat(values,' '))
 end)
end
for side,s in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(s.hp,s.hp+15,'native mobility boundary health '..side,function(at,value,mask)
  if at~=s.hp or serial==0 or frame>start+120 or p:read_u16(0x010601d0)~=2 then return end
  log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X op0=%04X op1=%04X op2=%04X',
   side,at,p:read_u16(at),value&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,
   p:read_u16(cpu.PC.value-48),p:read_u16(cpu.PC.value-32),p:read_u16(cpu.PC.value-16)))
 end)
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for _,range in ipairs({{0xfff9a400,0xfff9d000},{0xffffd1c0,0xffffd340},{0xff831a60,0xff831bc0},{0xff876be0,0xff876e00}})do
   local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
end
