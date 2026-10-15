-- Entire tested Sonya P1 controller unchanged until its earned ending +300.
-- A scoped, read-only source loader inserts only the later normal Kano join.
assert(os.getenv('MK2KS_TEST_FIGHTER')=='sonya' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
local function read(path)
 local f=assert(io.open(path,'rb'));local t=f:read('a');f:close();return t
end
local function one(text,before,after)
 local a,b=text:find(before,1,true)
 assert(a and not text:find(before,b+1,true),'One exact verified source boundary')
 return text:sub(1,a-1)..after..text:sub(b+1)
end
local template=read('mk2ks_native_kano_p2_postending_sonya.lua')
local first=assert(template:find('local helper=[[\n',1,true))+#'local helper=[[\n'
local last=assert(template:find('\n]]\none(',first,true))
local helper=template:sub(first,last-1)
helper=helper:gsub('slots%[1%]','slots[_OTHER_]'):gsub('slots%[2%]','slots[1]'):gsub('slots%[_OTHER_%]','slots[2]')
helper=one(helper,'sample(2),sample(1)','sample(1),sample(2)')
helper=one(helper,'slot=2 target=18','slot=1 target=17')
helper=one(helper,'if row[1]==18 then','if row[1]==17 then')
helper=one(helper,'human.id==18 and human.roster==18','human.id==17 and human.roster==17')
helper=one(helper,' id=18',' id=17')
helper=one(helper,'identity=18 input=','identity=17 input=')
helper=helper:gsub('Sonya','Kano')
local function adapt(source)
 local mark='-- Observe actual own special entries independently of intended button plans.'
 source=one(source,mark,helper..'\n'..mark)
 source=one(source,"if frame>=300 and frame<304 then press('High Punch')end",
  "if ending_completed and frame-ending_completed>=300 then postending_join();return end\n if frame>=300 and frame<304 then press('High Punch')end")
 source=one(source,'if ending_completed and frame-ending_completed>=300 then manager.machine:exit()end',
  '-- The genuine post-ending join owns exit after the original300 attract fields.')
 return source
end
local base_path='mk2ks_sonya_extended_guard_base_ram_v5201.lua'
local original_base=read(base_path)
local patched_base=one(original_base,"local source=file:read('*a');file:close()",
 "local source=file:read('*a');file:close()\nsource=_native_postending_adapt(source)")
local scoped_io=setmetatable({open=function(path,mode)
 if path==base_path then
  assert(mode=='rb')
  return {read=function(_,format)assert(format=='a');return patched_base end,close=function()return true end}
 end
 return io.open(path,mode)
end},{__index=io})
local environment=setmetatable({io=scoped_io,_native_postending_adapt=adapt},{__index=_ENV})
assert(load(read('mk2ks_sonya_extended_tested_ram_v5206.lua'),
 '@mk2ks_sonya_extended_tested_ram_v5206.lua::unchanged_physical_campaign_then_genuine_Kano_join','t',environment))()
