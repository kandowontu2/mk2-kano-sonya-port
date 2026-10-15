-- Current cold real selection and ordinary controls, unchanged native RAM taps.
-- Read the existing whole observer; replace its signature-move input program,
-- not its body/shadow kernels. No guest/CPU/health/position/RNG writes.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_special_shadow_v5131.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local marker='-- END v1763 read-only consecutive move-phase observer'
local first,last=source:find(marker,1,true);assert(first and not source:find(marker,last+1,true))
source=source:sub(1,last)
source=source:gsub('MK2_HSPECIAL_','MK2_BASIC_')
local before="local text={'slot='..n,'mode='..p:read_u16(0x010601d0)}"
local after="local text={'slot='..n,'mode='..p:read_u16(0x010601d0),'stage='..p:read_u16(0x01061ac0),'stageY='..p:read_i16(0x0105ecd0)}"
local index=assert(source:find(before,1,true));assert(not source:find(before,index+1,true))
source=source:sub(1,index-1)..after..source:sub(index+#before)
source=source..[=[
local basic_phases={
 {0,'idle'},{32,'forward_walk'},{76,'backward_walk'},
 {120,'neutral_jump'},{200,'forward_jump'},{280,'backward_jump'},
 {360,'crouch'},{420,'standing_block'},{480,'crouch_block'},
 {540,'high_punch'},{600,'low_punch'},{660,'high_kick'},{720,'low_kick'},
 {780,'crouch_punch'},{840,'crouch_kick'},{900,'uppercut'},
 {960,'sweep'},{1020,'roundhouse'},{1080,'close_approach'},
 {1160,'close_high_punch'},{1220,'close_high_kick'},
 {1280,'opponent_blocked_punch'},{1360,'close_low_punch'},
 {1420,'close_low_kick'},{1480,'final_recovery'}}
local basic_seen,basic_complete={},false
local function basic_button(button,age,at,duration,n)
 pulse(n or side,button,age,at,duration)
end
emu.register_frame(function()
 frame=frame+1
 for n=1,2 do for _,field in pairs(fields[n])do field:clear_value()end end
 if frame>=300 and frame<304 then input(1,'High Punch')end
 if frame>=600 and frame<604 then input(1,'Coin')end
 if frame>=608 and frame<612 then input(2,'Coin')end
 if frame>=620 and frame<624 then input(1,'Start')end
 if join_at then
  local age=frame-join_at;pulse(1,'Coin',age,0);pulse(2,'Coin',age,8);pulse(2,'Start',age,20)
 end
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
  if not pair_live(a,b)then log('FAILED','reason=lost_native_owned_pair');manager.machine:exit();return end
  local own,victim=side==1 and a or b,side==1 and b or a
  local age=frame-ready
  forward=own.x<victim.x and'Right'or'Left';backward=forward=='Right'and'Left'or'Right'
  for i,phase in ipairs(basic_phases)do
   if age==phase[1]then basic_seen[i]=true;log('STEP','age='..age..' phase='..phase[2]);marks[frame]=phase[2]..'_before'end
   if age==phase[1]+12 then marks[frame]=phase[2]..'_phase12'end
   if age==phase[1]+28 then marks[frame]=phase[2]..'_phase28'end
  end
  basic_button(forward,age,32,24);basic_button(backward,age,76,24)
  basic_button('Up',age,120,3)
  basic_button('Up',age,200,3);basic_button(forward,age,200,16)
  basic_button('Up',age,280,3);basic_button(backward,age,280,16)
  basic_button('Down',age,360,24)
  basic_button('Block',age,420,24)
  basic_button('Down',age,480,24);basic_button('Block',age,480,24)
  basic_button('High Punch',age,540,3);basic_button('Low Punch',age,600,3)
  basic_button('High Kick',age,660,3);basic_button('Low Kick',age,720,3)
  basic_button('Down',age,780,24);basic_button('Low Punch',age,784,3)
  basic_button('Down',age,840,24);basic_button('Low Kick',age,844,3)
  basic_button('Down',age,900,16);basic_button('High Punch',age,904,3)
  basic_button(backward,age,960,4);basic_button('Low Kick',age,961,3)
  basic_button(backward,age,1020,4);basic_button('High Kick',age,1021,3)
  if age>=1080 and age<1140 and math.abs(own.x-victim.x)>40 then input(side,forward)end
  basic_button('High Punch',age,1160,3);basic_button('High Kick',age,1220,3)
  basic_button('Block',age,1280,24,3-side);basic_button('High Punch',age,1286,3)
  basic_button('Low Punch',age,1360,3);basic_button('Low Kick',age,1420,3)
  part(1,a);part(2,b)
  if age>=1540 then
   basic_complete=clean(a)and clean(b)and a.hp>0 and b.hp>0
   log('FINAL','age='..age..' clean='..(basic_complete and 1 or 0)..' aHP='..a.hp..' bHP='..b.hp)
   if not basic_complete then log('FAILED','reason=ordinary_final_not_clean')end
   marks[frame]='ordinary_final';rawset(_G,'MK2_SPECIAL_EXIT_PENDING',true)
  end
 end
 if frame>=4300 then log('FAILED','reason=absolute_physical_deadline');manager.machine:exit()end
end)
emu.register_stop(function()
 local count=0;for _ in pairs(basic_seen)do count=count+1 end
 log('RESULT',string.format('css=%d live=%d ready=%d terminalAge=%d phases=%d completed=%d fullPortAcceptance=false scope=ordinary_native_controls_deadpool_kitana_diagnostic',
  css or-1,live or-1,ready or-1,ready and frame-ready or-1,count,basic_complete and 1 or 0))
 for _,tap in ipairs(taps)do tap:remove()end
end)
]=]
assert(load(source,'@'..path..'::ordinary_controls_v5993','t',_ENV))()
