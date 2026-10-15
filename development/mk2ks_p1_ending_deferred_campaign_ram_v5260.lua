-- Exact accepted P1 buttons; one strictly read-only complete ending observer.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
if fighter=='kano'then
 dofile('mk2ks_current_kano_p1_campaign_ram_v5194.lua')
elseif fighter=='sonya'then
 dofile('mk2ks_sonya_extended_tested_ram_v5206.lua')
else error('Only true Kano/Sonya P1 ending contexts')end
dofile('mk2ks_p1_ending_deferred_io_ram_v5259.lua')
