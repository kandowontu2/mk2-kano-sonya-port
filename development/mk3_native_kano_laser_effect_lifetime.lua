-- Physically earned original laser; passive real task/object lifetimes.
-- Freeze all earlier controllers. No guest memory/register/state writes.
local filename='mk3_native_secondary_kano_source_distance.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local boundary="assert(load(source,'@'..filename..'::original_source_distance'))()"
local instrumentation=[==[
local additions={
 {'local lastposes,objects,pending={},{},{}',[=[
local laser_effect_jobs,laser_effect_objects,laser_effect_serial={},{},0
local function effect_chain(head,limit)
 local found={};local at=p:read_u32(head)
 for _=1,limit do
  if not valid(at)or found[at]then break end
  found[at]=true;at=p:read_u32(at)
 end
 return found
end
local function effect_born(kind,job)
 assert(valid(job));laser_effect_serial=laser_effect_serial+1
 local record={kind=kind,job=job,epoch=laser_effect_serial,born=frame-start}
 laser_effect_jobs[job]=record
 log('EFFECT_BORN',string.format('age=%d kind=%s job=%08X epoch=%d type=%04X entry=%08X saved_actor=%08X mode=%08X',
  frame-start,kind,job,record.epoch,p:read_u16(job+0x20),p:read_u32(job+0xe0),p:read_u32(job+0xc0),p:read_u32(job+0x80)))
end
local lastposes,objects,pending={},{},{}]=]},
 {"  for _,where in ipairs({0xff9b5cd0",[=[
  for _,where in ipairs({0xff9b6740,0xff9b6890,0xffa951a0,0xffa95270,0xffa95320,0xffa95650,0xff9602a0,0xff926ac0,0xff9271f0})do
   local at=where
   taps[#taps+1]=p:install_read_tap(at,at+15,'passive original effect allocation epoch',function(address)
    if address~=at or cpu.PC.value~=at+16 or not start then return end
    local job=cpu.A13.value;local record=laser_effect_jobs[job]
    if at==0xff9b6740 or at==0xff9b6890 then effect_born('emitter',cpu.A0.value)
    elseif at==0xffa95270 then effect_born('smoke',cpu.A0.value)
    elseif at==0xffa951a0 and record then
     log('EFFECT_EMIT',string.format('age=%d kind=%s job=%08X epoch=%d count=%d victim=%08X',frame-start,record.kind,job,record.epoch,cpu.A10.value,cpu.A8.value))
    elseif at==0xffa95320 and record then
     record.actor=cpu.A8.value;laser_effect_objects[record.actor]=record
     log('EFFECT_OBJECT',string.format('age=%d job=%08X epoch=%d actor=%08X bank=%04X',frame-start,job,record.epoch,record.actor,p:read_u16(record.actor+0x140)))
    elseif at==0xffa95650 and record then
     log('EFFECT_ANIMATION_END',string.format('age=%d job=%08X epoch=%d actor=%08X born=%d fields=%d',frame-start,job,record.epoch,cpu.A8.value,record.born,frame-start-record.born))
    elseif at==0xff9602a0 then
     local object=cpu.A0.value;local own=laser_effect_objects[object]
     if own then log('EFFECT_OBJECT_DELETE',string.format('age=%d job=%08X epoch=%d actor=%08X',frame-start,own.job,own.epoch,object))end
    elseif at==0xff926ac0 and record then
     record.retired=frame-start
     log('EFFECT_RETIRED',string.format('age=%d kind=%s job=%08X epoch=%d actor=%08X born=%d fields=%d',frame-start,record.kind,job,record.epoch,record.actor or 0,record.born,frame-start-record.born))
    elseif at==0xff9271f0 then
     local deleted=cpu.A2.value;local own=laser_effect_jobs[deleted]
     if own then log('EFFECT_MASS',string.format('age=%d kind=%s job=%08X epoch=%d actor=%08X type=%04X selector=%08X mask=%08X',frame-start,own.kind,deleted,own.epoch,own.actor or 0,p:read_u16(deleted+0x20),cpu.A0.value,cpu.A1.value))end
    end
   end)
  end
  for _,where in ipairs({0xff9b5cd0]=]},
 {"  geometry('FIELD')",[=[
  geometry('FIELD')
  local active=effect_chain(0x01069b90,512);local free=effect_chain(0x01069bb0,512)
  local object_free=effect_chain(0x010608c0,768)
  local lists={effect_chain(0x0105dc10,768),effect_chain(0x0105dc30,768),effect_chain(0x0105dc50,768)}
  for job,record in pairs(laser_effect_jobs)do
   if not record.final then
    local actor=record.actor;local colors={};local bank=actor and p:read_u16(actor+0x140)&0x7f00 or 0
    if actor then for pen=0,15 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01880000+(bank+pen)*16))end end
    log('EFFECT_FIELD',string.format('age=%d kind=%s job=%08X epoch=%d active=%d free=%d type=%04X entry=%08X actor=%08X actor_free=%d lists=%d,%d,%d bank=%04X colors=%s x=%d y=%d vx=%08X vy=%08X pose=%08X',
     frame-start,record.kind,job,record.epoch,active[job]and 1 or 0,free[job]and 1 or 0,p:read_u16(job+0x20),p:read_u32(job+0xe0),actor or 0,
     actor and object_free[actor]and 1 or 0,actor and lists[1][actor]and 1 or 0,actor and lists[2][actor]and 1 or 0,actor and lists[3][actor]and 1 or 0,
     bank,table.concat(colors,','),actor and p:read_i16(actor+0x90)or 0,actor and p:read_i16(actor+0xb0)or 0,
     actor and p:read_u32(actor+0x40)or 0,actor and p:read_u32(actor+0x60)or 0,actor and p:read_u32(actor+0x1d0)or 0))
    if not active[job]then record.final=true end
   end
  end]=]},
 {'{1,24,60,120,180,300,450}','{1,68,72,100,102,106,132,162,164,170,180,196,200,240,300,450,480,600,750}'},
 {'  if age>=451 then','  if age>=751 then'}
}
for _,pair in ipairs(additions)do
 local at=assert(source:find(pair[1],1,true));assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::laser_effect_lifetime'))()
]==]
local at=assert(source:find(boundary,1,true));assert(not source:find(boundary,at+#boundary,true))
source=source:sub(1,at-1)..instrumentation..source:sub(at+#boundary)
assert(load(source,'@'..filename..'::laser_effect_lifetime_wrapper'))()
