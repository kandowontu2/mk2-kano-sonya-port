-- CONTROLLED DIAGNOSTIC ONLY: set the victim's alternate-palette flag once
-- during the finish prompt. This proves branch/palette handling, NOT natural
-- alternate-costume selection. Never used by the normal acceptance matrix.
local p=manager.machine.devices[":maincpu"].spaces.program
local side=tonumber(os.getenv("MK2_TRACE_NATIVE_FINISH_SIDE") or "1")
local identity=assert(tonumber(os.getenv("MK2_TRACE_EXPECT_VICTIM_ID") or "",16))
local frame,applied,errors=0,0,0
emu.register_frame(function()
    frame=frame+1
    if applied~=0 or p:read_u16(0x01061b00)~=3 then return end
    local own=p:read_u32(side==1 and 0x01060220 or 0x01060df0)
    local other=p:read_u32(side==1 and 0x01060df0 or 0x01060220)
    if own<0x01000000 or own>=0x01100000 or other<0x01000000 or other>=0x01100000 then return end
    if p:read_u16(own+0x1f0)~=17 or p:read_u16(other+0x1f0)~=identity then return end
    if p:read_u32(own+0x1d0)==0xfe9b2670 then errors=errors+1 return end
    local flags=p:read_u16(other+0x160)
    p:write_u16(other+0x160,flags|0x40)
    applied=applied+1
    print(string.format("MK2_STOCK_ALT_FLAG_ASSIST frame=%d side=%d id=%04X old=%04X new=%04X",frame,side,identity,flags,flags|0x40))
end)
dofile("mk2ks_native_stock_body_test.lua")
emu.register_stop(function()
    print(string.format("MK2_STOCK_ALT_FIXTURE_RESULT pass=%s applied=%d errors=%d natural_selection_verified=false",tostring(applied==1 and errors==0),applied,errors))
end)
