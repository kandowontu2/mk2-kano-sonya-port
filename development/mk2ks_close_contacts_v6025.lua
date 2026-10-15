-- Whole existing native RAM observer, real approach/guard/strike/throw controls.
-- Passive taps never replace guest reads/writes or assign processor state.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_special_shadow_v5131.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local marker='-- END v1763 read-only consecutive move-phase observer'
local first,last=source:find(marker,1,true);assert(first and not source:find(marker,last+1,true))
source=source:sub(1,last):gsub('MK2_HSPECIAL_','MK2_BASIC_')
local before="local text={'slot='..n,'mode='..p:read_u16(0x010601d0)}"
local after="local text={'slot='..n,'mode='..p:read_u16(0x010601d0),'stage='..p:read_u16(0x01061ac0),'stageY='..p:read_i16(0x0105ecd0)}"
local count;source,count=source:gsub(before:gsub('([^%w])','%%%1'),function()return after end);assert(count==2)
source=source..'\n'..[=[
local contacts={
 {'own_high_punch_block','High Punch',false,false,false},
 {'own_high_kick_block','High Kick',false,false,false},
 {'own_low_kick_crouch_block','Low Kick',false,true,false},
 {'stock_high_punch_own_block','High Punch',true,false,false},
 {'own_high_punch_hit','High Punch',false,false,true},
 {'own_ground_throw','Low Punch',false,false,true},
 {'stock_ground_throw','Low Punch',true,false,true}}
local contact_index,contact_mode,contact_at,contact_settle=1,'approach',nil,nil
local contact_completed,contact_final=0,false
local function current_contact()return contacts[contact_index]end
local function contact_log(tag,text)
 local c=current_contact();log(tag,'cycle='..contact_index..' phase='..(c and c[1]or'complete')..' driver='..contact_mode..' '..(text or''))
end
for _,address in ipairs({0xff8b6bb0,0xff842d90,0xff906110,0xff836150,0xff835e50,0xff835e70,0xff80f6b0})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual ordinary contact and native throw lookup',function(at,data,mask)
  if not ready or at~=address or regs.PC.value~=address+16 then return end
  local c=current_contact();if not c then return end
  local slot=nil
  for n=1,2 do local a=sample(n);if a and regs.A8.value==a.actor and regs.A13.value==a.main then slot=n end end
  if not slot then return end
  local a=sample(slot)
  contact_log('CONTACT',string.format('slot=%d address=%08X pc=%08X opcode=%04X mask=%04X a8=%08X a13=%08X a9=%08X b2=%08X a0=%08X a7=%08X status=%08X id=%d action=%d',
   slot,address,regs.PC.value,data&0xffff,mask,regs.A8.value,regs.A13.value,regs.A9.value,regs.B2.value,regs.A0.value,regs.A7.value,regs.ST.value,a.id,a.action))
  if address==0xff8b6bb0 then marks[frame]=c[1]..'_entry' end
 end)
end
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(fields[n])do field:clear_value()end end
 if frame>=300 and frame<304 then input(1,'High Punch')end
 if frame>=600 and frame<604 then input(1,'Coin')end
 if frame>=608 and frame<612 then input(2,'Coin')end
 if frame>=620 and frame<624 then input(1,'Start')end
 if join_at then local age=frame-join_at;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(2,'Start',age,20)end
 local mode=p:read_u16(0x010601d0)
 for n=1,2 do
  if mode~=4 then css_marks[n]=nil end
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css_marks[n]then
   css_marks[n]=frame;css=css or frame;plans[n]=route(p:read_u16(slots[n].roster),expected[n])
   if n==1 and not join_at then join_at=frame;log('JOIN_BEGIN','slot=2')end
   log('SELECT','slot='..n..' target='..expected[n]..' path='..table.concat(plans[n],','))
  end
  if css_marks[n]and mode==4 then
   local age=frame-css_marks[n]
   for i,button in ipairs(plans[n])do pulse(n,button,age,56+(i-1)*12)end
   pulse(n,'High Punch',age,148,8)
  end
 end
 local a,b=sample(1),sample(2)
 if not live and frame>1200 and pair_live(a,b)then live=frame;log('LIVE')end
 if live and not ready and frame>=live+60 and pair_live(a,b)and clean(a)and clean(b)then
  ready=frame;command=frame;attempt=1;log('READY')
 end
 if ready then
  if not pair_live(a,b)or a.hp==0 or b.hp==0 then log('FAILED','reason=lost_live_native_owned_pair');manager.machine:exit();return end
  local c=current_contact()
  if c then
   local attacker=c[3]and 3-side or side;local defender=3-attacker
   local own,victim=attacker==1 and a or b,defender==1 and a or b
   local direction=own.x<victim.x and'Right'or'Left';local gap=math.abs(own.x-victim.x)
   if contact_mode=='approach'then
    if gap>43 and clean(own)and clean(victim)then input(attacker,direction);contact_settle=nil
    elseif gap>43 and(own.vx~=0 or victim.vx~=0)then input(attacker,direction);contact_settle=nil
    elseif clean(own)and clean(victim)then
     contact_settle=contact_settle or frame
     if frame-contact_settle>=20 then
      contact_mode='execute';contact_at=frame;marks[frame]=c[1]..'_before'
      contact_log('STEP',string.format('attacker=%d defender=%d gap=%d ownHP=%d victimHP=%d',attacker,defender,gap,own.hp,victim.hp))
     end
    else contact_settle=nil end
   end
   if contact_mode=='execute'then
    local age=frame-contact_at
    if not c[5]and age<72 then input(defender,'Block');if c[4]then input(defender,'Down')end end
    if c[1]:find('throw',1,true)then pulse(attacker,direction,age,20,4);pulse(attacker,c[2],age,21,3)
    else pulse(attacker,c[2],age,20,3)end
    if age==32 or age==48 or age==80 then marks[frame]=c[1]..'_phase'..age end
    if age>=160 and clean(a)and clean(b)then
     contact_log('RECOVERED',string.format('aHP=%d bHP=%d elapsed=%d',a.hp,b.hp,age));marks[frame]=c[1]..'_recovered'
     contact_completed=contact_completed+1;contact_index=contact_index+1;contact_mode='approach';contact_at=nil;contact_settle=nil
    elseif age>=400 then log('FAILED','reason=contact_recovery_deadline');manager.machine:exit()end
   end
  else
   contact_final=clean(a)and clean(b)
   log('FINAL','age='..(frame-ready)..' clean='..(contact_final and 1 or 0)..' aHP='..a.hp..' bHP='..b.hp)
   marks[frame]='contacts_final';rawset(_G,'MK2_SPECIAL_EXIT_PENDING',true)
  end
  part(1,a);part(2,b)
 end
 if frame>=4500 then log('FAILED','reason=absolute_physical_deadline');manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('css=%d live=%d ready=%d terminalAge=%d phases=%d completed=%d fullPortAcceptance=false scope=current_ordinary_contacts_and_throw_roles_deadpool_kitana',
  css or-1,live or-1,ready or-1,ready and frame-ready or-1,contact_completed,contact_final and 1 or 0))
 for _,tap in ipairs(taps)do tap:remove()end
end)
]=]
assert(load(source,'@'..path..'::actual_close_contacts_v6025','t',_ENV))()
