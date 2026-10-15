-- Small ordinary-input pilot of the explicit root-global observer bridge.
assert(os.getenv("MK2KS_PROJECTILE_OBSERVER_ONLY")=="1")
_G.MK2KS_PROJECTILE_OBSERVER_ARMED=false
dofile("mk2ks_projectile_choreography_probe.lua")
local frame=0
emu.register_frame(function()
    frame=frame+1
    if frame==2600 then
        _G.MK2KS_PROJECTILE_OBSERVER_ARMED=true
        print("MK2_OBSERVER_BRIDGE_ARM frame="..frame.." writes=0")
    end
end)
dofile("mk2ks_join_projectile_probe.lua")
