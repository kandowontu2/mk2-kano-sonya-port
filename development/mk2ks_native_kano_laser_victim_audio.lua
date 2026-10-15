-- Same earned trial; only requested opponent selection/identity predicates vary.
local victim=assert(tonumber(os.getenv('MK2KS_LASER_VICTIM')))
assert(victim>=0 and victim<=18 and victim%1==0 and victim~=12 and victim~=13)
local native_load=load
load=function(source,name,mode,environment)
 if name and name:find('::allocation_epoch_successor',1,true)then
  local edits={{'victim.id==18','victim.id=='..victim,1},
   {'n==side and 17 or 18','n==side and 17 or '..victim,2},
   {'victim.id~=18','victim.id~='..victim,1},
   {'victim.roster~=18','victim.roster~='..victim,1}}
  for _,edit in ipairs(edits)do
   local count=0;local start=1
   while true do
    local first,last=source:find(edit[1],start,true);if not first then break end
    source=source:sub(1,first-1)..edit[2]..source:sub(last+1);start=first+#edit[2];count=count+1
   end
   assert(count==edit[3],'Only exact opponent identity/selection constants may change')
  end
 end
 return native_load(source,name,mode,environment)
end
local okay,err=pcall(dofile,'mk2ks_native_kano_laser_audio.lua')
load=native_load
assert(okay,err)
