-- Original released-input paid continue and entire UI, ordinary fresh controls.
local f=assert(io.open('mk2ks_continue_presentation_v6602.lua','rb'))
local source=f:read('a');f:close()
local before="assert(load(helper..source,'@mk2ks_native_ui_flow_v2_probe.lua::real_paid_continue_full_native_UI'))()"
local after=[=[
edit("  fields.Block:set_value(1);log('INPUT','button=Block age='..(frame-live_at))", [[  local age=frame-live_at
  local own=p:read_u32(slots[side].actor);local enemy=p:read_u32(slots[3-side].actor)
  local away=valid(own)and valid(enemy)and p:read_i16(own+0x90)<p:read_i16(enemy+0x90)and'Left'or'Right'
  pulse(away,age,12,24);pulse('Up',age,64,3);pulse('High Punch',age,128,3)]])
assert(load(helper..source,'@whole_native_cross_continue_UI_ordinary_fresh_controls'))()
]=]
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@same_native_UI_paid_continue_original_ordinary_control_schedule'))()
