local ready=nil

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
local killer_id=assert(({cage=2,baraka=3,kitana=4,kung_lao=0,jax=11})[killer])
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
local sequence=assert(commands[command])
local release_button=command:match('_lp_release$')and'Low Punch'or(command:match('_lk_release$')and'Low Kick'or nil)
local release_age=10+(#sequence-1)*8
local target_gap=assert(tonumber(os.getenv('MK2KS_STOCK_GAP')))
local p=manager.machine.devices[':maincpu'].spaces.program
local action_addresses={p:read_u32(0xff8ba210+killer_id*32),p:read_u32(0xff8ba390+killer_id*32)}
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
  roster=p:read_u16(s.id),hp=p:read_u16(s.hp),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),action=p:read_u16(m+0x1f0),
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
 action_start=frame;ready=frame
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

local regs=cpu
local actual_dma={}
local clip_tap=p:install_write_tap(0x01a80000,0x01a800ff,'passive exact native DMA banked registers',function(at,data,mask)
 if (at-0x01a80000)%16~=0 then return end
 local n=(at-0x01a80000)//16
 if n==12 or n==13 then
  local bank=(p:read_u16(0x01a800f0)>>5)&1
  if bank==0 then n=n+4 end
 end
 mask=mask&65535;data=data&65535
 local before=actual_dma[n]or 0
 actual_dma[n]=(before&(~mask&65535))|(data&mask)
end)
local function clip_trace(kind,slot,id,source,x,y,w,h,c)
 assert(actual_dma[0]~=nil and actual_dma[12]~=nil and actual_dma[13]~=nil and actual_dma[16]~=nil and actual_dma[17]~=nil,'Clip and skip state actually initialized by native writes')
 log('IDLE_DMA_CLIP',string.format('kind=%s slot=%d id=%d source=%08X x=%d y=%d width=%d height=%d command=%04X lrskip=%04X top=%d bottom=%d left=%d right=%d config=%04X',
  kind,slot,id,source,x,y,w,h,c,actual_dma[0],actual_dma[12]&511,actual_dma[13]&511,actual_dma[16]&1023,actual_dma[17]&1023,p:read_u16(0x01a800f0)))
end
emu.register_stop(function()assert(clip_tap)end)

