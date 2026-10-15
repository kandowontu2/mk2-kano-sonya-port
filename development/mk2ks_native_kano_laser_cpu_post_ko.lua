-- Full previous physical/child/channel root; extend observation past real KO.
-- No controller, CPU choice, health, actor, timer, RNG or register writes.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('*a'):gsub('\r\n','\n');f:close();return s
end
local function once(source,before,after)
 local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
 return source:sub(1,at-1)..after..source:sub(at+#before)
end
local native_load=load
_G.load=function(source,name,mode,environment)
 if name=='@isolated_original_body_shadow_CPU_observer_v5328'then
  source=once(source,"if not pair_live(a,b)then log('FAILED','reason=lost_owned_pair_at_field_done');manager.machine:exit();return end",[[if not pair_live(a,b)then
   if p:read_u16(0x010601d0)~=2 or p:read_u16(0x010602f0)==0 or p:read_u16(0x01060ec0)==0 then
    phase_log('ROUND_BOUNDARY','reason=native_noncombat_or_earned_KO');return
   end
   log('FAILED','reason=lost_owned_pair_at_field_done');manager.machine:exit();return
  end]])
 end
 return native_load(source,name,mode,environment)
end
assert(load(read('mk2ks_native_kano_laser_cpu_leg_children.lua'),'@whole_current_cpu_children_root','t',_G))()
_G.load=native_load
local source=read('mk2ks_physical_p2_cpu_round_trace_v1998.lua')
source=once(source,"dofile('mk2ks_physical_p2_cpu_continuation_v1997.lua')",'-- Existing full physical root already loaded; no second controller.')
assert(load(source,'@whole_original_passive_round_observer','t',_G))()

local p=manager.machine.devices[':maincpu'].spaces.program
local frame,started,ko,resumed,terminal=0,nil,nil,nil,false
local function log(tag,reason)
 print(string.format('MK2_POST_KO_%s frame=%d first_live=%d earned_ko=%d resumed=%d mode=%d states=%d,%d ids=%d,%d hp=%d,%d stage=%d schedule=%08X winner=%d reason=%s writes=0 assistance=none',
  tag,frame,started or -1,ko or -1,resumed or -1,p:read_u16(0x010601d0),
  p:read_u16(0x010601f0),p:read_u16(0x01060dc0),p:read_u16(0x01060280),p:read_u16(0x01060e50),
  p:read_u16(0x010602f0),p:read_u16(0x01060ec0),p:read_u16(0x01061b30),p:read_u32(0x01061b10),p:read_u16(0x01061b00),reason))
end
emu.register_frame(function()
 frame=frame+1
 local mode=p:read_u16(0x010601d0)
 local live=mode==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==0 and
  p:read_u16(0x01060280)==18 and p:read_u16(0x01060e50)==18
 if not started and live then started=frame;log('BEGIN','native_first_match')end
 if started and not ko and mode==2 and p:read_u16(0x010602f0)==0 then ko=frame;log('KO','native_health_zero')end
 if ko and not resumed and live and p:read_u16(0x010602f0)==161 and p:read_u16(0x01060ec0)==161 then
  resumed=frame;log('RESUMED','actual_native_full_health_round')
 end
 if resumed and frame>=resumed+60 then terminal=true;log('END','sixty_actual_post_reset_fields');manager.machine:exit()end
 if frame>=5600 and not terminal then terminal=true;log('FAILED','bounded_observation_no_round_resume');manager.machine:exit()end
end)
emu.register_stop(function()log('RESULT',terminal and 'declared_observation_exit'or'other_native_exit')end)
