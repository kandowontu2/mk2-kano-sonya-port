-- Whole original earned cross controller, ordinary physical both-Down only.
-- No writes to game/register/health/position/character/palette/RNG state.
local f=assert(io.open('mk2ks_current_stage_ram_driver_v3594.lua','rb'))
local source=f:read('a');f:close()
local function replace(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
replace("  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local f=assert(io.open(assert(os.getenv('MK2KS_STAGE_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()",
 "  -- The read-only audio observer sends the actual whole guest to RAM.")
replace('if at~=entry or not window then return end','if at~=entry or cpu.PC.value~=at+16 or not window then return end')
replace('local rematch_at,action_arena,last_state=nil,nil,nil','local rematch_at,action_arena,last_state=nil,nil,nil\nlocal drop_fields=0')
replace(' -- A normal paid challenger after an expired finish window. Never touch state.',[[
 -- Actual physical input only, after genuine native stage activation.
 if action and frame-action>=32 and frame-action<64 then
  press(1,'Down');press(2,'Down');drop_fields=drop_fields+1
  log('DROP_INPUT','origin='..action..' age='..(frame-action)..' pressed_fields='..drop_fields)
 end
 -- A normal paid challenger after an expired finish window. Never touch state.]])
replace("emu.register_stop(function()\n log('RESULT'","emu.register_stop(function()\n log('DROP_RESULT','pressed_fields='..drop_fields)\n log('RESULT'")
assert(source:find('local victim_id=id==17 and 18 or 17',1,true))
assert(not source:find(':write_',1,true)and not source:find("'wb'",1,true))
assert(load(source,'@complete3594_actual_cross_native_both_Down_5852','t',_ENV))()
