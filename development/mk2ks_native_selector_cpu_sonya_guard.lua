-- Whole actual live native shadow/drawing observer, both real Sonya actors.
local file=assert(io.open('mk2ks_native_selector_cpu_guard_shadow.lua','rb'))
local source=file:read('*a'):gsub('\r\n','\n');file:close()
local function once(before,after)
 local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
 source=source:sub(1,at-1)..after..source:sub(at+#before)
end
once('mk2ks_native_selector_cpu_blade_knife.lua','mk2ks_native_selector_cpu_sonya_base.lua')
once('a.id==17 and b.id==17 and','a.id==18 and b.id==18 and')
once('a.roster==17 and b.roster==17 and','a.roster==18 and b.roster==18 and')
once('own.id~=17 or own.roster~=17','own.id~=18 or own.roster~=18')
once("{{'knife',0xffffb000},{'ball',0xffffde00},\n                     {'blade',0xfff8cc00},{'choke',0xfff91400}}",
     "{{'ring',0xffffb400},{'square',0xffffca00},\n                     {'bicycle',0xfff9a400},{'leg',0xfff80800}}")
once('local entry_observer=[[',[[
change('a.id==17 and b.id==17 and a.roster==17 and b.roster==17',
       'a.id==18 and b.id==18 and a.roster==18 and b.roster==18')
local entry_observer=[[
]])
assert(load(source,'@whole_current_Sonya_live_body_shadow_entries','t',_G))()
