-- Ordinary controls only: early retreat and retried Up edges, no Ring startup.
local path='mk2ks_native_paired_stumble_subzero_ring.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before="replacement=ranged..'\\n'..replacement"
local after=[====[
local input_begin=assert(ranged:find('    local forward=',1,true))
local input_end=assert(ranged:find("    log('RANGE_DECISION'",input_begin,true))
assert(not ranged:find('    local forward=',input_begin+1,true))
local physical=[==[
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    local reason
    local height=human.floor-human.y
    if height>8 then
     -- Captured/lifted victims also have height. Never call that flight or
     -- claim a kick from buttons; only the native jump/airkick action admits
     -- this physical attack attempt. The original engine decides contact.
     if human.action==0x308 or human.action==0x200 then
      reason='native_air_phase_kick_attempt'
      if rs_jumpdir and frame-rs_jump<48 then press(rs_jumpdir)end
      if frame%6<3 then press('High Kick')end
     else reason='nonflight_height_release' end
    elseif gap<220 then
     rs_ring=nil
     -- Retry after three on/one off. A failed Up edge never buys a38-field
     -- standing/crouching wait inside the observed61..77 native throw range.
     if frame-rs_jump>=4 then rs_jump=frame;rs_jumpdir=back end
     if frame-rs_jump<3 then
      reason='early_retreat_up_edge_attempt';press('Up');press(rs_jumpdir)
     else reason='early_retreat_up_release';press(rs_jumpdir)end
    else
     rs_ring=rs_ring or frame
     reason='far_crouch_guard_attempt';press('Down')
     if frame-rs_ring>=3 then press('Block')end
    end
]==]
ranged=ranged:sub(1,input_begin-1)..physical..ranged:sub(input_end)
replacement=ranged..'\n'..replacement
]====]
local a,b=source:find(before,1,true)
assert(a and not source:find(before,b+1,true),'One entire Sub-Zero-only ordinary control replacement')
source=source:sub(1,a-1)..after..source:sub(b+1)
local old='original_Ring_routine=whole earlier_inputs=unchanged'
local first,last=source:find(old,1,true)
assert(first and not source:find(old,last+1,true))
source=source:sub(1,first-1)..'physical_feedback=early_retreat_retry native_flight_actions=required passive_observers=retained earlier_inputs=unchanged'..source:sub(last+1)
assert(load(source,'@'..path..'::only_SubZero_early_physical_retreat_retry','t',_ENV))()
