-- Complete original2062 CPU/FIFO/DMA/shift/scanout observer, unchanged reads.
-- Original3624 RAM-only sinks; actual opposite-character physical both-Down driver.
local handle=assert(io.open('mk2ks_native_tomb_ram_v3624.lua','rb'))
local source=handle:read('a');handle:close()
local old="dofile('mk2ks_current_stage_provenance_v3595.lua')"
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1).."dofile('mk2ks_current_cross_pressed_tomb_provenance_v5853.lua')"..source:sub(last+1)
assert(not source:find(':write_',1,true)and not source:find('set_value',1,true))
assert(load(source,'@complete3624_native_cross_pressed_scene_RAM_sinks_5864','t',_ENV))()
emu.register_frame_done(function()
 if emu.time()>=890 then
  print('MK2_CURRENT_TOMB_RENDER_DEADLINE writes=0 assistance=none')
  manager.machine:exit()
 end
end)
