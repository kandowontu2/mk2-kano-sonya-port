-- Same whole1166 controller and sole PNG omission; explicit read-only source
-- path permits an isolated capture cwd/error.log, never a shared root log.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_natural_mirror_finish_v1166.lua','rb'))
local source=f:read('*a');f:close()
local before="for _,file in ipairs(pending)do screen:snapshot(file);log('SNAPSHOT','file='..file)end"
local first,last=assert(source:find(before,1,true))
assert(not source:find(before,last+1,true))
source=source:sub(1,first-1).."for _,file in ipairs(pending)do log('OMITTED_SNAPSHOT','file='..file)end"..source:sub(last+1)
assert(load(source,'@whole1166physical_controller_only_PNG_sink_omitted'))()
