-- Same physical two-round trial; add passive burst/global/timing observers.
local filename='mk2ks_native_kano_laser_typed_epochs.lua'
local file=assert(io.open(filename,'r'));local wrapper=file:read('a');file:close()
local boundary="assert(load(source,'@'..filename..'::allocation_epoch_successor'))()"
local instrumentation=[==[
local additions={
 {'local serial,bones,particles,emitters=0,0,0,0',
  'local serial,bones,particles,emitters=0,0,0,0\nlocal burst_jobs,quake_jobs={},{}'},
 {'local sent=false',[=[
tap(address(0xb0d00),'actual own independent burst constructor',function()
 if started then log('BURST_CREATE',string.format('actor=%08X main=%08X id=%d bg=%04X palette=%04X y32=%08X',cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A8.value+0x1f0),p:read_u16(0x105d070),p:read_u16(0x105d0b0),p:read_u32(0x105d130)))end
end)
tap(0xff9e1290,'actual native source-recipe shake constructor',function()
 if started and cpu.A11.value==0xc0012 then log('QUAKE_CREATE',string.format('actor=%08X main=%08X recipe=%08X y32=%08X',cpu.A8.value,cpu.A13.value,cpu.A11.value,p:read_u32(0x105d130)))end
end)
tap(address(0xb0d40),'actual independent flash worker',function()
 if started then
  local job=cpu.A13.value;assert(not burst_jobs[job])
  burst_jobs[job]={actor=cpu.A8.value,birth=frame}
  log('BURST_TASK',string.format('job=%08X actor=%08X owner=%08X type=%04X id=%d bg=%04X palette=%04X',job,cpu.A8.value,p:read_u32(job+0xc0),p:read_u16(job+0x20),p:read_u16(cpu.A8.value+0x1f0),p:read_u16(0x105d070),p:read_u16(0x105d0b0)))
 end
end)
tap(address(0xb0d80),'actual six-field flash private coroutine',function()
 local e=burst_jobs[cpu.A13.value]
 if started and e and not e.retired and cpu.A8.value==e.actor then
  e.flash=frame;e.background=p:read_u16(0x105d070)
  log('FLASH_ENTER',string.format('job=%08X actor=%08X id=%d life=%d bg=%04X palette=%04X sp=%08X private_sp=%08X',cpu.A13.value,cpu.A8.value,p:read_u16(cpu.A8.value+0x1f0),frame-e.birth,e.background,p:read_u16(0x105d0b0),cpu.SP.value,cpu.A12.value))
 end
end)
tap(address(0xb0da2),'actual flash background restoration',function()
 local e=burst_jobs[cpu.A13.value]
 if started and e and not e.retired then
  log('FLASH_RESTORE',string.format('job=%08X actor=%08X flash_fields=%d saved=%04X bg=%04X palette=%04X',cpu.A13.value,cpu.A8.value,frame-e.flash,cpu.A9.value&0xffff,p:read_u16(0x105d070),p:read_u16(0x105d0b0)))
 end
end)
tap(0xff9e1390,'actual native54field quake worker step',function()
 if started and frame-started>=164 and p:read_u16(cpu.A13.value+0x20)==0x103 then
  local job=cpu.A13.value;local e=quake_jobs[job]
  if not e then e={actor=cpu.A8.value,birth=frame,y=p:read_u32(0x105d130),steps=0};quake_jobs[job]=e end
  e.steps=e.steps+1
  log('QUAKE_STEP',string.format('job=%08X actor=%08X type=%04X step=%d remaining=%d amplitude=%08X y32=%08X',job,cpu.A8.value,p:read_u16(job+0x20),e.steps,cpu.A10.value,cpu.A11.value,p:read_u32(0x105d130)))
 end
end)
tap(0xff80de20,'actual independent burst/shake task retirement',function()
 local job=cpu.A13.value;local e=burst_jobs[job];local q=quake_jobs[job]
 if started and e and not e.retired and cpu.A8.value==e.actor and p:read_u16(job+0x20)==0x201 then
  e.retired=frame
  log('AUX_RETIRE',string.format('kind=flash job=%08X actor=%08X life=%d bg=%04X palette=%04X',job,cpu.A8.value,frame-e.birth,p:read_u16(0x105d070),p:read_u16(0x105d0b0)))
 elseif started and q and not q.retired and cpu.A8.value==q.actor and p:read_u16(job+0x20)==0x103 then
  q.retired=frame
  log('AUX_RETIRE',string.format('kind=quake job=%08X actor=%08X life=%d steps=%d initial_y32=%08X y32=%08X',job,cpu.A8.value,frame-q.birth,q.steps,q.y,p:read_u32(0x105d130)))
 end
end)
for _,where in ipairs({0x105d070,0x105d0b0,0x105d130})do
 local global=where;local width=global==0x105d130 and 32 or 16
 taps[#taps+1]=p:install_write_tap(global,global+width-1,'passive real background/palette/camera writes',function(at,data,mask)
  if started and frame-started>=160 and frame-started<=240 and at==global then
   log('GLOBAL_WRITE',string.format('at=%08X pc=%08X main=%08X actor=%08X data=%08X mask=%08X',at,cpu.PC.value,cpu.A13.value,cpu.A8.value,data,mask))
  end
 end)
end
local sent=false]=]},
 {'  if age<=750 then',[=[
  if age<=300 then
   log('BURST_FIELD',string.format('bg=%04X palette=%04X y32=%08X',p:read_u16(0x105d070),p:read_u16(0x105d0b0),p:read_u32(0x105d130)))
  end
  if age<=750 then]=]},
 {'[164]=true,[170]=true',
  '[164]=true,[165]=true,[166]=true,[167]=true,[168]=true,[169]=true,[170]=true,[171]=true,[172]=true,[173]=true,[174]=true,[175]=true,[176]=true,[217]=true,[218]=true,[219]=true,[220]=true'}
}
-- Expand only passive raster capture, not physical input/gameplay timing.
for _,pair in ipairs(additions)do
 local at=assert(source:find(pair[1],1,true));assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::allocation_epoch_successor'))()
]==]
local at=assert(wrapper:find(boundary,1,true));assert(not wrapper:find(boundary,at+#boundary,true))
wrapper=wrapper:sub(1,at-1)..instrumentation..wrapper:sub(at+#boundary)
assert(load(wrapper,'@'..filename..'::burst_timing_observer'))()
