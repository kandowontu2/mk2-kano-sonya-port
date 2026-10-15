-- Original extended physical CPU driver/choice/startup taps, new RAM-only observer transport.
-- Replace the old file-writing display observer with the full original native body/shadow observer.
local f=assert(io.open('mk2ks_cpu_choke_shadow_v5328.lua','rb'))
local source=f:read('*a'):gsub('\r\n','\n');f:close()
local function change(before,after)
 local a=assert(source:find(before,1,true));assert(not source:find(before,a+1,true))
 source=source:sub(1,a-1)..after..source:sub(a+#before)
end
change("local move,side,attempt,air='choke',2,1,false","local move,side,attempt,air='square',2,1,false")
change("local expected={human=='kano'and 17 or 18,17}","local expected={human=='kano'and 17 or 18,18}")
local before=[[local file=assert(io.open('mk2ks_cpu_recovery_probe_v1438.lua','rb'))
local driver=file:read('*a'):gsub('\r\n','\n');file:close()
local count
driver,count=driver:gsub("manager.machine.screens%[':screen'%]:snapshot",'snapshot_ram')
assert(count==6,'Exact original physical driver media transport substitutions')
assert(not driver:find(':snapshot',1,true),'No original media file writes')
assert(load(driver,'@mk2ks_cpu_recovery_probe_v1438.lua','t',environment))()]]
local after=[=[local allowed={
 ['mk2ks_physical_p2_cpu_continuation_v1997.lua']=6,
 ['mk2ks_physical_p2_cpu_round_trace_v1998.lua']=0,
 ['mk2ks_physical_p2_cpu_overlap_trace_v1999.lua']=1,
 ['mk2ks_physical_p2_cpu_choice_trace_v2035.lua']=1,
 ['mk2ks_physical_p2_cpu_square_trace_v2038.lua']=0,
 ['mk2ks_native_cpu_square_boundary_v2993.lua']=0,
 ['mk2ks_native_cpu_square_locks_v3000.lua']=0}
local loaded={}
environment.dofile=function(name)
 local snapshots=assert(allowed[name],'Only exact original physical/read-only sources')
 assert(not loaded[name],'Each original source loaded exactly once');loaded[name]=true
 local file=assert(io.open(name,'rb'));local driver=file:read('*a'):gsub('\r\n','\n');file:close()
 if name=='mk2ks_native_cpu_square_boundary_v2993.lua'then
  local before="dofile('mk2ks_physical_p2_cpu_square_display_v2039.lua')"
  local at=assert(driver:find(before,1,true));assert(not driver:find(before,at+1,true))
  driver=driver:sub(1,at-1).."dofile('mk2ks_physical_p2_cpu_square_trace_v2038.lua')"..driver:sub(at+#before)
 end
 local count
 driver,count=driver:gsub("manager.machine.screens%[':screen'%]:snapshot",'snapshot_ram')
 assert(count==snapshots,'Exact original snapshot transport substitution count')
 assert(not driver:find(':snapshot',1,true),'No old media files')
 return assert(load(driver,'@'..name,'t',environment))()
end
environment.dofile('mk2ks_native_cpu_square_locks_v3000.lua')
for name in pairs(allowed)do assert(loaded[name],'Entire original controller/provenance chain loaded')end
local square_origin
local observer_tap=p:install_read_tap(0xffffca00,0xffffca0f,'RAM preview actual native CPU Square',function(at)
 local own=sample(2)
 local cpu=manager.machine.devices[':maincpu'].state
 if at==0xffffca00 and cpu.PC.value==0xffffca10 and own and pair_live(sample(1),own)
  and cpu.A8.value==own.actor and cpu.A13.value==own.main then
  square_origin=frame;marks[frame]='cpu_square_entry'
 end
end)
taps[#taps+1]=observer_tap
emu.register_frame(function()
 if square_origin then
  local age=frame-square_origin
  if({[8]=true,[9]=true,[19]=true,[35]=true,[39]=true,[70]=true})[age]then marks[frame]='cpu_square_phase_'..age end
 end
end)]=]
change(before,after)
assert(load(source,'@CPU_Square_original_input_chain_RAM_body_shadow_v5341','t',_G))()
