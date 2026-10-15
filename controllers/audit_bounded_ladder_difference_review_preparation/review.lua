-- Input-only current UI/ladder/fight presentation in either campaign slot.
local fighter=assert(os.getenv('MK2KS_UI_FIGHTER'))
local side=assert(tonumber(os.getenv('MK2KS_UI_SIDE')))
assert((fighter=='kano'or fighter=='sonya')and(side==1 or side==2))
local boot=tonumber(os.getenv('MK2KS_UI_BOOT')or'604')
local stock_control=os.getenv('MK2KS_UI_STOCK_CONTROL')=='1'
local identity=stock_control and (fighter=='kano'and 1 or 9) or (fighter=='kano'and 17 or 18)
local frame,css_at,exit_at,live_at=0,nil,nil,nil
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local high,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local fields={}
for _,name in ipairs({'High Punch','Left','Right','Up','Down','Block'})do fields[name]=high['P'..side..' '..name]end
fields.Coin=system['Coin '..side];fields.Start=system[side==1 and'1 Player Start'or'2 Players Start']
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
 print(string.format('MK2_UI_%s frame=%d side=%d fighter=%s writes=0 assistance=none %s',tag,frame,side,fighter,text))
end
local function sample(slot)
 local s=slots[slot];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 local t=string.format('slot=%d actor=%08X main=%08X roster=%d state=%d hp=%d',slot,a,m,p:read_u16(s.roster),p:read_u16(s.state),p:read_u16(s.hp))
 if valid(a)and valid(m)then
  t=t..string.format(' id=%d owner=%08X pose=%08X list=%08X action=%d flags=%04X body=%04X xraw=%08X yraw=%08X vx=%08X vy=%08X gravity=%08X floor=%d',p:read_u16(a+0x1f0),p:read_u32(m+0xc0),p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_u16(m+0x1f0),p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u32(a+0x80),p:read_u32(a+0xa0),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20),p:read_i16(m+0x200))
 end
 return t
end
local function pulse(name,age,first,hold)
 if age>=first and age<first+(hold or 4)then fields[name]:set_value(1);log('INPUT','button='..name..' age='..age)end
