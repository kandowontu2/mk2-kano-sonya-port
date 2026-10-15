-- Real grounded counters: crouching Low Kick against the compact roll;
-- walk inward, crouch and earlier HP against Bicycle's displaced startup.
-- Same full passive guest/GFX/body/channel/DAC/PCM inventory, no game writes.
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
 assert(move=='ball'or move=='bicycle','Grounded counter scope')
 local function press(button)
  local port=button=='Low Kick'and':IN2'or':IN0'
  manager.machine.ioport.ports[port].fields['P'..(3-side)..' '..button]:set_value(1)
  log('INPUT',string.format('serial=%d slot=%d button=%s ground=1',entry and serial or serial+1,3-side,button:gsub(' ','_')))
 end
 if command then
  local age=frame-command
  if move=='bicycle'then
   local own_forward=assert(rawget(_G,'MK2PORT_INTERRUPT_FORWARD'))
   if age>=0 and age<6 then press(own_forward=='Right'and'Left'or'Right')end
   if age>=6 and age<25 then press('Down')end
   if age>=delay and age<delay+5 then press('High Punch')end
  else
   if not entry and age>=79 then press('Down')end
   if entry then
    local live=frame-entry
    if live>=1 and live<delay+9 then press('Down')end
    if live>=delay and live<delay+5 then press('Low Kick')end
   end
  end
 end]])
]=]
adapter=change(adapter,"assert(load(source,'@whole_current_interruption_with_precrouch_and_actual_uppercut_entry','t',_G))()",
 extra.."assert(load(source,'@whole_current_interruption_actual_ground_counters','t',_G))()")
assert(load(adapter,'@whole_current_observer_real_grounded_counter_inputs','t',_G))()
