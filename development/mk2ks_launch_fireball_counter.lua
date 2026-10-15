-- Real selected Liu Kang1 uses F,F,HP. Full original two-cycle own commands,
-- passive source/audio/body inventory and real native IN0/IN2 remain intact.
-- No guest/actor/task/HP/RNG/sound assignments, saved states or helper attacks.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local controller=read('mk2ks_launch_ground_counter_v6703.lua')
controller=change(controller,[[  if move=='bicycle'then
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
  end]],[[  local onset=move=='ball'and 55+delay or delay-1
  local age=age-onset
  local own_forward=assert(rawget(_G,'MK2PORT_INTERRUPT_FORWARD'))
  local toward=own_forward=='Right'and'Left'or'Right'
  if (age>=0 and age<3)or(age>=5 and age<8)then press(toward)end
  if age>=6 and age<9 then press('High Punch')end]])
rawset(_G,'MK2PORT_FIREBALL_COUNTER_SOURCE',controller)
local source=read('mk2ks_launch_ground_io_v6706.lua')
source=change(source,"'extra..'+string.format","'extra..'..string.format")
source=change(source,"local adapter=read('mk2ks_launch_ground_counter_v6703.lua')",
 "local adapter=assert(rawget(_G,'MK2PORT_FIREBALL_COUNTER_SOURCE'))")
assert(load(source,'@whole_current_fireball_counter_correct_native_inputs','t',_G))()

-- Native collision provenance, including genuine projectile Main parent links.
local cpu=manager.machine.devices[':maincpu'];local p,r=cpu.spaces.program,cpu.state
local frame=0;local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame(function()frame=frame+1 end)
for label,address in pairs({collision=0xff835440,rectangles=0xff835b70,contact=0xff835e50,miss=0xff835e70})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual stock counter '..label,function(at,data,mask)
  if at~=address or r.PC.value~=address+16 or not rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')then return end
  local a,m=r.A8.value,r.A13.value
  print(string.format('MK2_FIREBALL_COUNTER_EVENT frame=%d seconds=%.12f writes=0 assistance=none kind=%s at=%08X pc=%08X opcode=%04X mask=%04X a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X a5=%08X a6=%08X a7=%08X a8=%08X a9=%08X a10=%08X a11=%08X a13=%08X id=%d mainActor=%08X parentActor=%08X parentMain=%08X victimActor=%08X victimMain=%08X',
   frame,emu.time(),label,at,r.PC.value,data&0xffff,mask,r.A0.value,r.A1.value,r.A2.value,r.A3.value,r.A4.value,r.A5.value,r.A6.value,r.A7.value,a,r.A9.value,r.A10.value,r.A11.value,m,
   valid(a)and p:read_u16(a+0x1f0)or-1,valid(m)and p:read_u32(m+0xc0)or 0,valid(m)and p:read_u32(m+0x230)or 0,
   valid(m)and p:read_u32(m+0x250)or 0,valid(m)and p:read_u32(m+0x140)or 0,valid(m)and p:read_u32(m+0x170)or 0))
 end)
end
emu.register_stop(function()for _,t in ipairs(taps)do t:remove()end end)