local point_vram=nil
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_local_videoram$')then assert(not point_vram);point_vram=emu.item(index)end
end end
assert(point_vram and point_vram.size==2 and point_vram.count>=512*512)
local idle_points={}
local footprint_stats={points=0,source_fail=0,display_fail=0,offscreen=0,slots={0,0}}
local shadow_queries={}
local coverage_context=nil
local sole_gfx=assert(manager.machine.memory.regions[':gfxrom'])
local function opaque_bounds(source,w,h,command)
    assert(w>0 and w<=200 and h>0 and h<=200)
    local mapped=source
    if source>=0x10000000 and source<0x1a000000 then mapped=source-0x0a000000 end
    assert(mapped>=0 and mapped<0x10000000)
    local bit=mapped
    local bpp=(command>>12)&7;if bpp==0 then bpp=8 end
    local function take(n)
        assert(bit+n<=sole_gfx.size*8,'Complete actual source bits')
        local at=bit//8
        local word=sole_gfx:read_u8(at)|(sole_gfx:read_u8(at+1)<<8)
        local value=(word>>(bit%8))&((1<<n)-1)
        bit=bit+n;return value
    end
    local count,low,high=0,nil,nil
    local point_x,point_pixel
    for y=0,h-1 do
        local pre,post=0,0
        if command&0x80~=0 then
            local header=take(8)
            pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
        end
        assert(pre+post<=w,'Valid native compressed row')
        for x=pre,w-post-1 do
            local pixel=take(bpp)
            if pixel~=0 then
                local yy=command&0x20~=0 and -y or y
                if coverage_context and frame-ready>=31 and frame-ready<=60 then
                 assert(command&15==2 and actual_dma[0]==0,'Complete unit-scale opaque copy scope')
                 local xx=command&0x10~=0 and -x or x
                 local dx,dy=(coverage_context.x+xx)&1023,(coverage_context.y+yy)&511
                 if dx<400 and dx>=actual_dma[16] and dx<=actual_dma[17] and dy>=actual_dma[12] and dy<=actual_dma[13] then
                  idle_points[#idle_points+1]={frame=frame,slot=coverage_context.slot,id=coverage_context.id,kind='body',fullbody=true,x=dx,y=dy,index=coverage_context.bank|pixel}
                 end
                end

                if coverage_context then
                 local xx=command&0x10~=0 and -x or x
                 local key=string.format('%d_%d_%d',frame,(coverage_context.x+xx)&1023,(coverage_context.y+yy)&511)
                 for _,q in ipairs(shadow_queries[key]or{})do
                  q.cover_index=coverage_context.bank|pixel;q.cover_id=coverage_context.id;q.cover_slot=coverage_context.slot
                  q.cover_source=source;q.cover_sx=x;q.cover_sy=y;q.cover_pixel=pixel;q.cover_command=command;q.cover_pc=coverage_context.pc
                 end
                end

                if not high or yy>high then point_x=command&0x10~=0 and -x or x;point_pixel=pixel end
                count=count+1;low=low and math.min(low,yy) or yy;high=high and math.max(high,yy) or yy
            end
        end
    end
    return count,low or -999,high or -999,bit-mapped,point_x,point_pixel
end

local idle_owned={}
local idle_fifo= p:install_read_tap(0xff804410,0xff80441f,'bounded idle actual FIFO',function(at)
 if not ready or ((frame-ready)%8~=0 and not(frame-ready>=31 and frame-ready<=60)) or at~=0xff804410 or regs.PC.value~=0xff804420 then return end
 for slot=1,2 do
  local a=sample(slot)
  if a and a.actor==regs.A0.value then

   local size,xy,c=regs.A9.value,regs.A10.value,(regs.A12.value>>16)&0xffff
   local key=string.format('%d_%08X_%d_%d_%04X_%d_%d',frame,regs.A11.value,size&0x3ff,(size>>16)&0x3ff,c,xy&0x3ff,(xy>>16)&0x1ff)
   assert(not idle_owned[key]);idle_owned[key]={slot=slot,id=a.id,pose=a.pose}
   log('IDLE_FIFO',string.format('slot=%d id=%d pose=%08X source=%08X size=%08X xy=%08X command=%08X y=%d floor=%d action=%04X',
    slot,a.id,a.pose,regs.A11.value,regs.A9.value,regs.A10.value,regs.A12.value,a.y,a.floor,a.action))
  end
 end
end)
emu.register_stop(function()assert(idle_fifo);log('STOP','ready='..tostring(ready)..' raw_media=none')end)

local idle_dma=p:install_write_tap(0x01a80010,0x01a8001f,'actual idle body opaque bounds',function(at,data)
 if not ready or at~=0x01a80010 then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local src=reg(2)|(reg(3)<<16);local w,h=reg(6)&0x3ff,reg(7)&0x3ff
 local c,x,y=data&0xffff,reg(4)&0x3ff,reg(5)&0x1ff
 local key=string.format('%d_%08X_%d_%d_%04X_%d_%d',frame,src,w,h,c,x,y)
 local own=idle_owned[key];if not own then return end
 clip_trace('body',own.slot,own.id,src,x,y,w,h,c)
 coverage_context={x=x,y=y,bank=reg(8)&0x7f00,id=own.id,slot=own.slot,pc=regs.PC.value}
 local count,top,bottom,bits,px,pixel=opaque_bounds(src,w,h,c)
 coverage_context=nil

 local q={frame=frame,slot=own.slot,id=own.id,kind='body',x=(x+px)&1023,y=(y+bottom)&511,index=(reg(8)&0x7f00)|pixel}
 idle_points[#idle_points+1]=q
 local query_key=string.format('%d_%d_%d',frame,q.x,q.y)
 shadow_queries[query_key]=shadow_queries[query_key]or{};shadow_queries[query_key][#shadow_queries[query_key]+1]=q

 log('IDLE_OPAQUE',string.format('slot=%d id=%d pose=%08X source=%08X width=%d height=%d command=%04X x=%d y=%d opaque=%d top=%d bottom=%d endpoint=%d bits=%d scaleX=%d scaleY=%d clip12=%d clip13=%d config=%04X skip=%04X',
  own.slot,own.id,own.pose,src,w,h,c,x,y,count,top,bottom,(y+bottom)&511,bits,reg(10),reg(11),reg(12),reg(13),reg(15),reg(0)))
 idle_owned[key]=nil
end)
emu.register_stop(function()assert(idle_dma);local pending=0;for _ in pairs(idle_owned)do pending=pending+1 end;log('IDLE_OPAQUE_STOP','pending='..pending)end)

emu.register_frame_done(function()
 if #idle_points==0 then return end
 if idle_points[1].frame>=frame then return end
 local control=p:read_u16(0xc0000080);local adr=p:read_u16(0xc00001e0)
 local veb,vsb=p:read_u16(0xc0000050),p:read_u16(0xc0000060)
 local effective=(adr+(vsb-veb)*(control&0x3fc))&65535
 local address=control&0x400~=0 and effective or effective~0xfffc
 local row=(address>>4)&511;local column=((((address&0x7c)<<4)|(p:read_u16(0xc00001b0)&0x3fff))*2)&511
 local w,h=manager.machine.video:snapshot_size();local raw=manager.machine.video:snapshot_pixels();assert(w==400 and h==254 and #raw==406400)
 local future_points={}
 for _,q in ipairs(idle_points)do
  if q.frame<frame then
  local xx,yy=q.x-column,q.y-row
  local word=p:read_u16(0x01800000+q.index*16)
  local function expand(v)return (v<<3)|(v>>2)end
  local expected=(expand((word>>10)&31)<<16)|(expand((word>>5)&31)<<8)|expand(word&31)
  local actual=-1
  if xx>=0 and xx<w and yy>=0 and yy<h then actual=string.unpack('<I4',raw,(yy*w+xx)*4+1)&0xffffff end


  if q.fullbody then
   local index=q.all_index or q.cover_index or q.index
   local current=point_vram:read(q.y*512+q.x)&0x7fff
   local value=p:read_u16(0x01800000+index*16)
   local final=(expand((value>>10)&31)<<16)|(expand((value>>5)&31)<<8)|expand(value&31)
   footprint_stats.source_frame=q.frame;footprint_stats.points=footprint_stats.points+1
   footprint_stats.slots[q.slot]=footprint_stats.slots[q.slot]+1
   if q.source_vram~=index or current~=index then footprint_stats.source_fail=footprint_stats.source_fail+1 end
   
   if actual==-1 then footprint_stats.offscreen=footprint_stats.offscreen+1
   elseif actual~=final then
    footprint_stats.display_fail=footprint_stats.display_fail+1
    if footprint_stats.display_fail<=4 then
     log('FOOTPRINT_VISIBLE_GAP',string.format('source_frame=%d slot=%d x=%d y=%d display_x=%d display_y=%d expected=%06X actual=%06X',q.frame,q.slot,q.x,q.y,xx,yy,final,actual))
    end
   end
  else
  if q.kind=='shadow' or q.kind=='body' then
   local index=q.all_index or q.cover_index or q.index
   local value=p:read_u16(0x01800000+index*16)
   local final=(expand((value>>10)&31)<<16)|(expand((value>>5)&31)<<8)|expand(value&31)


   local current=point_vram:read(q.y*512+q.x)&0x7fff
   local rgbword=p:read_u16(0x01800000+current*16)
   local vrgb=(expand((rgbword>>10)&31)<<16)|(expand((rgbword>>5)&31)<<8)|expand(rgbword&31)
   log('IDLE_VRAM_POINT',string.format('kind=%s source_frame=%d slot=%d id=%d dma_x=%d dma_y=%d predicted=%d source_vram=%d display_vram=%d vram_rgb=%06X actual=%06X source_matches=%d display_matches=%d',
    q.kind,q.frame,q.slot,q.id,q.x,q.y,index,q.source_vram or -1,current,vrgb,actual,q.source_vram==index and 1 or 0,vrgb==actual and 1 or 0))
   log('IDLE_ALL_DRAW_FINAL',string.format('kind=%s source_frame=%d slot=%d id=%d dma_x=%d dma_y=%d index=%d source=%08X command=%04X pc=%08X source_x=%d source_y=%d final=%06X actual=%06X match=%d',
    q.kind,q.frame,q.slot,q.id,q.x,q.y,index,q.all_source or 0,q.all_command or 0,q.all_pc or 0,q.all_sx or -1,q.all_sy or -1,final,actual,final==actual and 1 or 0))
   log('IDLE_SHADOW_COVER',string.format('kind=%s source_frame=%d slot=%d id=%d dma_x=%d dma_y=%d covered=%d cover_slot=%d cover_id=%d cover_source=%08X cover_sx=%d cover_sy=%d cover_pixel=%d cover_command=%04X cover_pc=%08X index=%d final=%06X actual=%06X match=%d',
    q.kind,q.frame,q.slot,q.id,q.x,q.y,q.cover_index and 1 or 0,q.cover_slot or 0,q.cover_id or 0,q.cover_source or 0,q.cover_sx or -1,q.cover_sy or -1,q.cover_pixel or 0,q.cover_command or 0,q.cover_pc or 0,index,final,actual,final==actual and 1 or 0))
  end
  log('IDLE_SCANPOINT',string.format('kind=%s source_frame=%d slot=%d id=%d dma_x=%d dma_y=%d display_x=%d display_y=%d row=%d column=%d effective=%04X dpyadr=%04X control=%04X veb=%d vsb=%d palette_index=%d expected=%06X actual=%06X match=%d',
   q.kind or "body",q.frame,q.slot,q.id,q.x,q.y,xx,yy,row,column,effective,adr,control,veb,vsb,q.index,expected,actual,actual==expected and 1 or 0))

  end -- full footprint bypasses per-pixel logging
  else future_points[#future_points+1]=q end
 end
 if footprint_stats.points>0 and not footprint_stats.reported then
  footprint_stats.reported=true
  log('COMPLETE_FOOTPRINT',string.format('source_age=%d points=%d slot1=%d slot2=%d source_fail=%d display_fail=%d offscreen=%d column=%d row=%d raw_media=none',footprint_stats.source_frame-ready,footprint_stats.points,footprint_stats.slots[1],footprint_stats.slots[2],footprint_stats.source_fail,footprint_stats.display_fail,footprint_stats.offscreen,column,row))
 end
 footprint_stats={points=0,source_fail=0,display_fail=0,offscreen=0,slots={0,0}}

 idle_points=future_points
 shadow_queries={}
 for _,q in ipairs(future_points)do
  if not q.fullbody then
   local key=string.format('%d_%d_%d',q.frame,q.x,q.y)
   shadow_queries[key]=shadow_queries[key]or{}
   shadow_queries[key][#shadow_queries[key]+1]=q
  end
 end
end)

local shadow_tap=p:install_write_tap(0x01a80010,0x01a8001f,'cache-owned native idle shadow output',function(at,data)
 if not ready or (frame-ready)%8~=0 or at~=0x01a80010 or (regs.PC.value~=0xff8015a0 and regs.PC.value~=0xff801610)then return end
 local row=regs.A9.value;local own,slot
 for n=1,2 do
  local a=sample(n);if not a then return end;local cache=p:read_u32(a.actor+0x1a0)
  if valid(cache) and row>=cache and row<cache+12*112 and (row-cache)%112==0 and p:read_u32(row)~=0 then
   assert(not own,'Unique actual cache owner');own=a;slot=n
  end
 end
 assert(own and own.owner==own.actor,'Native owned shadow row')
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local c=data&65535;local source=reg(2)|(reg(3)<<16)
 local x,y,w,h=reg(4)&1023,reg(5)&511,reg(6)&1023,reg(7)&1023
 assert(h==1 and c&15==8,'Original one-row solid nonzero shadow')
 clip_trace('shadow',slot,own.id,source,x,y,w,h,c)
 local count,top,bottom,bits,px,pixel=opaque_bounds(source,w,h,c)
 log('IDLE_SHADOW_DMA',string.format('slot=%d id=%d actor=%08X main=%08X owner=%08X pose=%08X cache_row=%08X graphic=%08X source=%08X command=%04X x=%d y=%d width=%d height=%d opaque=%d pc=%08X scaleX=%d scaleY=%d',
  slot,own.id,own.actor,own.main,own.owner,own.pose,row,p:read_u32(row),source,c,x,y,w,h,count,regs.PC.value,reg(10),reg(11)))

 if count>0 then
  local q={frame=frame,slot=slot,id=own.id,kind='shadow',x=(x+px)&1023,y=(y+bottom)&511,index=(reg(8)&0x7f00)|(reg(9)&255)}
  idle_points[#idle_points+1]=q
  local key=string.format('%d_%d_%d',frame,q.x,q.y)
  shadow_queries[key]=shadow_queries[key]or{};shadow_queries[key][#shadow_queries[key]+1]=q
 end

end)
emu.register_stop(function()assert(shadow_tap,'Retained native shadow observer')end)

local source_row_cache={}
local source_row_frame=-1
local function queried_source_pixel(source,w,h,c,sx,sy)
 local bpp=(c>>12)&7;if bpp==0 then bpp=8 end
 local mapped=source
 if source>=0x10000000 and source<0x1a000000 then mapped=source-0x0a000000
 elseif mapped>=0xf8000000 then mapped=mapped-0xf8000000
 end -- MK2 init uses large-ROM native source addressing
 assert(mapped>=0 and mapped<sole_gfx.size*8,'Actual later source region')
 local function read(bit,n)
  assert(bit+n<=sole_gfx.size*8)
  local at=bit//8;return ((sole_gfx:read_u8(at)|(sole_gfx:read_u8(at+1)<<8))>>(bit%8))&((1<<n)-1)
 end
 local bit=mapped
 local startskip=c&0x40~=0 and (actual_dma[0]&255) or 0
 local endskip=c&0x40~=0 and (actual_dma[0]>>8) or actual_dma[0]
 if sx<startskip or sx>=w-endskip then return nil end
 if c&0x80==0 then return read(bit+(sy*w+sx)*bpp,bpp)end

 if source_row_frame~=frame then source_row_frame=frame;source_row_cache={}end
 local key=string.format('%08X_%d_%d_%04X',mapped,w,h,c)
 local rows=source_row_cache[key]
 if not rows then
  rows={};source_row_cache[key]=rows
  for y=0,h-1 do
   local header=read(bit,8);bit=bit+8
   local pre=(header&15)<<((c>>8)&3);local post=(header>>4)<<((c>>10)&3)
   rows[y]={bit=bit,pre=pre,post=post}
   bit=bit+math.max(0,w-pre-post)*bpp
  end
 end
 local row=assert(rows[sy])
 if sx<row.pre or sx>=w-row.post then return nil end
 return read(row.bit+(sx-row.pre)*bpp,bpp)
end
local all_draw_tap=p:install_write_tap(0x01a80010,0x01a8001f,'all later draws at sparse shadow queries',function(at,data)
 if not ready or at~=0x01a80010 or data&0x8000==0 then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local c=data&65535;local w,h=reg(6)&1023,reg(7)&1023
 local x,y=reg(4)&1023,reg(5)&511;local src=reg(2)|(reg(3)<<16)
 if w==0 or h==0 then return end
 for _,q in ipairs(idle_points)do
  if (q.kind=='shadow' or q.kind=='body') and q.frame==frame then
   local sx=c&16~=0 and ((x-q.x)&1023)or((q.x-x)&1023)
   local sy=c&32~=0 and ((y-q.y)&511)or((q.y-y)&511)
   if sx<w and sy<h and q.x>=actual_dma[16] and q.x<=actual_dma[17] and q.y>=actual_dma[12] and q.y<=actual_dma[13]then
    assert((reg(10)==0 or reg(10)==256)and(reg(11)==0 or reg(11)==256),'Finite queried unit scale')
    local mode=c&15;local pixel=mode==12 and 1 or queried_source_pixel(src,w,h,c,sx,sy)
    if pixel~=nil then
     local index=nil
     if pixel~=0 then
      if mode&8~=0 then index=(reg(8)&0x7f00)|(reg(9)&255)
      elseif mode&2~=0 then index=(reg(8)&0x7f00)|pixel end
     else
      if mode&4~=0 then index=(reg(8)&0x7f00)|(reg(9)&255)
      elseif mode&1~=0 then index=reg(8)&0x7f00 end
     end
     if index then q.all_index=index;q.all_source=src;q.all_command=c;q.all_pc=regs.PC.value;q.all_sx=sx;q.all_sy=sy end
    end
   end
  end
 end
end)
emu.register_stop(function()assert(all_draw_tap)end)

emu.register_frame_done(function()
 for _,q in ipairs(idle_points)do
  if (q.kind=='shadow' or q.kind=='body') and q.frame==frame then q.source_vram=point_vram:read(q.y*512+q.x)&0x7fff end
 end
end)

local contact_health_taps={}
for n,s in ipairs(slots)do
 contact_health_taps[#contact_health_taps+1]=p:install_write_tap(s.hp,s.hp+15,'actual physical contact health',function(at,data,mask)
  if not ready or at~=s.hp then return end
  log('CONTACT_HEALTH',string.format('slot=%d before=%d after=%d mask=%04X pc=%08X',n,p:read_u16(at),data&65535,mask,regs.PC.value))
 end)
end
emu.register_stop(function()assert(#contact_health_taps==2)end)
local throw_dispatch_taps={}
for _,address in ipairs({0xff8b6e30,0xfffe1140,0xff8b6e80})do
 throw_dispatch_taps[#throw_dispatch_taps+1]=p:install_read_tap(address,address+15,'actual native ground throw dispatch',function(at,data,mask)
  if not ready or at~=address or regs.PC.value~=address+16 then return end
  local a,b=sample(1),sample(2)
  log('THROW_DISPATCH',string.format('entry=%08X pc=%08X op=%04X a0=%08X a1=%08X a8=%08X a9=%08X a10=%08X a13=%08X actor1=%08X main1=%08X id1=%d actor2=%08X main2=%08X id2=%d',
   address,regs.PC.value,data&65535,regs.A0.value,regs.A1.value,regs.A8.value,regs.A9.value,regs.A10.value,regs.A13.value,a.actor,a.main,a.id,b.actor,b.main,b.id))
 end)
end
emu.register_stop(function()assert(#throw_dispatch_taps==3)end)
