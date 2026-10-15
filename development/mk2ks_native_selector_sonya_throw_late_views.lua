-- Same original inputs and unsupplied CPU. Only additional passive observers.
dofile('mk2ks_native_selector_sonya_human_kano_cpu.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,sequence=0,0
local taps,bound,marks={},{},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 sequence=sequence+1
 print(string.format('MK2_LATE_THROW_%s frame=%d sequence=%d %s writes=0 assistance=none',tag,frame,sequence,text))
end
local function mark(label,ages)
 for _,age in ipairs(ages)do
  local at=frame+age
  marks[at]=marks[at] and(marks[at]..'_'..label..'_age'..age)or(label..'_age'..age)
 end
end
local function context(a,m)
 local words={}
 for n=0,14 do words[#words+1]=string.format('a%d=%08X',n,cpu['A'..n].value)end
 local pc=cpu.PC.value
 return string.format('pc=%08X op0=%04X op1=%04X actor=%08X main=%08X owner=%08X id=%d floor=%d xraw=%08X yraw=%08X pose=%08X body=%04X action=%04X %s',
  pc,p:read_u16(pc-32),p:read_u16(pc-16),a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_i16(m+0x200),
  p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x1d0),p:read_u16(a+0x160),p:read_u16(m+0x1f0),table.concat(words,' '))
end
emu.register_frame(function()
 frame=frame+1
 for slot,field in ipairs({0x01060220,0x01060df0})do
  local a,m=p:read_u32(field),p:read_u32(field+0x40)
  local mode=p:read_u16(0x010601d0)
  if (mode==2 or mode==7)and valid(a)and valid(m)and p:read_u32(m+0xc0)==a and
     p:read_u16(a+0x1f0)==(slot==1 and 18 or 17)and not bound[m]then
   bound[m]=a
   log('BIND',string.format('slot=%d actor=%08X main=%08X floorAt=%08X bodyAt=%08X',slot,a,m,m+0x200,a+0x160))
   taps[#taps+1]=p:install_write_tap(m+0x200,m+0x20f,'passive true actor Main floor',function(at,data,mask)
    if at~=m+0x200 or p:read_u32(m+0xc0)~=a then return end
    local before=p:read_u16(at);local after=(before&(~mask&0xffff))|(data&mask&0xffff)
    log('FLOOR_STORE',string.format('slot=%d at=%08X before=%04X after=%04X data=%04X mask=%04X ',slot,at,before,after,data&0xffff,mask&0xffff)..context(a,m))
    if slot==1 and before-after==8 then mark('native_floor_lowering',{0,1,3,12,24,64})end
   end)
   taps[#taps+1]=p:install_write_tap(a+0x160,a+0x16f,'passive actual victim body flag handoff',function(at,data,mask)
    if at~=a+0x160 or p:read_u32(m+0xc0)~=a then return end
    local before=p:read_u16(at);local after=(before&(~mask&0xffff))|(data&mask&0xffff)
    log('BODY_STORE',string.format('slot=%d at=%08X before=%04X after=%04X data=%04X mask=%04X ',slot,at,before,after,data&0xffff,mask&0xffff)..context(a,m))
    if slot==1 and before&0x20==0 and after&0x20~=0 then mark('native_body_handoff',{0,1,3,12,32,64})end
   end)
  end
 end
end)
taps[#taps+1]=p:install_read_tap(0xff804190,0xff80419f,'passive actual native multipart skip test',function(at,data,mask)
 if at~=0xff804190 or cpu.PC.value~=0xff8041a0 then return end
 local a=cpu.A0.value
 for slot,field in ipairs({0x01060220,0x01060df0})do
  local actor,m=p:read_u32(field),p:read_u32(field+0x40)
  if actor==a and valid(a)and valid(m)and p:read_u32(m+0xc0)==a and p:read_u16(a+0x160)&0x20~=0 then
   log('BODY_SKIP_TEST',string.format('slot=%d at=%08X opcode=%04X mask=%04X ',slot,at,data&0xffff,mask&0xffff)..context(a,m))
  end
 end
end)
emu.register_frame_done(function()
 local label=marks[frame]
 if not label then return end
 marks[frame]=nil
 log('VIEW_CONTEXT',string.format('label=%s mode=%d stage=%d winner=%d p1=%08X p1main=%08X p2=%08X p2main=%08X',
  label,p:read_u16(0x010601d0),p:read_u16(0x0105d110),p:read_u16(0x01060200),
  p:read_u32(0x01060220),p:read_u32(0x01060260),p:read_u32(0x01060df0),p:read_u32(0x01060e30)))
 for a=0x0102d6f0,0x0105b740,0x210 do
  local pose=p:read_u32(a+0x1d0)
  if pose~=0 then
   log('POOL_ACTOR',string.format('label=%s actor=%08X next=%08X type=%d id=%d body=%04X facing=%04X pose=%08X cache=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X',
    label,a,p:read_u32(a),p:read_u16(a+0xc0),p:read_u16(a+0x1f0),p:read_u16(a+0x160),p:read_u16(a+0xf0),
    pose,p:read_u32(a+0x1a0),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60)))
  end
 end
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',
  frame,label,w,h,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end)
emu.register_stop(function()
 for _,tap in ipairs(taps)do tap:remove()end
 log('RESULT',string.format('boundOwners=%d observerTaps=%d scope=passive_original_throw_handoff_not_art_acceptance',
  (function()local n=0;for _ in pairs(bound)do n=n+1 end;return n end)(),#taps))
end)
