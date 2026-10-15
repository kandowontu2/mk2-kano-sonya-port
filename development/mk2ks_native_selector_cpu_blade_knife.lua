-- Current cold windows and original physical CPU blade/knife trajectory.
-- Allocation, guard, motion and shadow observers are passive; no second driver.
dofile('mk2ks_native_shang_drain_startup.lua')
local function read(name)
 local file=assert(io.open(name,'rb'));local source=file:read('*a'):gsub('\r\n','\n');file:close();return source
end
local source=read('mk2ks_current_cpu_blade_knife_shadow_v6312.lua')
local before="dofile('mk2ks_current_kano_cpu_extended_ram_v6290.lua')"
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1).."dofile('mk2ks_current_cpu_blade_allocation_v6340.lua')"..source:sub(at+#before)
assert(load(source,'@whole_CPU_shadow_plus_whole_allocation','t',_G))()
local done=false
emu.register_frame(function()
 if done then return end;done=true
 local gfx=assert(manager.machine.memory.regions[':gfxrom']);local bytes={}
 for _,span in ipairs({{0x1fa0000,11944},{0x1fa4000,7032}})do
  for i=0,span[2]-1 do bytes[#bytes+1]=string.format('%02X',gfx:read_u8(span[1]+i))end
 end
 assert(#bytes==18976)
 print('MK2_HPHASE_GFX frame=1 bytes=18976 hex='..table.concat(bytes))
end)
local channels=read('mk2ks_native_kano_laser_special_shadow.lua')
local marker='-- Passive current nineteen-channel/private-finisher-pool observer only.'
local start=assert(channels:find(marker,1,true));assert(not channels:find(marker,start+1,true))
assert(load(channels:sub(start),'@whole_current_passive_nineteen_channels','t',_G))()
