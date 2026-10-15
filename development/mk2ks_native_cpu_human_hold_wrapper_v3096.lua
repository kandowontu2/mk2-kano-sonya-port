-- Redirect only the physical human driver. Every native observer is unchanged.
-- v3095 changes only ordinary controller buttons after genuine grab recovery.
local original_dofile=dofile
function dofile(path)
    if path=='mk2ks_physical_p2_cpu_continuation_v1997.lua' then
        return original_dofile('mk2ks_physical_p2_cpu_continuation_v3095.lua')
    end
    return original_dofile(path)
end
original_dofile('mk2ks_native_cpu_mobility_boundary_v3025.lua')
dofile=original_dofile
