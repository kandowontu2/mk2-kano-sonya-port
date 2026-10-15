-- Real readiness is native stance/ground/velocity/body/trail/suppression state.
-- Stock Jax also retains his callback address in idle main290. Log the whole
-- field and every actual callback; prove retirement and next-jump reset later.
-- Do not alter native scratch RAM to satisfy a mistaken observer assumption.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_air_throw_roles_v6039.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local before='clean(c)and c.callback==0 and p:read_u16(0x010619d0)==0'
local first,last=source:find(before,1,true);assert(first and not source:find(before,last+1,true))
source=source:sub(1,first-1)..'clean(c)and p:read_u16(0x010619d0)==0'..source:sub(last+1)
assert(load(source,'@'..path..'::native_ready_and_actual_air_dispatch_v6047','t',_ENV))()
