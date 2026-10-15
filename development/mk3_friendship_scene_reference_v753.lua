-- Original MK3 scene oracle only. Explicit opponent-health assistance;
-- no position, identity, command-history, winner/finisher-state writes.
dofile('mk3_finish_input_selection.lua')
local side=tonumber(os.getenv('MK3_FRIEND_SIDE')or'1')
assert(side==1 or side==2)
local frame,cpu,p,fields=0,nil,nil,{}
local taps,kos,window,action,health_writes={},0,nil,nil,0
local was_alive=false
local last_pose={}
local command_start
local winning_task,last_part
local addresses={0x010609b0,0x01061560}
local hp_addresses={0x01060a40,0x010615f0}
local function valid(a)return a>=0x01000000 and a<0x01400000 end
local function log(tag,value)
 print(string.format('MK3_FRIEND_%s frame=%d winner_slot=%d assistance=opponent_health_only %s',tag,frame,side,value or''))
end
local function press(name)assert(fields[name]):set_value(1);log('INPUT','button='..name:gsub(' ','_'))end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  cpu=manager.machine.devices[':maincpu'];p=cpu.spaces.program
  for _,port in ipairs({':IN0',':IN1'})do
   for _,key in ipairs({'Left','Right','Down','Low Kick','High Kick','Run'})do
    local field=manager.machine.ioport.ports[port].fields['P'..side..' '..key]
    if field then fields[key]=field end
   end
  end
  for _,at in ipairs({0xff982880,0xff993660,0xff993570,0xff9ccce0,0xff9ccde0,
                       0xff9ccd50,0xff9cd160,0xff9cd1d0,0xff9cd450,0xff9d9a20,0xff9ba5e0,
                       0xff9936f0,0xff993700,0xff9937b0,0xff993b00,
                       0xff9920d0,0xff992120,0xff9823b0,0xff982440,0xff982480,
                       0xff9824d0,0xff982500,0xff9825a0,0xff982620,0xff982670,
                       0xff9826d0,0xff982750})do
   taps[#taps+1]=p:install_read_tap(at,at+15,'original friendship scene',function(offset)
    if offset~=at or not window then return end
    if at==0xff9ccce0 then action=action or frame;winning_task=cpu.state.A13.value end
    if action and frame-action>450 then return end
    local actor=cpu.state.A8.value
    log('ENTRY',string.format('entry=%08X a8=%08X a13=%08X a9=%08X a11=%08X id=%d slotflag=%d counters=%d,%d finish=%d a0=%08X a1=%08X a4=%08X a7=%08X',at,actor,cpu.state.A13.value,cpu.state.A9.value,cpu.state.A11.value,valid(actor)and p:read_u16(actor+0x1f0)or-1,valid(actor)and p:read_u16(actor+0x1c0)or-1,p:read_u16(0x01062450),p:read_u16(0x01062460),p:read_u16(0x01062250),cpu.state.A0.value,cpu.state.A1.value,cpu.state.A4.value,cpu.state.A7.value))
   end)
  end
  for _,base in ipairs({0xff9d1690,0xff9d27d0})do
   taps[#taps+1]=p:install_read_tap(base,base+0x600-1,'original friendship animation stream',function(offset,data,mask)
    if not action or frame-action>250 then return end
    log('STREAM',string.format('base=%08X entry=%08X value=%04X mask=%04X pc=%08X a8=%08X a9=%08X',base,offset,data&0xffff,mask,cpu.state.PC.value,cpu.state.A8.value,cpu.state.A9.value))
   end)
  end
 end
 if frame<3800 then return end
 for _,field in pairs(fields)do field:clear_value()end
 local actors={p:read_u32(addresses[1]),p:read_u32(addresses[2])}
 if not valid(actors[1])or not valid(actors[2])then return end
 if frame==3800 then
  assert(p:read_u16(actors[1]+0x1f0)==0 and p:read_u16(actors[2]+0x1f0)==1,'Actual original Kano/Sonya selection')
  log('SELECT',string.format('actors=%08X,%08X ids=0,1 slotflags=%d,%d',actors[1],actors[2],p:read_u16(actors[1]+0x1c0),p:read_u16(actors[2]+0x1c0)))
  manager.machine.video:snapshot()
 end
 local target=hp_addresses[3-side]
 local hp=p:read_u16(target)
 if not action and not window and hp>1 and hp<=166 then
  p:write_u16(target,1);health_writes=health_writes+1;log('HEALTH_ASSIST','address='..string.format('%08X',target)..' before='..hp)
  hp=1
 end
 if hp>0 and hp<=166 then was_alive=true end
 if was_alive and hp==0 then kos=kos+1;was_alive=false;log('KO','count='..kos)end
 if not window and kos==2 and p:read_u16(0x01062250)==3 then
  window=frame;log('WINDOW','block_counters='..p:read_u16(0x01062450)..','..p:read_u16(0x01062460));manager.machine.screens[':screen']:snapshot('finish_window.png')
 end
 if action then return end
 local own,other=actors[side],actors[3-side]
 local x,y=p:read_i16(own+0x90),p:read_i16(other+0x90)
 local forward=x<y and'Right'or'Left';local backward=x<y and'Left'or'Right'
 if not window and hp>0 and hp<=166 then
  if math.abs(x-y)>65 then press(forward)
  elseif frame%30<4 then press('High Kick')end
 elseif window then
  local age=frame-window
  if side==1 then
   if not command_start then
    if math.abs(x-y)<160 then press(backward);return end
    command_start=frame;log('COMMAND_POSITION','gap='..math.abs(x-y))
   end
   age=frame-command_start
   -- The standing LK's native action remains busy through the 40-field
   -- command. A crouching LK recovers before HK without using Block.
   if age>=15 and age<25 then press('Down')end
   -- Actual original Kano HK record: LK,Run,Run,HK. Button history includes HK.
   for _,item in ipairs({{20,'Low Kick'},{30,'Run'},{40,'Run'},{50,'High Kick'}})do
    if age>=item[1]and age<item[1]+4 then press(item[2])end
   end
  else
   -- Actual original Sonya Run record: B,F,B,D + Run (42-field window).
   for _,item in ipairs({{20,backward},{30,forward},{40,backward},{50,'Down'},{52,'Run'}})do
    if age>=item[1]and age<item[1]+4 then press(item[2])end
   end
  end
 end
 if not action and frame%120==0 then log('LIVE',string.format('x=%d,%d hp=%d,%d kos=%d finish=%d',x,y,p:read_u16(hp_addresses[1]),p:read_u16(hp_addresses[2]),kos,p:read_u16(0x01062250)))end
