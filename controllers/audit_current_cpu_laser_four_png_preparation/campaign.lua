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
local smoke_plan,smoke_forward,smoke_entry,smoke_recovered=nil,nil,nil,nil
local visual_start,visual_winner,visual_motion=nil,nil,nil
local visual_pending,visual_captured={},{}
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
  body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140),action=p:read_u16(m+0x1f0),vy=p:read_u32(a+0x60),vx=p:read_u32(a+0x40),gravity=p:read_u32(a+0x20),trail=p:read_u32(m+0x190)}
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
 if move_name=='ring'and smoke_plan then smoke_entry=smoke_entry or frame end
 log('SPECIAL',string.format('move=%s entry=%08X at=%08X pc=%08X actor=%08X main=%08X a8=%08X a13=%08X id=%d roster=%d stage=%d',
  move_name,move_entry,at,cpu.PC.value,a,m,cpu.A8.value,cpu.A13.value,
  p:read_u16(a+0x1f0),p:read_u16(slots[side].roster),p:read_u16(0x01061b30)))
end)
end
for n,slot in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'natural campaign native health '..n,function(at,data,mask)
  if mask==0xffff and first_live then
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
 if frame>=16000 then log('HOST_BOUND','maximum_fields=16000 full_campaign_acceptance=false');manager.machine:exit();return end
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
  if winner==0 and human.hp>0 and other.hp>0 and not visual_start then
   visual_motion=visual_motion or frame;local age=frame-visual_motion
   if age>=10 and age<20 then press('Right')end
   if age>=50 and age<54 then press('Up')end
   if age>=80 and age<84 then press('High Punch')end
   if age>=90 and age<180 then press('Block')end
  end
 else visual_motion=nil
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
local smoke_items,smoke_channels,smoke_launches={},{},{}
emu.register_frame(function()
 if frame~=1 then return end
 for name,index in pairs(manager.machine.devices[':'].items)do
  for _,field in ipairs({'actor','main','health','id','mode'})do
   if name:match('/m_mk2ks_battle_'..field..'$')then smoke_items[field]=emu.item(index)end
  end
 end
 for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
  local n,field=name:match('^(%x+)/chan%.(.+)$')
  if n and tonumber(n,16)>=10 and tonumber(n,16)<=13 then
   n=tonumber(n,16);smoke_channels[n]=smoke_channels[n]or{};smoke_channels[n][field]=emu.item(index)
  end
 end
 assert(smoke_items.actor and smoke_items.main and smoke_channels[10]and smoke_channels[13])
end)
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'combined actual sound words',function(at,data,mask)
 if at~=0x01d01030 or mask~=0xffff then return end
 log('COMBINED_SOUND_WORD',string.format('word=%04X pc=%08X a8=%08X a13=%08X mode=%d',data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(0x010601d0)))
 if data<0x6b00 or data>0x6b03 then return end
 for n=1,2 do local a=sample(n)
  if a and(a.id==17 or a.id==18)and a.roster==a.id and a.owner==a.actor and a.hp>0 and cpu.A8.value==a.actor and cpu.A13.value==a.main then
   smoke_launches[n]={frame=frame,actor=a.actor,main=a.main,id=a.id}
   log('COMBINED_AUDIO_CUE',string.format('slot=%d cue=%04X pc=%08X actor=%08X main=%08X id=%d state=%d hp=%d action=%d',n,data,cpu.PC.value,a.actor,a.main,a.id,a.state,a.hp,a.action))
  end
 end
end)
emu.register_frame_done(function()
 for n,launch in pairs(smoke_launches)do if frame-launch.frame<=120 then
  local a=sample(n);local index=n-1
  log('COMBINED_AUDIO_OWNER',string.format('slot=%d launch=%d age=%d saved_actor=%08X saved_main=%08X saved_id=%d saved_mode=%d saved_hp=%d mode=%d guest_actor=%08X guest_main=%08X guest_id=%d roster=%d state=%d hp=%d',n,launch.frame,frame-launch.frame,smoke_items.actor:read(index),smoke_items.main:read(index),smoke_items.id:read(index),smoke_items.mode:read(index),smoke_items.health:read(index),p:read_u16(0x010601d0),a and a.actor or 0,a and a.main or 0,a and a.id or 0,a and a.roster or 0,a and a.state or -1,a and a.hp or 0))
  for channel=10+index*2,11+index*2 do local c=smoke_channels[channel]
   log('COMBINED_AUDIO_CHANNEL',string.format('slot=%d launch=%d age=%d channel=%d sample=%d length=%d pos=%.8f paused=%d loop=%d',n,launch.frame,frame-launch.frame,channel,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.paused:read(0),c.loop:read(0)))
  end
 end end
end)


