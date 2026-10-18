-- Observe the actual random fourteen-fighter attract roster. No forced state.
local m=manager.machine
local cpu=m.devices[':maincpu']
local p=cpu.spaces.program
local function u16(a) return p:read_u8(a)|(p:read_u8(a+8)<<8) end
local function u32(a)
 local v=0
 for i=0,3 do v=v|(p:read_u8(a+i*8)<<(i*8)) end
 return v
end
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
local tag=assert(tonumber(os.getenv('KS_MISSING_TAG')))
local actor=assert(tonumber(os.getenv('KS_MISSING_ACTOR')))
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local budget=tonumber(os.getenv('KS_CPU_FIELDS') or '30000')
local ackStart=tonumber(os.getenv('KS_CPU_ACK_START') or '0')
local log=assert(io.open('cpu_attract.csv','w'))
log:write('frame,mode,p1selected,p2selected,p1char,p2char,p1hp,p2hp,p1action,p2action,p1shape,p2shape,missing,missingTag,missingActor,pc\n')
local n=0
local seen={}
local combatSeen={}
emu.register_frame_done(function()
 n=n+1
 -- Only acknowledge startup diagnostics; no coins, Starts or gameplay inputs.
 for _,port in pairs(m.ioport.ports) do
  if port.fields['P1 High Punch'] then port.fields['P1 High Punch']:set_value(n>=ackStart and n<3000 and n%40<4 and 1 or 0) end
 end
 local a,b=u32(0x01060220),u32(0x01060df0)
 local c1,c2=a~=0 and u16(a+0x1f0) or -1,b~=0 and u16(b+0x1f0) or -1
 local proc1,proc2=u32(0x01060260),u32(0x01060e30)
 local count=u32(missing)
 local pc=cpu.state['PC'].value
 local badpc=n>3000 and (c1==17 or c1==18 or c2==17 or c2==18) and pc<0xff800000
 if n%2==0 or count>0 or pc==recovery or badpc then
  log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%d,%d,%d,%08x\n',n,u16(0x010601d0),u16(0x01060280),u16(0x01060e50),c1,c2,
   u16(0x010602f0),u16(0x01060ec0),proc1~=0 and u16(proc1+0x1f0) or 0,proc2~=0 and u16(proc2+0x1f0) or 0,
   a~=0 and u32(a+0x1d0) or 0,b~=0 and u32(b+0x1d0) or 0,count,u16(tag),u16(actor),cpu.state['PC'].value))
 end
 for _,c in ipairs({c1,c2}) do
  if n>3000 and (c==17 or c==18) and not seen[c] then
   seen[c]=n;m.screens[':screen']:snapshot(string.format('cpu_actor%d_%d.png',c,n))
  end
  if seen[c] and not combatSeen[c] and n-seen[c]>=60 and
     u16(0x010602f0)>0 and u16(0x01060ec0)>0 and
     (u16(0x010602f0)<161 or u16(0x01060ec0)<161) then
   combatSeen[c]=true
   m.screens[':screen']:snapshot(string.format('cpu_actor%d_combat_%d.png',c,n))
  end
 end
 if n%120==0 then log:flush() end
 if pc==recovery or badpc then
  local fault=assert(io.open('cpu_fault.txt','w'))
  fault:write(string.format('frame=%d PC=%08x recovery=%08x\n',n,pc,recovery))
  for name,reg in pairs(cpu.state) do fault:write(name,'=',string.format('%08x',reg.value),'\n') end
  for _,base in ipairs({proc1,proc2}) do
   if base>=0x01000000 and base<0x01100000 then
    for i=0,47 do fault:write(string.format('process %08x=%08x\n',base+i*32,u32(base+i*32))) end
   end
  end
  fault:close()
 end
 if count>0 or pc==recovery or badpc or n>=budget then log:close();m:exit() end
end)
