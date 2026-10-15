-- Complete original physical trajectory, read-only KO/round renderer window.
local f=assert(io.open('mk2ks_native_tomb_ram_v3624.lua','rb'))
local transport=f:read('*a');f:close()
local stop=assert(transport:find('local handle=assert(io.open',1,true))
assert(load(transport:sub(1,stop-1),'@original_complete3624_RAM_delta_and_snapshot_sinks','t',_ENV))()
f=assert(io.open('mk2ks_cpu_square_scene_ram_v5357.lua','rb'))
local source=f:read('*a'):gsub('\r\n','\n');f:close()
local function once(before,after)
 local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
 source=source:sub(1,at-1)..after..source:sub(at+#before)
end
once(" if name=='mk2ks_physical_p2_cpu_square_display_v2039.lua'then",[[
 if name=='mk2ks_physical_p2_cpu_square_display_v2039.lua'then
  change('local function window_end()return observed_recovery and observed_recovery+30 or command and command+480 end','local function window_end()return 3340 end')
  change('frame>=command and frame<=window_end()','frame>=3000 and frame<=window_end()')
  change('f>=command+1 and f<=window_end()','f>=3001 and f<=window_end()')]])
once(" print(string.format('MK2_SCENE_RAM label=%s bytes=%d hex=%s',file,#raw,raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))",' MK2KS_TOMB_RAM_SAVE(file,raw)')
once(" local file=string.format('display_%d.rgb',frame);local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400);save(file,raw)"," local file=string.format('display_%d.rgb',frame);MK2KS_TOMB_RAM_PIXELS(file)")
assert(load(source,'@entire_original_physical_scene_KO_round_window_RAM_only_5382','t',_ENV))()
