-- Retain the original causal observer and controller; add exact finish lookup taps.
local f=assert(io.open('mk2ks_native_cpu_kano_cache_cause.lua','rb'))
local source=f:read('a');f:close()
local function once(before,after)
 local a,b=source:find(before,1,true)
 assert(a and not source:find(before,b+1,true),'One source-bound passive tracing boundary')
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
once('local ring_size=1800','local ring_size=6000')
once('frame<35000','frame<36000')
once("{0xff83c870,'animation_loop'}","{0xff876b40,'fatality1_dispatch'},{0xff876b80,'fatality2_dispatch'},\n {0xff83b7f0,'id_lookup'},{0xff83b850,'id_lookup_result'},\n {0xff8d2410,'wrong_Mileena_finish_entry'},{0xff83c870,'animation_loop'}")
once("assert(#taps==10,'All exact passive native taps retained')",
 "assert(#taps==15,'All exact passive native taps retained')")
assert(load(source,'@mk2ks_native_cpu_kano_cache_cause.lua::additional_finish_lookup_taps','t',_ENV))()
