-- Preserve the exact Jax insertion anchor used by the existing Sub-Zero loader.
-- Disable only Jax's close-guard branch; Ring context11 and readonly observer
-- remain as declared by5652. All original failure bytes stay immutable.
local path='mk2ks_sonya_p2_jax_ring_probe_v5652.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before=[==["once('local replacement=[[\\n','local replacement=[[\\n')"]==]
local after=[==[[=[jax=jax:gsub('other%.roster==11 then','other.roster==11 and false then',1)
once('local replacement=[[\n','local replacement=[[\n'..jax)]=]]==]
local a,b=source:find(before,1,true)
assert(a and not source:find(before,b+1,true),'One exact Jax-only input branch insertion change')
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@'..path..'::keep_SubZero_insertion_anchor_disable_Jax_guard_only','t',_ENV))()
