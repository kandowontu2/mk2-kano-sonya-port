-- Unchanged genuine physical driver plus retained native grammar taps.
dofile('mk2ks_native_split_trace_v1098.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local gfx=manager.machine.memory.regions[':gfxrom']
local output=assert(os.getenv('MK2KS_REPTILE_AUDIT_DIR'))
local frame=0
emu.register_frame(function()
 frame=frame+1
 if frame~=1 then return end
 assert(p:read_u32(0xff61c000)==0x3150534b,'Owned KSP1 split header loaded')
 local first=p:read_u32(0xff61c040)
 local second=p:read_u32(0xff61c080)
 assert(first>0 and first<=0xe000 and second>0 and second<=0x4000)
 local bytes={}
 for at=0,first+second-1 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1f60000+at))end
 local file=assert(io.open(output..'/native_split_gfx.bin','wb'))
 file:write(table.concat(bytes));file:close()
 print(string.format('MK2_SPLIT_DISPLAY_V1111_BOOT frame=%d gfx_bytes=%d writes=0 assistance=none',frame,first+second))
end)
