-- Entire genuine-input1166 controller, omitting only its one PNG output call.
-- Small native palette records and one diagnostic guest dump remain intact.
local f=assert(io.open('mk2ks_natural_mirror_finish_v1166.lua','rb'))
local source=f:read('*a');f:close()
local before="for _,file in ipairs(pending)do screen:snapshot(file);log('SNAPSHOT','file='..file)end"
local first,last=assert(source:find(before,1,true))
assert(not source:find(before,last+1,true))
source=source:sub(1,first-1).."for _,file in ipairs(pending)do log('OMITTED_SNAPSHOT','file='..file)end"..source:sub(last+1)
assert(load(source,'@whole1166physical_controller_only_PNG_sink_omitted'))()
