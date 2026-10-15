-- Entire original physical driver and native scene observer, RAM media transport only.
local allowed={
 ['mk2ks_physical_p2_cpu_continuation_v1997.lua']=6,
 ['mk2ks_physical_p2_cpu_round_trace_v1998.lua']=0,
 ['mk2ks_physical_p2_cpu_overlap_trace_v1999.lua']=1,
 ['mk2ks_physical_p2_cpu_choice_trace_v2035.lua']=1,
 ['mk2ks_physical_p2_cpu_square_trace_v2038.lua']=0,
 ['mk2ks_physical_p2_cpu_square_display_v2039.lua']=0,
 ['mk2ks_native_cpu_square_boundary_v2993.lua']=0,
 ['mk2ks_native_cpu_square_locks_v3000.lua']=0}
local loaded={}
local environment=setmetatable({}, {__index=_G})
environment.snapshot_ram=function(label)print('MK2_SCENE_ORIGINAL_MARK label='..label..' writes=0 assistance=none')end
environment.dofile=function(name)
 local snapshots=assert(allowed[name],'Only original physical/native observer chain')
 assert(not loaded[name],'Every original source loaded once');loaded[name]=true
 local f=assert(io.open(name,'rb'));local source=f:read('*a'):gsub('\r\n','\n');f:close()
 local function change(before,after)
  local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
  source=source:sub(1,at-1)..after..source:sub(at+#before)
 end
 if name=='mk2ks_physical_p2_cpu_square_display_v2039.lua'then
  change(" local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",
   " print(string.format('MK2_SCENE_RAM label=%s bytes=%d hex=%s',file,#raw,raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))")
  change(" local file=string.format('display_%d.png',frame);screen:snapshot(file)",
   " local file=string.format('display_%d.rgb',frame);local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400);save(file,raw)")
 end
 local count
 source,count=source:gsub("manager.machine.screens%[':screen'%]:snapshot",'snapshot_ram')
 assert(count==snapshots,'Exact original media transport call count')
 assert(not source:find(':snapshot',1,true)and not source:find("io.open(output",1,true),'No persistent ROM/VRAM/RGB media')
 return assert(load(source,'@'..name,'t',environment))()
end
environment.dofile('mk2ks_native_cpu_square_locks_v3000.lua')
for name in pairs(allowed)do assert(loaded[name],'Whole original input/scene/collision/entry chain loaded')end
