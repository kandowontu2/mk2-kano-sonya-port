-- Entire2092 passive native Pit observer, original3624 RAM-only sinks.
-- Only the driver target and disk sinks change; no game/register writes.
local handle=assert(io.open('mk2ks_native_tomb_ram_v3624.lua','rb'))
local source=handle:read('a');handle:close()
local changes={
 {"mk2ks_native_tomb_display_v2062.lua","mk2ks_native_pit_display_v2092.lua",1},
 {"dofile%('mk2ks_stage_branch_provenance_v1722%.lua'%)","dofile%('mk2ks_native_stage_performer_v806%.lua'%)",1},
 {"dofile('mk2ks_current_stage_provenance_v3595.lua')","dofile('mk2ks_current_cross_tomb_provenance_v5834.lua')",1},
}
for _,pair in ipairs(changes)do
 local result,count={},0;local from=1
 while true do
  local first,last=source:find(pair[1],from,true)
  if not first then result[#result+1]=source:sub(from);break end
  result[#result+1]=source:sub(from,first-1);result[#result+1]=pair[2]
  count=count+1;from=last+1
 end
 assert(count==pair[3]);source=table.concat(result)
end
assert(load(source,'@entire2092_native_Pit_3624_RAM_sinks_5904','t',_ENV))()
emu.register_frame_done(function()
 if emu.time()>=890 then
  print('MK2_CURRENT_PIT_RENDER_DEADLINE writes=0 assistance=none')
  manager.machine:exit()
 end
end)
