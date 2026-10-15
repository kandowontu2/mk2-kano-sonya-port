-- Whole original physical policy; isolate its text from enclosing Lua strings.
local path='mk2ks_native_paired_stumble_subzero_retreat_retry.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local function once(before,after)
 local a,b=source:find(before,1,true)
 assert(a and not source:find(before,b+1,true),'One exact original nested delimiter boundary')
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
once('local physical=[==[','local physical=[=================[')
once('\n]==]\nranged=','\n]=================]\nranged=')
assert(load(source,'@'..path..'::whole_early_retreat_inputs_with_isolated_text_delimiter','t',_ENV))()
