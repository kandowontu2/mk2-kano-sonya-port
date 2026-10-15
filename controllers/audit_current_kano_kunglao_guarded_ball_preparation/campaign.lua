local kb_last,kb_start,kb_release=nil,nil,-1000
local kl_last,kl_start,kl_retry,kl_guard=nil,nil,-1000,-1000
local kh_last,kh_start,kh_retry=nil,nil,-1000
local kc_start=nil
local ks_last,ks_start,ks_direction=nil,nil,nil
local function discard_snapshot(...)end
-- Cold campaign, genuine losses/paid continues. Inputs only, no guest writes.
if rawget(_G,'MK2_NATURAL_CAMPAIGN_ACTIVE')then
 print('MK2_NAT_CAMPAIGN_REENTRY duplicate_callbacks_prevented=true writes=0 assistance=none')
 return
end
rawset(_G,'MK2_NATURAL_CAMPAIGN_ACTIVE',true)
for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_CPU_HEALTH',
 'MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_P1_REGEN','MK2_P2_TOWER_HEALTH_ASSIST'})do
 assert(not os.getenv(key),'No campaign assistance: '..key)
end
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local identity=assert(({kano=17,sonya=18})[fighter])
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
assert(side==1 or side==2)
local opponent=3-side
local boot=tonumber(os.getenv('MK2KS_TEST_BOOT_FRAME')or'600')
local strategy=os.getenv('MK2KS_CAMPAIGN_STRATEGY')or'uppercut'
assert(strategy=='uppercut' or strategy=='jumpkick' or strategy=='reactive' or strategy=='zoning'or strategy=='leg'or strategy=='defensive_leg'or strategy=='lowkick'or strategy=='throw')
local leg_tactic=strategy=='leg'or strategy=='defensive_leg'
local boss_policy=os.getenv('MK2KS_BOSS_PHYSICAL_POLICY')or'shao_knife_retreat'
assert(boss_policy=='shao_knife_retreat','Physical boss input policy only')
local boss_last_jump,boss_jump_direction,boss_escape_origin=-1000,nil,nil -- v2112 physical attempt timing
local boss_guard_until=-1000
local boss_previous_airborne=false
local boss_action_taps={}
local boss_walk_direction,boss_walk_last_x,boss_walk_still=nil,nil,0
local boss_walk_counter=-1000
local boss_live_begin,boss_last_field=nil,nil
assert(not leg_tactic or fighter=='sonya','Leg tactic is Sonya only')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local high,system,low=manager.machine.ioport.ports[':IN0'].fields,
 manager.machine.ioport.ports[':IN1'].fields,manager.machine.ioport.ports[':IN2'].fields
local buttons={}
for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do buttons[key]=high['P'..side..' '..key]end
buttons['Low Punch']=low['P'..side..' Low Punch'];buttons['Low Kick']=low['P'..side..' Low Kick']
buttons.Coin=system['Coin '..side];buttons.Start=system[side==1 and '1 Player Start' or '2 Players Start']
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,selections,losses,wins,live_fields=0,0,0,0,0
local css,css_exit,loss_at,plan=nil,nil,nil,nil
local last_state,first_live,last_fight,ending=nil,nil,nil,nil
local seen,taps={},{}
local jump_start,last_jump,last_uppercut=nil,-1000,-1000
local previous_y=nil
local projectile_start,projectile_direction=nil,nil
local close_start,last_close=nil,-1000
local guard_until=-1000
local stage_wins,picture_reads,text_reads={},{0,0},{0,0}
local ending_completed=nil
local pending_pages,id_taps={},{}
local input_digest,input_events=2166136261,0
local function log(tag,value)
 if tag=='INPUT' then
  local bytes=tostring(frame)..':'..(value or'')
  for index=1,#bytes do input_digest=((input_digest~bytes:byte(index))*16777619)&0xffffffff end
  input_events=input_events+1
  return
 end
 print(string.format('MK2_NAT_CAMPAIGN_%s frame=%d human_slot=%d fighter=%s writes=0 assistance=none %s',tag,frame,side,fighter,value or''))
