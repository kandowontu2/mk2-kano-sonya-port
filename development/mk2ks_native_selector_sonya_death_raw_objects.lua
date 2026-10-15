-- Additional passive raw-object lifecycle/FIFO evidence; original inputs.
dofile('mk2ks_native_selector_sonya_throw_late_views.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,sequence=0,0
local taps,objects,marks={},{},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 sequence=sequence+1
 print(string.format('MK2_DEATH_RAW_%s frame=%d sequence=%d %s writes=0 assistance=none',tag,frame,sequence,value))
end
local function object_words(a)
 return string.format('actor=%08X next=%08X type=%d priority=%d id=%d body=%04X facing=%04X pose=%08X descriptor=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X size=%08X graphic=%08X',
  a,p:read_u32(a),p:read_u16(a+0xc0),p:read_u16(a+0xd0),p:read_u16(a+0x1f0),p:read_u16(a+0x160),p:read_u16(a+0xf0),
  p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),
  p:read_u32(a+0x120),p:read_u32(a+0x100))
end
local function registers()
 local out={};for n=0,14 do out[#out+1]=string.format('a%d=%08X',n,cpu['A'..n].value)end
 return table.concat(out,' ')
end
local function mark(label)
 for _,age in ipairs({0,1,3,8,16,32,64,80,81})do
  local at=frame+age
  marks[at]=marks[at] and(marks[at]..'_'..label..'_age'..age)or(label..'_age'..age)
 end
end
for _,entry in ipairs({{0xffa0e060,'first',9},{0xffa0e3b0,'second',10}})do
 taps[#taps+1]=p:install_read_tap(entry[1],entry[1]+15,'passive original death raw constructor return',function(at,data,mask)
  if at~=entry[1]or cpu.PC.value~=at+16 then return end
  local subject=cpu['A'..entry[3]].value
  if not valid(subject)or subject~=p:read_u32(0x01060220)or p:read_u16(subject+0x1f0)~=18 then return end
  local a=cpu.A8.value;assert(valid(a)and a~=subject and not objects[a])
  objects[a]={born=frame,kind=entry[2],subject=subject,descriptor=cpu.A5.value}
  log('CONSTRUCT',string.format('kind=%s subject=%08X entry=%08X pc=%08X opcode=%04X mask=%04X %s %s',
   entry[2],subject,at,cpu.PC.value,data&0xffff,mask&0xffff,object_words(a),registers()))
  mark('raw_'..entry[2]..'_constructor')
 end)
end
for _,entry in ipairs({{0xff840450,'actor_retire',0},{0xff83a4e0,'actor_clear',8}})do
 taps[#taps+1]=p:install_read_tap(entry[1],entry[1]+15,'passive tracked death raw removal',function(at,data,mask)
  if at~=entry[1]or cpu.PC.value~=at+16 then return end
  local a=cpu['A'..entry[3]].value;local item=objects[a]
  if not item then return end
  log('REMOVE',string.format('kind=%s removal=%s birth=%d subject=%08X entry=%08X pc=%08X opcode=%04X mask=%04X %s %s',
   item.kind,entry[2],item.born,item.subject,at,cpu.PC.value,data&0xffff,mask&0xffff,object_words(a),registers()))
  if entry[2]=='actor_retire'then item.retired=frame;mark('raw_'..item.kind..'_retirement')end
 end)
end
for _,entry in ipairs({{0xff8042a0,'CANDIDATE'},{0xff804410,'QUEUE'}})do
 taps[#taps+1]=p:install_read_tap(entry[1],entry[1]+15,'passive complete tracked raw native FIFO',function(at,data,mask)
  if at~=entry[1]or cpu.PC.value~=at+16 then return end
  local a=cpu.A0.value;local item=objects[a]
  if not item then return end
  log(entry[2],string.format('kind=%s birth=%d subject=%08X entry=%08X pc=%08X opcode=%04X mask=%04X %s %s',
   item.kind,item.born,item.subject,at,cpu.PC.value,data&0xffff,mask&0xffff,object_words(a),registers()))
 end)
end
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 for a,item in pairs(objects)do
  if not item.retired then log('FIELD',string.format('kind=%s birth=%d subject=%08X mode=%d %s',
   item.kind,item.born,item.subject,p:read_u16(0x010601d0),object_words(a)))end
 end
 local label=marks[frame]
 if label then
  marks[frame]=nil
  local raw,w,h=manager.machine.screens[':screen']:pixels()
  assert(w==400 and h==254 and #raw==406400)
  print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',
   frame,label,w,h,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
end)
emu.register_stop(function()
 local n=0;for _ in pairs(objects)do n=n+1 end
 for _,tap in ipairs(taps)do tap:remove()end
 log('RESULT',string.format('objects=%d taps=%d scope=passive_original_raw_path_not_whole_art_acceptance',n,#taps))
end)
