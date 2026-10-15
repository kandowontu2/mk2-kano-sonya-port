-- Only normal Sub-Zero controls change. All native game bytes remain untouched.
-- Keep the executed4807 controller immutable, including Kitana/Jax/bosses.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local path='mk2ks_sonya_extended_jax_ram_v5203.lua'
local file=assert(io.open(path,'rb'));local text=file:read('a');file:close()
local needle="once('local replacement=[[\\n','local replacement=[[\\n'..jax)\n"
local first,last=text:find(needle,1,true)
assert(first and not text:find(needle,last+1,true),'Exact unique existing Jax input insertion')
local addition=[==[
local subzero,count=kitana:gsub('kt_','sz_')
subzero,count=subzero:gsub('other%.roster==4','other.roster==8')
assert(count==5,'Separate actual CPU Sub-Zero context only')
subzero,count=subzero:gsub('other_now%.roster~=4','other_now.roster~=8')
assert(count==1,'Actual read-only Sub-Zero observer ownership guard')
subzero=subzero:gsub('KITANA_','SUBZERO_')
local before='if other.action==4 or other.action==0xa or other.action==0x10 then sz_guard=frame+40 end'
local after='if other.action==4 or other.action==0xa or other.action==0x10 or other.action==0x604 then sz_guard=frame+40 end'
local a,b=subzero:find(before,1,true)
assert(a and not subzero:find(before,b+1,true),'Exact native visible freeze guard predicate')
subzero=subzero:sub(1,a-1)..after..subzero:sub(b+1)
once([[local jx_pound,jx_jump=-1000,-1000\nlocal rs_last]],
 [[local jx_pound,jx_jump=-1000,-1000\nlocal sz_last,sz_leg,sz_last_leg,sz_upper,sz_guard=nil,nil,-1000,-1000,-1000\nlocal sz_move=nil\nlocal sz_action_taps={}\nlocal rs_last]])
once('local replacement=[[\n','local replacement=[[\n'..subzero)
]==]
text=text:sub(1,last)..addition..text:sub(last+1)
assert(load(text,'@'..path..'::SubZero_physical_freeze_guard_and_leg_only_5159','t',_ENV))()