end)
emu.register_frame_done(function()
 if not action then return end
 local age=frame-action
 if winning_task and valid(winning_task)then
  local part=p:read_u32(winning_task+0x190)
  if valid(part)then
   local pose=p:read_u32(part+0x1d0)
   if pose~=last_part then
    local bank=p:read_u16(part+0x140)&0x7f00;local colors={}
    for index=0,15 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01880000+(bank+index)*16))end
    log('PART',string.format('age=%d object=%08X x=%d y=%d pose=%08X bank=%04X colors=%s',age,part,p:read_i16(part+0x90),p:read_i16(part+0xb0),pose,bank,table.concat(colors,',')))
    last_part=pose
   end
  end
 end
 local own=p:read_u32(addresses[side])
 if valid(own)then
  local pose=p:read_u32(own+0x1d0)
  if pose~=last_pose[side]then
   log('POSE',string.format('age=%d actor=%08X id=%d x=%d y=%d pose=%08X bank=%04X width=%d height=%d',age,own,p:read_u16(own+0x1f0),p:read_i16(own+0x90),p:read_i16(own+0xb0),pose,p:read_u16(own+0x140),p:read_u16(own+0x120),p:read_u16(own+0x130)))
   last_pose[side]=pose
   manager.machine.screens[':screen']:snapshot('pose_'..age..'.png')
  end
 end
 if age%8==0 then manager.machine.screens[':screen']:snapshot('friendship_'..age..'.png')end
 if age>=480 then manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('kos=%d window=%d action=%d health_writes=%d position_writes=0 identity_writes=0 state_writes=0 auto_cheat=false',kos,window or-1,action or-1,health_writes))
 for _,tap in ipairs(taps)do tap:remove()end
end)
