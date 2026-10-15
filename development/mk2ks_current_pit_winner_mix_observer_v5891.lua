-- Entire5779 passive source DAC/ROM/PCM/precise14channel observer; Pit origin.
local f=assert(io.open('mk2ks_current_tomb_winner_mix_observer_v5779.lua','rb'))
local source=f:read('a');f:close()
local function replace(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
replace("0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'",
 "0xff8bdde0,0xff8bddef,'actual native Pit audio origin'")
replace('at~=0xff8bdfe0','at~=0xff8bdde0')
assert(not source:find(':write_',1,true)and not source:find('set_value',1,true))
assert(load(source,'@entire5779_native_Pit_origin_5891','t',_ENV))()
