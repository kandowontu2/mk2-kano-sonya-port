-- Cold physical-input mirror selection. Every guest-memory operation is read-only.
local name=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local identity=assert(({kano=17,sonya=18,liu_kang=1})[name])
local confirm_first=assert(tonumber(os.getenv('MK2KS_MIRROR_CONFIRM_FIRST')))
assert(confirm_first==1 or confirm_first==2)
local output=assert(os.getenv('MK2KS_REPTILE_AUDIT_DIR'))
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local high,system,low=manager.machine.ioport.ports[':IN0'].fields,
 manager.machine.ioport.ports[':IN1'].fields,manager.machine.ioport.ports[':IN2'].fields
local buttons={}
for n=1,2 do
 buttons[n]={}
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[n][key]=high['P'..n..' '..key]end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=low['P'..n..' '..key]end
 buttons[n].Coin=system['Coin '..n]
 buttons[n].Start=system[n==1 and '1 Player Start'or'2 Players Start']
end
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,join_at,first_live,last_mode=0,nil,nil,nil
local css,plans,confirmed={},{},{}
local live_fields,seen_fifo,seen_palette,taps=0,{},{},{}
local pending={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,s)
 print(string.format('MK2_NATURAL_MIRROR_V1142_%s frame=%d fighter=%s writes=0 assistance=none %s',tag,frame,name,s or''))
end
local function save(file,data)local f=assert(io.open(output..'/'..file,'wb'));f:write(data);f:close()end
local function press(n,key)
 buttons[n][key]:set_value(1);log('INPUT',string.format('slot=%d button=%s',n,key:gsub(' ','_')))
end
local function route(start,target)
 local queue={{start,{}}};local seen={[start]=true};local index=1
 local tables={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
 while queue[index]do
  local item=queue[index];index=index+1
  if item[1]==target then return item[2]end
  for _,key in ipairs({'Left','Right','Down'})do
   local id=p:read_u16(tables[key]+item[1]*16)
   if id<=18 and not seen[id]then
    local path={table.unpack(item[2])};path[#path+1]=key
    queue[#queue+1]={id,path};seen[id]=true
   end
  end
 end
 error('No native CSS route')
end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.id),
  flags=p:read_u16(a+0x160),bank=p:read_u16(a+0x140),pose=p:read_u32(a+0x1d0),
  x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),hp=p:read_u16(s.hp)}
end
-- Observe the original game's own flag assignment, without replacing a value.
taps[#taps+1]=p:install_write_tap(0x01000000,0x010fffff,'native mirror flag writer',function(at,data,mask)
 if frame<700 or mask&0xffff~=0xffff then return end
 for n=1,2 do
  local a=p:read_u32(slots[n].actor)
  if valid(a)and at==a+0x160 then
   log('FLAG_WRITE',string.format('slot=%d actor=%08X id=%d old=%04X new=%04X pc=%08X',n,a,p:read_u16(a+0x1f0),p:read_u16(at),data&0xffff,cpu.PC.value))
  end
 end
end)
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'native mirror physical fighter FIFO',function(at)
 if not first_live or at~=0xff804410 or cpu.PC.value~=0xff804420 then return end
 local a=cpu.A0.value
 for n=1,2 do
  local own=sample(n)
  if own and a==own.actor and not seen_fifo[n]then
   seen_fifo[n]=true
   log('FIFO',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d flags=%04X source=%08X pose=%08X bank=%04X command=%04X',
    n,a,own.main,own.owner,own.id,own.flags,cpu.A11.value,own.pose,own.bank,cpu.A12.value))
  end
 end
