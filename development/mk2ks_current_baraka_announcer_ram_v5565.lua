-- Preserve whole5554 physical/raster/PCM/BPRIO observer. Additional passive
-- dual-dispatcher snapshots and an independent original announcer route tap.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local file=assert(io.open(root..'/mk2ks_current_baraka_priority_ram_v5554.lua','rb'))
local source=file:read('*a');file:close()
assert(load(source,'@unchanged_whole5554_native_observer','t',_ENV))()
source=source:gsub('\r\n','\n')
local function replace(before,after)
 local a,b=source:find(before,1,true)
 assert(a and not source:find(before,b+1,true),'One exact original observer adaptation')
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
replace([[local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local file=assert(io.open(root..'/mk2ks_current_baraka_audio_ram_v5536.lua','rb'))
local source=file:read('*a');file:close()
assert(load(source,'@whole5536_current_native_physical_raster_and_audio','t',_ENV))()
]],'')
replace('MK2_BPRIO_%s','MK2_APRIO_%s')
replace('tap(0xffa12530,function(entry)',[[for _,dispatcher in ipairs({0xffa12530,0xffa12430})do
tap(dispatcher,function(entry)]])
replace([[ local command=cpu.A0.value;local table_at=(0xffa0ef20+((command<<5)&0xffffffff))&0xffffffff
 local header,base=0,0
 if table_at>=0xffa0ef20 and table_at<0xffa10ee0 then]],[[ local command=cpu.A0.value
 local table_base=entry==0xffa12430 and 0xffa10ee0 or 0xffa0ef20
 local table_limit=entry==0xffa12430 and 0xffa11a40 or 0xffa10ee0
 local table_at=(table_base+((command<<5)&0xffffffff))&0xffffffff
 local header,base=0,0
 if table_at>=table_base and table_at<table_limit then]])
replace([[end)
for _,entry in ipairs({0xffa12a10,0xffa12a80,0xffa12b00})do]],[[end)
end
for _,entry in ipairs({0xffa12a10,0xffa12a80,0xffa12b00})do]])
replace("assert(#taps==7,'All seven read-only priority observers retained')",
        "assert(#taps==8,'All eight dual-dispatcher priority observers retained')")
assert(load(source,'@entire5554_dual_native_dispatcher_priority_snapshots','t',_ENV))()

local device=manager.machine.devices[':maincpu']
local p,cpu=device.spaces.program,device.state
local frame,calls=0,0
local route=p:install_read_tap(0xffa12430,0xffa1243f,'independent original announcer route',function(at)
 local start=rawget(_G,'MK2_STOCK_V921_ACTION_START')
 if at~=0xffa12430 or cpu.PC.value~=at+16 or not start or frame<start or frame>start+749 then return end
 calls=calls+1
 print(string.format('MK2_AROUTE_CALL frame=%d seconds=%.12f writes=0 assistance=none entry=%08X a0=%08X a1=%08X a8=%08X a13=%08X return_pc=%08X',
  frame,emu.time(),at,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,p:read_u32(cpu.SP.value)))
end)
emu.register_frame(function()frame=frame+1 end)
emu.register_stop(function()
 print(string.format('MK2_AROUTE_RESULT frame=%d calls=%d writes=0 assistance=none',frame,calls))
 route:remove()
end)
