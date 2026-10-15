-- Whole5993 corrected binding and explicit separator before appended controls.
-- Lua long bracket literals discard their leading newline: retain an explicit
-- newline so the original observer's closing comment cannot consume the driver.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_basic_ground_shadow_v5993.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local function replace_once(before,after)
 local index=assert(source:find(before,1,true));assert(not source:find(before,index+1,true))
 source=source:sub(1,index-1)..after..source:sub(index+#before)
end
replace_once("local index=assert(source:find(before,1,true));assert(not source:find(before,index+1,true))\nsource=source:sub(1,index-1)..after..source:sub(index+#before)",
 [[local index=assert(source:find(before,1,true));local second=assert(source:find(before,index+1,true));assert(not source:find(before,second+1,true))
source=source:sub(1,second-1)..after..source:sub(second+#before)
source=source:sub(1,index-1)..after..source:sub(index+#before)]])
replace_once('source=source..[=[',"source=source..'\\n'..[=[")
assert(load(source,'@'..path..'::explicit_driver_separator_v6001','t',_ENV))()
