-- Real paid challenger interrupts an actual current startup cue.
-- Entire existing human selection/join/ordinary-play route retained.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true))
 return s:sub(1,a-1)..after..s:sub(b+1)
end
local side=assert(tonumber(os.getenv('MK2PORT_ACCEPT_SIDE')))
local move=assert(os.getenv('MK2PORT_ACCEPT_MOVE'));assert(move=='ball'or move=='square')
local identity=move=='ball'and 17 or 18
local source=read('mk2ks_current_challenger_v6486.lua')
source=change(source,"controls[n]['Low Punch']=low['P'..n..' Low Punch']",
 "controls[n]['Low Punch']=low['P'..n..' Low Punch'];controls[n]['Low Kick']=low['P'..n..' Low Kick']")
source=change(source,"local frame,cold_css,cold_match,join,css,match,ready=0,nil,nil,nil,nil,nil,nil",
 "local frame,cold_css,cold_match,join,css,match,ready=0,nil,nil,nil,nil,nil,nil\nlocal launched,launch_command=nil,nil")
source=change(source,"cold_match=frame;log('COLD_MATCH'", "cold_match=frame;rawset(_G,'MK2PORT_NATIVE_AUDIO_READY',frame);log('COLD_MATCH'")
source=change(source,[[  if frame-cold_match>=100 then controls[side].Block:set_value(1)end
  if frame-cold_match==600 then
   join=frame;log('JOIN','ownState='..p:read_u16(slots[side].state)..' otherState='..p:read_u16(slots[3-side].state)..' mode='..mode)
  end]],[[  local age=frame-cold_match
  pulse(3-side,'Coin',age,80);pulse(3-side,'Coin',age,90)
  local own=actor(side)
  if not launch_command and age>=100 and own and own.y==own.floor and own.vx==0 and own.vy==0 and own.gravity==0 and own.flags&0x1c==0 then
   launch_command=frame;log('LAUNCH_COMMAND','id='..identity)
  end
  if launch_command then
   local age=frame-launch_command
   if fighter=='kano'then pulse(side,'Low Kick',age,0,84)
   else
    local forward=own and(p:read_u16(own.actor+0xf0)&0x10)~=0 and'Left'or'Right'
    pulse(side,forward,age,0,3);pulse(side,forward=='Right'and'Left'or'Right',age,5,3);pulse(side,'High Punch',age,6,3)
   end
   if age==160 and not launched then launch_command=nil;log('LAUNCH_RETRY')end
  end
  if launched and frame>launched then
   join=frame;log('JOIN','ownState='..p:read_u16(slots[side].state)..' otherState='..p:read_u16(slots[3-side].state)..' mode='..mode)
  end]])
source=change(source,"local age=frame-join;pulse(3-side,'Coin',age,10);pulse(3-side,'Coin',age,30);pulse(3-side,'Start',age,60)",
 "local age=frame-join;pulse(3-side,'Start',age,0,5)")
source=change(source,"for n,s in ipairs(slots)do\n taps[#taps+1]",[[taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual startup before challenger join',function(at,data,mask)
 if not cold_match or join or launched or at~=0x01d01030 or mask~=0xffff or data~=(fighter=='kano'and 0x6b03 or 0x6b00)then return end
 local own=assert(actor(side));assert(cpu.A8.value==own.actor and cpu.A13.value==own.main and own.id==identity)
 launched=frame;log('ACTUAL_LAUNCH',string.format('word=%04X actor=%08X main=%08X pc=%08X',data,own.actor,own.main,cpu.PC.value))
end)
for n,s in ipairs(slots)do
 taps[#taps+1]])
source=change(source,"'MK2_CR_GUEST frame=1 bytes=1048576 hex='","'MK2_HPHASE_GUEST frame=1 bytes=1048576 hex='")
source=change(source,"'MK2_CR_GFX frame=1 bytes=18976 hex='","'MK2_HPHASE_GFX frame=1 bytes=18976 hex='")
source=change(source,"'MK2_CR_RGB frame=%d filename=%s bytes=%d hex=%s'",
 "'MK2_HPHASE_RGB frame=%d move="..move.." side="..side.." attempt=1 stage=%s width=400 height=254 bytes=%d hex=%s'")
source=change(source,"if age==600 then manager.machine:exit()end",
 "if age==600 then rawset(_G,'MK2PORT_NATIVE_AUDIO_FINAL',frame);manager.machine:exit()end")
assert(load(source,'@whole_original_challenger_route_actual_launch_transition','t',_G))()

-- Complete original owner/channel/health/PCM/DAC/ROM observer; no opponent input.
local passive=read('mk2ks_launch_interrupt_v6680.lua')
local at=assert(passive:find("local cpu=manager.machine.devices[':maincpu'];local p,regs=cpu.spaces.program,cpu.state",1,true))
passive=passive:sub(at)
passive=change(passive,' if entry then\n  local age=frame-entry',' if false and entry then\n  local age=frame-entry')
local prefix=read('mk2ks_launch_interrupt_v6680.lua')
local start=assert(prefix:find('local function read(name)',1,true))
local finish=assert(prefix:find('local getenv=os.getenv',start,true))
prefix=prefix:sub(start,finish-1)..'\nlocal side='..side..';local move='..string.format('%q',move)..';local identity='..identity..';local delay=1\n'
assert(load(prefix..passive,'@whole_native_audio_observer_challenger_transition','t',_G))()
local template=read('mk2ks_launch_ko_round.lua')
local at=assert(template:find("local p=manager.machine.devices[':maincpu'].spaces.program",1,true))
assert(load(template:sub(at),'@whole_continuous_physical_transition_observer','t',_G))()
