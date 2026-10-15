-- Whole previously established actual-control controller, released startup,
-- complete native UI and passive ladder. Never schedules during hurt then
-- calls the input a response. No actor, CPU, health, position or RNG writes.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true));return s:sub(1,a-1)..after..s:sub(b+1)
end
local source=read('mk2ks_continue_presentation_v6602.lua')
local control=read('mk2ks_single_continue_controls_v6579.lua')
local a,b=assert(control:find('local after=[[',1,true));local stop=assert(control:find(']]',b+1,true))
local ordinary=control:sub(b+1,stop-1)
local before="edit(fixed,' -- Native UI driver owns its full180-field post-selection Block window.')"
local after=[=[
edit("{'Left','Right','Up','Down','High Punch'}","{'Left','Right','Up','Down','High Punch','Block'}")
edit('local phase,lastMode,lastRoster=1,nil,nil',[[local phase,lastMode,lastRoster=1,nil,nil
local walk,jump,punch,recover,walkStart,jumpStart,punchStart,walkX=nil,nil,nil,nil,nil,nil,nil,nil]])
edit('cpuID=%d scope=unassisted_CPU_loss_paid_single_player_continue_not_full_port',
 'cpuID=%d walk=%d jump=%d punch=%d recover=%d scope=unassisted_CPU_loss_paid_single_player_continue_actual_controls_not_full_port')
edit('reLive or -1,reReady or -1,cpuID or -1))',
 'reLive or -1,reReady or -1,cpuID or -1,walk or -1,jump or -1,punch or -1,recover or -1))')
]=]..'\nedit(fixed,'..string.format('%q',ordinary)..')'
source=change(source,before,after)
source=change(source,"'frame=frame+1;if css_at then for _,field in pairs(fields)do field:clear_value()end end'",
 "'frame=frame+1;if css_at and not live_at then for _,field in pairs(fields)do field:clear_value()end end'")
local final="assert(load(helper..source,'@mk2ks_native_ui_flow_v2_probe.lua::real_paid_continue_full_native_UI'))()"
local template=read('mk2ks_continue_ladder_positions_v6605.lua')
local a,b=assert(template:find('local after=[=[',1,true));local stop=assert(template:find(']=]',b+1,true))
local additions=template:sub(b+1,stop-1)
local release=[=[
edit("  fields.Block:set_value(1);log('INPUT','button=Block age='..(frame-live_at))",' -- Original adaptive base controller exclusively owns combat controls.')
edit('if frame>=live_at+180 then manager.machine:exit()end',' -- Base exits only after actual controls recover and180 native survival fields.')
]=]
source=change(source,final,release..additions)
assert(load(source,'@whole_original_adaptive_controls_released_input_UI_ladder'))()
