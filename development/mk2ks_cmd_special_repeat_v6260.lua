-- Test-only configuration routing: the production CMD deliberately clears MK2KS_.
-- Execute the entire previously qualified physical controller unchanged.
local original_getenv=os.getenv
os.getenv=function(key)
 local suffix=key:match('^MK2KS_HUMAN_SPECIAL_(.+)$')
 if suffix then return original_getenv('MK2PORT_ACCEPT_'..suffix)end
 return original_getenv(key)
end
local source=assert(io.open('mk2ks_special_repeat_v5099.lua','rb'))
local text=source:read('*a');source:close()
assert(load(text,'@mk2ks_special_repeat_v5099.lua'))()
