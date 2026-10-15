-- Exact original5324 physical miss trajectory; no raster or snapshot files.
local function read(name)
 local file=assert(io.open(name,'rb'));local source=file:read('a'):gsub('\r\n','\n');file:close();return source
end
local physical=read('mk2ks_current_cpu_ring_miss_render_ram_v6410.lua')
local function change(source,before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 return source:sub(1,first-1)..after..source:sub(last+1)
end
physical=change(physical,"assert(load(source,'@whole_original5324_physical_inputs_and2014_continuous_RAM_renderer','t',_G))()",[[
local stop=assert(source:find("local source=read('mk2ks_physical_p2_cpu_ring_display_v2014.lua')",1,true))
assert(load(source:sub(1,stop-1),'@whole_original5324_physical_miss_driver_no_raster','t',_G))()
]])
physical=change(physical,"assert(load(extra,'@'..pair[1],'t',_G))()",[[
-- The original choice observer has one screenshot. Keep its callback,
-- route it through the same validated RGB-in-RAM physical sink instead.
local count
extra,count=extra:gsub("manager.machine.screens%[':screen'%]:snapshot%(",'current_choice_snapshot(frame,')
assert(count==(pair[1]=='mk2ks_physical_p2_cpu_choice_trace_v3303.lua'and 1 or 0))
local memory_env=setmetatable({current_choice_snapshot=function(actual_frame,label)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',actual_frame,label,w,h,#raw,
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end},{__index=_G})
assert(not extra:find(':snapshot',1,true)and not extra:find("'wb'",1,true))
assert(load(extra,'@'..pair[1],'t',memory_env))()
]])
assert(load(physical,'@whole_qualified_physical_miss_RAM_only_driver','t',_G))()
local source=read('mk2ks_current_cpu_ring_audio_v6383.lua')
local first=assert(source:find("local source=read('mk2ks_current_tomb_winner_mix_observer_v5779.lua')",1,true))
source=source:sub(first)
source=change(source,'frame<=origin+639','frame<=origin+750')
source=change(source,"origin==2077 and frame==3623,'Both complete sound ROM checks and unchanged physical Ring terminal; audio2077..2716'",
 "origin==1879 and frame==3623,'Both complete sound ROM checks and unchanged physical miss terminal; audio1879..2629 includes full KO, winner EOF and round reset'")
assert(load(source,'@whole_native_current_missed_Ring_audio_RAM_only','t',_G))()
