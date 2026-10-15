-- Same whole ordinary driver/observer, but attack after actual crouch settling.
-- Preserve initial four-frame button attempts which produced no crouched attack.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_basic_ground_separator_v6001.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local before="assert(load(source,'@'..path..'::explicit_driver_separator_v6001','t',_ENV))()"
local after=[=[
replace_once("basic_button('Down',age,780,24);basic_button('Low Punch',age,784,3)",
 "basic_button('Down',age,780,24);basic_button('Low Punch',age,792,6)")
replace_once("basic_button('Down',age,840,24);basic_button('Low Kick',age,844,3)",
 "basic_button('Down',age,840,24);basic_button('Low Kick',age,852,6)")
replace_once("basic_button('Down',age,900,16);basic_button('High Punch',age,904,3)",
 "basic_button('Down',age,900,24);basic_button('High Punch',age,912,6)")
assert(load(source,'@'..path..'::settled_crouch_controls_v6007','t',_ENV))()
]=]
local index=assert(source:find(before,1,true));assert(not source:find(before,index+1,true))
source=source:sub(1,index-1)..after..source:sub(index+#before)
assert(load(source,'@'..path..'::whole_settled_crouch_wrapper_v6007','t',_ENV))()