end
local native_direction=fighter=='kano'and'Left'or'Right'
local stock_direction=fighter=='kano'and'Right'or'Left'
local first_count=(side==1 and fighter=='sonya'or side==2 and fighter=='kano')and 4 or 1
local route={}
for i=1,first_count do route[#route+1]={native_direction,12+(i-1)*12}end
for _,step in ipairs({{stock_direction,72},{native_direction,96},{stock_direction,120},{native_direction,144},
 {'Down',168},{'Up',192},{native_direction,216}})do route[#route+1]=step end
local photo_draws,pose_draws,css_pose_actor=0,0,0
local taps={}
taps[#taps+1]=p:install_read_tap(0xff804410,0xff80441f,'native CSS lifetime FIFO census',function(at)
 if at~=0xff804410 or cpu.PC.value~=0xff804420 or not css_at or live_at then return end
 local src=cpu.A11.value
 if src==0x0f008000 or src==0x0f010000 then photo_draws=photo_draws+1 end
 local actor=cpu.A0.value
 if valid(actor) and (p:read_u16(actor+0x1f0)==17 or p:read_u16(actor+0x1f0)==18) and src>=0x10000000 and src<0x11000000 then
  if not exit_at then css_pose_actor=actor end
  if actor==css_pose_actor then pose_draws=pose_draws+1 end
 end
end)
for id=17,18 do
 local address=0xffff3000+id*32
 taps[#taps+1]=p:install_read_tap(address,address+31,'native ladder actual portrait lookup',function(at,data,mask)
  if at~=address or cpu.PC.value~=0xff8a0c00 then return end
  log('LADDER',string.format('id=%d at=%08X descriptor=%08X mask=%08X pc=%08X a0=%08X a8=%08X a13=%08X',id,at,data,mask,cpu.PC.value,cpu.A0.value,cpu.A8.value,cpu.A13.value))
 end)
end
local pixels,width,refs
local function pixel(x,y)return string.unpack('<I4',pixels,(y*width+x)*4+1)&0xffffff end
local captured=0
local function snapshot(scene,age)
 if captured>=0 then return end
 if scene=='select' and not(age==66 or age==90 or age==108 or age==156 or age==228) then return end
 if scene=='transition' and not(age==2 or age==60) then return end
 if scene=='fight' and age>2 then return end
 captured=captured+1
 local name=string.format('ui_%04d.png',frame);screen:snapshot(name)
 log('SNAP',string.format('scene=%s age=%d file=%s roster=%d',scene,age or-1,name,p:read_u16(slots[side].roster)))
end
emu.register_frame(function()
 if css_at and not live_at then
  log('TEARDOWN',string.format('cssphotos=%d addedposes=%d exitframe=%d cssactor=%08X',photo_draws,pose_draws,exit_at or -1,css_pose_actor))
 end
 photo_draws,pose_draws=0,0
 frame=frame+1;for _,field in pairs(fields)do field:clear_value()end
 if frame==1 then
  for _,range in ipairs({{0xfffe1800,0xfffe2400},{0xffff0800,0xffff3880}})do
   local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
   log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
  end
 end
 if frame>=300 and frame<304 then fields['High Punch']:set_value(1)end
 pixels,width=screen:pixels();assert(width==400 and#pixels>=400*254*4)
 local yellow,early=0,0
 for y=0,24,2 do for x=40,360,2 do local c=pixel(x,y);local r,g,b=(c>>16)&255,(c>>8)&255,c&255
  if r>175 and g>140 and b<100 then yellow=yellow+1;if y==4 then early=early+1 end end
 end end
 local css=yellow>=400 and yellow<=430 and early>=10
 if not css_at and frame>=boot then local age=(frame-boot)%300;pulse('Coin',age,0);pulse('Start',age,20)end
 if not css_at and frame>700 and css then css_at=frame;log('CSS','yellow='..yellow..' early='..early)end
 if css_at and not exit_at then
  local age=frame-css_at
  for _,step in ipairs(route)do pulse(step[1],age,step[2])end
  if stock_control then pulse(stock_direction,age,240,4)end
  pulse('High Punch',age,264,8)
  log('SELECT',string.format('age=%d roster=%d css=%d',age,p:read_u16(slots[side].roster),css and 1 or 0))
  if css then
   local roster=p:read_u16(slots[side].roster)
   local locations={[17]=19,[1]=79,[0]=139,[2]=199,[9]=259,[18]=319}
   local left=locations[roster]
   if left then
    local lit=0
    for y=20,97 do for x=left,left+62 do
     if x<left+4 or x>left+58 or y<24 or y>93 then
      local c=pixel(x,y)
      if (side==1 and c==0x00ff00)or(side==2 and c==0xff0000)then lit=lit+1 end
     end
    end end
    local h=2166136261
    local px=side==1 and 0 or 320
    for y=105,240 do for x=px,px+79 do h=((h~pixel(x,y))*16777619)&0xffffffff end end
    log('CADENCE',string.format('age=%d roster=%d border=%d posehash=%08X',age,roster,lit,h))
   end
  end
  if age==8 then
   refs={};for _,left in ipairs({23,323})do for y=28,88,4 do for x=left+4,left+48,4 do refs[#refs+1]={x,y,pixel(x,y)}end end end
  end
  if (age>=54 and age<=70 or age>=78 and age<=94 or age>=98 and age<=112 or
    age==132 or age==156 or age==180 or age==204 or age==228 or age>=260)then snapshot('select',age)end
  if age>264 and not css then exit_at=frame;log('EXIT','age='..age..' yellow='..yellow..' early='..early)end
 end
 if exit_at then
  if not live_at then
   local w,h=manager.machine.video:snapshot_size()
   local raw=manager.machine.video:snapshot_pixels()
   assert(w==400 and h==254 and #raw==406400)
   local left,right=0xcbf29ce484222325,0xcbf29ce484222325
   for y=24,240 do
    for x=0,79 do left=(left~(string.unpack('<I4',raw,(y*400+x)*4+1)&0xffffff))*0x100000001b3 end
    for x=320,399 do right=(right~(string.unpack('<I4',raw,(y*400+x)*4+1)&0xffffff))*0x100000001b3 end
   end
   log('SCANOUT',string.format('age=%d left=%016X right=%016X stock=%d',frame-exit_at,left,right,stock_control and 1 or 0))
   local age=frame-exit_at
   if age==87 or age==100 or age==200 or age==360 then screen:snapshot(string.format('difference_%03d.png',age))end
  end
  local matches={0,0}
  for i,r in ipairs(refs or{})do if pixel(r[1],r[2])==r[3]then local k=i<=#refs/2 and 1 or 2;matches[k]=matches[k]+1 end end
  log('OUTSIDE',string.format('age=%d css=%d kano_matches=%d sonya_matches=%d refs=%d mode=%d stage=%d schedule=%08X',frame-exit_at,css and 1 or 0,matches[1],matches[2],refs and#refs/2 or 0,p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u32(0x01061b10)))
  if not live_at then
   local a,m=p:read_u32(slots[side].actor),p:read_u32(slots[side].main)
   if p:read_u16(0x010601d0)==2 and p:read_u16(slots[side].state)==1 and
    p:read_u16(slots[3-side].state)==0 and valid(a)and valid(m)and p:read_u16(a+0x1f0)==identity and
    p:read_u32(m+0xc0)==a then live_at=frame;log('LIVE','stage='..p:read_u16(0x01061b30)..' schedule='..string.format('%08X',p:read_u32(0x01061b10)))end
   local age=frame-exit_at
   if frame%2==0 and(age<=100 or age%12<2)then snapshot('transition',age)end
  end
 end
 if live_at then
  for slot=1,2 do log('FIELD','age='..(frame-live_at)..' '..sample(slot))end
  fields.Block:set_value(1);log('INPUT','button=Block age='..(frame-live_at))
  if frame%2==0 and(frame-live_at<=12 or(frame-live_at)%30<2)then snapshot('fight',frame-live_at)end
  if frame>=live_at+180 then manager.machine:exit()end
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('schema=1 css=%d exit=%d live=%d scope=current_native_UI_and_first_campaign_not_full_game',css_at or-1,exit_at or-1,live_at or-1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
