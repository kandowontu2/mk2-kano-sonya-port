-- Identical released-input genuine continue controller. Additional observation
-- only: native ladder objects may be outside the viewport on a continued tower.
local f=assert(io.open('mk2ks_continue_presentation_v6602.lua','rb'))
local source=f:read('*a');f:close()
local before="assert(load(helper..source,'@mk2ks_native_ui_flow_v2_probe.lua::real_paid_continue_full_native_UI'))()"
local after=[=[
edit('local taps={}', 'local ladder_objects={}\nlocal taps={}')
edit("log('LADDER',string.format(",
 "ladder_objects[cpu.A8.value]={id=id,born=frame}\n  log('LADDER',string.format(")
edit('if exit_at then', [[if exit_at then
  if not live_at then
   for actor,entry in pairs(ladder_objects)do
    log('LADDER_OBJECT',string.format('id=%d actor=%08X born=%d xraw=%08X yraw=%08X pose=%08X width=%d height=%d flags=%04X',
     entry.id,actor,entry.born,p:read_u32(actor+0x80),p:read_u32(actor+0xa0),
     p:read_u32(actor+0x1d0),p:read_u16(actor+0x100),p:read_u16(actor+0x110),p:read_u16(actor+0x160)))
   end
  end]])
assert(load(helper..source,'@mk2ks_native_ui_flow_v2_probe.lua::continued_ladder_passive_objects'))()
]=]
local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@mk2ks_continue_presentation_v6602.lua::passive_ladder_objects'))()
