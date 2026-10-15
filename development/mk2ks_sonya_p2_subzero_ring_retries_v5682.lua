-- Same actual qualified Ring controls; allow at most3real lost encounters.
-- No stage/health/identity/AI/RNG writes, save state or duplicate long run.
local path='mk2ks_sonya_p2_subzero_ring_probe_v5671.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local marker=']====]\nsource=source:sub(1,a-1)..addition..source:sub(a)'
local a,b=source:find(marker,1,true)
assert(a and not source:find(marker,b+1,true),'One exact existing comparison assembly')
local addition=[======[
outer_once("once('stage==2 and mode==3','stage==7 and mode==3')",
 "once('stage==2 and mode==3','stage==7 and mode==3 and observed_losses>=3')")
outer_once("once('MK2_KITANA_RING_PROBE_BOUNDARY','MK2_SUBZERO_RING_PROBE_BOUNDARY')",
 "once('MK2_KITANA_RING_PROBE_BOUNDARY','MK2_SUBZERO_RING_RETRY_BOUNDARY')")
local inner_site="assert(load(source,'@'..path..'::existing_Ring_spacing_for_Jax11_only','t',_ENV))()"
local ia,ib=source:find(inner_site,1,true)
assert(ia and not source:find(inner_site,ib+1,true),'One actual inner native observer loader')
local observer_adaptation=[===[
once('local frame,seen=0,false\n','local frame,seen=0,false\nlocal observed_losses,last_loss=0,false\n')
local before=" local stage=p:read_u16(0x01061b30);local mode=p:read_u16(0x010601d0)\n"
local after=[==[
 local stage=p:read_u16(0x01061b30);local mode=p:read_u16(0x010601d0)
 local lost=stage==7 and mode==3 and p:read_u16(0x01060dc0)==2 and
  p:read_u16(0x01061b00)==1 and p:read_u32(0x01060df0)==0
 if lost and not last_loss then
  observed_losses=observed_losses+1
  print(string.format('MK2_SUBZERO_RING_RETRY_LOSS frame=%d actual_losses=%d human_slot=2 fighter=sonya writes=0 assistance=none',frame,observed_losses))
 end
 last_loss=lost
 if frame>=52000 then
  print(string.format('MK2_SUBZERO_RING_RETRY_FRAME_LIMIT frame=%d actual_losses=%d accepted=false writes=0 assistance=none',frame,observed_losses))
  manager.machine:exit()
 end
]==]
once(before,after)
]===]
source=source:sub(1,ia-1)..observer_adaptation..source:sub(ia)
]======]
source=source:sub(1,a-1)..addition..source:sub(a)
assert(load(source,'@'..path..'::same_buttons_three_actual_loss_limit','t',_ENV))()
