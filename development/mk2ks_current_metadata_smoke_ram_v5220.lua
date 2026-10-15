-- Read-only finite startup/early-play observer; physical policy is unchanged.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local path=assert(({kano='mk2ks_current_kano_p1_campaign_ram_v5194.lua',
 sonya='mk2ks_sonya_extended_tested_ram_v5206.lua'})[fighter])
dofile(path)
local observed=0
emu.register_frame_done(function()
 observed=observed+1
 if observed==6000 then
  print('MK2_METADATA_SMOKE_STOP observed_fields=6000 writes=0 assistance=none')
  manager.machine:exit()
 end
end)
