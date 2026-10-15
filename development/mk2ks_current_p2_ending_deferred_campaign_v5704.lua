-- Exact qualified cold P2 campaigns plus one complete RAM-only observer.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')
if fighter=='kano'then
 dofile('mk2ks_kano_current_p2_campaign_ram_v4472.lua')
elseif fighter=='sonya'then
 dofile('mk2ks_sonya_p2_verified_subzero_campaign_v5687.lua')
else error('Only true Kano/Sonya P2 ending contexts')end
dofile('mk2ks_current_p2_ending_deferred_io_v5703.lua')
