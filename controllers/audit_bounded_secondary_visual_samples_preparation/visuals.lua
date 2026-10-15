
for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
 assert(not os.getenv(key),'No forced finisher assistance')
end
-- Genuine two-human rounds and stock fatality commands; physical inputs only.
assert(not rawget(_G,'MK2_REPTILE_V879_ACTIVE'),'Duplicate observer/driver')
rawset(_G,'MK2_REPTILE_V879_ACTIVE',true)
local name=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local identity=assert(({kano=17,sonya=18,liu_kang=1,kitana=4,mileena=5})[name])
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
assert(side==1 or side==2)
local winner_side=3-side
local killer=assert(os.getenv('MK2KS_STOCK_KILLER'))
local killer_id=assert(({cage=2,baraka=3,kitana=4,kung_lao=0,jax=11,kano=17,sonya=18})[killer])
local command=assert(os.getenv('MK2KS_STOCK_COMMAND'))
local commands={ddff_lp={'Down','Down','Forward','Forward','Low Punch'},
 bbbb_hp={'Back','Back','Back','Back','High Punch'},
 bbdb_hk={'Back','Back','Down','Back','High Kick'},
 ffff_hp={'Forward','Forward','Forward','Forward','High Punch'},
 ffdf_hk={'Forward','Forward','Down','Forward','High Kick'},
 ffdf_lk_release={'Forward','Forward','Down','Forward','Release Low Kick'},
 bbdb_lk_release={'Back','Back','Down','Back','Release Low Kick'}}
commands.fff_lk={'Forward','Forward','Forward','Low Kick'}
commands.fff_lp_release={'Forward','Forward','Forward','Release Low Punch'}
commands.bf_lp_release={'Back','Forward','Release Low Punch'}
commands.bbbb_lp={'Block','Block','Block','Block','Low Punch'}
commands.kano_own={'Back','Down','Forward','High Kick'}
commands.sonya_own={'Back','Forward','Down','Down','Low Punch'}
commands.kano_laser={'Low Punch','Block','Block','High Kick'}
commands.sonya_orb={'Up','Up','Back','Down','High Kick'}
local sequence=assert(commands[command])
local release_button=command:match('_lp_release$')and'Low Punch'or(command:match('_lk_release$')and'Low Kick'or nil)
local release_age=10+(#sequence-1)*8
local target_gap=assert(tonumber(os.getenv('MK2KS_STOCK_GAP')))
local p=manager.machine.devices[':maincpu'].spaces.program
local action_addresses={p:read_u32(p:read_u32(0xff876b50)+killer_id*32),p:read_u32(p:read_u32(0xff876b90)+killer_id*32)}
for _,address in ipairs(action_addresses)do assert(address>=0xff800000 and address<0xffff0000)end
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local high,system,low=manager.machine.ioport.ports[':IN0'].fields,
 manager.machine.ioport.ports[':IN1'].fields,manager.machine.ioport.ports[':IN2'].fields
local buttons={}
for n=1,2 do
 buttons[n]={}
 for _,key in ipairs({'Left','Right','Up','Down','Block','High Punch','High Kick'})do
  buttons[n][key]=high['P'..n..' '..key]
 end
 for _,key in ipairs({'Low Punch','Low Kick'})do buttons[n][key]=low['P'..n..' '..key]end
 buttons[n].Coin=system['Coin '..n]
 buttons[n].Start=system[n==1 and '1 Player Start'or'2 Players Start']
end
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local frame,first_live,finish_start,approach_done,action_start,wrap=0,nil,nil,nil,nil,nil
local css,plans,taps={},{},{}
local damage,wins,last_mode=0,0,nil
local join_at=nil
local function log(tag,s)
 print(string.format('MK2_STOCK_HEAD_V921_%s frame=%d victim=%s side=%d killer=%s writes=0 assistance=none %s',tag,frame,name,side,killer,s or''))
end
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),
  roster=p:read_u16(s.id),hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),
  pose=p:read_u32(a+0x1d0),bank=p:read_u16(a+0x140),flags=p:read_u16(a+0x160)}
