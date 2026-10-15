-- Retain executed6039 shared-timer readiness counterexample. A native walk
-- leaves8 in main290; only active air callback addresses obstruct clean ground.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_air_throw_roles_v6039.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local before='c.callback==0'
local first,last=source:find(before,1,true);assert(first and not source:find(before,last+1,true))
source=source:sub(1,first-1)..'c.callback~=0xfffff800 and c.callback~=0xff8b7f40'..source:sub(last+1)
assert(load(source,'@'..path..'::native_readiness_timer_v6043','t',_ENV))()
