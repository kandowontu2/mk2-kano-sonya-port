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
assert(strategy=='uppercut' or strategy=='jumpkick' or strategy=='specials')
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
local command=nil
local reset_seen=nil
local draw_count=0
local function log(tag,value)
 print(string.format('MK2_NAT_CAMPAIGN_%s frame=%d human_slot=%d fighter=%s writes=0 assistance=none %s',tag,frame,side,fighter,value or''))
end
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
 log('WIN',string.format('slot=%d stage=%d id=%d entry=%08X pc=%08X health=%d,%d',winner,p:read_u16(0x01061b30),(at-0xfffef800)//32,at,cpu.PC.value,p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)))
end)
for _,address in ipairs({0x010601d0,0x01061b00,0x010601f0,0x01060dc0})do
 taps[#taps+1]=p:install_write_tap(address,address+15,'native campaign transition provenance',function(at,data,mask)
  if not first_live or mask~=0xffff or p:read_u16(at)==data&0xffff then return end
  log('TRANSITION',string.format('at=%08X before=%d after=%d pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X sp=%08X callers=%08X,%08X,%08X mode=%d phase=%d',at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,cpu.SP.value,p:read_u32(cpu.SP.value),p:read_u32(cpu.SP.value+32),p:read_u32(cpu.SP.value+64),p:read_u16(0x010601d0),p:read_u16(0x01061b00)))
 end)
end
for _,address in ipairs({0xffffffe0,0xffa1e800,0xffa1e880,0xfffaae00,0xfffab200})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'native campaign reset or finish boundary',function(at)
  if not first_live or at~=address then return end
  if address~=0xffffffe0 and cpu.PC.value~=address+16 then return end
  log('BOUNDARY',string.format('entry=%08X pc=%08X a8=%08X a13=%08X mode=%d phase=%d stage=%d',address,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(0x010601d0),p:read_u16(0x01061b00),p:read_u16(0x01061b30)))
  if address==0xffffffe0 then reset_seen=reset_seen or frame end
 end)