end)
emu.register_frame(function()
 assert(#taps==2)
 frame=frame+1
 for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
 if frame==1 then
  local blocks={}
  for block=0,0xfffff,0x1000 do
   local bytes={};for at=0,0xfff do bytes[#bytes+1]=string.char(p:read_u8(0xff800000+(block+at)*8))end
   blocks[#blocks+1]=table.concat(bytes)
  end
  save('guest_maincpu.bin',table.concat(blocks));log('BOOT','guest_bytes=1048576')
 end
 if frame>=300 and frame<304 then press(1,'High Punch')end
 if frame>=600 and frame<604 then press(1,'Coin')end
 if frame>=608 and frame<612 then press(2,'Coin')end
 if frame>=620 and frame<624 then press(1,'Start')end
 local mode=p:read_u16(0x010601d0)
 if join_at then
  local age=frame-join_at
  if age>=0 and age<4 then press(1,'Coin')end
  if age>=8 and age<12 then press(2,'Coin')end
  if age>=20 and age<24 then press(2,'Start')end
 end
 if mode~=last_mode then log('MODE','mode='..mode);last_mode=mode end
 for n=1,2 do
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css[n]then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].id),identity)
   if n==1 and not join_at then join_at=frame end
   log('SELECT',string.format('slot=%d target=%d path=%s',n,identity,table.concat(plans[n],',')))
  end
  if css[n]and mode==4 then
   local age=frame-css[n]
   for i,key in ipairs(plans[n])do if age>=56+(i-1)*12 and age<60+(i-1)*12 then press(n,key)end end
   if age==120 then pending[#pending+1]='select_p'..n..'_'..frame..'.png' end
   local both_ready=css[1]and css[2]and math.max(css[1],css[2])
   if both_ready then
    local begin=both_ready+(n==confirm_first and 148 or 210)
    if frame>=begin and frame<begin+8 then
     if not confirmed[n]then confirmed[n]=frame;log('CONFIRM','slot='..n..' roster='..p:read_u16(slots[n].id))end
     press(n,'High Punch')
    end
   end
  end
 end
 local a,b=sample(1),sample(2)
 if not a or not b or a.id~=identity or b.id~=identity or a.owner~=a.actor or b.owner~=b.actor then return end
 if (mode==2 or mode==6)and p:read_u16(0x01061b00)==0 and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then
  if not first_live then first_live=frame;log('FIRST_LIVE',string.format('ids=%d,%d actors=%08X,%08X flags=%04X,%04X confirm_first=%d',a.id,b.id,a.actor,b.actor,a.flags,b.flags,confirm_first))end
  live_fields=live_fields+1
  local age=frame-first_live
  if age==30 or age==180 or age==360 then pending[#pending+1]='mirror_live_'..age..'_'..frame..'.png' end
  if age>=210 and age<250 then press(1,'Left');press(2,'Right')end
  if age>=270 and age<300 then press(1,'Down');press(2,'Block')end
  for n,own in ipairs({a,b})do
   if not seen_palette[n]and age>=30 then
    seen_palette[n]=true
    local colors={};local pal=manager.machine.palettes[':palette'];local base=own.bank&0x7f00
    for pen=0,63 do colors[#colors+1]=string.pack('<I4',pal:pen_color(base+pen)&0xffffff)end
    local file='mirror_palette_p'..n..'.bin';save(file,table.concat(colors))
    log('PALETTE',string.format('slot=%d actor=%08X id=%d flags=%04X bank=%04X file=%s',n,own.actor,own.id,own.flags,base,file))
   end
   if age%30==0 then log('STATE',string.format('age=%d slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d flags=%04X pose=%08X bank=%04X x=%d y=%d floor=%d hp=%d',
    age,n,own.actor,own.main,own.owner,own.id,own.roster,own.flags,own.pose,own.bank,own.x,own.y,own.floor,own.hp))end
  end
 end
end)
emu.register_frame_done(function()
 for _,file in ipairs(pending)do screen:snapshot(file);log('SNAPSHOT','file='..file)end
 pending={}
end)
emu.register_stop(function()
 log('RESULT',string.format('first_live=%d live_fields=%d confirmed=%s,%s fifo=%s,%s palettes=%s,%s scope=natural_mirror_selection_not_full_port',
  first_live or-1,live_fields,tostring(confirmed[1]),tostring(confirmed[2]),tostring(seen_fifo[1]),tostring(seen_fifo[2]),tostring(seen_palette[1]),tostring(seen_palette[2])))
end)
