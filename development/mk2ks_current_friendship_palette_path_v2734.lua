-- Read-only instruction/stack trace of the actual bubble palette allocator.
-- Physical controls, native health, identities and all registers untouched.
dofile('mk2ks_current_friendship_extended_wins_v2688.lua')
local cpu=manager.machine.devices[':maincpu']
local p,s=cpu.spaces.program,cpu.state
local side=assert(tonumber(os.getenv('MK2KS_FRIEND_SIDE')))
assert(os.getenv('MK2KS_FRIEND_WINNER')=='kano')
local physical=side==1 and 0x01060220 or 0x01060df0
local frame,action,object,main=0,nil,nil,nil
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,entry)
 local sp=s.SP.value;local stack={}
 if valid(sp)then for index=0,15 do stack[#stack+1]=string.format('%08X',p:read_u32(sp+index*32))end end
 print(string.format('MK2_PAL_PATH_%s frame=%d side=%d writes=0 assistance=none entry=%08X pc=%08X a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X a8=%08X a13=%08X sp=%08X st=%08X stack=%s',tag,frame,side,entry,s.PC.value,s.A0.value,s.A1.value,s.A2.value,s.A3.value,s.A4.value,s.A8.value,s.A13.value,sp,s.ST.value,#stack>0 and table.concat(stack,',')or'-'))
end
local action_address=0xff800000+0xf9a00*8
taps[#taps+1]=p:install_read_tap(action_address,action_address+15,'actual physical palette path context',function(at)
 if action or at~=action_address or s.PC.value~=at+16 then return end
 local actor,m=p:read_u32(physical),p:read_u32(physical+0x40)
 if not valid(actor)or not valid(m)or p:read_u16(actor+0x1f0)~=17 or s.A8.value~=actor or s.A13.value~=m then return end
 action,main=frame,m;log('ACTION',at)
end)
for _,address in ipairs({0xff80cf60,0xff80cfd0,0xff80d030,0xff80d3a0,0xff80d3c0,0xff80d3e0,0xff80d430,0xff80d440,0xff80c6b0,0xff80c7e0,0xff80d460,0xff80d480,0xff80d490,0xff80d4a0,0xff80d550,0xff80d570,0xff83af70})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'original palette allocation instruction and call stack',function(at)
  if not action or at~=address or s.PC.value~=at+16 or s.A13.value~=main then return end
  if address==0xff80cf60 and s.A0.value==0xfecdf710 and not object then object=s.A8.value;log('BEGIN',at)end
  if not object or s.A8.value~=object then return end
  log('STEP',at)
  if address==0xff83af70 then log('CONSTRUCT_RETURN',at);object=nil;action=nil end
 end)
end
emu.register_frame(function()frame=frame+1 end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
