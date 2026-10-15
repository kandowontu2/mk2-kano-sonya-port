-- Extended original physical commands remain exclusively in the base driver.
-- Observe actual native shadow DMA/cache ownership and actor retirement only.
dofile('mk2ks_current_friendship_extended_wins_v2688.lua')
local cpu=manager.machine.devices[':maincpu']
local p,state=cpu.spaces.program,cpu.state
local gfx=manager.machine.memory.regions[':gfxrom']
local side=assert(tonumber(os.getenv('MK2KS_FRIEND_SIDE')))
local fighter=assert(os.getenv('MK2KS_FRIEND_WINNER'))
local identity=assert(({kano=17,sonya=18,cage=2,liu_kang=1})[fighter])
local victim=assert(({[17]=18,[18]=17,[2]=1,[1]=2})[identity])
local ids=side==1 and {identity,victim}or {victim,identity}
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,hp=0x010602f0,state=0x010601f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,hp=0x01060ec0,state=0x01060dc0}}
local frame,active,action,cleanup=0,false,nil,nil
local components,taps,emitted={},{},{}
local unknown,all_copies,total_copies,total_components,total_unknown=0,0,0,0,0
local dma=nil
for _,device in pairs(manager.machine.devices)do
 for name,index in pairs(device.items)do
  if name:match('m_dma_register$')then dma=emu.item(index)end
 end
end
assert(dma,'Actual native DMA register item')
local mapping={{[0]=0,1,2,3,4,5,6,7,8,9,10,11,16,17,14,15},
 {[0]=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 print(string.format('MK2_FRIEND_SHADOW_%s frame=%d fighter=%s side=%d writes=0 assistance=none %s',tag,frame,fighter,side,value or''))
end
local function sample(n)
 local slot=slots[n];local a,m=p:read_u32(slot.actor),p:read_u32(slot.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(slot.roster),
  cache=p:read_u32(a+0x1a0),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),
  body=p:read_u16(a+0x160),facing=p:read_u16(a+0xf0),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),
  floor=p:read_i16(m+0x200),hp=p:read_u16(slot.hp),state=p:read_u16(slot.state)}
end
local function graphics(source,command,width,height)
 local key=string.format('%08X_%04X_%d_%d',source,command,width,height)
 if emitted[key]then return end
 emitted[key]=true
 local offset=source
 if source>=0x10000000 and source<0x1a000000 then offset=source-0x0a000000 end
 if offset>=0xf8000000 then offset=offset-0xf8000000 end
 local first=offset//8;local bpp=(command>>12)&7;if bpp==0 then bpp=8 end
 local bytes=math.ceil((offset%8+width*height*bpp+(command&0x80~=0 and height*8 or 0))/8)+8
 assert(first>=0 and first+bytes<=0x2000000,'Complete actual shadow source bounds')
 local raw={};for at=first,first+bytes-1 do raw[#raw+1]=string.format('%02X',gfx:read_u8(at))end
 log('GFX',string.format('key=%s source=%08X command=%04X width=%d height=%d offset=%d first=%d bytes=%d data=%s',key,source,command,width,height,offset,first,bytes,table.concat(raw)))
end
local action_address=identity<17 and p:read_u32(0xff880d90+identity*32)or 0xff800000+(identity==17 and 0xf9a00 or 0xf9c00)*8
for _,address in ipairs({action_address,0xff880cc0})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'Friendship shadow action/cleanup context',function(at)
  if at~=address or not active then return end
  if address==action_address and not action then action=frame;log('ACTION',string.format('entry=%08X actor=%08X main=%08X id=%d',address,state.A8.value,state.A13.value,identity))end
  if address==0xff880cc0 and action then cleanup=cleanup or frame;log('CLEANUP',string.format('entry=%08X actor=%08X main=%08X',address,state.A8.value,state.A13.value))end
 end)
end
for n=1,2 do
 local address=slots[n].actor
 taps[#taps+1]=p:install_write_tap(address,address+31,'Friendship actual actor-global stores',function(at,data,mask)
  if not active then return end
  log('POINTER',string.format('slot=%d at=%08X value=%04X mask=%04X pc=%08X mode=%d finish=%d',n,at,data&65535,mask,state.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061b00)))
 end)
