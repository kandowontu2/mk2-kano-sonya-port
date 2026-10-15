-- New physical controller only. Original selection, schedule, bosses and endings remain intact.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')
local path='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local function once(old,new)
 local at=assert(source:find(old,1,true),'Declared original source boundary')
 assert(not source:find(old,at+#old,true),'Unique original source boundary')
 source=source:sub(1,at-1)..new..source:sub(at+#old)
end
once("assert(strategy=='uppercut' or strategy=='jumpkick' or strategy=='reactive' or strategy=='zoning'or strategy=='leg'or strategy=='defensive_leg'or strategy=='lowkick'or strategy=='throw')",
 "assert(strategy=='uppercut' or strategy=='jumpkick' or strategy=='reactive' or strategy=='zoning'or strategy=='leg'or strategy=='defensive_leg'or strategy=='lowkick'or strategy=='throw'or strategy=='guard_punish')")
once("local guard_until=-1000", "local guard_until=-1000\nlocal gp_last,gp_leg,gp_last_leg,gp_upper,gp_guard=nil,nil,-1000,-1000,-1000\nlocal gp_move=nil\nlocal gp_action_taps={}\nlocal rs_last,rs_ring,rs_dir,rs_jumpdir=nil,nil,nil,nil\nlocal rs_jump=-1000\nlocal rs_taps={}")
once("(strategy=='zoning' or leg_tactic) and (other.roster==12 or other.roster==13)",
 "(strategy=='zoning' or strategy=='guard_punish' or leg_tactic) and (other.roster==12 or other.roster==13)")
local original="   elseif strategy=='zoning' then\n"
local replacement=[[
   elseif strategy=='guard_punish' and other.roster==5 then
    -- Ordinary D,F,LP Ring edges; back-jump before the previous throw range.
    -- All state reads/taps are observers. Neither action303 nor507 is safe.
    local reset=not rs_last or frame-rs_last~=1
    if reset then rs_ring=nil;rs_dir=nil;rs_jump=-1000;rs_jumpdir=nil end
    rs_last=frame
    for _,n in ipairs({side,opponent})do
     local observed=sample(n);local observed_main=observed.main
     if not rs_taps[observed_main] then
      local observed_side=n
      rs_taps[observed_main]=p:install_write_tap(observed_main+0x1f0,observed_main+0x1ff,'read-only actual ranged combat native action stores',function(at,data,mask)
       if at~=observed_main+0x1f0 or mask~=0xffff or p:read_u32(slots[observed_side].main)~=observed_main or
        p:read_u16(slots[side].state)~=1 or p:read_u16(slots[opponent].state)~=0 then return end
       local own,target=sample(side),sample(opponent);local actor=sample(observed_side)
       if not own or not target or not actor or own.id~=18 or own.roster~=18 or target.id~=5 or target.roster~=5 or
        own.owner~=own.actor or target.owner~=target.actor or own.hp<=0 or target.hp<=0 or
        cpu.A8.value~=actor.actor or cpu.A13.value~=actor.main then return end
       log(observed_side==side and'RANGE_ACTION'or'RANGE_CPU_ACTION',string.format('stage=%d actor=%08X main=%08X owner=%08X id=%d roster=%d at=%08X before=%d after=%d mask=%04X pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X health=%d,%d',
        p:read_u16(0x01061b30),actor.actor,actor.main,actor.owner,actor.id,actor.roster,at,p:read_u16(at),data&0xffff,mask,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,own.hp,target.hp))
      end)
      taps[#taps+1]=rs_taps[observed_main]
     end
    end
    log('RANGE_FIELD',string.format('stage=%d reset=%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X human_id=%d cpu_id=%d human_roster=%d cpu_roster=%d human_owner=%08X cpu_owner=%08X h_x=%d h_y=%d h_floor=%d c_x=%d c_y=%d c_floor=%d human_action=%d cpu_action=%d flags=%04X body=%04X cpu_flags=%04X cpu_body=%04X health=%d,%d human_pose=%08X cpu_pose=%08X',
     stage,reset and 1 or 0,human.actor,human.main,other.actor,other.main,human.id,other.id,human.roster,other.roster,human.owner,other.owner,
     human.x,human.y,human.floor,other.x,other.y,other.floor,human.action,other.action,human.flags,human.body,other.flags,other.body,human.hp,other.hp,human.pose,other.pose))
    local forward=human.x<other.x and'Right'or'Left'
    local back=forward=='Right'and'Left'or'Right'
    local reason
    if rs_ring and frame-rs_ring<64 then
     reason='ring_sequence';local age=frame-rs_ring
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(rs_dir)end
     if age>=8 and age<12 then press('Low Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif human.floor-human.y>8 then
     reason='actual_air_kick'
     if rs_jumpdir and frame-rs_jump<48 then press(rs_jumpdir)end
     if frame%6<3 then press('High Kick')end
    elseif gap<150 then
     rs_ring=nil
     if frame-rs_jump>=40 then
      reason='back_jump_attempt';rs_jump=frame;rs_jumpdir=back;press('Up');press(back)
     elseif frame-rs_jump<4 then reason='back_jump_edge';press('Up');press(rs_jumpdir)
     else reason='grounded_guard';press('Down');press('Block')end
    else
     reason='ring_attempt';rs_ring=frame;rs_dir=forward
    end
    log('RANGE_DECISION',string.format('reason=%s ring_start=%d ring_dir=%s jump_start=%d jump_dir=%s scope=physical_input_not_assumed_activation',
     reason,rs_ring or-1,rs_dir or'none',rs_jump,rs_jumpdir or'none'))
   elseif strategy=='guard_punish' and other.roster==18 then
    local forward=human.x<other.x and'Right'or'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    local reset=not gp_last or frame-gp_last~=1
    if reset then gp_leg=nil;gp_move=nil;gp_last_leg=-1000;gp_upper=-1000;gp_guard=-1000 end
    gp_last=frame
    if not gp_action_taps[human.main] then
     local observed_main=human.main
     gp_action_taps[observed_main]=p:install_write_tap(observed_main+0x1f0,observed_main+0x1ff,'read-only guarded physical human action stores',function(at,data,mask)
      if at~=observed_main+0x1f0 or mask~=0xffff or p:read_u32(slots[side].main)~=observed_main or
       p:read_u16(slots[side].state)~=1 or p:read_u16(slots[opponent].state)~=0 then return end
      local own,other_now=sample(side),sample(opponent)
      if not own or not other_now or own.id~=18 or own.roster~=18 or own.owner~=own.actor or own.hp<=0 or
       (other_now.roster~=5 and other_now.roster~=10 and other_now.roster~=18) or
       cpu.A8.value~=own.actor or cpu.A13.value~=own.main then return end
      log('GUARD_ACTION',string.format('actor=%08X main=%08X owner=%08X id=%d roster=%d at=%08X before=%d after=%d mask=%04X pc=%08X a1=%08X a8=%08X a13=%08X health=%d,%d',
       own.actor,own.main,own.owner,own.id,own.roster,at,p:read_u16(at),data&0xffff,mask,cpu.PC.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,own.hp,other_now.hp))
     end)
     taps[#taps+1]=gp_action_taps[observed_main]
    end
    -- Original block handlers use actions700/701 and body bit08. Release Block
    -- during the initial three Down fields before a genuine LP+Block leg edge.
    local blocking=human.action==0x700 or human.action==0x701
    local ready=height<=8 and (blocking or human.action==0 or human.action==0x303 or human.action==0x302 or human.action==0x304 or human.action==0x107)
      and human.flags&(other.roster==18 and 0x18 or 0x1c)==0 and (blocking or human.body&0x0c==0)
    local safe=other.action==0 or other.action==0x303 or other.action==0x302 or other.action==0x304 or other.action==0x107
      or (other.action>=0x600 and other.action<=0x60f)
    if other.action==4 or other.action==0xa or other.action==0x10 then gp_guard=frame+40 end
    log('GUARD_FIELD',string.format('stage=%d reset=%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X human_id=%d cpu_id=%d human_roster=%d cpu_roster=%d human_owner=%08X cpu_owner=%08X h_x=%d h_y=%d h_floor=%d c_x=%d c_y=%d c_floor=%d human_action=%d cpu_action=%d flags=%04X body=%04X cpu_flags=%04X cpu_body=%04X health=%d,%d human_pose=%08X cpu_pose=%08X',
      stage,reset and 1 or 0,human.actor,human.main,other.actor,other.main,human.id,other.id,human.roster,other.roster,human.owner,other.owner,
      human.x,human.y,human.floor,other.x,other.y,other.floor,human.action,other.action,human.flags,human.body,other.flags,other.body,human.hp,other.hp,human.pose,other.pose))
    local reason
    if gp_leg and frame-gp_leg<12 then
     reason=gp_move..'_sequence';local age=frame-gp_leg
     if gp_move=='leg' then
      if age<7 then press('Down')end
      if age>=3 and age<7 then press('Low Punch');press('Block')end
     else
      -- Same Down9/HP6..8 physical command as the proven clean HUMAN107 test.
      if age<9 then press('Down')end
      if age>=6 and age<9 then press('High Punch')end
     end
    elseif height>8 then
     reason='actual_air_recovery';press('Block')
     if gap<105 and frame%6<3 then press('High Kick')end
    elseif cpu_height>15 and gap<100 then
     reason='anti_air_guard';press('Down')
     if ready and gap<78 and frame-gp_upper>=26 then
      reason='anti_air_attempt';press('High Punch');gp_upper=frame
     else press('Block')end
    elseif frame<gp_guard then
     reason='projectile_guard';press('Down');press('Block')
    elseif not safe and gap<125 then
     reason='active_guard';press('Down');press('Block')
    elseif ready and safe and gap<(other.roster==18 and 85 or 63) and frame-gp_last_leg>=32 then
     gp_move=other.roster==18 and'leg'or'uppercut'
     reason=gp_move..'_attempt';gp_leg=frame;gp_last_leg=frame;press('Down')
    elseif ready and safe and gap>(other.roster==18 and 75 or 58) and cpu_height<=8 then
     reason='grounded_approach';gp_leg=nil;press(forward)
    else
     reason='stance_guard';press('Down');press('Block')
    end
    log('GUARD_DECISION','reason='..reason..' scope=physical_attempt_not_assumed_activation')
   elseif strategy=='zoning' or strategy=='guard_punish' then
]]
once(original,replacement)
local guest_sink="local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()"
once(guest_sink,'_campaign_guest(raw)')
local adapted,count=source:gsub('screen:snapshot%(', '_campaign_emit(')
assert(count==6,'All original six media sinks retained, no extra files')
local prefix=[[
local function _campaign_guest(raw)
 assert(#raw==1048576)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print(string.format('MK2_CAMPAIGN_GUEST_RAM frame=1 bytes=%d hex=%s',#raw,hex))
end
local function _campaign_emit(name)
 local s=manager.machine.screens[':screen'];local raw,width,height=s:pixels()
 assert(width==400 and height==254 and #raw==width*height*4)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=%s seconds=%.9f width=%d height=%d bytes=%d hex=%s',
  name,manager.machine.time:as_double(),width,height,#raw,hex))
end
]]
assert(load(prefix..adapted,'@'..path..'::mileena_ring_spacing_inputs_and_RAM_sinks','t',_ENV))()
local limit=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_OBSERVER_LIMIT')))
assert(limit==1500,'Finite host-only observation; no victory supplied')
emu.register_frame_done(function()
 if manager.machine.time:as_double()>=limit then
  print(string.format('MK2_CAMPAIGN_HOST_DEADLINE seconds=%.9f limit=%d assistance=none writes=0',manager.machine.time:as_double(),limit))
  manager.machine:exit()
 end
end)
dofile('mk2ks_mileena_campaign_trace_v3848.lua')
