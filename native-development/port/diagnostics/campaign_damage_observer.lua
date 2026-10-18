-- Bounded read-only evidence window; never drives inputs or alters game state.
local damageMachine=manager.machine
local damageSpace=damageMachine.devices[':maincpu'].spaces.program
local function dw(a) return damageSpace:read_u8(a)|(damageSpace:read_u8(a+8)<<8) end
local function dl(a) return dw(a)|(dw(a+16)<<16) end
local function ds(a) local v=dw(a);return v<0x8000 and v or v-0x10000 end
local begin=assert(tonumber(os.getenv('KS_DAMAGE_BEGIN')))
local finish=assert(tonumber(os.getenv('KS_DAMAGE_END')))
local objects=assert(tonumber(os.getenv('KS_OBJECT_LIST')))
local processes=assert(tonumber(os.getenv('KS_ACTIVE_LIST')))
local queue=assert(tonumber(os.getenv('KS_DAMAGE_JCQ')))
local tick=assert(tonumber(os.getenv('KS_DAMAGE_TICK')))
local ground=assert(tonumber(os.getenv('KS_DAMAGE_GROUND')))
assert(begin>0 and finish>begin and finish-begin<=300)
local objectLog=assert(io.open('damage_objects.csv','w'))
local processLog=assert(io.open('damage_processes.csv','w'))
local queueLog=assert(io.open('damage_queue.csv','w'))
local boundsLog=assert(io.open('damage_bounds.csv','w'))
boundsLog:write('frame,player,object,y,highest,parts,ground,action,animationGround\n')
queueLog:write('frame,tick,next,sw1,time1,sw2,time2,sw3,time3,sw4,time4,sw5,time5,sw6,time6\n')
objectLog:write('frame,object,char,x,y,shape,image,flags,flags2\n')
processLog:write('frame,process,pid,wake,object,otherObject,otherProcess,action,flags,animation\n')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if frame<begin or frame>finish then return end
 -- Mirror MKUTIL.highest_mpart exactly: 112-bit multipart records, signed
 -- Y offset at bit 96. Read only the two actual player objects, not effects.
 for player=1,2 do
  local obj=dl(player==1 and 0x01060220 or 0x01060df0)
  local proc=dl(player==1 and 0x01060260 or 0x01060e30)
  if obj~=0 and proc~=0 then
   local part=dl(obj+0x1a0);local highest=65535;local parts=0
   while part~=0 do
    assert(part>=0x01000000 and part+112<0x01400000 and parts<64,'Invalid player multipart bounds')
    highest=math.min(highest,ds(obj+0xb0)-ds(part+96));parts=parts+1
    part=part+112
    if dl(part)==0 then break end
   end
   boundsLog:write(string.format('%d,%d,%08x,%d,%d,%d,%d,%04x,%d\n',frame,player,obj,
    ds(obj+0xb0),highest,parts,ds(ground),dw(proc+0x1f0),ds(proc+0x200)))
  end
 end
 local cursor=dl(queue)
 assert(cursor>=queue+32 and cursor<=queue+20*32,'Invalid native joystick queue pointer')
 local fields={frame,dw(tick),string.format('%08x',cursor)}
 for _=1,6 do
  cursor=cursor-32
  if cursor<=queue then cursor=cursor+20*32 end
  local entry=dl(cursor)
  fields[#fields+1]=(entry>>16)&65535;fields[#fields+1]=entry&65535
 end
 queueLog:write(table.concat(fields,',')..'\n')
 if (frame-begin)%20==0 then damageMachine.screens[':screen']:snapshot(string.format('damage_%05d.png',frame)) end
 local current=dl(objects);local seen={};local count=0
 while current~=0 do
  assert(current>=0x01000000 and current<0x01400000 and not seen[current] and count<512)
  seen[current]=true;count=count+1
  objectLog:write(string.format('%d,%08x,%d,%d,%d,%08x,%08x,%04x,%04x\n',
   frame,current,dw(current+0x1f0),ds(current+0x90),ds(current+0xb0),dl(current+0x1d0),dl(current+0x1a0),dw(current+0xf0),dw(current+0x160)))
  current=dl(current)
 end
 current=dl(processes);seen={};count=0
 while current~=0 do
  assert(current>=0x01000000 and current<0x01400000 and not seen[current] and count<512)
  seen[current]=true;count=count+1
  processLog:write(string.format('%d,%08x,%04x,%08x,%08x,%08x,%08x,%04x,%04x,%08x\n',frame,
   current,dw(current+0x20),dl(current+0xe0),dl(current+0xc0),dl(current+0x140),dl(current+0x170),dw(current+0x1f0),dw(current+0x210),dl(current+0xa0)))
  current=dl(current)
 end
 if frame==finish then objectLog:close();processLog:close();queueLog:close();boundsLog:close()
 elseif frame%16==0 then objectLog:flush();processLog:flush();queueLog:flush();boundsLog:flush() end
end)
