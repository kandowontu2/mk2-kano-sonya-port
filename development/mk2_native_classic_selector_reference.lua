-- Read the actual original MK2 program, then use unchanged physical UI inputs.
local main=assert(manager.machine.memory.regions[':maincpu'])
local done=false
emu.register_frame_done(function()
    if done then return end;done=true
    for offset=0,0xfffff,4096 do
        local hex={}
        for i=0,4095 do hex[#hex+1]=string.format('%02x',main:read_u8(offset+i))end
        print(string.format('MK2_CLASSIC_STARTUP offset=%d bytes=4096 writes=0 assistance=none hex=%s',offset,table.concat(hex)))
    end
    print('MK2_CLASSIC_STARTUP_COMPLETE writes=0 assistance=none')
end)
local f=assert(io.open('mk2ks_native_anchor_ui_ram.lua','rb'))
local source=f:read('a');f:close()
local before="dofile('mk2ks_native_shang_drain_startup.lua')\n"
local at=assert(source:find(before,1,true))
assert(not source:find(before,at+#before,true),'One private startup observer excluded from original driver')
source=source:sub(1,at-1)..source:sub(at+#before)
assert(load(source,'@mk2ks_native_anchor_ui_ram.lua::original_mk2_physical_reference','t',_ENV))()
