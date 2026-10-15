-- Same one physical controller and all current passive observers.
-- Different real P1 approach: walk in and pulse High Punch when controllable.
-- No CPU/HP/RNG/actor/register/position/state writes or prescribed CPU action.
local f=assert(io.open('mk2ks_native_selector_sonya_choice_shadow_bound.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once('local original_dofile=function(path)','local function original_dofile(path)')
once('a8=%08X a13=%08X writes=0 assistance=none',
     'a8=%08X a13=%08X a6=%08X a7=%08X a9=%08X a10=%08X a11=%08X a12=%08X a14=%08X status=%08X writes=0 assistance=none')
once('regs.A4.value,regs.A5.value,regs.A8.value,regs.A13.value))',
     'regs.A4.value,regs.A5.value,regs.A8.value,regs.A13.value,regs.A6.value,regs.A7.value,regs.A9.value,regs.A10.value,regs.A11.value,regs.A12.value,regs.A14.value,regs.ST.value))')
once(" loads[path]=(loads[path]or 0)+1\n print('MK2_SONYA_OBSERVER_LOAD",[====[
 if path=='mk2ks_current_kano_cpu_extended_ram_v6290.lua' then
  local marker=" local n;source,n=source:gsub(\"manager.machine.screens%[':screen'%]:snapshot\",'mk2_ram_snapshot')"
  local addition=[==[
 if path=='mk2ks_physical_p2_cpu_continuation_v3300.lua' then
  source=replace_once(source,"assert(approach=='original' or approach=='guard_wait' or approach=='guard_until_close','Only genuine human input strategies')",
   "assert(approach=='original' or approach=='guard_wait' or approach=='guard_until_close' or approach=='pressure_hp','Only genuine human input strategies')")
  source=replace_once(source,'    if complete then\n',[=[
    if approach=='pressure_hp' then
        local gap=math.abs(s.x-v.x)
        local eligible=v.hp>0 and s.hp>0 and clean(v)
        local toward=eligible and gap>76
        local punch=eligible and (frame-first_live)%24<4
        fields['P1 Block']:set_value(0)
        fields['P1 Up']:set_value(0);fields['P1 Down']:set_value(0)
        if toward then fields['P1 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)end
        if punch then fields['P1 High Punch']:set_value(1)end
        log('PRESSURE_INPUT',string.format('policy=pressure_hp eligible=%d gap=%d toward=%d punch=%d',
            eligible and 1 or 0,gap,toward and 1 or 0,punch and 1 or 0))
    elseif complete then
]=])
  print('MK2_PRESSURE_BIND count=1 controller=original_physical_P1 inputs=walk_high_punch writes=0 assistance=none')
 end
]==]
  local a,b=assert(text:find(marker,1,true));assert(not text:find(marker,b+1,true))
  text=text:sub(1,a-1)..addition..'\n'..text:sub(a)
 end
 loads[path]=(loads[path]or 0)+1
 print('MK2_SONYA_OBSERVER_LOAD
]====])
assert(not source:match(':write_[ui]%d+')and not source:match('%.value%s*=[^=]'))
assert(load(source,'@whole_original_Sonya_observers_one_real_pressure_controller','t',_G))()
