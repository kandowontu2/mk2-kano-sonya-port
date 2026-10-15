-- Physical test inputs only. Keep every native field/action ownership observer.
local path='mk2ks_native_paired_stumble_subzero_ring.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before="replacement=ranged..'\\n'..replacement"
local after=[===================[
local input_begin=assert(ranged:find('    local forward=',1,true))
local input_end=assert(ranged:find("    log('RANGE_DECISION'",input_begin,true))
assert(not ranged:find('    local forward=',input_begin+1,true))
local physical=[=================[
    local forward=human.x<other.x and'Right'or'Left'
    -- This table contains controller history only, never a guest task/state.
    local feedback=rs_taps.subzero_guard_pressure_inputs
    if reset or not feedback then
     feedback={last_leg=-1000,last_upper=-1000,guard_until=-1000,last_cpu=-1}
     rs_taps.subzero_guard_pressure_inputs=feedback
    end
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    local blocking=human.action==0x700 or human.action==0x701
    local ready=height<=8 and (blocking or human.action==0 or human.action==0x303 or
     human.action==0x302 or human.action==0x304 or human.action==0x107) and
     human.flags&0x18==0 and (blocking or human.body&0x0c==0)
    -- Guard the actual visible freeze startup. Do not keep renewing a40-field
    -- lock on every startup field; once near, try the native leg before the
    -- observed61..77 ground-throw interval. Only native collision earns a hit.
    if other.action==0x604 and feedback.last_cpu~=0x604 then
     feedback.guard_until=frame+45
    end
    feedback.last_cpu=other.action
    local reason
    if feedback.leg and frame-feedback.leg<12 then
     reason='guard_pressure_leg_sequence';local age=frame-feedback.leg
     if age<7 then press('Down')end
     if age>=3 and age<7 then press('Low Punch');press('Block')end
    elseif height>8 then
     if human.action==0x308 or human.action==0x200 then
      reason='guard_pressure_native_air_kick_attempt'
      if gap<115 and height<90 and frame%6<3 then press('High Kick')end
     else reason='guard_pressure_nonflight_release' end
    elseif cpu_height>15 and gap<100 then
     reason='guard_pressure_anti_air';press('Down')
     if ready and gap<78 and frame-feedback.last_upper>=26 then
      press('High Punch');feedback.last_upper=frame
     else press('Block')end
    elseif frame<feedback.guard_until then
     reason='guard_pressure_visible_freeze_guard';press('Down');press('Block')
    elseif ready and gap<115 and cpu_height<=8 and other.action~=0x604 and
      frame-feedback.last_leg>=32 then
     reason='guard_pressure_early_leg_attempt';feedback.leg=frame
     feedback.last_leg=frame;press('Down')
    elseif ready and gap>105 and cpu_height<=8 and (other.action==0 or
      other.action==0x301 or other.action==0x302 or other.action==0x303 or other.action==0x304) then
     reason='guard_pressure_grounded_approach';press(forward)
    else
     reason='guard_pressure_stance_guard';press('Down');press('Block')
    end
    rs_ring=feedback.leg;rs_dir='guard_pressure'
]=================]
ranged=ranged:sub(1,input_begin-1)..physical..ranged:sub(input_end)
replacement=ranged..'\n'..replacement
]===================]
local a,b=source:find(before,1,true)
assert(a and not source:find(before,b+1,true),'One SubZero-only physical feedback replacement')
source=source:sub(1,a-1)..after..source:sub(b+1)
local old='original_Ring_routine=whole earlier_inputs=unchanged'
local first,last=source:find(old,1,true)
assert(first and not source:find(old,last+1,true))
source=source:sub(1,first-1)..'physical_feedback=guard_pressure native_flight_actions=required passive_observers=retained earlier_inputs=unchanged'..source:sub(last+1)
assert(load(source,'@'..path..'::only_SubZero_guard_and_early_leg_physical_inputs','t',_ENV))()
