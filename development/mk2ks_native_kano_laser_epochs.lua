-- Successor passive observer. Preserve the executed physical controller.
-- A loop visit is not a new allocation; an address reused after retirement
-- is not evidence that the old allocation remains alive.
local filename='mk2ks_native_kano_laser_action.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local changes={
 {'local serial,bones,particles,emitters=0,0,0,0',
  'local serial,bones,particles,emitters=0,0,0,0\nlocal retained_epochs={}'},
 { [=[local function epoch(kind)
 local job,actor=cpu.A13.value,cpu.A8.value;serial=serial+1
 local cache=valid(actor)and p:read_u32(actor+0x1a0)-0x100 or 0
 epochs[job]={serial=serial,kind=kind,birth=frame,actor=actor,cache=cache,active=true,seq=p:read_u32(job+0x250)}
 log('TASK',string.format('epoch=%d kind=%s job=%08X actor=%08X cache=%08X type=%04X seq=%08X count=%d',serial,kind,job,actor,cache,p:read_u16(job+0x20),p:read_u32(job+0x250),p:read_u32(job+0x80)))
end]=], [=[local function chain(head)
 local found={};local node=p:read_u32(head)
 for _=1,768 do
  if not valid(node)or found[node]then return found end
  found[node]=true;node=p:read_u32(node)
 end
 error('Native linked-list observation exceeded finite bound')
end
local function epoch(kind)
 local job,actor=cpu.A13.value,cpu.A8.value;local old=epochs[job]
 if kind=='emitter'and old and old.kind==kind and old.active and not old.final and old.actor==actor then
  log('EMIT',string.format('epoch=%d job=%08X victim=%08X count=%d',old.serial,job,actor,p:read_u32(job+0x80)))
  return
 end
 if old and not old.final then
  log('REUSE',string.format('epoch=%d kind=%s job=%08X retired=%d mass=%d',old.serial,old.kind,job,old.retired or-1,old.mass or-1))
  old.final=true
 end
 serial=serial+1
 local owner=actor;local cache=kind=='particle'and p:read_u32(actor+0x1a0)-0x100 or 0
 if kind=='bone'then actor=0 end -- real child is only known AFTER the native allocator
 local e={serial=serial,kind=kind,birth=frame,actor=actor,owner=owner,cache=cache,active=true,seq=p:read_u32(job+0x250),job=job}
 epochs[job]=e;retained_epochs[#retained_epochs+1]=e
 log('TASK',string.format('epoch=%d kind=%s job=%08X actor=%08X owner=%08X cache=%08X type=%04X seq=%08X count=%d',serial,kind,job,actor,owner,cache,p:read_u16(job+0x20),e.seq,p:read_u32(job+0x80)))
 if kind=='emitter'then
  emitters=emitters+1;log('EMIT',string.format('epoch=%d job=%08X victim=%08X count=%d',serial,job,owner,p:read_u32(job+0x80)))
 end
end
tap(0xff9f31e0,'actual bone child after native initializer',function()
 local e=epochs[cpu.A13.value]
 if started and e and e.kind=='bone'and e.active and not e.final and not e.object then
  e.actor=cpu.A8.value;e.object=true
  log('OBJECT',string.format('epoch=%d kind=bone job=%08X actor=%08X owner=%08X seq=%08X',e.serial,e.job,e.actor,e.owner,p:read_u32(e.job+0x250)))
 end
end)
tap(0xff80e550,'actual native masked task unlink',function()
 local target=cpu.A2.value;local e=epochs[target]
 if started and e and not e.final then
  log('MASS',string.format('epoch=%d kind=%s job=%08X actor=%08X type=%04X selector=%08X mask=%08X current=%08X',e.serial,e.kind,target,e.actor,p:read_u16(target+0x20),cpu.A0.value,cpu.A1.value,cpu.A13.value))
  e.mass=frame
 end
end)]=]},
 {"if started then emitters=emitters+1;epoch('emitter')end", "if started then epoch('emitter')end"},
 {'  if age<=450 then','  if age<=750 then'},
 { [=[  for job,e in pairs(epochs)do
   if e.retired==frame and not e.checked then e.checked=true
    log('EPOCH_END',string.format('epoch=%d kind=%s job=%08X actor=%08X cache=%08X life=%d active=%s free=%s cache_active=%s render_primary=%s render_secondary=%s render_tertiary=%s',e.serial,e.kind,job,e.actor,e.cache,frame-e.birth,membership(job,0x01068e30),membership(job,0x01068e50),membership(e.cache,0x01068e30),membership(e.actor,0x0105d480),membership(e.actor,0x0105d4a0),membership(e.actor,0x0105d4c0)))
   end
  end]=], [=[  local active,free=chain(0x01068e30),chain(0x01068e50)
  local primary,secondary,tertiary=chain(0x0105d480),chain(0x0105d4a0),chain(0x0105d4c0)
  for job,e in pairs(epochs)do
   if not e.final then
    local colors={};local a=e.actor
    if e.kind=='particle'then
     local bank=p:read_u16(a+0x140)&0x7f00
     for pen=0,15 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01880000+(bank+pen)*16))end
    end
    log('EFFECT_FIELD',string.format('epoch=%d kind=%s job=%08X actor=%08X cache=%08X life=%d active=%d free=%d cache_active=%d lists=%d,%d,%d type=%04X seq=%08X colors=%s x=%d y=%d vx=%08X vy=%08X pose=%08X',e.serial,e.kind,job,a,e.cache,frame-e.birth,active[job]and 1 or 0,free[job]and 1 or 0,active[e.cache]and 1 or 0,primary[a]and 1 or 0,secondary[a]and 1 or 0,tertiary[a]and 1 or 0,p:read_u16(job+0x20),p:read_u32(job+0x250),table.concat(colors,','),valid(a)and p:read_i16(a+0x90)or 0,valid(a)and p:read_i16(a+0xb0)or 0,valid(a)and p:read_u32(a+0x40)or 0,valid(a)and p:read_u32(a+0x60)or 0,valid(a)and p:read_u32(a+0x1d0)or 0))
    if not active[job]then e.final=true;e.active=false end
   end
  end
  if age>=610 and age<=650 or age==750 then
   local visible,active_count,cache_count=0,0,0
   for _,e in ipairs(retained_epochs)do
    if primary[e.actor]or secondary[e.actor]or tertiary[e.actor]then visible=visible+1 end
    if active[e.job]then active_count=active_count+1 end
    if active[e.cache]then cache_count=cache_count+1 end
   end
   log('SCENE',string.format('mode=%d primary=%08X secondary=%08X tertiary=%08X retained=%d reused_pointer_render_hits=%d reused_pointer_active_hits=%d reused_pointer_cache_hits=%d',p:read_u16(0x010601d0),p:read_u32(0x0105d480),p:read_u32(0x0105d4a0),p:read_u32(0x0105d4c0),#retained_epochs,visible,active_count,cache_count))
  end]=]}
}
for _,pair in ipairs(changes)do
 local at=assert(source:find(pair[1],1,true));assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::allocation_epoch_successor'))()
