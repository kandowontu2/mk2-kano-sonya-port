-- Passive native render-list observation. Existing physical UI inputs unchanged.
local f=assert(io.open('mk2ks_native_anchor_ui_ram.lua','rb'))
local source=f:read('a');f:close()
local before='    local raw,w,h=screen:pixels()'
local after=[=[    local ptr=program:read_u32(0x0105d480)
    local seen,n={},0
    while ptr~=0 do
        assert(ptr>=0x01000000 and ptr<0x01100000 and not seen[ptr] and n<240)
        seen[ptr]=true;n=n+1
        print(string.format('MK2_ANCHOR_UI_DEPTH seq=%d label=%s frame=%d order=%d actor=%08X z=%08X x=%04X y=%04X descriptor=%08X id=%04X next=%08X writes=0 assistance=none',
            snapshots,label,frame,n,ptr,program:read_u32(ptr+0xc0),program:read_u16(ptr+0x90),
            program:read_u16(ptr+0xb0),program:read_u32(ptr+0x1a0),program:read_u16(ptr+0x1f0),program:read_u32(ptr)))
        ptr=program:read_u32(ptr)
    end
    local raw,w,h=screen:pixels()]=]
local at=assert(source:find(before,1,true))
assert(not source:find(before,at+#before,true))
source=source:sub(1,at-1)..after..source:sub(at+#before)
assert(load(source,'@mk2ks_native_anchor_ui_ram.lua::passive_native_sorted_list','t',_ENV))()
