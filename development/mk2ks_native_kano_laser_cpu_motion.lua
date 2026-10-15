-- Normal first-loss Kano continue, then walk/jump/punch/guard and release.
-- No finisher command, guest/state/AI/RNG writes or forced CPU choice.
local file=assert(io.open('mk2ks_native_kano_laser_cpu_continue.lua','r'));local source=file:read('a');file:close()
local original_load=load
local function scoped_load(text,name,mode,environment)
 if name and name:find('::first_loss_ordinary_paid_Kano_continue',1,true)then
  local function once(before,after)
   local a,b=assert(text:find(before,1,true));assert(not text:find(before,b+1,true))
   text=text:sub(1,a-1)..after..text:sub(b+1)
  end
  once("{'High Punch','Left','Right','Down'}","{'High Punch','Left','Right','Down','Up','Block'}")
  once('local loss,css,plan,lastmode,losses=nil,nil,nil,nil,0',
       'local loss,css,plan,lastmode,losses=nil,nil,nil,nil,0\nlocal motion_live=nil')
  once(' if mode==2 and state==1 then loss=nil;css=nil;plan=nil end',[=[
 if mode==2 and state==1 then loss=nil;css=nil;plan=nil end
 local h,k=sample(1),sample(2)
 if mode==2 and state==1 and h and k and h.id==17 and h.roster==17 and k.id==17 and k.roster==17 and
 h.owner==h.actor and k.owner==k.actor and h.hp>0 and k.hp>0 and k.state==0 then
  motion_live=motion_live or f;local age=f-motion_live
  if age>=10 and age<20 then input('Right')end
  if age>=50 and age<54 then input('Up')end
  if age>=80 and age<84 then input('High Punch')end
  if age>=90 and age<180 then input('Block')end
 else motion_live=nil end]=])
 end
 return original_load(text,name,mode,environment or _G)
end
local environment=setmetatable({load=scoped_load},{__index=_G})
assert(original_load(source,'@mk2ks_native_kano_laser_cpu_continue.lua::ordinary_motion_then_released_mirror','t',environment))()