local function laser_pair()
 local k,h=sample(2),sample(1)
 return k and h and k.id==17 and k.roster==17 and k.state==0 and k.owner==k.actor and h.id==17 and h.roster==17 and h.state==1 and h.owner==h.actor,k,h
end
taps[#taps+1]=p:install_read_tap(0xffd85800,0xffd8580f,'actualnaturalCPUlaserentry',function(at)
 if at~=0xffd85800 or cpu.PC.value~=0xffd85810 or visual_start then return end
 local ok,k,h=laser_pair();if not ok or cpu.A8.value~=k.actor or cpu.A13.value~=k.main then return end
 assert(h.hp==0 and k.hp>0);visual_start=frame
 log('VISUAL_LASER_ENTRY',string.format('actor=%08X main=%08X owner=%08X victim=%08X victim_main=%08X id=%d victim_id=%d cpu_state=%d victim_state=%d hp=%d,%d pc=%08X',k.actor,k.main,k.owner,h.actor,h.main,k.id,h.id,k.state,h.state,k.hp,h.hp,cpu.PC.value))
end)
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'naturalCPUlaserphasewords',function(at,data,mask)
 if not visual_start or at~=0x01d01030 or mask~=0xffff or data<0x6b40 or data>0x6b44 then return end
 local ok,k,h=laser_pair();if not ok or cpu.A8.value~=k.actor or cpu.A13.value~=k.main then return end
 log('VISUAL_LASER_PHASE',string.format('cue=%04X pc=%08X actor=%08X main=%08X victim=%08X victim_main=%08X palettes=%04X,%04X poses=%08X,%08X hp=%d,%d',data,cpu.PC.value,k.actor,k.main,h.actor,h.main,k.bank,h.bank,k.pose,h.pose,k.hp,h.hp))
 local label=({[0x6b40]='charge',[0x6b41]='beam',[0x6b43]='burst'})[data]
 if label and not visual_captured[label]then visual_pending[frame+4]=label end
end)
taps[#taps+1]=p:install_read_tap(0xffa14860,0xffa1486f,'actualCPUlaserwinner',function(at)
 if not visual_start or visual_winner or at~=0xffa14860 or cpu.PC.value~=0xffa14870 then return end
 local k=sample(2);if k and cpu.A8.value==k.actor and cpu.A13.value==k.main then visual_winner=frame;visual_pending[frame+60]='postscene';log('VISUAL_LASER_WINNER','main='..string.format('%08X',k.main))end
end)
emu.register_frame_done(function()
 if not visual_start then return end
 if(frame-visual_start)%10==0 or visual_pending[frame]then
  for n=1,2 do local a=sample(n);if a then log('VISUAL_LASER_ACTOR',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d pose=%08X palette=%04X x=%d y=%d floor=%d body=%04X trail=%08X',n,a.actor,a.main,a.owner,a.id,a.roster,a.state,a.hp,a.pose,a.bank,a.x,a.y,a.floor,a.body,a.trail))end end
 end
 local label=visual_pending[frame]
 if label and not visual_captured[label]then
  visual_captured[label]=true;local count=0;for _ in pairs(visual_captured)do count=count+1 end;assert(count<=4)
  log('VISUAL_LASER_CAPTURE','label='..label..' start='..visual_start..' mode='..p:read_u16(0x010601d0)..' actors='..string.format('%08X,%08X',p:read_u32(slots[1].actor),p:read_u32(slots[2].actor)))
  screen:snapshot(assert(os.getenv('MK2KS_LASER_PNG_DIR'))..'/'..label..'.png')
 end
 if visual_captured.postscene or frame-visual_start>=850 then log('VISUAL_LASER_COMPLETE','started='..visual_start..' winner='..(visual_winner or-1));manager.machine:exit()end
end)
