-- Exact original921 physical controller/retained state taps; no raster files.
local file=assert(io.open('mk2ks_stock_head_victim_v921.lua','rb'))
local source=file:read('a');file:close()
local count
source,count=source:gsub('screen:snapshot%(', 'MK2KS_STOCK_RAM_DRIVER_SNAPSHOT(')
assert(count==1,'Exactly one old periodic diagnostic image sink')
function MK2KS_STOCK_RAM_DRIVER_SNAPSHOT(file)
 -- The full native scene observer owns continuous RGB transport. Preserve
 -- original command/state timing; omit only this redundant PNG write.
 print('MK2_STOCK_RAM_DRIVER_SNAPSHOT_SKIPPED file='..file..' writes=0 assistance=none')
end
assert(not source:find('screen:snapshot',1,true))
assert(load(source,'@mk2ks_stock_head_victim_v921_RAM_image_sink','t',_ENV))()
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 local action=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if action and frame>=action+750 or frame>=7000 then
  print(string.format('MK2_STOCK_RAM_HOST_EXIT frame=%d action=%d writes=0 assistance=none',frame,action or-1))
  manager.machine:exit()
 end
end)