end
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
local function tap(address,label,callback)
 taps[#taps+1]=p:install_read_tap(address,address+15,label,function(at)
  if at==address and frame>600 then callback()end
 end)
end
taps[#taps+1]=p:install_write_tap(slots[side].hp,slots[side].hp+15,'actual victim health',function(at,data,mask)
 if at~=slots[side].hp or mask&0xffff~=0xffff or not first_live then return end
 local before,after=p:read_u16(at),data&0xffff
 log('HEALTH',string.format('before=%d after=%d pc=%08X',before,after,cpu.PC.value))
 if cpu.PC.value==0xff836700 and after<before and before<=161 then damage=damage+before-after end
end)
tap(0xff876fa0,'stock fatality distance gate',function()
 if cpu.A7.value==0xff876b40 or cpu.A7.value==0xff876b80 then
  log('GATE',string.format('action=%08X distance=%d limit=%d actor=%08X main=%08X pc=%08X',
   cpu.A7.value,cpu.A3.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,cpu.PC.value))
 end
end)
for variant,action_address in ipairs(action_addresses)do
tap(action_address,'original stock fatality variant '..variant,function()
 local own,victim=sample(winner_side),sample(side)
 if not own or not victim or cpu.A8.value~=own.actor or cpu.A13.value~=own.main or
  own.id~=killer_id or victim.id~=identity or victim.hp~=0 then return end
 if action_start then return end
 action_start=frame
 rawset(_G,'MK2_STOCK_V921_ACTION_START',frame)
 log('ACTION',string.format('variant=%d address=%08X actor=%08X main=%08X victim_actor=%08X victim_main=%08X damage=%d mode=%d',
  variant,action_address,own.actor,own.main,victim.actor,victim.main,damage,p:read_u16(0x010601d0)))
end)
end
tap(0xff877580,'original button history parser',function()
 if finish_start and not action_start then log('BUTTON_PARSER',string.format('table=%08X actor=%08X main=%08X',cpu.A11.value,cpu.A8.value,cpu.A13.value))end
end)
tap(0xff83b7f0,'native ID-indexed pointer lookup entry',function()
 if action_start and frame-action_start<650 then
  log('TABLE_ENTER',string.format('age=%d table=%08X actor=%08X main=%08X id=%d',frame-action_start,cpu.A0.value,cpu.A8.value,cpu.A13.value,valid(cpu.A8.value)and p:read_u16(cpu.A8.value+0x1f0)or-1))
 end
end)
tap(0xff83b850,'native ID-indexed pointer lookup return',function()
 if action_start and frame-action_start<650 then
  log('TABLE_RETURN',string.format('age=%d table=%08X value=%08X actor=%08X main=%08X id=%d',frame-action_start,cpu.A1.value,cpu.A0.value,cpu.A8.value,cpu.A13.value,valid(cpu.A8.value)and p:read_u16(cpu.A8.value+0x1f0)or-1))
 end
end)
tap(0xff8775d0,'original command history parser',function()
 if finish_start and not action_start then
  log('PARSER',string.format('table=%08X a0=%08X a1=%08X actor=%08X main=%08X pc=%08X',
   cpu.A11.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,cpu.PC.value))
 end
end)
tap(0xff877790,'native command history comparison',function()
 if finish_start and not action_start then
  log('COMPARE',string.format('wanted=%d actual=%d tick=%d table=%08X pc=%08X',
   cpu.A8.value>>16,cpu.A0.value>>16,cpu.A0.value&0xffff,cpu.A11.value,cpu.PC.value))
 end
end)
tap(0xff906090,'actual native animation lookup',function()
 if action_start then
  local victim=sample(side)
  if victim and cpu.A8.value==victim.actor then
   log('LOOKUP',string.format('age=%d index=%08X actor=%08X main=%08X',frame-action_start,cpu.A9.value,cpu.A8.value,cpu.A13.value))
  end
 end
end)
for _,operand in ipairs({0xff8cc790,0xff8ccc80})do
 local address=p:read_u32(operand)
 taps[#taps+1]=p:install_read_tap(address,address+19*16-1,'Kitana actual victim parameter',function(at,data,mask)
  if killer~='kitana'or not action_start or mask~=0xffff or cpu.PC.value~=0xff82ee10 then return end
  if at~=address+identity*16 then return end
  log('PARAMETER',string.format('age=%d operand=%08X table=%08X at=%08X row=%d value=%04X actor=%08X main=%08X pc=%08X',
   frame-action_start,operand,address,at,identity,data&0xffff,cpu.A8.value,cpu.A13.value,cpu.PC.value))
 end)
