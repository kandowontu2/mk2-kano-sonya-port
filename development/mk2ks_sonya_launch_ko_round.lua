-- Whole prior controller/observer, genuine Sonya Square KO and native next round.
-- P1 uses its source-qualified uppercut counter; P2 its actual jump-kick route.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true))
 return s:sub(1,a-1)..after..s:sub(b+1)
end
local side=assert(tonumber(os.getenv('MK2PORT_ACCEPT_SIDE')));assert(side==1 or side==2)
assert(os.getenv('MK2PORT_ACCEPT_MOVE')=='square')
local limit=side==1 and 5 or 7
local template=read('mk2ks_launch_ko_round.lua')
local boundary=assert(template:find("local dual=read('mk2ks_launch_dual_roll.lua')",1,true))
local driver=assert(load(template:sub(1,boundary-1)..'\nreturn driver','@unchanged_KO_controller_construction','t',_G))()
driver=change(driver,'if recovered and attempt<4 and frame>=recovered+32 then','if recovered and attempt<'..limit..' and frame>=recovered+32 then')
driver=change(driver,"rearm=frame;attempt=5;rawset(_G,'MK2PORT_DUAL_COMMAND',frame)",
 "rearm=frame;attempt="..(limit+1)..";local own,victim=side==1 and a or b,side==1 and b or a;forward=own.x<victim.x and'Right'or'Left';backward=forward=='Right'and'Left'or'Right';rawset(_G,'MK2PORT_INTERRUPT_COMMAND',frame);rawset(_G,'MK2PORT_INTERRUPT_FORWARD',forward)")
driver=change(driver,"pulse(side,'Low Kick',frame-rearm,0,84)",
 "pulse(side,forward,frame-rearm,0,3);pulse(side,backward,frame-rearm,5,3);pulse(side,'High Punch',frame-rearm,6,3)")
driver=change(driver,"completed=5;log('KO_FINAL'","completed="..(limit+1)..";log('KO_FINAL'")
local adapter=read('mk2ks_launch_precrouch_v6683.lua')
adapter=change(adapter,"local source=read('mk2ks_launch_interrupt_v6680.lua')",
 "local source=read('mk2ks_launch_interrupt_v6680.lua')\nsource=change(source,\"local driver=read('mk2ks_special_repeat_v5099.lua')\",'local driver='.."..string.format('%q',string.format('%q',driver))..")")
adapter=change(adapter,[[  taps[#taps+1]=p:install_read_tap(0x01d00000,0x01d0000f,'actual physical input port read',function(at,data,mask)
   if rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then log('IO',string.format('at=%08X value=%04X mask=%04X pc=%08X',at,data&0xffff,mask,regs.PC.value))end
  end)]],[[  for _,port in ipairs({{0x01600000,'IO'},{0x01600020,'LOW_IO'}})do
   taps[#taps+1]=p:install_read_tap(port[1],port[1]+15,'actual native Sonya KO input read',function(at,data,mask)
    if rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then log(port[2],string.format('at=%08X value=%04X mask=%04X pc=%08X',at,data&0xffff,mask,regs.PC.value))end
   end)
  end]])
if side==2 then
 local jump=read('mk2ks_launch_jump_interrupt_v6693.lua')
 jump=change(jump,"local adapter=read('mk2ks_launch_precrouch_v6683.lua')",'local adapter='..string.format('%q',adapter))
 adapter=jump
end
assert(load(adapter,'@actual_Sonya_collision_KO_native_round_reset_rearm','t',_G))()
local observer=template:sub(assert(template:find("local p=manager.machine.devices[':maincpu'].spaces.program",boundary,true)))
assert(load(observer,'@unchanged_complete_KO_round_physical_publication_observer','t',_G))()