end
-- Native ending/table/store observers only. The ending is entered only after
-- actual owned boss victories and the original native actor retirement.
for page=0,1 do
 local entry=0xff800000+0xf4900*8+(50+(identity-17)*2+page)*32
 taps[#taps+1]=p:install_read_tap(entry,entry+31,'own native ending picture',function(at,data,mask)
  if at~=entry or not first_live or p:read_u16(0x01061b30)~=16 or
   p:read_u16(slots[side].roster)~=identity or p:read_u16(0x01061b00)~=side then return end
  picture_reads[page+1]=picture_reads[page+1]+1
  log('PICTURE',string.format('page=%d entry=%08X value=%04X mask=%04X pc=%08X roster=%d',page+1,at,data&0xffff,mask,cpu.PC.value,p:read_u16(slots[side].roster)))
  pending_pages[frame+60]='ending_page'..(page+1)..'_'..frame
  pending_pages[frame+180]='ending_page'..(page+1)..'_late_'..frame
 end)
 local table_base=0xff800000+(page==0 and 0xf4a00 or 0xf4b00)*8
 local first=table_base+identity*3*32
 taps[#taps+1]=p:install_read_tap(first,first+3*32-1,'own native ending text',function(at,data,mask)
  if(at-first)%32~=0 or not first_live or p:read_u16(0x01061b30)~=16 or
   p:read_u16(slots[side].roster)~=identity or p:read_u16(0x01061b00)~=side then return end
  text_reads[page+1]=text_reads[page+1]+1
  log('TEXT',string.format('page=%d segment=%d entry=%08X value=%04X mask=%04X pc=%08X roster=%d',page+1,(at-first)//32,at,data&0xffff,mask,cpu.PC.value,p:read_u16(slots[side].roster)))
 end)
end
emu.register_frame_done(function()
 if pending_pages[frame]then
  discard_snapshot(pending_pages[frame]..'.png')
  log('PAGE_SNAP','file='..pending_pages[frame]..'.png');pending_pages[frame]=nil
 end
end)
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a) or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(s.roster),
  state=p:read_u16(s.state),hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),
  floor=p:read_i16(m+0x200),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),
  body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140),action=p:read_u16(m+0x1f0)}
