-- Existing natural P2-CPU physical/body/shadow/channel probe, with complete
-- original passive child/guard provenance. No additional physical controller.
local function read(name)
 local file=assert(io.open(name,'rb'));local source=file:read('*a'):gsub('\r\n','\n');file:close();return source
end
local function once(source,before,after)
 local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
 return source:sub(1,at-1)..after..source:sub(at+#before)
end
assert(load(read('mk2ks_native_kano_laser_cpu_leg_repeat_p2.lua'),'@whole_current_cpu_leg_p2_root','t',_G))()
local source=read('mk2ks_physical_p2_cpu_overlap_trace_v1999.lua')
source=once(source,"dofile('mk2ks_physical_p2_cpu_round_trace_v1998.lua')",'-- Existing physical/body/channel root already loaded; no second controller.')
source=once(source,"if cycle==2 and frame%10==0 then manager.machine.screens[':screen']:snapshot('overlap_'..frame..'.png')end",'-- Original native scenes remain in the existing RAM-only observer; no legacy files.')
assert(load(source,'@whole_original_passive_child_overlap','t',_G))()
local source=read('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')
source=once(source,"dofile('mk2ks_physical_p2_cpu_overlap_trace_v1999.lua')",'-- Complete original passive child observer already loaded above.')
assert(load(source,'@whole_original_passive_child_guard','t',_G))()
