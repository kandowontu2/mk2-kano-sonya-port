-- Original5324 physical jump-on-launch inputs; continuous original Ring display.
local function read(name)
 local file=assert(io.open(name,'rb'));local source=file:read('a'):gsub('\r\n','\n');file:close();return source
end
local source=read('mk2ks_current_cpu_ring_render_ram_v6375.lua')
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace("env.dofile=function(name)\n assert(counts[name]~=nil",[[env.dofile=function(name)
 local aliases={['mk2ks_physical_p2_cpu_continuation_v1997.lua']='mk2ks_physical_p2_cpu_continuation_v3300.lua',
 ['mk2ks_physical_p2_cpu_round_trace_v1998.lua']='mk2ks_physical_p2_cpu_round_trace_v3301.lua',
 ['mk2ks_physical_p2_cpu_overlap_trace_v1999.lua']='mk2ks_physical_p2_cpu_overlap_trace_v3302.lua'}
 local requested=name;name=aliases[name]or name
 local replacements={['mk2ks_physical_p2_cpu_continuation_v3300.lua']=6,
 ['mk2ks_physical_p2_cpu_round_trace_v3301.lua']=0,['mk2ks_physical_p2_cpu_overlap_trace_v3302.lua']=1}
 counts[name]=counts[requested]or replacements[name]or counts[name]
 assert(counts[name]~=nil]])
replace("env.dofile('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')",[[env.dofile('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')
-- Preserve5324's independent whole-choice and compound-Square observations,
-- without loading its already-installed physical/round/overlap callbacks twice.
for _,pair in ipairs({{'mk2ks_physical_p2_cpu_choice_trace_v3303.lua','mk2ks_physical_p2_cpu_overlap_trace_v3302.lua'},
 {'mk2ks_physical_p2_cpu_square_trace_v3304.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua'}})do
 local extra=read(pair[1]);local dependency="dofile('"..pair[2].."')"
 local first,last=assert(extra:find(dependency,1,true));assert(not extra:find(dependency,last+1,true))
 extra=extra:sub(1,first-1)..'-- Original dependency already installed.'..extra:sub(last+1)
 assert(not extra:find('set_value',1,true)and not extra:find('write_u',1,true))
 assert(load(extra,'@'..pair[1],'t',_G))()
end]])
assert(load(source,'@whole_original5324_physical_inputs_and2014_continuous_RAM_renderer','t',_G))()