end
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'Friendship actual native floor-shadow DMA',function(at,data,mask)
 if not active then return end
 local bank=(dma:read(15)>>5)&1;local reg=mapping[bank+1][(at-0x01a80000)//16]
 local command=(dma:read(reg)&(~mask))|(data&mask)
 if reg~=1 or command&0x8000==0 or (state.PC.value~=0xff8015a0 and state.PC.value~=0xff801610)then return end
 all_copies=all_copies+1;total_copies=total_copies+1
 assert(command&15==8 and dma:read(8)&0x7f00==0 and dma:read(9)&255==15 and dma:read(7)&0x3ff==1,'Actual original black one-row native shadow DMA')
 local row=state.A9.value;local slot,body=nil,nil
 for n=1,2 do
  local a=sample(n)
  if a and valid(a.cache)and row>=a.cache and row<a.cache+12*0x70 and (row-a.cache)%0x70==0 then
   assert(not slot,'One unambiguous actual physical shadow cache owner');slot,body=n,a
  end
 end
 if not slot then
  unknown=unknown+1;total_unknown=total_unknown+1
  log('UNOWNED',string.format('row=%08X source=%08X pc=%08X mode=%d finish=%d',row,dma:read(2)|(dma:read(3)<<16),state.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061b00)))
  return
 end
 assert(body.id==ids[slot]and body.roster==body.id and body.owner==body.actor,'True physical character owns native shadow cache')
 local key=string.format('%d_%08X_%08X_%08X',slot,body.actor,row,body.pose)
 if not components[key]then
  local source=p:read_u32(row);local c=p:read_u16(row+0x40);local width,height=p:read_u16(row+0x20),p:read_u16(row+0x30)
  components[key]={slot=slot,a=body,row=row,source=source,command=c,width=width,height=height,
   mode=p:read_u16(0x010601d0),finish=p:read_u16(0x01061b00),copies=0,first=dma:read(2)|(dma:read(3)<<16),first_x=dma:read(4)&1023,first_y=dma:read(5)&511}
  graphics(source,c|0x8002,width,height)
 end
 local c=components[key];c.copies=c.copies+1;c.last=dma:read(2)|(dma:read(3)<<16);c.last_x=dma:read(4)&1023;c.last_y=dma:read(5)&511;c.last_pc=state.PC.value
end)
emu.register_frame(function()
 frame=frame+1;components={};unknown=0;all_copies=0
 if not active then
  local a,b=sample(1),sample(2)
  if p:read_u16(0x010601d0)==2 and a and b and a.id==ids[1]and b.id==ids[2]and a.owner==a.actor and b.owner==b.actor then
   active=true;log('BEGIN',string.format('ids=%d,%d',ids[1],ids[2]))
  end
 end
end)
emu.register_frame_done(function()
 if not active then return end
 local count,copies=0,0
 for _,c in pairs(components)do
  count=count+1;copies=copies+c.copies;local a=c.a
  log('COMPONENT',string.format('slot=%d id=%d roster=%d actor=%08X main=%08X owner=%08X cache=%08X row=%08X pose=%08X flags=%04X body=%04X facing=%04X floor=%d x=%d y=%d mode=%d finish=%d source=%08X command=%04X width=%d height=%d copies=%d first=%08X last=%08X firstX=%d firstY=%d lastX=%d lastY=%d lastPC=%08X',
   c.slot,a.id,a.roster,a.actor,a.main,a.owner,a.cache,c.row,a.pose,a.flags,a.body,a.facing,a.floor,a.x,a.y,c.mode,c.finish,c.source,c.command,c.width,c.height,c.copies,c.first,c.last,c.first_x,c.first_y,c.last_x,c.last_y,c.last_pc))
 end
 assert(copies+unknown==all_copies,'Every actual original shadow DMA callback accounted')
 total_components=total_components+count
 log('FIELD',string.format('mode=%d finish=%d action=%d cleanup=%d copies=%d ownedCopies=%d components=%d unresolvedCopies=%d stage=%d stageY=%d cameraX=%d cameraY=%d displayY=%d',
  p:read_u16(0x010601d0),p:read_u16(0x01061b00),action or -1,cleanup or -1,all_copies,copies,count,unknown,p:read_u16(0x01061ac0),p:read_i16(0x0105ecd0),p:read_i16(0x0105d120),p:read_i16(0x0105d130),p:read_i16(0x0105d060)))
 for n=1,2 do
  local a=sample(n)
  if a then
   log('BODY',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d cache=%08X pose=%08X flags=%04X body=%04X facing=%04X floor=%d x=%d y=%d',n,a.actor,a.main,a.owner,a.id,a.roster,a.state,a.hp,a.cache,a.pose,a.flags,a.body,a.facing,a.floor,a.x,a.y))
  else
   log('ABSENT',string.format('slot=%d actor=%08X main=%08X roster=%d state=%d',n,p:read_u32(slots[n].actor),p:read_u32(slots[n].main),p:read_u16(slots[n].roster),p:read_u16(slots[n].state)))
  end
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('action=%d cleanup=%d nativeCopies=%d physicalComponents=%d unresolvedCopies=%d',action or -1,cleanup or -1,total_copies,total_components,total_unknown))
 for _,tap in ipairs(taps)do tap:remove()end
end)
