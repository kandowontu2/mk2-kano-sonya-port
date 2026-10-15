-- Read-only provenance of every native continuation, not only the first pair.
-- The original v1438 physical input driver and its exit condition are intact.
-- v2002 additionally records the actual bicycle fall call and unchanged routine words.
dofile('mk2ks_physical_p2_cpu_round_trace_v1940.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,cycle,serial=0,0,0
local taps,children={},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function live()
 return p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and
  (p:read_u16(0x01060e50)==17 or p:read_u16(0x01060e50)==18)
end
local function context()
 local a,m=cpu.A8.value,cpu.A13.value
 local t={string.format('a8=%08X a13=%08X pc=%08X',a,m,cpu.PC.value)}
 for _,n in ipairs({0,1,2,3,4,5,6,7,9,10,11,12,14})do t[#t+1]=string.format('a%d=%08X',n,cpu['A'..n].value)end
 if valid(a)and valid(m)then
  t[#t+1]=string.format('main_owner=%08X shot_owner=%08X id=%d action=%04X pose=%08X xraw=%08X yraw=%08X floor=%d flags=%04X body=%04X vx=%08X vy=%08X gravity=%08X trail=%08X',
   p:read_u32(m+0xc0),p:read_u32(m+0x230),p:read_u16(a+0x1f0),p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),
   p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_i16(m+0x200),p:read_u16(m+0x210),p:read_u16(a+0x160),
   p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20),p:read_u32(m+0x190))
 end
 return table.concat(t,' ')
end
local function log(tag,text)
 print(string.format('MK2_CPU_OVERLAP_%s frame=%d cycle=%d serial=%d %s writes=0 assistance=none',tag,frame,cycle,serial,text))
end
local instructions={
 {0xfff80800,'leg'},{0xfff91400,'choke'},{0xffffb400,'ring'},{0xfffc4800,'ring_release'},{0xffffb000,'knife'},{0xfffc3800,'knife_release'},
 {0xfffc5c00,'ring_create'},{0xfffc7000,'ring_child'},{0xfffc5800,'knife_create'},{0xfffc6000,'knife_child'},
 {0xff837d40,'guard'},{0xff837340,'damage'},{0xff876650,'fling'},{0xff876420,'landing'},
 {0xff83ed80,'cleanup'},{0xff861350,'ready'},{0xff861500,'regain'},
 {0xffffca00,'square'},{0xfff9a400,'bicycle'},{0xfff8cc00,'blade'},
 {0xff876660,'fall'},{0xfff9aaa0,'bicycle_recovery'},
 {0xff8b6820,'retire'},{0xff838790,'group'}}
for _,item in ipairs(instructions)do
 local address,kind=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'all-cycle native continuation '..kind,function(at)
  if at~=address or cpu.PC.value~=address+16 or not live()then return end
  local a,m=cpu.A8.value,cpu.A13.value
  if(kind=='leg'or kind=='choke')and a==p:read_u32(0x01060df0)and m==p:read_u32(0x01060e30)then cycle=cycle+1 end
  if(kind=='ring'or kind=='knife')and a==p:read_u32(0x01060df0)and m==p:read_u32(0x01060e30)then serial=serial+1 end
  if(kind=='ring_child'or kind=='knife_child')and valid(a)and valid(m)and p:read_u32(m+0x230)==p:read_u32(0x01060df0)then
   assert(not children[a],'Native child allocation reused before retirement')
   children[a]={main=m,serial=serial,cycle=cycle}
   log('CHILD',string.format('entry=%08X ',address)..context())
  end
  if kind=='group'and not children[a]then return end
  log('EVENT',string.format('kind=%s entry=%08X ',kind,address)..context())
  if kind=='retire'and children[a]and children[a].main==m then
   local child=children[a]
   log('RETIRE',string.format('child_serial=%d child_cycle=%d ',child.serial,child.cycle)..context())
   children[a]=nil
  end
 end)
end
for n,hp in ipairs({0x010602f0,0x01060ec0})do
 taps[#taps+1]=p:install_write_tap(hp,hp+15,'all-cycle native live damage provenance',function(at,data,mask)
  if live()then log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d mask=%04X ',n,at,p:read_u16(hp),data&0xffff,mask)..context())end
 end)
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for _,range in ipairs({{0xfff9a400,0xfff9ad00},{0xff876650,0xff876b60},{0xff83ed80,0xff83f060},{0xff837d40,0xff837dc0},{0xff861350,0xff861700},{0xfffc3800,0xfffc5800},{0xfffc6000,0xfffc8000}})do
   local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
 if not live()then return end
 for a,c in pairs(children)do
  local m=c.main
  log('CHILD_FIELD',string.format('child_serial=%d child_cycle=%d actor=%08X main=%08X owner=%08X shot_owner=%08X id=%d type=%d action=%04X pose=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X flags=%04X body=%04X parameter=%08X',
   c.serial,c.cycle,a,m,p:read_u32(m+0xc0),p:read_u32(m+0x230),p:read_u16(a+0x1f0),p:read_u16(a+0xc0),p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),
   p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u32(m+0x250)))
 end
 if cycle==2 and frame%10==0 then manager.machine.screens[':screen']:snapshot('overlap_'..frame..'.png')end
end)
emu.register_stop(function()
 local count=0;for _ in pairs(children)do count=count+1 end
 log('RESULT','live_children='..count..' scope=all_cycle_read_only_provenance_not_full_port')
 for _,tap in ipairs(taps)do tap:remove()end
end)
