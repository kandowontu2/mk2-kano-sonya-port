-- Current Sonya P2. Existing physical policy unchanged; only loader slot
-- preconditions and the independent Jax read-only observer's slot addresses swap.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya')
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')
local originals={
 ['mk2ks_sonya_extended_tested_ram_v5206.lua']=true,
 ['mk2ks_sonya_extended_prime_ram_v5205.lua']=true,
 ['mk2ks_sonya_extended_subzero_ram_v5204.lua']=true,
 ['mk2ks_sonya_extended_jax_ram_v5203.lua']=true,
 ['mk2ks_sonya_extended_kitana_ram_v5202.lua']=true,
 ['mk2ks_sonya_extended_guard_base_ram_v5201.lua']=true,
 ['mk2ks_natural_campaign_shao_ring_retreat_v3485.lua']=true}
local loaded={}
local function once(source,before,after)
 local a,b=source:find(before,1,true)
 assert(a and not source:find(before,b+1,true),'Unique declared slot-only source boundary')
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local function read_source(path)
 assert(originals[path] and not loaded[path],'Exact immutable transitive source, loaded once')
 loaded[path]=true
 local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
 if path:find('mk2ks_sonya_extended_',1,true) and
  path~='mk2ks_sonya_extended_guard_base_ram_v5201.lua' then
  source=once(source,"assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')",
   "assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')")
 end
 if path=='mk2ks_sonya_extended_kitana_ram_v5202.lua' then
  source=once(source,
   '"assert(os.getenv(\'MK2KS_TEST_FIGHTER\')==\'sonya\' and os.getenv(\'MK2KS_CAMPAIGN_SIDE\')==\'1\')")',
   '"assert(os.getenv(\'MK2KS_TEST_FIGHTER\')==\'sonya\' and os.getenv(\'MK2KS_CAMPAIGN_SIDE\')==\'2\')")')
 end
 if path=='mk2ks_sonya_extended_jax_ram_v5203.lua' then
  local first=assert(source:find('-- Independent native callbacks;',1,true))
  local prefix=source:sub(1,first-1);local observer=source:sub(first)
  observer=once(observer,'local h,hm=actor(1);local c,cm=actor(2)',
   'local h,hm=actor(2);local c,cm=actor(1)')
  observer=once(observer,'human_slot=1 fighter=sonya','human_slot=2 fighter=sonya')
  local opposite={['010601f0']='01060dc0',['01060dc0']='010601f0',
   ['01060280']='01060e50',['01060e50']='01060280',
   ['010602f0']='01060ec0',['01060ec0']='010602f0'}
  local replacements=0
  observer=observer:gsub('0x(%x%x%x%x%x%x%x%x)',function(address)
   if opposite[address] then replacements=replacements+1;return '0x'..opposite[address] end
   return '0x'..address
  end)
  assert(replacements==8,'Exactly eight read-only Jax state/roster/health addresses')
  source=prefix..observer
 end
 print('MK2_CAMPAIGN_P2_SOURCE path='..path..' bytes='..#source..' slot=2 writes=0 assistance=none')
 return source
end
-- This local I/O facade supplies only existing source text to the unchanged
-- nested loaders. It cannot open media sinks or alter game/controller state.
local scoped_io=setmetatable({open=function(path,mode)
 assert(mode=='r' or mode=='rb','Read-only declared source loader')
 local source=read_source(path)
 return {read=function(_,format)assert(format=='a' or format=='*a');return source end,
  close=function()return true end}
end},{__index=io})
local environment=setmetatable({io=scoped_io},{__index=_ENV})
local path='mk2ks_sonya_extended_tested_ram_v5206.lua'
assert(load(read_source(path),'@'..path..'::P2_slot_preconditions_and_Jax_observer_only','t',environment))()
for name in pairs(originals)do assert(loaded[name],'Every declared transitive source actually loaded')end
