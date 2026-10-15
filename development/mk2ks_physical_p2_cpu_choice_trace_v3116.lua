-- Read-only actual P2 Sonya native AI special selection and RNG-return branches.
-- Inputs remain the v1997 physical cold-selection/continuation driver.
dofile('mk2ks_physical_p2_cpu_overlap_trace_v3115.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,serial=0,0
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function own()
 local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 return p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and
  p:read_u16(0x01060e50)==18 and valid(a)and valid(m)and
  cpu.A8.value==a and cpu.A13.value==m and p:read_u32(m+0xc0)==a and p:read_u16(a+0x1f0)==18
end
local function log(tag,value)
 print(string.format('MK2_CPU_CHOICE_%s frame=%d serial=%d %s writes=0 assistance=none',tag,frame,serial,value))
end
local kinds={{0xfffbc200,'entry'},{0xfffbc220,'first_call'},{0xfffbc250,'first_result'},
 {0xfffbc280,'second_call'},{0xfffbc2b0,'second_result'},
 {0xfffbc2c0,'ring'},{0xfffbc2f0,'square'},{0xfffbc320,'bicycle'}}
for _,item in ipairs(kinds)do
 local address,kind=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual native AI branch '..kind,function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or not own()then return end
  if kind=='entry'then serial=serial+1 end
  local a,m=cpu.A8.value,cpu.A13.value
  log('EVENT',string.format('kind=%s entry=%08X pc=%08X opcode=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d human_state=%d stage=%d schedule=%08X mode=%d action=%04X pose=%08X xraw=%08X yraw=%08X floor=%d flags=%04X body=%04X status=%08X carry=%d a0=%08X a1=%08X a2=%08X a3=%08X',
   kind,address,cpu.PC.value,data,mask,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(0x01060e50),
   p:read_u16(0x01060dc0),p:read_u16(0x010601f0),p:read_u16(0x01061b30),p:read_u32(0x01061b10),p:read_u16(0x010601d0),
   p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_i16(m+0x200),
   p:read_u16(m+0x210),p:read_u16(a+0x160),cpu.ST.value,(cpu.ST.value>>30)&1,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value))
  if kind=='square'then manager.machine.screens[':screen']:snapshot('native_square_choice_'..frame..'.png')end
 end)
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for _,range in ipairs({{0xfffbc200,0xfffbc350},{0xff80ec20,0xff80ed40}})do
   local words={}
   for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
end)
emu.register_stop(function()
 log('RESULT','choices='..serial..' scope=actual_native_rng_branch_discovery_not_full_special_or_port_acceptance')
 for _,tap in ipairs(taps)do tap:remove()end
end)
