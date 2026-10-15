-- Original physical inputs/display and v2993 entry/collision snapshots retained.
-- Bind read-only write observers at actual instruction entry, before the move
-- locks its Main, including the first mode7-to-mode2 startup instruction window.
dofile('mk2ks_native_cpu_square_boundary_v2993.lua')
do
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,serial,start=0,0,-1000
local taps,bound={},{}
local slots={{a=0x01060220,m=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {a=0x01060df0,m=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_SQUARE_LOCK_%s frame=%d serial=%d %s writes=0 assistance=none',tag,frame,serial,text))
end
local function scope()return serial>0 and frame<=start+85 and p:read_u16(0x010601d0)==2 end
taps[#taps+1]=p:install_read_tap(0xffffca00,0xffffca0f,'bind actual Square initial locks',function(at,data,mask)
 local own,m=p:read_u32(slots[2].a),p:read_u32(slots[2].m)
 if at~=0xffffca00 or cpu.PC.value~=0xffffca10 or p:read_u16(0x010601d0)~=2 or
  p:read_u16(slots[1].state)~=1 or p:read_u16(slots[2].state)~=0 or not valid(own)or not valid(m)or
  cpu.A8.value~=own or cpu.A13.value~=m or p:read_u32(m+0xc0)~=own or p:read_u16(own+0x1f0)~=18 then return end
 serial=serial+1;start=frame
 for side,s in ipairs(slots)do
  local a,main=p:read_u32(s.a),p:read_u32(s.m)
  assert(valid(a)and valid(main)and p:read_u32(main+0xc0)==a,'Both real entry owners')
  for _,kind in ipairs({'action','body','flags'})do
   local address=kind=='body'and a+0x160 or main+(kind=='action'and 0x1f0 or 0x210)
   local key=string.format('%d:%s:%08X',side,kind,address)
   if not bound[key]then
    bound[key]=true
    taps[#taps+1]=p:install_write_tap(address,address+15,'Square entry state provenance '..key,function(offset,value,fieldmask)
     if offset~=address or not scope()or p:read_u32(s.a)~=a or p:read_u32(s.m)~=main then return end
     log('FLAG',string.format('slot=%d kind=%s at=%08X before=%04X after=%04X mask=%04X pc=%08X a8=%08X a13=%08X a0=%08X a1=%08X op0=%04X op1=%04X actor=%08X main=%08X owner=%08X id=%d state=%d',
      side,kind,address,p:read_u16(address),value&0xffff,fieldmask,cpu.PC.value,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A1.value,
      p:read_u16(cpu.PC.value-32),p:read_u16(cpu.PC.value-16),a,main,p:read_u32(main+0xc0),p:read_u16(a+0x1f0),p:read_u16(s.state)))
    end)
   end
  end
 end
end)
for side,s in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(s.hp,s.hp+15,'Square boundary health provenance '..side,function(at,value,mask)
  if at~=s.hp or not scope()then return end
  log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X op0=%04X op1=%04X op2=%04X',
   side,at,p:read_u16(at),value&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,
   p:read_u16(cpu.PC.value-48),p:read_u16(cpu.PC.value-32),p:read_u16(cpu.PC.value-16)))
 end)
end
emu.register_frame(function()frame=frame+1 end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
end
