-- Original real two-human buttons/state tracing, plus read-only native guard push.
dofile('mk2ks_human_bicycle_block_trace_v3345.lua')
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,start=0,nil
local taps={}
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,request=0x010602d0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,request=0x01060ea0}}
local function active()return start and frame<=start+180 end
local function owner(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 local ident=n==side and 18 or 17
 if a<0x01000000 or a>=0x01100000 or m<0x01000000 or m>=0x01100000 then return end
 if p:read_u16(0x010601d0)~=2 or p:read_u16(s.id)~=ident or p:read_u16(s.state)~=1 or
  p:read_u16(a+0x1f0)~=ident or p:read_u32(m+0xc0)~=a then return end
 return a,m
end
local function log(tag,text)
 print(string.format('MK2_BBPUSH_%s frame=%d side=%d writes=0 assistance=none %s',tag,frame,side,text))
end
local function event(kind,at,data,mask,n,a,m)
 local values={}
 for k=0,14 do values[#values+1]=string.format('a%d=%08X',k,cpu['A'..k].value)end
 log('EVENT',string.format('kind=%s slot=%d actor=%08X main=%08X at=%08X pc=%08X opcode=%04X mask=%04X ',
  kind,n,a,m,at,cpu.PC.value,data,mask)..table.concat(values,' '))
end
for _,item in ipairs({{0xfff9a400,'own_entry'},{0xff8e8230,'guard_handler'},
 {0xff876be0,'away_request'},{0xff8e9fc0,'guard_cycle'},{0xff80dcc0,'sleep'},
 {0xff8ea120,'guard_stop'},{0xff8e9d80,'guard_return'}})do
 local at,kind=item[1],item[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'native real blocked push '..kind,function(address,data,mask)
  if address~=at or cpu.PC.value~=at+16 then return end
  for n=1,2 do
   local a,m=owner(n)
   if a and cpu.A8.value==a and cpu.A13.value==m then
    if kind=='own_entry'and n==side then assert(not start);start=frame end
    if active()and(kind=='own_entry'and n==side or n==3-side and frame<=start+40)then
     event(kind,address,data,mask,n,a,m)
    end
   end
  end
 end)
end
for n,s in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(s.request,s.request+31,'physical desired blocked push '..n,function(at,value,mask)
  if at~=s.request or not active()then return end
  local a,m=owner(n);if not a then return end
  log('REQUEST',string.format('slot=%d actor=%08X main=%08X at=%08X before=%08X after=%08X mask=%08X pc=%08X a8=%08X a13=%08X op0=%04X',
   n,a,m,at,p:read_u32(at),value,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(cpu.PC.value-16)))
 end)
end
emu.register_frame(function()
 frame=frame+1
 if active()then
  for n,s in ipairs(slots)do
   local a,m=assert(owner(n));assert(m)
   log('REQUEST_STATE',string.format('slot=%d actor=%08X main=%08X requested=%08X',n,a,m,p:read_u32(s.request)))
  end
 end
end)
emu.register_stop(function()
 log('RESULT','start='..(start or -1)..' last='..frame..' fullPortAcceptance=false')
 for _,tap in ipairs(taps)do tap:remove()end
end)
