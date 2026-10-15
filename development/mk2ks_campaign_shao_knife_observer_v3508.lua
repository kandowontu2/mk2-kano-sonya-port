-- Read-only companion to the frozen v3510 Kano cold campaign driver.
-- Observe actual child ownership, guard and native damage; never add inputs.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
assert(side==1 or side==2)
assert(os.getenv('MK2KS_TEST_FIGHTER')=='kano')
local opponent=3-side
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,serial=0,0
local taps,children={},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_BOSS_KNIFE_%s frame=%d serial=%d human_slot=%d %s writes=0 assistance=none',tag,frame,serial,side,text))
end
local function active()
 local a,m=p:read_u32(slots[side].actor),p:read_u32(slots[side].main)
 return p:read_u16(0x01061b30)==16 and p:read_u16(0x010601d0)==2 and
  p:read_u16(slots[side].state)==1 and p:read_u16(slots[opponent].state)==0 and
  p:read_u16(slots[side].roster)==17 and p:read_u16(slots[opponent].roster)==13 and
  valid(a)and valid(m)and p:read_u16(a+0x1f0)==17 and p:read_u32(m+0xc0)==a
end
local function context()
 local a,m=cpu.A8.value,cpu.A13.value
 local values={string.format('a8=%08X a13=%08X pc=%08X mode=%d stage=%d roster=%d,%d states=%d,%d actors=%08X,%08X mains=%08X,%08X health=%d,%d',
  a,m,cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),
  p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor),
  p:read_u32(slots[1].main),p:read_u32(slots[2].main),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp))}
 for _,n in ipairs({0,1,2,3,4,5,6,7,9,10,11,12,14})do values[#values+1]=string.format('a%d=%08X',n,cpu['A'..n].value)end
 if valid(a)and valid(m)then
  local vm=p:read_u32(m+0x170)
  values[#values+1]=string.format('owner=%08X parent=%08X id=%d action=%04X descriptor=%08X pose=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X floor=%d flags=%04X body=%04X victim_main=%08X',
   p:read_u32(m+0xc0),p:read_u32(m+0x230),p:read_u16(a+0x1f0),p:read_u16(m+0x1f0),p:read_u32(m+0x100),
   p:read_u32(a+0x1d0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),
   p:read_i16(m+0x200),p:read_u16(m+0x210),p:read_u16(a+0x160),vm)
  if valid(vm)then
   local va=p:read_u32(vm+0xc0)
   values[#values+1]=string.format('victim_actor=%08X victim_flags=%04X victim_id=%d',va,p:read_u16(vm+0x210),valid(va)and p:read_u16(va+0x1f0)or-1)
  end
 end
 return table.concat(values,' ')
end
local instructions={{0xffffb000,'entry'},{0xfffc3800,'release'},{0xfffc5800,'create'},{0xfffc6000,'child'},
 {0xff8b6ac0,'frontgate'},{0xff835410,'strike'},{0xff837d40,'guard'},{0xff837d90,'tested_guard'},
 {0xff837ae0,'unblocked'},{0xff837b90,'blocked'},{0xff837bd0,'blocked'},{0xff832040,'physical_block'},
 {0xff835d20,'normal_damage_extract'},{0xff836040,'blocked_damage_extract'},{0xff8369f0,'shao_scaler'},
 {0xff8afe80,'travel'},{0xff8affb0,'impact'},{0xff838790,'group'},{0xff8b6820,'retire'},
 {0xff861350,'ready'},{0xff861500,'regain'}}
for _,item in ipairs(instructions)do
 local at,kind=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'read-only actual Shao Knife '..kind,function(address)
  if address~=at or cpu.PC.value~=at+16 then return end
  local a,m=cpu.A8.value,cpu.A13.value
  local own=active()and a==p:read_u32(slots[side].actor)and m==p:read_u32(slots[side].main)
  if kind=='entry'and own then serial=serial+1 end
  if kind=='child'and active()and valid(a)and valid(m)and p:read_u16(a+0x1f0)==17 and
   p:read_u32(m+0xc0)==a and p:read_u32(m+0x230)==p:read_u32(slots[side].actor)then
   local old=children[a]
   log('BIRTH',string.format('reused_unretired=%d entry=%08X ',old and 1 or 0,at)..context())
   children[a]={main=m,serial=serial,parent=p:read_u32(m+0x230)}
  end
  local child=children[a]
  if not own and not(child and child.main==m)then return end
  log('EVENT',string.format('kind=%s entry=%08X child_serial=%d ',kind,at,child and child.serial or 0)..context())
  if kind=='retire'and child and child.main==m then
   log('RETIRE',string.format('child_serial=%d birth_parent=%08X ',child.serial,child.parent)..context());children[a]=nil
  end
 end)
end
for n,s in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(s.hp,s.hp+15,'read-only Shao Knife health provenance',function(at,data,mask)
  if active()then
   log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d mask=%04X ',n,at,p:read_u16(at),data&0xffff,mask)..context())
  end
 end)
end
emu.register_frame(function()
 frame=frame+1
 if not active()then return end
 for a,c in pairs(children)do
  local m=c.main
  log('CHILD_FIELD',string.format('child_serial=%d actor=%08X main=%08X owner=%08X parent=%08X birth_parent=%08X id=%d action=%04X descriptor=%08X pose=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X flags=%04X body=%04X',
   c.serial,a,m,p:read_u32(m+0xc0),p:read_u32(m+0x230),c.parent,p:read_u16(a+0x1f0),p:read_u16(m+0x1f0),p:read_u32(m+0x100),
   p:read_u32(a+0x1d0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u16(m+0x210),p:read_u16(a+0x160)))
 end
end)
emu.register_stop(function()
 local count=0;for _ in pairs(children)do count=count+1 end
 log('RESULT','tracked_unretired_children='..count..' scope=read_only_source_prepared_runtime_not_accepted')
 for _,tap in ipairs(taps)do tap:remove()end
end)
