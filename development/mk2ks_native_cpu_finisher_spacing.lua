-- Same ordinary physical controller and finisher capture, with passive geometry.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,started,busy=0,nil,false
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(slot)
 local s=slot==1 and {0x01060220,0x01060260,0x01060280,0x010601f0,0x010602f0}
  or {0x01060df0,0x01060e30,0x01060e50,0x01060dc0,0x01060ec0}
 local a,m=p:read_u32(s[1]),p:read_u32(s[2])
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),
  roster=p:read_u16(s[3]),state=p:read_u16(s[4]),hp=p:read_u16(s[5]),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
  pose=p:read_u32(a+0x1d0),action=p:read_u16(m+0x1f0),flags=p:read_u16(m+0x210),
  body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140)}
end
local function own()
 local h,k=sample(1),sample(2)
 return h and k and h.id==18 and h.roster==18 and h.owner==h.actor and h.state==1 and
  k.id==17 and k.roster==17 and k.owner==k.actor and k.state==0 and
  cpu.A8.value==k.actor and cpu.A13.value==k.main and p:read_u16(0x010601d0)==2
end
local function log(tag)
 local h,k=sample(1),sample(2)
 if not h or not k then return end
 print(string.format('MK2_FINISH_SPACING_%s frame=%d age=%d mode=%d pc=%08X a0=%08X a1=%08X h_actor=%08X h_main=%08X h_owner=%08X h_id=%d h_roster=%d h_state=%d h_hp=%d h_x=%d h_y=%d h_floor=%d h_pose=%08X h_action=%d h_flags=%04X h_body=%04X h_bank=%04X k_actor=%08X k_main=%08X k_owner=%08X k_id=%d k_roster=%d k_state=%d k_hp=%d k_x=%d k_y=%d k_floor=%d k_pose=%08X k_action=%d k_flags=%04X k_body=%04X k_bank=%04X gap=%d writes=0 assistance=none',
 tag,frame,started and frame-started or -1,p:read_u16(0x010601d0),cpu.PC.value,cpu.A0.value,cpu.A1.value,
 h.actor,h.main,h.owner,h.id,h.roster,h.state,h.hp,h.x,h.y,h.floor,h.pose,h.action,h.flags,h.body,h.bank,
 k.actor,k.main,k.owner,k.id,k.roster,k.state,k.hp,k.x,k.y,k.floor,k.pose,k.action,k.flags,k.body,k.bank,
 math.abs(h.x-k.x)))
end
taps[#taps+1]=p:install_read_tap(0xff83b850,0xff83b85f,'readonly own finisher distance result',function(at)
 if busy or at~=0xff83b850 or cpu.PC.value~=0xff83b860 or cpu.A1.value~=0xfff9cae0 or not own()then return end
 busy=true;log('LOOKUP');busy=false
end)
taps[#taps+1]=p:install_read_tap(0xfffaae00,0xfffaae0f,'readonly own finisher actual geometry',function(at)
 if busy or started or at~=0xfffaae00 or cpu.PC.value~=0xfffaae10 or not own()then return end
 busy=true;started=frame;log('OWN_ENTRY');busy=false
end)
emu.register_frame_done(function()
 frame=frame+1;assert(#taps==2,'Both passive geometry taps retained')
 if started and frame-started<=900 then log('FIELD')end
end)
emu.register_stop(function()
 print(string.format('MK2_FINISH_SPACING_RESULT frame=%d started=%d writes=0 assistance=none',frame,started or -1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
dofile('mk2ks_native_cpu_finisher_repair_regression.lua')