end
local adjacency={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}
local function route(start)
 local queue={{start,{}}};local visited={[start]=true};local cursor=1
 while queue[cursor]do
  local current=queue[cursor];cursor=cursor+1
  if current[1]==identity then return current[2]end
  for _,button in ipairs({'Left','Right','Down'})do
   local next_id=p:read_u16(adjacency[button]+current[1]*16)
   if next_id<=18 and not visited[next_id]then
    local steps={};for _,step in ipairs(current[2])do steps[#steps+1]=step end
    steps[#steps+1]=button;queue[#queue+1]={next_id,steps};visited[next_id]=true
   end
  end
 end
 error('No native selection route to actual character')
end
local function press(button)
 buttons[button]:set_value(1)
 log('INPUT','button='..button:gsub(' ','_')..' selection='..selections)
end
-- Observe actual own special entries independently of intended button plans.
-- Same cold campaign, no actor/health/difficulty/ladder assistance.
local own_moves=fighter=='kano'and{{'knife',0xffffb000},{'ball',0xffffde00},{'blade',0xfff8cc00},{'choke',0xfff91400}}
 or{{'ring',0xffffb400},{'square',0xffffca00},{'bicycle',0xfff9a400},{'leg',0xfff80800}}
for _,move in ipairs(own_moves)do
local move_name,move_entry=move[1],move[2]
taps[#taps+1]=p:install_read_tap(move_entry+16,move_entry+31,'owned natural special '..move_name,function(at)
 if at~=move_entry+16 or not first_live then return end
 local a,m=p:read_u32(slots[side].actor),p:read_u32(slots[side].main)
 if not valid(a)or not valid(m)or cpu.A8.value~=a or cpu.A13.value~=m or
  p:read_u16(a+0x1f0)~=identity or p:read_u16(slots[side].roster)~=identity then return end
 log('SPECIAL',string.format('move=%s entry=%08X at=%08X pc=%08X actor=%08X main=%08X a8=%08X a13=%08X id=%d roster=%d stage=%d',
  move_name,move_entry,at,cpu.PC.value,a,m,cpu.A8.value,cpu.A13.value,
  p:read_u16(a+0x1f0),p:read_u16(slots[side].roster),p:read_u16(0x01061b30)))
end)
end
for n,slot in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'natural campaign native health '..n,function(at,data,mask)
  if mask==0xffff and first_live then

   if p:read_u16(0x01061b30)==4 and cpu.PC.value==0xff836700 then
    local before,after=p:read_u16(at),data&0xffff
    local own,other=sample(1),sample(2)
    if before<=161 and after<before and own and other then
     log('KUNGLAO_DAMAGE_DETAIL',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d heights=%d,%d gap=%d',n,before,after,cpu.A8.value,cpu.A13.value,own.actor,own.main,other.actor,other.main,own.id,other.id,own.action,other.action,own.floor-own.y,other.floor-other.y,math.abs(own.x-other.x)))
    end
   end
   log('HEALTH',string.format('slot=%d at=%08X before=%d after=%d pc=%08X a8=%08X a13=%08X',n,at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value))
  end
 end)
end
taps[#taps+1]=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,'natural campaign native winner',function(at)
 if not first_live or (at-0xfffef800)%32~=0 then return end
 local winner=p:read_u16(0x01061b00)
 if winner~=1 and winner~=2 then return end
 wins=wins+1
 if winner==side then stage_wins[p:read_u16(0x01061b30)]=(stage_wins[p:read_u16(0x01061b30)]or 0)+1 end
 log('WIN',string.format('slot=%d stage=%d id=%d entry=%08X pc=%08X health=%d,%d',winner,p:read_u16(0x01061b30),(at-0xfffef800)//32,at,cpu.PC.value,p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)))
end)
emu.register_frame(function()
 if frame>=24000 then log('HOST_BOUND','maximum_fields=24000 full_campaign_acceptance=false');manager.machine:exit();return end
 frame=frame+1
 for _,field in pairs(buttons)do field:clear_value()end
 if frame==1 then
  log('BOOT','schema=30 strategy='..strategy..' boot='..boot)
  log('NO_RAW_DUMP','guest_memory_read_and_file_sink_omitted=true')
  assert(p:read_u16(0xff86e650)==0xb128 and p:read_u16(0xff86e660)==0x1f0)
  assert(p:read_u16(0xffa166e0)==0xb008 and p:read_u16(0xffa166f0)==0x1f0)
  log('MORPH_ROM','morph=FF86E650:B128,01F0 restore=FFA166E0:B008,01F0')
  local rom_table=p:read_u32(0xff8a11f0)
  for order=0,5 do
   local list=p:read_u32(rom_table+order*32);local ids={}
   for stage=0,16 do ids[#ids+1]=p:read_u16(list+stage*16)end
   log('ROM',string.format('table=%08X order=%d list=%08X ids=%s',rom_table,order,list,table.concat(ids,',')))
  end
 end
 if frame>=300 and frame<304 then press('High Punch')end
 local mode=p:read_u16(0x010601d0);local state=p:read_u16(slots[side].state)
 local stage=p:read_u16(0x01061b30);local schedule=p:read_u32(0x01061b10)
 local winner=p:read_u16(0x01061b00)
 local key=string.format('%d:%d:%d:%d:%08X:%d:%d:%08X:%08X',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),stage,schedule,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor))
 if key~=last_state or frame%120==0 then
  log('STATE',string.format('mode=%d states=%d,%d stage=%d schedule=%08X roster=%d,%d actors=%08X,%08X health=%d,%d winner=%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),stage,schedule,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),winner))
  last_state=key
 end
 if first_live and not loss_at and mode==3 and state==2 and winner==opponent and p:read_u32(slots[side].actor)==0 then
  losses=losses+1;loss_at=frame;css=nil;css_exit=nil
  log('LOSS','number='..losses..' stage='..stage)
  discard_snapshot(string.format('campaign_loss_%d.png',losses))
 end
 if loss_at and not css then
  local age=frame-loss_at
  if age>=20 and age<25 or age>=270 and age<275 then press('Coin')end
  if age>=310 and age<315 then press('Start')end
 end
 if selections==0 and not css and frame>=boot then
  local age=(frame-boot)%300
  if age<4 then press('Coin')end
  if age>=20 and age<24 then press('Start')end
 end
 if not css and frame>700 and mode==4 and state==3 and p:read_u16(slots[side].roster)<=18 then
  css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster))
  log('SELECT',string.format('number=%d initial=%d target=%d path=%s continue=%d stage=%d schedule=%08X',selections,p:read_u16(slots[side].roster),identity,table.concat(plan,','),loss_at or -1,stage,schedule))
 end
 if css and not css_exit then
  local age=frame-css
  for index,direction in ipairs(plan)do
   local at=56+(index-1)*12
   if age>=at and age<at+4 then press(direction)end
  end
  if age==130 or age==146 then
   log('SELECT_ID',string.format('number=%d roster=%d state=%d',selections,p:read_u16(slots[side].roster),state))
   discard_snapshot(string.format('campaign_selection_%d_%d.png',selections,age))
  end
  if age>=148 and age<156 then press('High Punch')end
  if age>148 and mode~=4 then css_exit=frame;log('SELECT_EXIT','number='..selections)end
 end
 local human,other=sample(side),sample(opponent)
 if stage==14 and other and other.roster==6 and not id_taps[other.actor]then
  local actor=other.actor
  id_taps[actor]=p:install_write_tap(actor+0x1f0,actor+0x1ff,'original CPU Shang ID provenance',function(at,data,mask)
   if p:read_u32(slots[opponent].actor)~=actor or p:read_u16(slots[opponent].roster)~=6 or
    p:read_u16(0x01061b30)~=14 then return end
   log('CPU_ID',string.format('actor=%08X before=%d after=%d pc=%08X a0=%08X a9=%08X a8=%08X a13=%08X mask=%04X',actor,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A0.value,cpu.A9.value,cpu.A8.value,cpu.A13.value,mask))
  end)
 end
 if mode==2 and state==1 and p:read_u16(slots[opponent].state)==0 and human and other and human.owner==human.actor and other.owner==other.actor then
  if not first_live then first_live=frame end
  local fight_key=string.format('%d:%d:%08X:%08X',selections,stage,human.actor,other.actor)
  if fight_key~=last_fight then
   last_fight=fight_key;loss_at=nil;jump_start=nil;previous_y=nil;projectile_start=nil;close_start=nil;last_close=-1000;guard_until=-1000
   log('FIGHT',string.format('selection=%d stage=%d schedule=%08X human=%d:%d cpu=%d:%d actors=%08X,%08X',selections,stage,schedule,human.roster,human.id,other.roster,other.id,human.actor,other.actor))
   discard_snapshot(string.format('campaign_fight_selection%d_stage%d.png',selections,stage))
  end
  local seen_key=stage..':'..schedule
  if not seen[seen_key]then seen[seen_key]=true;log('STAGE','stage='..stage..' schedule='..string.format('%08X',schedule))end
  live_fields=live_fields+1
  if live_fields<300 or frame%30==0 then
   log('LIVE',string.format('selection=%d stage=%d schedule=%08X human=%d:%d cpu=%d:%d health=%d,%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X hpos=%d,%d hfloor=%d cpos=%d,%d cfloor=%d poses=%08X,%08X actions=%d,%d flags=%04X,%04X banks=%04X,%04X',selections,stage,schedule,human.roster,human.id,other.roster,other.id,human.hp,other.hp,human.actor,human.main,other.actor,other.main,human.x,human.y,human.floor,other.x,other.y,other.floor,human.pose,other.pose,human.action,other.action,human.flags,other.flags,human.bank,other.bank))
  end
  if winner==0 and human.hp>0 and other.hp>0 then
   local gap=math.abs(human.x-other.x)
   if identity==17 and other.roster==0 then
    local height=human.floor-human.y
    local stance=human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793
    local ready=height<=8 and human.flags&0x1c==0 and stance
    if not kb_last or frame-kb_last~=1 then kb_start=nil;kb_release=-1000 end
    kb_last=frame
    if kb_start then
     local age=frame-kb_start
     if age<84 or not ready then
      press('Low Kick');press('Down');press('Block')
     else
      kb_start=nil;kb_release=frame
      log('KANO_KUNGLAO_BALL_RELEASE',string.format('stage=%d gap=%d age=%d action=%d cpu_action=%d health=%d,%d',stage,gap,age,human.action,other.action,human.hp,other.hp))
     end
    elseif ready and frame-kb_release>=60 then
     kb_start=frame;press('Low Kick');press('Down');press('Block')
     log('KANO_KUNGLAO_BALL_CHARGE',string.format('stage=%d gap=%d action=%d cpu_action=%d',stage,gap,human.action,other.action))
    elseif human.action~=531 and frame-kb_release>=12 then
     press('Down');press('Block')
    end
   elseif identity==17 and other.roster==4 then
    local back=human.x<other.x and 'Left' or 'Right'
    local ready=human.floor-human.y<=8 and human.flags&0x1c==0 and (human.action==0 or human.action==771 or human.action==772)
    if not ks_last or frame-ks_last~=1 then ks_start=nil end
    ks_last=frame
    if gap<105 and human.floor-human.y<=8 then
     ks_start=nil
     local stance=human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793
     local cpu_stance=other.action==0 or other.action==771 or other.action==772 or other.action==770
     if not kh_last or frame-kh_last~=1 then kh_start=nil;kh_retry=-1000 end
     kh_last=frame
     if kh_start and frame-kh_start<32 then
      local age=frame-kh_start
      if age>=6 and age<10 then press('High Kick')end
      if age>=10 then press('Down');press('Block')end
     elseif stance and human.flags&0x1c==0 and cpu_stance and other.floor-other.y<=8 and frame-kh_retry>=32 then
      kh_start=frame;kh_retry=frame
      log('KANO_KITANA_STANDING_COUNTER',string.format('gap=%d action=%d cpu_action=%d health=%d,%d',gap,human.action,other.action,human.hp,other.hp))
     else
      kh_start=nil;press('Down');press('Block')
     end
    elseif ks_start and frame-ks_start<12 then
     local age=frame-ks_start
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(ks_direction)end
     if age>=8 and age<12 then press('High Punch')end
    elseif human.floor-human.y>8 then
     if human.action==512 or human.action==779 then press('High Kick')end
    elseif gap<170 or other.action==300 then
     ks_start=nil;press(back)
    elseif ks_start and frame-ks_start<52 then
     if gap<230 then press(back)end
    elseif ready then
     ks_start=frame;ks_direction=back
     log('KANO_KITANA_SPACING_KNIFE',string.format('gap=%d action=%d cpu_action=%d',gap,human.action,other.action))
    else
     -- Release buttons to recover; don't keep Block asserted across startup.
    end
   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then
    local forward=human.x<other.x and'Right'or'Left'
    local height=human.floor-human.y
    local cpu_height=other.floor-other.y
    -- Native Sub-Zero's visible freeze launch is action 604 (intro 10).
    -- Physical crouch-block holds through projectile travel, then approach.
    if strategy=='defensive_leg'and other.roster==8 and gap>100 and
     (other.action==0x604 or other.action==0x10)then guard_until=frame+40 end
    if close_start and frame-close_start<12 then
     local age=frame-close_start
     if leg_tactic then
      if age<7 then press('Down')end
      if age>=3 and age<7 then press('Low Punch');press('Block')end
     elseif strategy=='lowkick'then
      press('Down');if age<4 then press('Low Kick')end
     else
      if age<4 then press('Low Punch');press(forward)end
     end
    elseif strategy=='defensive_leg'and frame<guard_until and gap>90 then
     press('Down');press('Block')
    elseif height>8 then
     if gap<100 and frame%6<3 then press('High Kick')end
    elseif cpu_height>15 and gap<80 then
     press('Down')
     if frame-last_uppercut>=22 then press('High Punch');last_uppercut=frame
     else press('Block')end
    elseif gap<(strategy=='throw'and 42 or leg_tactic and 85 or 70)then
     if frame-last_close>=24 and human.flags&0x1c==0 and human.body&0x0c==0 then
      close_start=frame;last_close=frame
      log('DECISION',string.format('move=%s gap=%d human_action=%d cpu_action=%d',strategy,gap,human.action,other.action))
      if leg_tactic then press('Down')
      elseif strategy=='lowkick'then press('Down');press('Low Kick')
      else press('Low Punch');press(forward)end
     end
    else
     close_start=nil;press(forward)
    end
   elseif strategy=='uppercut' then
    if gap>65 then press(human.x<other.x and'Right'or'Left')
    else press('Down');if frame%22<4 then press('High Punch')end end
   elseif strategy=='jumpkick' then
    if gap>80 then press(human.x<other.x and'Right'or'Left')end
    if frame%56<4 then press('Up')end
    if frame%56>=12 and frame%56<20 then press('High Kick')end
   -- BEGIN actual-input boss clean-uppercut response v2332; physical buttons and read-only observation only.
   elseif (strategy=='zoning' or leg_tactic) and (other.roster==12 or other.roster==13) then
    if not boss_action_taps[human.main] then
     local observed_main=human.main
     boss_action_taps[observed_main]=p:install_write_tap(observed_main+0x1f0,observed_main+0x1ff,'read-only actual human boss action stores',function(at,data,mask)
      local current_stage=p:read_u16(0x01061b30)
      local observed_actor=p:read_u32(slots[side].actor)
      if at~=observed_main+0x1f0 or (current_stage~=15 and current_stage~=16) or
       p:read_u32(slots[side].main)~=observed_main or observed_actor<0x01000000 or observed_actor>=0x01100000 or
       p:read_u16(slots[side].state)~=1 or p:read_u16(slots[side].roster)~=identity or
       p:read_u16(observed_actor+0x1f0)~=identity or p:read_u32(observed_main+0xc0)~=observed_actor or
       p:read_u16(slots[side].hp)==0 or p:read_u16(slots[opponent].hp)==0 then return end
      log('BOSS_ACTION',string.format('stage=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=1 at=%08X before=%d after=%d mask=%04X pc=%08X a1=%08X a8=%08X a13=%08X health=%d,%d',
       current_stage,observed_actor,observed_main,p:read_u32(observed_main+0xc0),identity,p:read_u16(slots[side].roster),at,p:read_u16(at),data&0xffff,mask,cpu.PC.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,p:read_u16(slots[side].hp),p:read_u16(slots[opponent].hp)))
     end)
     taps[#taps+1]=boss_action_taps[observed_main]
    end
    if not boss_action_taps.native_handlers then
     boss_action_taps.native_handlers=true
     for _,address in ipairs({0xff82f9f0,0xff8300c0,0xff830200,0xff832040,0xff877d80,0xff837e40,0xff8304d0,0xff870dc0,0xff82fd70,0xff831360})do
      taps[#taps+1]=p:install_read_tap(address,address+15,'read-only actual boss native guard/HP handler',function(at)
       local current_stage=p:read_u16(0x01061b30)
       if(address==0xff82fd70 or address==0xff831360)and current_stage~=16 then return end
       if at~=address or cpu.PC.value~=address+16 or (current_stage~=15 and current_stage~=16)or
        p:read_u16(0x010601d0)~=2 or p:read_u16(slots[side].state)~=1 or
        p:read_u16(slots[side].hp)==0 or p:read_u16(slots[opponent].hp)==0 then return end
       local own=sample(side)
       if not own or own.id~=identity or own.roster~=identity or own.owner~=own.actor or
        cpu.A8.value~=own.actor or cpu.A13.value~=own.main then return end
       log('BOSS_HANDLER',string.format('policy=%s stage=%d entry=%08X pc=%08X actor=%08X main=%08X owner=%08X a8=%08X a13=%08X id=%d roster=%d state=1 action=%d flags=%04X body=%04X repeat_count=%d hardware0=%04X a0=%08X a1=%08X health=%d,%d',
        boss_policy,current_stage,address,cpu.PC.value,own.actor,own.main,own.owner,cpu.A8.value,cpu.A13.value,own.id,own.roster,own.action,own.flags,own.body,p:read_u16(own.main+0x220),p:read_u16(0x01600000),cpu.A0.value,cpu.A1.value,p:read_u16(slots[side].hp),p:read_u16(slots[opponent].hp)))
      end)
     end
    end
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    local height=human.floor-human.y
    local cpu_height=other.floor-other.y
    -- Physical defense is allowed during crouch/recovery; native code decides
    -- when it can act. Body bits are not a license to drop held inputs.
    if not boss_last_field or frame-boss_last_field>1 then
     boss_live_begin=frame;boss_walk_direction=nil;boss_walk_last_x=nil;boss_walk_still=0
     boss_guard_until=frame+36;boss_walk_counter=-1000;projectile_start=nil
     boss_last_jump=-1000;boss_jump_direction=nil
    end
    boss_last_field=frame
    local grounded=height<=8
    local ready=grounded and human.action==0x303 and human.flags&0x1c==0 and human.body&0x0c==0
    log('BOSS_FIELD',string.format('policy=%s stage=%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X human_id=%d cpu_id=%d gap=%d height=%d cpu_height=%d h_x=%d h_y=%d h_floor=%d c_x=%d c_y=%d c_floor=%d human_action=%d cpu_action=%d flags=%04X body=%04X cpu_flags=%04X cpu_body=%04X human_pose=%08X cpu_pose=%08X human_vy=%08X cpu_vy=%08X health=%d,%d',
     boss_policy,stage,human.actor,human.main,other.actor,other.main,human.id,other.id,gap,height,cpu_height,
     human.x,human.y,human.floor,other.x,other.y,other.floor,human.action,other.action,human.flags,human.body,other.flags,other.body,human.pose,other.pose,
     p:read_u32(human.actor+0x60),p:read_u32(other.actor+0x60),human.hp,other.hp))
    if height>8 and not boss_previous_airborne then
     log('BOSS_RESPONSE',string.format('policy=%s kind=actual_airborne stage=%d attempt=%d actor=%08X main=%08X id=%d height=%d x=%d y=%d',
      boss_policy,stage,boss_last_jump,human.actor,human.main,human.id,height,human.x,human.y))
    end
    boss_previous_airborne=height>8
    local function decision(move,direction)
     log('BOSS_PLAN',string.format('policy=%s move=%s stage=%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X human_id=%d cpu_id=%d gap=%d height=%d cpu_height=%d human_action=%d cpu_action=%d flags=%04X body=%04X health=%d,%d direction=%s scope=physical_attempt_not_assumed_activation',
      boss_policy,move,stage,human.actor,human.main,other.actor,other.main,human.id,other.id,
      gap,height,cpu_height,human.action,other.action,human.flags,human.body,human.hp,other.hp,direction or'none'))
    end
    -- Physical Down preparation, then fresh HP only in the measured
    -- native descending-stomp window. Never assign actor/action or positions.
    local quiet=false -- v2332: no artificial guard-only opening delay
    local can_crouch=height==0 and human.flags&0x0c==0 and human.body&0x0c==0 and
      (human.action==0x303 or human.action==0x302 or human.action==0x304)
    local cpu_vy=p:read_u32(other.actor+0x60)
    local descending=cpu_vy>0 and cpu_vy<0x80000000
    local escape=true
    local preparation_gap=170
    local jump_gap=145
    if stage==16 then
     -- Genuine Kano D,B,HP command, with ordinary retreat at close range.
     -- Native code decides activation, projectile collision and boss damage.
     boss_walk_last_x=nil
     if projectile_start and frame-projectile_start<64 then
      local age=frame-projectile_start
      if age>=2 and age<5 then press('Down')end
      if age>=7 and age<10 then press(projectile_direction)end
      if age>=8 and age<12 then press('High Punch')end
      if age>=15 then press('Down');press('Block')end
     elseif height>8 then
      if frame-boss_last_jump<48 then press(boss_jump_direction)end
      if frame%6<3 then press('High Kick')end
     elseif gap<140 then
      projectile_start=nil
      if frame-boss_last_jump>=40 then
       boss_last_jump=frame;boss_jump_direction=back
       decision('shao_knife_retreat_jump_attempt',back)
       press('Up');press(back)
      elseif frame-boss_last_jump<4 then
       press('Up');press(boss_jump_direction)
      else press('Down');press('Block')end
     else
      projectile_start=frame;projectile_direction=back
      decision('shao_knife_command_attempt',back)
     end
    elseif quiet then
     boss_walk_last_x=nil;press('Block')
    elseif frame-boss_walk_counter<36 then
     local age=frame-boss_walk_counter
     if human.action~=0x107 and not can_crouch then
      log('BOSS_CANCEL',string.format('policy=%s start=%d stage=%d human_actor=%08X human_main=%08X human_id=%d human_action=%d flags=%04X body=%04X height=%d health=%d,%d reason=actual_native_nonstance',
       boss_policy,boss_walk_counter,stage,human.actor,human.main,human.id,human.action,human.flags,human.body,height,human.hp,other.hp))
      boss_walk_counter=-1000;boss_walk_last_x=nil;press('Down');press('Block')
     else
      boss_walk_last_x=boss_walk_last_x or frame
      press('Down');if age<=2 then press('High Punch')end
     end
    elseif escape and frame-boss_last_jump<16 then
     boss_walk_last_x=nil;press('Up');press(boss_jump_direction)
    elseif escape and height>8 then
     boss_walk_last_x=nil
     if frame-boss_last_jump<48 then press(boss_jump_direction)end
     local kick_vy=p:read_u32(human.actor+0x60)
     local kick_vy_min=boss_policy=='late_descend'and 0x20000 or 0
     if kick_vy>=kick_vy_min and kick_vy<0x80000000 and frame%6<3 then press('High Kick')end
    elseif other.action==0x407 then
     boss_walk_last_x=boss_walk_last_x or frame;press('Down')
     if can_crouch and gap<95 and frame-boss_walk_last_x>=12 and frame-last_uppercut>=30 and
      descending and cpu_height>160 and cpu_height<=240 then
      boss_walk_counter=frame;last_uppercut=frame
      decision('descending_stomp_uppercut_attempt');press('High Punch')
     end
    elseif escape and gap<preparation_gap then
     boss_walk_last_x=boss_walk_last_x or frame
     if can_crouch and frame-boss_walk_last_x>=12 and gap<jump_gap and cpu_height<20 and frame-boss_last_jump>=60 then
      boss_last_jump=frame;boss_jump_direction=forward;boss_walk_last_x=nil
      decision('close_pressure_jumpkick_attempt',boss_jump_direction)
      press('Up');press(boss_jump_direction)
     else press('Down')end
    else
     boss_walk_last_x=nil;press('Down');press('Block')
    end
   -- END actual-input boss clean-uppercut response v2332.
   elseif strategy=='zoning' then
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    local height=human.floor-human.y
    if projectile_start and frame-projectile_start<64 then
     local age=frame-projectile_start
     -- Preserve the direct-tested native commands: Kano D,B,HP;
     -- Sonya D,F,LP. F,B,HP belongs to Sonya's square-wave, not ring.
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(projectile_direction)end
     if age>=8 and age<12 then press(fighter=='kano'and'High Punch'or'Low Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif height>8 then
     if frame%6<3 then press('High Kick')end
    elseif gap<80 then
     projectile_start=nil
     if frame-last_jump>=40 then press('Up');press(back);last_jump=frame
     elseif frame-last_jump<4 then press('Up');press(back)
     else press('Down');press('Block')end
    else
     projectile_start=frame;projectile_direction=fighter=='kano'and back or forward
     log('DECISION',string.format('move=projectile gap=%d direction=%s',gap,projectile_direction))
    end
   else
    -- Read-only feedback: jump from actual grounded state, kick during the
    -- actual flight, and anti-air an approaching airborne CPU. No fixed
    -- health, action, position, schedule or difficulty changes are supplied.
    local forward=human.x<other.x and'Right'or'Left'
    local height=human.floor-human.y
    local cpu_height=other.floor-other.y
    local airborne=height>8
    if airborne then
     jump_start=jump_start or frame
     local age=frame-jump_start
     local descending=previous_y and human.y>previous_y
     if gap<115 and height<90 and(age>=9 or descending)then
      if age%6<3 then press('High Kick')end
     end
    else
     jump_start=nil
     if frame-last_jump<4 then
      press('Up');press(forward)
     elseif cpu_height>12 and gap<105 then
      press('Down')
      if gap<78 and frame-last_uppercut>=22 then
       press('High Punch');last_uppercut=frame
      else press('Block')end
     elseif gap<47 then
      press('Down')
      if frame-last_uppercut>=22 then
       press('High Punch');last_uppercut=frame
      else press('Block')end
     elseif frame-last_jump>=38 then
      press('Up');press(forward);last_jump=frame
      log('DECISION',string.format('move=jump gap=%d human_height=%d cpu_height=%d',gap,height,cpu_height))
     else
      press('Down');press('Block')
     end
    end
    previous_y=human.y
   end
  end
 end
 if first_live and stage==16 and mode==11 and winner==side and p:read_u16(slots[side].roster)==identity and
  p:read_u16(slots[opponent].hp)==0 and p:read_u16(slots[side].hp)>0 and
  p:read_u32(slots[1].actor)==0 and p:read_u32(slots[2].actor)==0 and(stage_wins[16]or 0)>0 then
  if not ending then ending=frame;log('ENDING_START',string.format('stage=%d winner=%d health=%d,%d actors=00000000,00000000 roster=%d',stage,winner,p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),identity))end
  if (frame-ending)%120==0 then discard_snapshot('campaign_ending_'..(frame-ending)..'.png');log('ENDING','age='..(frame-ending))end
 end
 if ending and not ending_completed and frame-ending>1200 and mode==11 and
  p:read_u16(slots[side].roster)~=identity and math.min(table.unpack(picture_reads))>0 and
  math.min(table.unpack(text_reads))>0 then
  ending_completed=frame
  log('ENDING_COMPLETED',string.format('age=%d mode=%d roster=%d,%d pictures=%d,%d texts=%d,%d',frame-ending,mode,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),picture_reads[1],picture_reads[2],text_reads[1],text_reads[2]))
  discard_snapshot('ending_return_to_attract.png')
 end
 if ending_completed and frame-ending_completed>=300 then manager.machine:exit()end
end)
emu.register_stop(function()
 local count=0;for _ in pairs(seen)do count=count+1 end
 log('RESULT',string.format('schema=30 selections=%d losses=%d native_win_reads=%d first_live=%d live_fields=%d seen_stages=%d ending=%d ending_completed=%d pictures=%d,%d texts=%d,%d scope=unassisted_campaign_observation_independent_verification_pending',selections,losses,wins,first_live or -1,live_fields,count,ending or -1,ending_completed or -1,picture_reads[1],picture_reads[2],text_reads[1],text_reads[2]))
 for _,tap in ipairs(taps)do tap:remove()end
end)
-- Kano-only read-only observer omitted; core physical policy unchanged.

emu.register_frame(function()
 if frame%300==0 then log('INPUT_DIGEST',string.format('events=%d fnv32=%08X',input_events,input_digest))end
end)
emu.register_stop(function()
 log('INPUT_DIGEST_FINAL',string.format('events=%d fnv32=%08X',input_events,input_digest))
end)

taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'owned close counter uppercut',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=0xff870dd0 or p:read_u16(0x01061b30)~=3 then return end
 local own=sample(side)
 if own and own.id==17 and own.roster==17 and cpu.A8.value==own.actor and cpu.A13.value==own.main then
  log('KANO_CLOSE_NATIVE_UPPER',string.format('actor=%08X main=%08X owner=%08X id=%d',own.actor,own.main,own.owner,own.id))
 end
end)

local kh_seen={}
emu.register_frame(function()
 if p:read_u16(0x01061b30)~=3 then return end
 local own=sample(side)
 if not own or own.id~=17 or own.roster~=17 or own.owner~=own.actor then return end
 if kh_seen.main~=own.main or kh_seen.action~=own.action then
  kh_seen.main=own.main;kh_seen.action=own.action
  log('KANO_STANDING_ACTION',string.format('actor=%08X main=%08X owner=%08X id=%d action=%d',own.actor,own.main,own.owner,own.id,own.action))
 end
end)

local kl_seen={}
emu.register_frame(function()
 if p:read_u16(0x01061b30)~=4 then return end
 local own,other=sample(1),sample(2)
 if not own or not other or own.id~=17 or own.roster~=17 or other.id~=0 or other.roster~=0 then return end
 if kl_seen.main~=own.main or kl_seen.a~=own.action or kl_seen.b~=other.action then
  kl_seen.main=own.main;kl_seen.a=own.action;kl_seen.b=other.action
  log('KUNGLAO_ACTION_CHANGE',string.format('p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d flags=%04X,%04X heights=%d,%d gap=%d counter_age=%d health=%d,%d',own.actor,own.main,other.actor,other.main,own.id,other.id,own.action,other.action,own.flags,other.flags,own.floor-own.y,other.floor-other.y,math.abs(own.x-other.x),kl_start and frame-kl_start or -1,own.hp,other.hp))
 end
end)

taps[#taps+1]=p:install_read_tap(0xffffde00,0xffffde0f,'owned campaign guarded ball entry',function(at)
 if at~=0xffffde00 or p:read_u16(0x01061b30)~=4 then return end
 local own=sample(side)
 if own and own.id==17 and own.roster==17 and own.owner==own.actor and cpu.A8.value==own.actor and cpu.A13.value==own.main then
  log('KANO_KUNGLAO_NATIVE_BALL',string.format('actor=%08X main=%08X owner=%08X id=%d pc=%08X',own.actor,own.main,own.owner,own.id,cpu.PC.value))
 end
end)
