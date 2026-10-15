-- Preserve original CPU exit; observer must not abort an earned native round end.
local f=assert(io.open('mk2ks_cpu_square_shadow_v5341.lua','rb'))
local source=f:read('*a'):gsub('\r\n','\n');f:close()
local before="assert(load(source,'@CPU_Square_original_input_chain_RAM_body_shadow_v5341','t',_G))()"
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
local after=[=[
local callback_line="local callback=slice('emu.register_frame_done(function()','-- END v1763 read-only consecutive move-phase observer')"
local replacement=callback_line..[[
local terminal="  if not pair_live(a,b)then log('FAILED','reason=lost_owned_pair_at_field_done');manager.machine:exit();return end"
local at=assert(callback:find(terminal,1,true));assert(not callback:find(terminal,at+1,true))
callback=callback:sub(1,at-1).."  if not pair_live(a,b)then phase_log('NATIVE_NONLIVE','mode='..p:read_u16(0x010601d0));return end"..callback:sub(at+#terminal)
]]
change(callback_line,replacement)
assert(load(source,'@CPU_Square_original_exit_preserved_native_round_observation_v5347','t',_G))()
]=]
source=source:sub(1,at-1)..after..source:sub(at+#before)
assert(load(source,'@Square_RAM_observer_normal_round_boundary_v5347','t',_G))()
