-- Current full Sonya campaign; change ordinary inputs only against Sub-Zero8.
-- Clone the complete established Ring routine, including its passive observers.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local scorpion='mk2ks_native_paired_stumble_scorpion_guard.lua'
local function read(path)
 local file=assert(io.open(path,'rb'));local text=file:read('a');file:close();return text
end
local source=read(scorpion)
local needle='local range_before="elseif strategy==\'guard_punish\' and (other.roster==5 or other.roster==10) then"'
local hook=[====[
local function ring_once(text,before,after)
 local a,b=text:find(before,1,true)
 assert(a and not text:find(before,b+1,true),'Whole original Ring branch, one exact context boundary')
 return text:sub(1,a-1)..after..text:sub(b+1)
end
local ring_begin=assert(replacement:find("   elseif strategy=='guard_punish' and (other.roster==5 or other.roster==10) then",1,true))
local ring_end=assert(replacement:find("\n   elseif strategy==",ring_begin+1,true))
local ranged=replacement:sub(ring_begin,ring_end-1)
ranged=ring_once(ranged,'(other.roster==5 or other.roster==10)','other.roster==8')
ranged=ring_once(ranged,'(target.roster~=5 and target.roster~=10)','target.roster~=8')
ranged=ring_once(ranged,'(target.roster==5 and target.id~=5)','target.id~=8')
replacement=ranged..'\n'..replacement
print('MK2_CURRENT_SUBZERO_RING_PHYSICAL_POLICY player=sonya slot=1 true_cpu=8 original_Ring_routine=whole earlier_inputs=unchanged boss_ending_join=retained writes=0 assistance=none')
]====]
local a,b=source:find(needle,1,true)
assert(a and not source:find(needle,b+1,true),'One late fully assembled physical-policy hook')
source=source:sub(1,a-1)..hook..'\n'..source:sub(a)
local scoped_io=setmetatable({open=function(path,mode)
 if path==scorpion then
  assert(mode=='rb')
  return {read=function(_,format)assert(format=='a');return source end,close=function()return true end}
 end
 return io.open(path,mode)
end},{__index=io})
local environment=setmetatable({io=scoped_io},{__index=_ENV})
assert(load(read('mk2ks_native_paired_stumble_mileena_guard.lua'),
 '@mk2ks_native_paired_stumble_mileena_guard.lua::whole_campaign_only_SubZero_Ring_inputs','t',environment))()
