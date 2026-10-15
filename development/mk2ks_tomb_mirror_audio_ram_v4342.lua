-- All fifteen native audio taps, complete mixed PCM and whole guest RAM-only.
-- The only controller is normal selection, earned KOs and facing commands.
dofile('mk2ks_tomb_mirror_provenance_ram_v4341.lua')
local f=assert(io.open('mk2ks_jax_arms_audio_routes_ram_v4210.lua','rb'))
local source=f:read('a');f:close()
local marker="local device=manager.machine.devices[':maincpu']"
local first,last=assert(source:find(marker,1,true));assert(not source:find(marker,last+1,true))
source=source:sub(first)
local function replace(old,new)
 local a,b=assert(source:find(old,1,true));assert(not source:find(old,b+1,true))
 source=source:sub(1,a-1)..new..source:sub(b+1)
end
replace('frame<=origin+749','frame<=origin+1100')
replace("0xff8be240,0xff8be24f,'actual native Jax arm-rip audio origin'",
 "0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'")
replace('at~=0xff8be240','at~=0xff8bdfe0')
replace('p:read_u16(a+0x1f0)~=11',"p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')])")
replace("'origin=%d a8=%08X a13=%08X id=11',origin,a,m",
 "'origin=%d a8=%08X a13=%08X id=%d',origin,a,m,p:read_u16(a+0x1f0)")
assert(not source:find('dofile',1,true)and not source:find(':write_',1,true)and not source:find('io.open',1,true))
assert(load(source,'@complete4210_generic_audio_true_tomb_mirror_4342','t',_ENV))()