end
for _,operand in ipairs({0xff9ec840,0xff9ec8b0,0xff9ecbd0})do
 local address=p:read_u32(operand)
 taps[#taps+1]=p:install_read_tap(address,address+19*32-1,'original inflation victim pointer consumer',function(at,data,mask)
  local row_at=address+identity*32
  if killer~='kitana'or not action_start or (at~=row_at and at~=row_at+16)or cpu.PC.value~=0xff83b850 then return end
  log('GORE_ROW',string.format('age=%d operand=%08X table=%08X at=%08X row=%d half=%d value=%04X mask=%08X actor=%08X main=%08X pc=%08X',
   frame-action_start,operand,address,at,identity,(at-row_at)//16,data&0xffff,mask,cpu.A8.value,cpu.A13.value,cpu.PC.value))
 end)
end
tap(0xff842d90,'native opponent animation lookup',function()
 if action_start then log('VICTIM_ANIMATION',string.format('age=%d index=%08X actor=%08X main=%08X caller=%08X pc=%08X',
  frame-action_start,cpu.A9.value,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.PC.value))end
end)
tap(0xff8cdc40,'original stock fatality common completion',function()
 if action_start then wrap=frame;log('WRAP',string.format('age=%d actor=%08X main=%08X pc=%08X',frame-action_start,cpu.A8.value,cpu.A13.value,cpu.PC.value))end
end)
tap(0xff90c8d0,'actual selected native death palette',function()
 if not action_start then return end
 local a=cpu.A8.value;local own=sample(side)
 if not valid(a)or p:read_u16(a+0x1f0)~=identity then return end
 log('PALETTE',string.format('age=%d pointer=%08X actor=%08X main=%08X id=%d flags=%04X physical_actor=%08X physical_main=%08X owner=%08X pc=%08X',
  frame-action_start,cpu.A0.value,a,cpu.A13.value,p:read_u16(a+0x1f0),p:read_u16(a+0x160),
  own and own.actor or 0,own and own.main or 0,own and own.owner or 0,cpu.PC.value))
end)
taps[#taps+1]=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,'actual native round wins',function(at)
 if first_live and at==0xfffef800+killer_id*32 and p:read_u16(slots[side].hp)==0 then
  wins=wins+1;log('WIN','count='..wins)
 end
end)
taps[#taps+1]=p:install_write_tap(0x01060100,0x010610ff,'reject body-cache global overrun',function(at,data,mask)
 if cpu.PC.value==0xff838860 then log('CACHE_OVERWRITE',string.format('at=%08X data=%04X mask=%04X',at,data&0xffff,mask))end
end)
emu.register_frame(function()
 assert(#taps==20,'Retain both original action variants and native table lookup observers')
 frame=frame+1
 for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end
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
 if mode~=last_mode then log('MODE',string.format('mode=%d states=%d,%d',mode,p:read_u16(slots[1].state),p:read_u16(slots[2].state)));last_mode=mode end
 for n=1,2 do
  if mode~=4 then css[n]=nil end
  if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css[n]then
   css[n]=frame;plans[n]=route(p:read_u16(slots[n].id),n==side and identity or killer_id)
   if n==1 and not join_at then join_at=frame;log('JOIN_BEGIN','slot=2')end
   log('SELECT',string.format('slot=%d target=%d path=%s',n,n==side and identity or killer_id,table.concat(plans[n],',')))
  end
  if css[n]and mode==4 then
   local age=frame-css[n]
   for i,key in ipairs(plans[n])do if age>=56+(i-1)*12 and age<60+(i-1)*12 then press(n,key)end end
   if age>=148 and age<156 then press(n,'High Punch')end
  end
 end
 local own,victim=sample(winner_side),sample(side)
 if not own or not victim or own.id~=killer_id or victim.id~=identity or own.owner~=own.actor or victim.owner~=victim.actor then return end
 local forward=own.x<victim.x and'Right'or'Left';local back=forward=='Right'and'Left'or'Right'
 local gap=math.abs(own.x-victim.x)
 local finish_flag=p:read_u16(0x01061b00)
 if (mode==2 or mode==6)and finish_flag==0 and p:read_u16(slots[1].state)==1 and p:read_u16(slots[2].state)==1 then
  if not first_live then first_live=frame;log('FIRST_LIVE',string.format('own=%08X victim=%08X ids=%d,%d',own.actor,victim.actor,own.id,victim.id))end
  if p:read_u16(0x01061b00)==0 and own.hp>0 and victim.hp>0 and frame-first_live>=180 then
   if gap>80 then press(winner_side,forward)
   else press(winner_side,'Down');if(frame-first_live)%42<4 then press(winner_side,'High Punch')end end
  end
 elseif finish_flag==3 and own.hp>0 and victim.hp==0 and not action_start then
  finish_start=finish_start or frame
  local age=frame-finish_start
  if age>=65 and not approach_done then
   if gap<target_gap-4 then press(winner_side,back)
   elseif gap>target_gap+4 then press(winner_side,forward)
   else approach_done=frame;log('APPROACH','gap='..gap)end
  end
  if approach_done then
   local command_age=frame-approach_done
   local offset=10
   if command=='sonya_orb' and command_age>=offset and command_age<offset+#sequence*8 then press(winner_side,'Block')end
   if (killer=='baraka'or command=='fff_lk')and command_age>=offset and command_age<offset+(#sequence-1)*8 then press(winner_side,'Block')end
   if release_button and command_age<release_age then press(winner_side,release_button)end
   for i,key in ipairs(sequence)do
    local start=offset+(i-1)*8
    if not key:match('^Release ')and command_age>=start and command_age<start+3 then
     press(winner_side,key=='Forward'and forward or key=='Back'and back or key)
    end
   end
  end
 end
 -- Start the release-button hold while still far apart in ordinary combat.
 -- Holding it through the last KO avoids attacking a dizzy opponent just to
 -- initialize the hold timer. The only mutations here are physical inputs.
 if release_button and first_live and not action_start and
  (not approach_done or frame-approach_done<release_age)then press(winner_side,release_button)end
 if frame%15==0 and first_live then log('STATE',string.format('mode=%d own=%08X:%08X:%d victim=%08X:%08X:%d hp=%d,%d gap=%d poses=%08X,%08X banks=%04X,%04X',
  mode,own.actor,own.main,own.id,victim.actor,victim.main,victim.id,own.hp,victim.hp,gap,own.pose,victim.pose,own.bank,victim.bank))end
end)
emu.register_stop(function()
 log('RESULT',string.format('damage=%d wins=%d first_live=%d action=%d wrap=%d scope=diagnostic_no_full_art_acceptance',damage,wins,first_live or-1,action_start or-1,wrap or-1))
end)

emu.register_frame(function()
 if action_start and wrap and frame-wrap>=120 then
  log('BOUNDED_TERMINAL','reason=native_common_completion_followthrough raw_media=none')
  manager.machine:exit()
 elseif frame>=5800 then
  log('BOUNDED_FAILED','reason=earned_finisher_timeout raw_media=none')
  manager.machine:exit()
 end
end)

local visual_count=0
emu.register_frame_done(function()
 if not action_start then return end
 local age=frame-action_start
 local label=({[30]='startup',[100]='active',[180]='late'})[age]
 if wrap and frame-wrap==100 then label='post_wrap' end
 if label then
  visual_count=visual_count+1;assert(visual_count<=4)
  screen:snapshot('secondary_'..label..'.png')
  log('VISUAL_SAVED','sample='..label..' count='..visual_count)
 end
end)
