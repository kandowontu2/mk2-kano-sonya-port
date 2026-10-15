-- Real cold selection, two airborne catches and ordinary paired follow-through.
-- Keep all native RAM body/shadow observers; no guest or processor assignments.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_special_shadow_v5131.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local marker='-- END v1763 read-only consecutive move-phase observer'
local first,last=source:find(marker,1,true);assert(first and not source:find(marker,last+1,true))
source=source:sub(1,last):gsub('MK2_HSPECIAL_','MK2_BASIC_')
local function replace(before,after,count)
 local seen;source,seen=source:gsub(before:gsub('([^%w])','%%%1'),function()return after end);assert(seen==count)
end
replace("local text={'slot='..n,'mode='..p:read_u16(0x010601d0)}",
 "local text={'slot='..n,'mode='..p:read_u16(0x010601d0),'stage='..p:read_u16(0x01061ac0),'stageY='..p:read_i16(0x0105ecd0),'suppression='..p:read_u16(0x010619d0)}",2)
replace('bank=p:read_u16(a+0x140)}',
 'bank=p:read_u16(a+0x140),xraw=p:read_u32(a+0x80),yraw=p:read_u32(a+0xa0),callback=p:read_u32(m+0x290)}',1)
replace("'body','trail','bank'})do","'body','trail','bank','xraw','yraw','callback'})do",2)
source=source..'\n'..[=[
assert(spec[1]==17 or victim_id==11,'Sonya is a living air-throw victim, not a new air-throw attacker')
local air_cycle,air_mode,air_at,air_settle=1,'approach',nil,nil
local air_caught,air_complete,air_final=nil,0,false
local air_follow_at=nil
local function air_attacker()
 if victim_id==11 and(spec[1]==18 or air_cycle==2)then return 3-side end
 return side
end
local function air_log(tag,text)
 log(tag,'cycle='..air_cycle..' driver='..air_mode..' attacker='..air_attacker()..' '..(text or''))
end
local addresses={
 gate=0xff8643e0,action=0xff8b6ff0,alignment=0xfffc0680,early_release=0xfffff980,
 own_flight=0xfffff580,victim_callback=0xfffff800,bounce=0xfffc2000,
 damage=0xff83a7a0,own_landing=0xfffc1c00,victim_getup=0xff8ea320,
 recovery=0xff861410,stock_flight=0xff8da830,handoff=0xff842710,
 victim_lookup=0xff842d90,animation_lookup=0xff906110,physics=0xff876660}
for kind,address in pairs(addresses)do
 taps[#taps+1]=p:install_read_tap(address,address+15,'actual real-role airborne throw '..kind,function(at,data,mask)
  if not ready or air_cycle>2 or at~=address or regs.PC.value~=address+16 then return end
  local slot=nil
  for n=1,2 do local a=sample(n);if a and regs.A8.value==a.actor and(kind=='gate'or regs.A13.value==a.main)then slot=n end end
  if not slot then return end
  if kind=='action'and slot==air_attacker()then
   assert(air_mode=='execute'and not air_caught,'Unexpected or duplicate actual airborne catch');air_caught=frame;marks[frame]='air_'..air_cycle..'_catch'
  end
  if kind~='gate'and kind~='physics'and kind~='animation_lookup'and kind~='victim_lookup'and not air_caught then return end
  local a=sample(slot)
  air_log('AIR_EVENT',string.format('kind=%s slot=%d address=%08X pc=%08X opcode=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d a8=%08X a13=%08X a0=%08X a1=%08X a2=%08X a3=%08X a6=%08X a7=%08X a9=%08X a10=%08X status=%08X xraw=%08X yraw=%08X callback=%08X y=%d floor=%d',
   kind,slot,address,regs.PC.value,data&0xffff,mask,a.actor,a.main,a.owner,a.id,regs.A8.value,regs.A13.value,
   regs.A0.value,regs.A1.value,regs.A2.value,regs.A3.value,regs.A6.value,regs.A7.value,regs.A9.value,regs.A10.value,regs.ST.value,
   a.xraw,a.yraw,a.callback,a.y,a.floor))
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
  if not pair_live(a,b)or a.hp==0 or b.hp==0 then log('FAILED','reason=lost_live_owned_air_pair');manager.machine:exit();return end
  local function fully_clean(c)return clean(c)and c.callback==0 and p:read_u16(0x010619d0)==0 end
  if air_cycle<=2 then
   local attacker=air_attacker();local own,victim=attacker==1 and a or b,attacker==1 and b or a
   local gap=math.abs(own.x-victim.x);local direction=own.x<victim.x and'Right'or'Left'
   if air_mode=='approach'then
    if gap>64 and(fully_clean(own)and fully_clean(victim)or own.vx~=0 or victim.vx~=0)then input(attacker,direction);air_settle=nil
    elseif fully_clean(own)and fully_clean(victim)then
     air_settle=air_settle or frame
     if frame-air_settle>=30 then
      air_mode='execute';air_at=frame;marks[frame]='air_'..air_cycle..'_before'
      air_log('STEP','age='..(frame-ready)..' gap='..gap..' attackerID='..own.id..' victimID='..victim.id)
     end
    else air_settle=nil end
   end
   if air_mode=='execute'then
    local age=frame-air_at
    pulse(1,'Up',age,0,3);pulse(2,'Up',age,0,3);pulse(attacker,'Block',age,20,6)
    for _,at in ipairs({20,24,32,40,48,56,64,80,96,120})do if age==at then marks[frame]='air_'..air_cycle..'_phase'..at end end
    if age>=180 and air_caught and fully_clean(a)and fully_clean(b)then
     air_log('RECOVERED','age='..(frame-ready)..' catch='..air_caught..' elapsed='..age..' aHP='..a.hp..' bHP='..b.hp)
     marks[frame]='air_'..air_cycle..'_recovered';air_mode='followup';air_follow_at=frame+16
    elseif age>=400 then log('FAILED','reason=air_catch_activation_or_recovery_deadline');manager.machine:exit()end
   end
   if air_mode=='followup'and frame>=air_follow_at then
    local age=frame-air_follow_at
    for n=1,2 do
     local me,them=n==1 and a or b,n==1 and b or a
     pulse(n,me.x<them.x and'Right'or'Left',age,0,8)
     pulse(n,'Up',age,40,3);pulse(n,'High Punch',age,112,3);pulse(n,'Block',age,136,6)
    end
    if age==0 then air_log('FOLLOWUP','begin='..air_follow_at)end
    if age==8 or age==64 or age==120 or age==144 then marks[frame]='air_'..air_cycle..'_follow'..age end
    if age==160 then
     if not fully_clean(a)or not fully_clean(b)then log('FAILED','reason=ordinary_post_air_throw_cleanup');manager.machine:exit();return end
     air_log('CYCLE_DONE','begin='..air_follow_at..' aHP='..a.hp..' bHP='..b.hp);marks[frame]='air_'..air_cycle..'_follow_final'
     air_complete=air_complete+1;air_cycle=air_cycle+1;air_mode='approach';air_at=nil;air_settle=nil;air_caught=nil;air_follow_at=nil
    end
   end
  else
   air_final=fully_clean(a)and fully_clean(b)
   log('FINAL','age='..(frame-ready)..' clean='..(air_final and 1 or 0)..' aHP='..a.hp..' bHP='..b.hp)
   marks[frame]='air_final';rawset(_G,'MK2_SPECIAL_EXIT_PENDING',true)
  end
  part(1,a);part(2,b)
 end
 if frame>=4500 then log('FAILED','reason=absolute_physical_air_deadline');manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('css=%d live=%d ready=%d terminalAge=%d phases=%d completed=%d fullPortAcceptance=false scope=current_two_air_catches_real_roles_and_both_ordinary_followups',
  css or-1,live or-1,ready or-1,ready and frame-ready or-1,air_complete,air_final and 1 or 0))
 for _,tap in ipairs(taps)do tap:remove()end
end)
]=]
assert(load(source,'@'..path..'::real_air_throw_roles_v6039','t',_ENV))()
