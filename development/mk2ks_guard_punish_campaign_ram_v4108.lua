-- New physical controller only. Original selection, schedule, bosses and endings remain intact.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')
local path='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local function once(old,new)
 local at=assert(source:find(old,1,true),'Declared original source boundary')
 assert(not source:find(old,at+#old,true),'Unique original source boundary')
 source=source:sub(1,at-1)..new..source:sub(at+#old)
end
once("or strategy=='throw')", "or strategy=='throw'or strategy=='guard_punish')")
once("local guard_until=-1000", "local guard_until=-1000\nlocal gp_last,gp_leg,gp_last_leg,gp_upper,gp_guard=nil,nil,-1000,-1000,-1000")
once("(strategy=='zoning' or leg_tactic) and (other.roster==12 or other.roster==13)",
 "(strategy=='zoning' or strategy=='guard_punish' or leg_tactic) and (other.roster==12 or other.roster==13)")
local original="   elseif strategy=='zoning' then\n"
local replacement=[[
   elseif strategy=='guard_punish' and (other.roster==5 or other.roster==10 or other.roster==18) then
    local forward=human.x<other.x and'Right'or'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    local reset=not gp_last or frame-gp_last~=1
    if reset then gp_leg=nil;gp_last_leg=-1000;gp_upper=-1000;gp_guard=-1000 end
    gp_last=frame
    local ready=height<=8 and (human.action==0 or human.action==0x303 or human.action==0x302 or human.action==0x304 or human.action==0x107)
      and human.flags&0x18==0 and human.body&0x0c==0
    local safe=other.action==0 or other.action==0x303 or other.action==0x302 or other.action==0x304 or other.action==0x107
      or (other.action>=0x600 and other.action<=0x60f)
    if other.action==4 or other.action==0xa or other.action==0x10 then gp_guard=frame+40 end
    log('GUARD_FIELD',string.format('stage=%d reset=%d human_actor=%08X human_main=%08X cpu_actor=%08X cpu_main=%08X human_id=%d cpu_id=%d human_roster=%d cpu_roster=%d human_owner=%08X cpu_owner=%08X h_x=%d h_y=%d h_floor=%d c_x=%d c_y=%d c_floor=%d human_action=%d cpu_action=%d flags=%04X body=%04X cpu_flags=%04X cpu_body=%04X health=%d,%d human_pose=%08X cpu_pose=%08X',
      stage,reset and 1 or 0,human.actor,human.main,other.actor,other.main,human.id,other.id,human.roster,other.roster,human.owner,other.owner,
      human.x,human.y,human.floor,other.x,other.y,other.floor,human.action,other.action,human.flags,human.body,other.flags,other.body,human.hp,other.hp,human.pose,other.pose))
    local reason
    if gp_leg and frame-gp_leg<12 then
     reason='leg_sequence';local age=frame-gp_leg
     if age<7 then press('Down')end
     if age>=3 and age<7 then press('Low Punch');press('Block')end
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
    elseif ready and safe and gap<85 and frame-gp_last_leg>=32 then
     reason='leg_attempt';gp_leg=frame;gp_last_leg=frame;press('Down')
    elseif ready and safe and gap>75 and cpu_height<=8 then
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
assert(load(prefix..adapted,'@'..path..'::guard_punish_inputs_and_RAM_sinks','t',_ENV))()
local limit=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_OBSERVER_LIMIT')))
assert(limit==5900,'Finite host-only observation; no victory supplied')
emu.register_frame_done(function()
 if manager.machine.time:as_double()>=limit then
  print(string.format('MK2_CAMPAIGN_HOST_DEADLINE seconds=%.9f limit=%d assistance=none writes=0',manager.machine.time:as_double(),limit))
  manager.machine:exit()
 end
end)
dofile('mk2ks_mileena_campaign_trace_v3848.lua')
