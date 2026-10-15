-- All four exact qualified cold physical policies; one passive audio observer.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local side=tonumber(assert(os.getenv('MK2KS_CAMPAIGN_SIDE')))
assert(side==1 or side==2)
if fighter=='kano'then
 if side==1 then dofile('mk2ks_current_kano_p1_campaign_ram_v5194.lua')
 else dofile('mk2ks_kano_current_p2_campaign_ram_v4472.lua')end
elseif fighter=='sonya'then
 if side==1 then dofile('mk2ks_sonya_extended_tested_ram_v5206.lua')
 else dofile('mk2ks_sonya_p2_verified_subzero_campaign_v5687.lua')end
else error('Only true Kano/Sonya cold campaigns')end
dofile('mk2ks_current_ending_audio_observer_v5734.lua')
