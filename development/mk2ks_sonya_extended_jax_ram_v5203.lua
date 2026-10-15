-- New ordinary Jax controls and readonly ground/jump observations only.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path='mk2ks_sonya_extended_kitana_ram_v5202.lua'
local file=assert(io.open(path,'rb'));local text=file:read('a');file:close()
local needle="assert(load(source,'@'..path..'::P1_physical_Kitana_guard_only_4793','t',_ENV))()"
local first,last=text:find(needle,1,true)
assert(first and not text:find(needle,last+1,true))
local addition=[=[
local jax,count=kitana:gsub('kt_','jx_')
jax,count=jax:gsub('other%.roster==4','other.roster==11')
assert(count==5,'Separate Jax context, not human identity')
jax,count=jax:gsub('other_now%.roster~=4','other_now.roster~=11')
assert(count==1,'Actual readonly Jax observer ownership guard')
jax=jax:gsub('KITANA_','JAX_')
local function jax_once(before,after)
 local a,b=jax:find(before,1,true)
 assert(a and not jax:find(before,b+1,true))
 jax=jax:sub(1,a-1)..after..jax:sub(b+1)
end
jax_once('jx_upper=-1000;jx_guard=-1000 end',
 'jx_upper=-1000;jx_guard=-1000;jx_pound=-1000;jx_jump=-1000 end')
jax_once("    local reason\n    if jx_leg and frame-jx_leg<12 then",
 "    local reason\n    if other.action==0x137 then jx_pound=frame+40 end\n    if frame<jx_pound and height<=8 then\n     jx_leg=nil\n     if frame-jx_jump>=4 then jx_jump=frame end\n     if frame-jx_jump<3 then reason='pound_jump_retry_edge';press('Up');press(human.x<other.x and'Left'or'Right')\n     else reason='pound_jump_retry_release' end\n    elseif jx_leg and frame-jx_leg<12 then")
jax_once("log('JAX_DECISION','reason='..reason..' scope=physical_attempt_not_assumed_activation')",
 "log('JAX_DECISION',string.format('reason=%s pound_until=%d jump_start=%d scope=physical_attempt_not_assumed_activation',reason,jx_pound,jx_jump))")
once([[local kt_action_taps={}\nlocal rs_last]],
 [[local kt_action_taps={}\nlocal jx_last,jx_leg,jx_last_leg,jx_upper,jx_guard=nil,nil,-1000,-1000,-1000\nlocal jx_move=nil\nlocal jx_action_taps={}\nlocal jx_pound,jx_jump=-1000,-1000\nlocal rs_last]])
once('local replacement=[[\n','local replacement=[[\n'..jax)
]=]
text=text:sub(1,first-1)..addition..text:sub(first)
assert(load(text,'@'..path..'::Jax_physical_pound_jump_guard_only_4807','t',_ENV))()

-- Independent native callbacks; no task/actor/health/register replacements.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,taps=0,{}
emu.register_frame_done(function()frame=frame+1 end)
local function actor(slot)
 local a=p:read_u32(slot==1 and 0x01060220 or 0x01060df0)
 local m=p:read_u32(slot==1 and 0x01060260 or 0x01060e30)
 if a<0x01000000 or a>=0x01100000 or m<0x01000000 or m>=0x01100000 then return end
 return a,m
end
for _,entry in ipairs({{0xff86dd90,'ground_entry'},{0xff86e020,'ground_result'},
 {0xff86e070,'ground_damage'},{0xff831360,'human_jump'}})do
 local address,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'readonly actual Jax137 ground/owned Sonya jump entry',function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or p:read_u16(0x010601d0)~=2 or
   p:read_u16(0x010601f0)~=1 or p:read_u16(0x01060dc0)~=0 then return end
  local h,hm=actor(1);local c,cm=actor(2)
  if not h or not c or p:read_u16(h+0x1f0)~=18 or p:read_u16(c+0x1f0)~=11 or
   p:read_u16(0x01060280)~=18 or p:read_u16(0x01060e50)~=11 or
   p:read_u32(hm+0xc0)~=h or p:read_u32(cm+0xc0)~=c or
   p:read_u16(0x010602f0)<=0 or p:read_u16(0x01060ec0)<=0 then return end
  local owner,main=kind=='human_jump'and h or c,kind=='human_jump'and hm or cm
  if cpu.A8.value~=owner or cpu.A13.value~=main then return end
  print(string.format('MK2_JAX_GROUND_NATIVE frame=%d human_slot=1 fighter=sonya writes=0 assistance=none kind=%s entry=%08X at=%08X pc=%08X opcode=%04X mask=%04X stage=%d h_actor=%08X h_main=%08X h_owner=%08X c_actor=%08X c_main=%08X c_owner=%08X h_id=18 c_id=11 h_y=%d h_floor=%d h_vy=%08X c_y=%d c_floor=%d c_vy=%08X health=%d,%d status=%08X carry=%d a0=%08X a1=%08X a8=%08X a13=%08X',
   frame,kind,address,at,cpu.PC.value,data&0xffff,mask,p:read_u16(0x01061b30),h,hm,p:read_u32(hm+0xc0),c,cm,p:read_u32(cm+0xc0),
   p:read_i16(h+0xb0),p:read_i16(hm+0x200),p:read_u32(h+0x60),p:read_i16(c+0xb0),p:read_i16(cm+0x200),p:read_u32(c+0x60),
   p:read_u16(0x010602f0),p:read_u16(0x01060ec0),cpu.ST.value,(cpu.ST.value>>30)&1,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value))
 end)
end
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)

