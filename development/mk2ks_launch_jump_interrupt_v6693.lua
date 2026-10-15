-- Distinct actual controller route: stock opponent jumps toward the special
-- and presses High Kick. All existing passive inventories remain unchanged.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local adapter=read('mk2ks_launch_precrouch_v6683.lua')
local extra=[=[
source=change(source,[[rawset(_G,'MK2PORT_INTERRUPT_COMMAND',frame);log]],
 [[rawset(_G,'MK2PORT_INTERRUPT_COMMAND',frame);rawset(_G,'MK2PORT_INTERRUPT_FORWARD',forward);log]])
source=change(source,[[ local actual_command=rawget(_G,'MK2PORT_INTERRUPT_COMMAND')
 if actual_command and command~=actual_command then command=actual_command;entry=nil end
 if command and not entry and frame>=command+assert(({ball=79,square=1,bicycle=7})[move])then
  high['P'..(3-side)..' Down']:set_value(1)
  log('INPUT',string.format('serial=%d slot=%d button=Down precrouch=1',serial+1,3-side))
 end
 if entry then
  local age=frame-entry
  if age>=1 and age<delay+9 then
   high['P'..(3-side)..' Down']:set_value(1)
   log('INPUT',string.format('serial=%d slot=%d button=Down',serial,3-side))
  end
  if age>=delay and age<delay+5 then
   high['P'..(3-side)..' High Punch']:set_value(1)
   log('INPUT',string.format('serial=%d slot=%d button=High_Punch',serial,3-side))
  end
 end]],[[ local actual_command=rawget(_G,'MK2PORT_INTERRUPT_COMMAND')
 if actual_command and command~=actual_command then command=actual_command;entry=nil end
 if command then
  local onset=({ball=80,square=2,bicycle=9})[move]
  local age=frame-command-onset
  local own_forward=assert(rawget(_G,'MK2PORT_INTERRUPT_FORWARD'))
  local toward=own_forward=='Right'and'Left'or'Right'
  if age>=0 and age<3 then
   for _,button in ipairs({'Up',toward})do
    high['P'..(3-side)..' '..button]:set_value(1)
    log('INPUT',string.format('serial=%d slot=%d button=%s jump=1',entry and serial or serial+1,3-side,button))
   end
  end
  if age>=delay+4 and age<delay+8 then
   high['P'..(3-side)..' High Kick']:set_value(1)
   log('INPUT',string.format('serial=%d slot=%d button=High_Kick jump=1',entry and serial or serial+1,3-side))
  end
 end]])
]=]
adapter=change(adapter,"assert(load(source,'@whole_current_interruption_with_precrouch_and_actual_uppercut_entry','t',_G))()",
 extra.."assert(load(source,'@whole_current_interruption_actual_jump_kick_inputs','t',_G))()")
assert(load(adapter,'@whole_precrouch_observer_distinct_jump_input_route','t',_G))()
