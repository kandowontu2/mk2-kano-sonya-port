-- Ordinary human attempt gap63, exact original controller otherwise retained.
dofile('mk2ks_guarded_campaign_close_leg_ram_v3945.lua')
local limit=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_OBSERVER_LIMIT')))
assert(limit==5900,'Declared finite host observation window only')
emu.register_frame_done(function()
 if manager.machine.time:as_double()>=limit then
  print(string.format('MK2_CAMPAIGN_HOST_DEADLINE seconds=%.9f limit=%d assistance=none writes=0',
   manager.machine.time:as_double(),limit))
  manager.machine:exit()
 end
end)
dofile('mk2ks_mileena_campaign_trace_v3848.lua')
