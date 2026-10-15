-- Unchanged cold real two-human controls; additional read-only native tracing.
dofile('mk2ks_human_special_negative_v9.lua')
assert(os.getenv('MK2KS_HUMAN_SPECIAL_MOVE')=='bicycle')
assert(os.getenv('MK2KS_HUMAN_SPECIAL_SCENARIO')=='block')
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local output=assert(os.getenv('MK2KS_BBLOCK_OUT'))
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,start=0,nil
local taps,bound={},{}
local slots={{a=0x01060220,m=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {a=0x01060df0,m=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(v)return v>=0x01000000 and v<0x01100000 end
local function active()return start and frame<=start+180 end
local function log(tag,text)
 print(string.format('MK2_BBLOCK_%s frame=%d side=%d writes=0 assistance=none %s',tag,frame,side,text or''))
end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.a),p:read_u32(s.m)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.id),state=p:read_u16(s.state),
  hp=p:read_u16(s.hp),pose=p:read_u32(a+0x1d0),xraw=p:read_u32(a+0x80),yraw=p:read_u32(a+0xa0),
  vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),flags=p:read_u16(m+0x210),
  body=p:read_u16(a+0x160),facing=p:read_u16(a+0xf0),trail=p:read_u32(m+0x190),action=p:read_u16(m+0x1f0),floor=p:read_i16(m+0x200)}
end
local function state(tag,n,a)
 local text={'slot='..n,'mode='..p:read_u16(0x010601d0),'stage_floor='..p:read_i16(0x0105ecd0),
  'suppression='..p:read_u16(0x010619d0),'arena='..p:read_u16(0x01061ac0)}
 for _,key in ipairs({'actor','main','owner','pose','xraw','yraw','vx','vy','gravity','flags','body','facing','trail','action'})do
  text[#text+1]=string.format('%s=%08X',key,a[key])
 end
 for _,key in ipairs({'id','roster','state','hp','floor'})do text[#text+1]=key..'='..a[key]end
 log(tag,table.concat(text,' '))
end
local function owns()
 local own=sample(side)
 return own and p:read_u16(0x010601d0)==2 and own.id==18 and own.roster==18 and own.state==1 and
  own.actor==own.owner and own.actor==cpu.A8.value and own.main==cpu.A13.value
end
for _,item in ipairs({{0xfff9a400,'entry'},{0xfff9aa30,'collision'},{0xfff9acf0,'contact'},
 {0xfff9ad50,'block_test'},{0xfff9b9f0,'blocked'},{0xfff9ade0,'paired'},
 {0xff876650,'fling'},{0xff876420,'landing'},{0xff861350,'ready'},{0xff861500,'regain'}})do
 local address,kind=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual human Bicycle '..kind,function(at,data,mask)
  if at~=address or cpu.PC.value~=address+16 or not owns()then return end
  if kind=='entry'then
   assert(not start,'Exactly one actual owned Bicycle entry');start=frame
   for n=1,2 do state('ENTRY_STATE',n,assert(sample(n)))end
  end
  if not active()then return end
  local values={}
  for n=0,14 do values[#values+1]=string.format('a%d=%08X',n,cpu['A'..n].value)end
  log('EVENT',string.format('kind=%s entry=%08X pc=%08X opcode=%04X mask=%04X status=%08X carry=%d b2=%08X ',
   kind,at,cpu.PC.value,data,mask,cpu.ST.value,(cpu.ST.value>>30)&1,cpu.B2.value)..table.concat(values,' '))
 end)
end
for n,s in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(s.hp,s.hp+15,'actual physical Bicycle block health',function(at,value,mask)
  if at~=s.hp or not active()then return end
  log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X op0=%04X op1=%04X op2=%04X',
   n,at,p:read_u16(at),value&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,
   p:read_u16(cpu.PC.value-48),p:read_u16(cpu.PC.value-32),p:read_u16(cpu.PC.value-16)))
 end)
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  local file=assert(io.open(output..'/guest_maincpu.bin','wb'));file:write(raw);file:close()
  log('GUEST','bytes=1048576')
 end
 for n=1,2 do
  local a=sample(n)
  if a and a.actor==a.owner and p:read_u16(0x010601d0)==2 then
   for _,kind in ipairs({'body','flags','action'})do
    local address=kind=='body'and a.actor+0x160 or a.main+(kind=='flags'and 0x210 or 0x1f0)
    local key=string.format('%d:%s:%08X',n,kind,address)
    if not bound[key]then
     bound[key]=true
     taps[#taps+1]=p:install_write_tap(address,address+15,'actual human Bicycle state '..key,function(at,value,mask)
      if at~=address or not active()or p:read_u32(slots[n].a)~=a.actor or p:read_u32(slots[n].m)~=a.main then return end
      log('FLAG',string.format('slot=%d kind=%s at=%08X before=%04X after=%04X mask=%04X pc=%08X op0=%04X op1=%04X actor=%08X main=%08X',
       n,kind,at,p:read_u16(at),value&0xffff,mask,cpu.PC.value,p:read_u16(cpu.PC.value-32),p:read_u16(cpu.PC.value-16),a.actor,a.main))
     end)
    end
   end
   if active()then state('FIELD',n,a)end
  end
 end
end)
emu.register_stop(function()
 log('RESULT','start='..(start or -1)..' last='..frame..' fullPortAcceptance=false')
 for _,tap in ipairs(taps)do tap:remove()end
end)
