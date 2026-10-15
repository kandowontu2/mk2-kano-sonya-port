-- Bounded genuine-controller comparison. Only Kitana's physical strategy changes.
-- Original long campaign remains a separate live job; never promote this probe
-- or its observer-triggered exit as a full tower clear.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')
local path='mk2ks_sonya_current_p2_extended_ram_v5627.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local needle=" local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()\n"
local a,b=source:find(needle,1,true)
assert(a and not source:find(needle,b+1,true),'One exact transitive source-read boundary')
local addition=[==[
 if path=='mk2ks_sonya_extended_guard_base_ram_v5201.lua' then
  source=once(source,"strategy=='guard_punish' and (other.roster==5 or other.roster==10)",
   "strategy=='guard_punish' and (other.roster==4 or other.roster==5 or other.roster==10)")
  source=once(source,"(target.roster~=5 and target.roster~=10)",
   "(target.roster~=4 and target.roster~=5 and target.roster~=10)")
  source=once(source,"(target.roster==5 and target.id~=5)",
   "((target.roster==4 and target.id~=4) or (target.roster==5 and target.id~=5))")
 end
 if path=='mk2ks_sonya_extended_kitana_ram_v5202.lua' then
  source=once(source,"once('local replacement=[[\\n','local replacement=[[\\n'..kitana)",
   "once('local replacement=[[\\n','local replacement=[[\\n')")
 end
]==]
source=source:sub(1,b)..addition..source:sub(b+1)
assert(load(source,'@'..path..'::Kitana_existing_ring_spacing_inputs_only','t',_ENV))()
local p=manager.machine.devices[':maincpu'].spaces.program
local frame,seen=0,false
emu.register_frame_done(function()
 frame=frame+1
 local stage=p:read_u16(0x01061b30);local mode=p:read_u16(0x010601d0)
 if stage==2 and mode==2 and p:read_u16(0x01060dc0)==1 and p:read_u16(0x010601f0)==0 and
  p:read_u16(0x01060e50)==18 and p:read_u16(0x01060280)==4 then seen=true end
 if seen and ((stage==3 and mode==2) or
  (stage==2 and mode==3 and p:read_u16(0x01060dc0)==2 and p:read_u16(0x01061b00)==1 and p:read_u32(0x01060df0)==0))then
  print(string.format('MK2_KITANA_RING_PROBE_BOUNDARY frame=%d human_slot=2 fighter=sonya writes=0 assistance=none stage=%d mode=%d winner=%d health=%d,%d scope=completed_encounter_not_tower',
   frame,stage,mode,p:read_u16(0x01061b00),p:read_u16(0x010602f0),p:read_u16(0x01060ec0)))
  manager.machine:exit()
 end
end)