end
-- Instruction and source provenance only. These taps never supply data or
-- change the guest, including the malformed group that is under investigation.
for _,address in ipairs({0xff838790,0xff83bb00,0xff85c420})do
 taps[#taps+1]=p:install_read_tap(address,address+15,'Pit cinematic group provenance',function(at)
  if at~=address or cpu.PC.value~=address+16 or p:read_u16(0x010601d0)~=9 then return end
  draw_count=draw_count+1
  if draw_count>900 then return end
  local a,m=cpu.A8.value,cpu.A13.value
  local cells={}
  if valid(m)then for offset=0x100,0x350,0x10 do cells[#cells+1]=string.format('%03X:%08X',offset,p:read_u32(m+offset))end end
  log('DRAW',string.format('entry=%08X a0=%08X a1=%08X a5=%08X a8=%08X a9=%08X a13=%08X sp=%08X actor_id=%d pose=%08X cache=%08X flags=%04X task=%s',address,cpu.A0.value,cpu.A1.value,cpu.A5.value,a,cpu.A9.value,m,cpu.SP.value,valid(a)and p:read_u16(a+0x1f0)or -1,valid(a)and p:read_u32(a+0x1d0)or 0,valid(a)and p:read_u32(a+0x1a0)or 0,valid(a)and p:read_u16(a+0x160)or 0,table.concat(cells,',')))
 end)
end
local components=0
taps[#taps+1]=p:install_read_tap(0xff8387f0,0xff8387ff,'Pit component source provenance',function(at)
 if at~=0xff8387f0 or cpu.PC.value~=0xff838800 or p:read_u16(0x010601d0)~=9 then return end
 components=components+1
 if components>150 then return end
 local source=cpu.A0.value
 log('COMPONENT',string.format('source=%08X value=%08X dst=%08X a8=%08X a9=%08X a13=%08X',source,p:read_u32(source),cpu.A1.value,cpu.A8.value,cpu.A9.value,cpu.A13.value))
end)
local cinematic_active=false
local pit_table=p:read_u32(0xff85c330)
assert(pit_table==p:read_u32(0xff85c4a0),'Both actual scene operands must agree')
local pit_lookups,pit_enter,pit_exit=0,nil,nil
taps[#taps+1]=p:install_read_tap(pit_table,pit_table+19*32-1,'actual native Pit victim table lookup',function(at,data)
 if cpu.PC.value~=0xff83b850 or (at-pit_table)%32~=0 then return end
 local a,m=cpu.A8.value,cpu.A13.value
 cinematic_active=true
 pit_lookups=pit_lookups+1;pit_enter=pit_enter or frame
 log('PIT_LOOKUP',string.format('at=%08X value=%08X pc=%08X a8=%08X a13=%08X id=%d a1=%08X table_slot=%d mode=%d',at,data,cpu.PC.value,a,m,p:read_u16(a+0x1f0),cpu.A1.value,(at-pit_table)//32,p:read_u16(0x010601d0)))
end)
local moves={knife=0xffffb000,ring=0xffffb400,choke=0xfff91400,leg=0xfff80800,
 blade=0xfff8cc00,ball=0xffffde00,bicycle=0xfff9a400,square=0xffffca00}
for move,address in pairs(moves)do
 taps[#taps+1]=p:install_read_tap(address,address+15,'natural campaign action '..move,function(at)
  if at~=address or cpu.PC.value~=address+16 then return end
  local own=sample(side)
  if own and own.actor==cpu.A8.value and own.main==cpu.A13.value and own.state==1 and own.id==identity then
   log('SPECIAL',string.format('move=%s entry=%08X pc=%08X actor=%08X main=%08X id=%d stage=%d',move,address,cpu.PC.value,own.actor,own.main,own.id,p:read_u16(0x01061b30)))
  end
 end)
end
emu.register_frame(function()
 frame=frame+1
 for _,field in pairs(buttons)do field:clear_value()end
 if frame==1 then
  log('BOOT','schema=7 strategy='..strategy..' boot='..boot)
  log('PIT_OPERANDS',string.format('first=%08X second=%08X',p:read_u32(0xff85c330),p:read_u32(0xff85c4a0)))
  for id=0,18 do log('PIT_ROM',string.format('id=%d value=%08X',id,p:read_u32(pit_table+id*32)))end
  local rom_table=p:read_u32(0xff8a11f0)
  for order=0,5 do
   local list=p:read_u32(rom_table+order*32);local ids={}
   for stage=0,16 do ids[#ids+1]=p:read_u16(list+stage*16)end
   log('ROM',string.format('table=%08X order=%d list=%08X ids=%s',rom_table,order,list,table.concat(ids,',')))
  end
 end
 if frame>=300 and frame<304 then press('High Punch')end
 local mode=p:read_u16(0x010601d0);local state=p:read_u16(slots[side].state)
 if cinematic_active and mode~=9 and not pit_exit then
  pit_exit=frame
  log('PIT_EXIT',string.format('enter=%d lookups=%d mode=%d states=%d,%d health=%d,%d',pit_enter,pit_lookups,mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)))
  screen:snapshot('campaign_pit_exit_'..frame..'.png')
 end
 local stage=p:read_u16(0x01061b30);local schedule=p:read_u32(0x01061b10)
 local winner=p:read_u16(0x01061b00)
 local key=string.format('%d:%d:%d:%d:%08X:%d:%d:%08X:%08X',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),stage,schedule,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor))
 if key~=last_state or frame%120==0 then
  log('STATE',string.format('mode=%d states=%d,%d stage=%d schedule=%08X roster=%d,%d actors=%08X,%08X health=%d,%d winner=%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state),stage,schedule,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u32(slots[1].actor),p:read_u32(slots[2].actor),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),winner))
  last_state=key
 end
 if first_live and mode==9 and last_state==key then
  if frame%30==0 then
   log('NINE',string.format('pc=%08X phase=%d stage=%d a8=%08X a13=%08X',cpu.PC.value,winner,stage,cpu.A8.value,cpu.A13.value))
   screen:snapshot('campaign_mode9_'..frame..'.png')
  end
 end
 if cinematic_active and mode==9 and frame%3==0 then screen:snapshot('campaign_pit_'..frame..'.png')end
 if reset_seen and frame>=reset_seen+240 then manager.machine:exit()end
 if first_live and not loss_at and mode==3 and state==2 and p:read_u16(slots[side].hp)==0 and p:read_u32(slots[side].actor)==0 then
  losses=losses+1;loss_at=frame;css=nil;css_exit=nil
  log('LOSS','number='..losses..' stage='..stage)
  screen:snapshot(string.format('campaign_loss_%d.png',losses))
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
 local selection_roster=p:read_u16(slots[side].roster)
 if not css and frame>700 and mode==4 and state==3 and selection_roster<=18 then
  plan=route(selection_roster);css=frame;selections=selections+1
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
   screen:snapshot(string.format('campaign_selection_%d_%d.png',selections,age))
  end
  if age>=148 and age<156 then press('High Punch')end
  if age>148 and mode~=4 then css_exit=frame;log('SELECT_EXIT','number='..selections)end
 end
 local human,other=sample(side),sample(opponent)
 if mode==2 and state==1 and p:read_u16(slots[opponent].state)==0 and human and other and human.owner==human.actor and other.owner==other.actor then
  if not first_live then first_live=frame end
  local fight_key=string.format('%d:%d:%08X:%08X',selections,stage,human.actor,other.actor)
  if fight_key~=last_fight then
   last_fight=fight_key;loss_at=nil;command=nil
   log('FIGHT',string.format('selection=%d stage=%d schedule=%08X human=%d:%d cpu=%d:%d actors=%08X,%08X',selections,stage,schedule,human.roster,human.id,other.roster,other.id,human.actor,other.actor))
   screen:snapshot(string.format('campaign_fight_selection%d_stage%d.png',selections,stage))
  end
  local seen_key=stage..':'..schedule
  if not seen[seen_key]then seen[seen_key]=true;log('STAGE','stage='..stage..' schedule='..string.format('%08X',schedule))end
  live_fields=live_fields+1
  if live_fields<300 or frame%30==0 then
   log('LIVE',string.format('selection=%d stage=%d schedule=%08X human=%d:%d cpu=%d:%d health=%d,%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X hpos=%d,%d hfloor=%d cpos=%d,%d cfloor=%d poses=%08X,%08X actions=%d,%d flags=%04X,%04X banks=%04X,%04X',selections,stage,schedule,human.roster,human.id,other.roster,other.id,human.hp,other.hp,human.actor,human.main,other.actor,other.main,human.x,human.y,human.floor,other.x,other.y,other.floor,human.pose,other.pose,human.action,other.action,human.flags,other.flags,human.bank,other.bank))
  end
  if winner==0 and human.hp>0 and other.hp>0 then
   local gap=math.abs(human.x-other.x)
   if strategy=='uppercut' then
    if gap>65 then press(human.x<other.x and'Right'or'Left')
    else press('Down');if frame%22<4 then press('High Punch')end end
   elseif strategy=='jumpkick' then
    if gap>80 then press(human.x<other.x and'Right'or'Left')end
    if frame%56<4 then press('Up')end
    if frame%56>=12 and frame%56<20 then press('High Kick')end
   else
    if command and (command.actor~=human.actor or command.main~=human.main or frame-command.frame>=110)then command=nil end
    if not command and human.y==human.floor and human.flags&0x1c==0 then
     if gap>150 or gap<=58 then
      local forward=human.x<other.x and'Right'or'Left'
      command={frame=frame,actor=human.actor,main=human.main,forward=forward,
       back=forward=='Right'and'Left'or'Right',move=gap>150 and(fighter=='kano'and'knife'or'ring')or(fighter=='kano'and'choke'or'leg')}
      log('COMMAND','move='..command.move..' gap='..gap..' forward='..forward)
     else press(human.x<other.x and'Right'or'Left')end
    end
    if command then
     local age=frame-command.frame;local move=command.move
     if move=='leg' then
      if age<7 then press('Down')end
      if age>=3 and age<7 then press('Low Punch');press('Block')end
     else
      if age<3 then press('Down')end
      if age>=5 and age<8 then press(move=='knife'and command.back or command.forward)end
      if age>=6 and age<9 then press(move=='knife'and'High Punch'or'Low Punch')end
     end
    end
   end
  end
 end
 if first_live and stage==16 and mode==11 and winner==side and p:read_u16(slots[side].roster)==identity then
  ending=ending or frame
  if (frame-ending)%120==0 then screen:snapshot('campaign_ending_'..(frame-ending)..'.png');log('ENDING','age='..(frame-ending))end
 end
end)
emu.register_stop(function()
 local count=0;for _ in pairs(seen)do count=count+1 end
 log('RESULT',string.format('schema=7 selections=%d losses=%d native_win_reads=%d first_live=%d live_fields=%d seen_stages=%d ending=%d reset=%d pit_lookups=%d pit_enter=%d pit_exit=%d scope=unassisted_campaign_observation_independent_verification_pending',selections,losses,wins,first_live or -1,live_fields,count,ending or -1,reset_seen or -1,pit_lookups,pit_enter or -1,pit_exit or -1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
