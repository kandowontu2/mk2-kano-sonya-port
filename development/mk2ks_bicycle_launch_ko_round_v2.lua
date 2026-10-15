-- Preserve the failed adapter. Construct the complete nested driver plainly.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true))
 return s:sub(1,a-1)..after..s:sub(b+1)
end
assert(os.getenv('MK2PORT_ACCEPT_MOVE')=='bicycle')
local template=read('mk2ks_launch_ko_round.lua')
local boundary=assert(template:find("local dual=read('mk2ks_launch_dual_roll.lua')",1,true))
local driver=assert(load(template:sub(1,boundary-1)..'\nreturn driver','@original_KO_controller_construction','t',_G))()
driver=change(driver,'if recovered and attempt<4 and frame>=recovered+32 then','if recovered and attempt<8 and frame>=recovered+32 then')
driver=change(driver,"rearm=frame;attempt=5;rawset(_G,'MK2PORT_DUAL_COMMAND',frame)",
 "rearm=frame;attempt=9;local own,victim=side==1 and a or b,side==1 and b or a;forward=own.x<victim.x and'Right'or'Left';backward=forward=='Right'and'Left'or'Right';rawset(_G,'MK2PORT_INTERRUPT_COMMAND',frame);rawset(_G,'MK2PORT_INTERRUPT_FORWARD',forward)")
driver=change(driver,"pulse(side,'Low Kick',frame-rearm,0,84)",
 "pulse(side,backward,frame-rearm,0,3);pulse(side,backward,frame-rearm,6,3);pulse(side,'Down',frame-rearm,12,3);pulse(side,'High Kick',frame-rearm,13,3)")
driver=change(driver,"completed=5;log('KO_FINAL'","completed=9;log('KO_FINAL'")
local adapter=read('mk2ks_launch_precrouch_v6683.lua')
adapter=change(adapter,"local source=read('mk2ks_launch_interrupt_v6680.lua')",
 "local source=read('mk2ks_launch_interrupt_v6680.lua')\nsource=change(source,\"local driver=read('mk2ks_special_repeat_v5099.lua')\",'local driver='.."..string.format('%q',string.format('%q',driver))..")")
local fire=read('mk2ks_launch_fireball_counter.lua')
fire=change(fire,"local controller=read('mk2ks_launch_ground_counter_v6703.lua')",
 "local controller=read('mk2ks_launch_ground_counter_v6703.lua')\ncontroller=change(controller,\"local adapter=read('mk2ks_launch_precrouch_v6683.lua')\",'local adapter='.."..string.format('%q',string.format('%q',adapter))..")")
assert(load(fire,'@whole_Bicycle_fireball_KO_reset_rearm','t',_G))()
local observer_at=assert(template:find("local p=manager.machine.devices[':maincpu'].spaces.program",boundary,true))
assert(load(template:sub(observer_at),'@whole_original_KO_round_physical_observer','t',_G))()
