-- Original MK3 reference, ordinary physical buttons and passive taps only.
-- No HP/position/actor/AI/RNG/register writes, cheats, or saved states.
local machine=manager.machine
local device=machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,pulses,fields,taps=0,{},{},{}
local zeros,alive,finish,start,command=0,false,nil,nil,nil
local lastposes,objects,pending={},{},{}
local installed,inventory=false,false
local function valid(a)return a>=0x01000000 and a<0x01400000 end
local function hex(raw)return raw:gsub('.',function(c)return string.format('%02X',c:byte())end)end
local function log(tag,content)
 print(string.format('MK3_SECONDARY_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),content))
end
local function pulse(field,first)
 assert(field);pulses[#pulses+1]={field,first,first+4}
end
local function geometry(tag)
 local a,b=p:read_u32(0x010609b0),p:read_u32(0x01061560)
 if not valid(a)or not valid(b)then return end
 log(tag,string.format('age=%d own=%08X victim=%08X ids=%d,%d hp=%d,%d x=%d,%d y=%d,%d poses=%08X,%08X bank=%04X,%04X finish=%d pc=%08X a8=%08X a9=%08X a13=%08X',
 start and frame-start or -1,a,b,p:read_u16(a+0x1f0),p:read_u16(b+0x1f0),
 p:read_u16(0x01060a40),p:read_u16(0x010615f0),p:read_i16(a+0x90),p:read_i16(b+0x90),
 p:read_i16(a+0xb0),p:read_i16(b+0xb0),p:read_u32(a+0x1d0),p:read_u32(b+0x1d0),
 p:read_u16(a+0x140),p:read_u16(b+0x140),p:read_u16(0x01062250),
 cpu.PC.value,cpu.A8.value,cpu.A9.value,cpu.A13.value))
end
local function press(name)
 fields[name]:set_value(1)
 log('INPUT','field='..name..' value=1')
end
emu.register_frame(function()
 frame=frame+1
 if not installed then
  installed=true
  local high,low,system=machine.ioport.ports[':IN0'].fields,machine.ioport.ports[':IN1'].fields,machine.ioport.ports[':IN2'].fields
  fields={right=high['P1 Right'],left=high['P1 Left'],hk=high['P1 High Kick'],
          lp=low['P1 Low Punch'],block=high['P1 Block']}
  -- Proven original selection route: start P1 first, then join P2.
  for base=360,1320,480 do
   pulse(system['Coin 1'],base);pulse(system['1 Player Start'],base+20)
   for _,offset in ipairs({180,220,260})do pulse(high['P1 Right'],base+offset)end
   pulse(high['P1 High Punch'],base+320)
  end
  for _,at in ipairs({2960,2980,3000})do pulse(system['Coin 2'],at)end
  pulse(system['2 Players Start'],3020)
  for _,at in ipairs({3060,3090,3120})do pulse(high['P1 Right'],at)end
  pulse(high['P1 High Punch'],3160)
  for _,at in ipairs({3100,3160,3220,3280})do pulse(high['P2 Left'],at)end
  pulse(high['P2 Down'],3340);pulse(high['P2 High Punch'],3400)
  for _,where in ipairs({0xff9b5cd0,0xff9b62c0,0xff9b12e0,0xff998750,0xff9987e0,0xff991f70,0xffa5ef10,0xffa5ef50})do
   local at=where
   taps[#taps+1]=p:install_read_tap(at,at+15,'passive original finisher entry',function(address)
    if address~=at or cpu.PC.value~=at+16 or not finish then return end
    if at==0xff9b5cd0 and not start then start=frame;geometry('OWN_ENTRY')end
    log('CODE',string.format('at=%08X pc=%08X a8=%08X a9=%08X a13=%08X a14=%08X',
      at,cpu.PC.value,cpu.A8.value,cpu.A9.value,cpu.A13.value,cpu.A14.value))
   end)
  end
  for _,address in ipairs({0x01060a40,0x010615f0})do
   local at=address
   taps[#taps+1]=p:install_write_tap(at,at+15,'passive physically earned health',function(offset,data,mask)
    if offset~=at or mask~=0xffff or frame<3800 then return end
    log('HEALTH',string.format('at=%08X before=%d after=%d pc=%08X a8=%08X a13=%08X',
     at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value))
   end)
  end
  taps[#taps+1]=p:install_write_tap(0x01680000,0x0168001f,'passive original sound packets',function(at,data,mask)
   if at==0x01680000 and mask&0xff~=0 and finish then
    log('SOUND',string.format('byte=%02X mask=%04X pc=%08X',data&0xff,mask,cpu.PC.value))
   end
  end)
 end
 for _,item in ipairs(pulses)do
  if frame==item[2]then item[1]:set_value(1);log('SELECT_INPUT','value=1 at='..item[2])end
  if frame==item[3]then item[1]:clear_value();log('SELECT_INPUT','value=0 at='..item[3])end
 end
 if frame<3800 then
  if frame==1800 or frame==3420 then pending[#pending+1]='selection_'..frame end
  return
 end
 for name,field in pairs(fields)do field:clear_value()end
 local a,b=p:read_u32(0x010609b0),p:read_u32(0x01061560)
 if not valid(a)or not valid(b)then return end
 local i,j=p:read_u16(a+0x1f0),p:read_u16(b+0x1f0)
 if frame==3800 then geometry('SELECTED');pending[#pending+1]='selected_3800' end
 if i~=0 or j~=1 then
  if frame==3800 then log('WRONG_SELECTION','actual='..i..','..j);machine:exit()end
  return
 end
 local hp=p:read_u16(0x010615f0)
 if hp>0 and hp<=166 then alive=true end
 if alive and hp==0 then
  alive=false;zeros=zeros+1;geometry('ROUND_ZERO');log('ROUND_COUNT','zeros='..zeros)
  if zeros==2 then finish=frame;pending[#pending+1]='earned_finish_window' end
 end
 local x,y=p:read_i16(a+0x90),p:read_i16(b+0x90)
 local gap=math.abs(x-y);local forward=x<y and 'right' or 'left'
 if start then
  geometry('FIELD')
  local age=frame-start
  for side,actor in ipairs({a,b})do
   local pose=p:read_u32(actor+0x1d0);local bank=p:read_u16(actor+0x140)&0x7f00
   if pose~=lastposes[side]then
    lastposes[side]=pose
    local colors={}
    for color=0,63 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01880000+(bank+color)*16))end
    log('POSE',string.format('age=%d side=%d actor=%08X pose=%08X bank=%04X colors=%s',age,side,actor,pose,bank,table.concat(colors,',')))
   end
  end
  if age%3==0 and age<=330 then
   for object=0x01020000,0x01060000,16 do
    if object~=a and object~=b then
     local pose=p:read_u32(object+0x1d0)
     if pose>=0xff800000 and pose<0xffe00000 and pose%16==0 and pose~=objects[object]then
      local ox,oy=p:read_i16(object+0x90),p:read_i16(object+0xb0)
      if ox>=100 and ox<2000 and oy>=-300 and oy<1000 and p:read_u16(object+0x1f0)<0x1000 then
       objects[object]=pose
       log('OBJECT',string.format('age=%d actor=%08X pose=%08X x=%d y=%d bank=%04X descriptor=%08X',
         age,object,pose,ox,oy,p:read_u16(object+0x140),p:read_u32(object+0x1a0)))
      end
     end
    end
   end
  end
  for _,at in ipairs({1,24,60,120,180,300,450})do if age==at then pending[#pending+1]='action_age_'..age end end
  if age>=451 then log('RESULT','own_action_observed=1 zeros='..zeros);machine:exit()end
 elseif finish then
  local age=frame-finish
  if age>=55 and not command then
   if gap>20 then press(forward)else command=frame;geometry('COMMAND_SPACING')end
  end
  if command then
   local ca=frame-command
   for _,item in ipairs({{'lp',10},{'block',20},{'block',30},{'hk',40}})do
    if ca>=item[2]and ca<item[2]+4 then press(item[1])end
   end
  end
  if age%20==0 then geometry('FINISH_WINDOW')end
  if age>=450 then pending[#pending+1]='command_no_action';log('RESULT','own_action_observed=0 zeros='..zeros);machine:exit()end
 elseif hp>0 and hp<=166 then
  if gap>45 then press(forward)elseif frame%30<4 then press('hk')end
  if frame%300==0 then geometry('COMBAT')end
 end
end)
emu.register_frame_done(function()
 if not inventory then
  inventory=true
  local bytes={}
  for at=0xff800000,0xfffffff0,16 do bytes[#bytes+1]=string.pack('<I2',p:read_u16(at))end
  local raw=table.concat(bytes)
  print(string.format('MK3_SECONDARY_GUEST bytes=%d hex=%s',#raw,hex(raw)))
 end
 for _,label in ipairs(pending)do
  local raw,w,h=machine.screens[':screen']:pixels()
  print(string.format('MK3_SECONDARY_RGB frame=%d stage=%s width=%d height=%d bytes=%d hex=%s',frame,label,w,h,#raw,hex(raw)))
 end
 pending={}
end)
emu.register_stop(function()
 log('STOP',string.format('zeros=%d own_action_observed=%d start=%d finish=%d command=%d',zeros,start and 1 or 0,start or -1,finish or -1,command or -1))
end)
