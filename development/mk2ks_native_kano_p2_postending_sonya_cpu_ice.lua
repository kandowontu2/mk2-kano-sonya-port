-- Same earned tower/ending/join. Only physical Block reacts to real CPU ice.
local path='mk2ks_native_kano_p2_postending_sonya_defensive.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local function replace(before,after)
 local a,b=source:find(before,1,true)
 assert(a and not source:find(before,b+1,true),'One exact retained controller expansion')
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
replace('if frame<guard_until and gap>65 then','if frame<guard_until then')
local hook=[==[
local cpu_ice_observer=[[
taps[#taps+1]=p:install_read_tap(0xff8a5900,0xff8a590f,'passive real CPU ice launch',function(at,data,mask)
 if at~=0xff8a5900 or cpu.PC.value~=0xff8a5910 or cpu.A0.value~=13 or mask~=0xffff or
  (data&0xffff)~=0x24a0 or p:read_u16(0x010601d0)~=2 then return end
 local human,other=sample(side),sample(opponent)
 if not human or not other or human.hp<=0 or other.hp<=0 or human.state~=1 or other.state~=0 or
  human.id~=17 or other.id~=8 or other.roster~=8 or cpu.A8.value~=other.actor or
  not valid(cpu.A13.value) or p:read_u32(cpu.A13.value+0xc0)~=other.actor then return end
 local distance=math.abs(human.x-other.x)
 guard_until=math.max(guard_until,frame+math.ceil(distance/4)+45)
 log('CPU_ICE',string.format('entry=FF8A5900 pc=%08X value=%04X mask=%04X actor=%08X main=%08X id=8 projectile=13 gap=%d guard_until=%d human_actor=%08X human_id=17 health=%d,%d',
  cpu.PC.value,data&0xffff,mask,other.actor,cpu.A13.value,distance,guard_until,human.actor,human.hp,other.hp))
end)
emu.register_frame_done(function()
 if losses>=8 and not ending_completed then
  log('CONTROLLER_STOP','reason=eight_actual_paid_continue_losses ending_not_reached=true')
  manager.machine:exit()
 end
end)
]]
one('-- Observe actual own special entries independently of intended button plans.',
 cpu_ice_observer..'\n-- Observe actual own special entries independently of intended button plans.')
]==]
replace('one(old,new)',"one(old,new)\n"..hook)
assert(load(source,'@'..path..'::real_CPU_ice_physical_guard_bounded_campaign','t',_ENV))()
