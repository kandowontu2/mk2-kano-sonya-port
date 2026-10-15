-- Existing genuine CPU-loss/payment/UI controller, then ordinary controls.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true));return s:sub(1,a-1)..after..s:sub(b+1)
end
local source=read('mk2ks_continue_presentation_v6602.lua')
local before="assert(load(helper..source,'@mk2ks_native_ui_flow_v2_probe.lua::real_paid_continue_full_native_UI'))()"
local after=[=[
edit("  fields.Block:set_value(1);log('INPUT','button=Block age='..(frame-live_at))", [[  local age=frame-live_at
  if age<180 then fields.Block:set_value(1);log('INPUT','button=Block age='..age)
  else
   local own=p:read_u32(slots[side].actor);local enemy=p:read_u32(slots[3-side].actor)
   local away=valid(own)and valid(enemy)and p:read_i16(own+0x90)<p:read_i16(enemy+0x90)and'Left'or'Right'
   pulse(away,age,192,24);pulse('Up',age,244,3);pulse('High Punch',age,308,3)
  end]])
edit('if frame>=live_at+180 then manager.machine:exit()end', 'if frame>=live_at+360 then manager.machine:exit()end')
assert(load(helper..source,'@whole_native_continue_UI_then_ordinary_controls'))()
]=]
source=change(source,before,after)
assert(load(source,'@same_released_startup_paid_continue_plus_real_controls'))()
