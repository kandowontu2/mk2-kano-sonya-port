-- Entire current guard/body/shadow observer and the original physical driver.
dofile('mk2ks_native_selector_cpu_guard_shadow.lua')
-- Independent projectile entries, including before live predicate/global publication.
-- No game/register/HP/AI/RNG/state writes. This observer never supplies a move.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,sequence=0,0
local taps,children={},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function pool(a)return a>=0x0102d6f0 and a<0x0105b950 and (a-0x0102d6f0)%0x210==0 end
local function chain(head,free)
 local at=p:read_u32(head);local nodes,seen={},{}
 while at~=0 do
  if free and(at==0x0105b950 or(at==0x00fe0190 and nodes[#nodes]==0x0105b740))then return nodes,true end
  if not pool(at)or seen[at]or #nodes>=358 then return nodes,false end
  seen[at]=true;nodes[#nodes+1]=at;at=p:read_u32(at)
 end
 return nodes,true
end
local function contains(nodes,a)for _,v in ipairs(nodes)do if v==a then return 1 end end;return 0 end
local function context()
 local a,m=cpu.A8.value,cpu.A13.value
 local s={string.format('a8=%08X a13=%08X pc=%08X mode=%d states=%d,%d p1=%08X p1main=%08X p2=%08X p2main=%08X roster=%d,%d',
  a,m,cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(0x010601f0),p:read_u16(0x01060dc0),
  p:read_u32(0x01060220),p:read_u32(0x01060260),p:read_u32(0x01060df0),p:read_u32(0x01060e30),
  p:read_u16(0x01060280),p:read_u16(0x01060e50))}
 for n=0,14 do if n~=8 and n~=13 then s[#s+1]=string.format('a%d=%08X',n,cpu['A'..n].value)end end
 if valid(a)and valid(m)then
  s[#s+1]=string.format('owner=%08X parent=%08X victim=%08X id=%d type=%d action=%04X pose=%08X descriptor=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X flags=%04X body=%04X parameter=%08X process_slot=%d',
   p:read_u32(m+0xc0),p:read_u32(m+0x230),p:read_u32(m+0x170),p:read_u16(a+0x1f0),p:read_u16(a+0xc0),p:read_u16(m+0x1f0),
   p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),
   p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u32(m+0x250),p:read_u16(m+0x20))
  local parent=p:read_u32(m+0x230)
  if valid(parent)then s[#s+1]=string.format('parent_id=%d parent_pose=%08X parent_xraw=%08X parent_yraw=%08X',
   p:read_u16(parent+0x1f0),p:read_u32(parent+0x1d0),p:read_u32(parent+0x80),p:read_u32(parent+0xa0))end
 end
 return table.concat(s,' ')
end
local function log(tag,text)
 sequence=sequence+1
 print(string.format('MK2_STARTUP_PROJECTILE_%s frame=%d sequence=%d %s writes=0 assistance=none',tag,frame,sequence,text))
end
for _,item in ipairs({{'knife',0xffffb000},{'knife_release',0xfffc3800},
 {'knife_create',0xfffc5800},{'knife_child',0xfffc6000},{'ring',0xffffb400},
 {'ring_release',0xfffc4800},{'ring_create',0xfffc5c00},{'ring_child',0xfffc7000},
 {'guard',0xff837d40},{'tested',0xff837d90},{'unblocked',0xff837ae0},
 {'blocked',0xff837b90},{'blocked_direct',0xff837bd0},{'physical_block',0xff832040},
 {'retire',0xff8b6820},{'group',0xff838790}})do
 taps[#taps+1]=p:install_read_tap(item[2],item[2]+15,'ungated native projectile '..item[1],function(at,data,mask)
  if at~=item[2]or cpu.PC.value~=at+16 then return end
  local a,m=cpu.A8.value,cpu.A13.value
  local child=children[a]
  if item[1]=='group'and not child then return end
  if item[1]=='retire'and not child then return end
  if item[1]=='knife_child'or item[1]=='ring_child'then
   assert(valid(a)and valid(m)and not child,'Actual ungated child allocation without live filter/reuse')
   children[a]={main=m,birth=frame,kind=item[1],parent=p:read_u32(m+0x230)}
   child=children[a]
  end
  log('EVENT',string.format('kind=%s entry=%08X opcode=%04X mask=%04X ',item[1],item[2],data&0xffff,mask)..context())
  if item[1]=='retire'then
   assert(child.main==m,'Native retirement matches original ungated child Main')
   log('RETIRE',string.format('birth=%d kind=%s original_parent=%08X ',child.birth,child.kind,child.parent)..context())
   children[a]=nil
  end
 end)
end
for side,hp in ipairs({0x010602f0,0x01060ec0})do
 taps[#taps+1]=p:install_write_tap(hp,hp+15,'ungated native projectile health context',function(at,data,mask)
  if not children[cpu.A8.value]then return end
  log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d mask=%04X ',side,at,p:read_u16(at),data&0xffff,mask)..context())
 end)
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for _,range in ipairs({{0xfffc3800,0xfffc8000},{0xff8b6820,0xff8b69a0}})do
   local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
 local active,active_ok=chain(0x0105d480,false)
 local free,free_ok=chain(0x01060130,true)
 for a,c in pairs(children)do
  local m=c.main
  log('FIELD',string.format('actor=%08X main=%08X birth=%d kind=%s original_parent=%08X owner=%08X parent=%08X id=%d type=%d pose=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X flags=%04X body=%04X parameter=%08X mode=%d active=%d free=%d active_valid=%d free_valid=%d',
   a,m,c.birth,c.kind,c.parent,p:read_u32(m+0xc0),p:read_u32(m+0x230),p:read_u16(a+0x1f0),p:read_u16(a+0xc0),
   p:read_u32(a+0x1d0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),
   p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u32(m+0x250),p:read_u16(0x010601d0),
   contains(active,a),contains(free,a),active_ok and 1 or 0,free_ok and 1 or 0))
 end
end)
emu.register_stop(function()
 local count=0;for _ in pairs(children)do count=count+1 end
 log('RESULT','live_children='..count..' scope=ungated_projectile_provenance_not_automatic_acceptance')
 for _,tap in ipairs(taps)do tap:remove()end
end)
