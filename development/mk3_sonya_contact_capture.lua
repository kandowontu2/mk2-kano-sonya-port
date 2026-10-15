-- Independent original-program trajectory observer, not an input-acceptance verdict.
dofile("mk3_fatality_asset_trace.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local frame,launch,child=0,nil,nil
local taps={}
local function signed(v) return v>=0x8000 and v-0x10000 or v end
for _,address in ipairs({0xff982880,0xff9af630,0xff9af7a0,0xff9af930,0xff9afbb0,0xff9afdc0,0xff9b0100}) do
    taps[#taps+1]=p:install_read_tap(address,address+15,"Sonya original contact program",function(offset)
        if offset~=address then return end
        local owner=p:read_u32(0x010609b0)
        if owner<0x01000000 or owner>=0x01400000 or p:read_u16(owner+0x1f0)~=1 then return end
        if address==0xff9af630 and cpu.A8.value==owner then launch=frame end
        if address==0xff9af7a0 and launch then child=cpu.A10.value end
        if address==0xff982880 and cpu.A8.value~=owner then return end
        if address~=0xff982880 and not launch then return end
        if address==0xff9af930 then return end
        print(string.format("MK3_SONYA_CONTACT_CODE frame=%d at=%08X a8=%08X a11=%08X owner=%08X child=%s",
            frame,address,cpu.A8.value,cpu.A11.value,owner,child and string.format("%08X",child) or "none"))
    end)
end
emu.register_frame(function()
    frame=frame+1
    assert(#taps==7)
    if not launch or not child or frame-launch>80 then return end
    local owner,victim=p:read_u32(0x010609b0),p:read_u32(0x01061560)
    if victim<0x01000000 or victim>=0x01400000 then return end
    print(string.format("MK3_SONYA_CONTACT_FRAME frame=%d launch_age=%d child=%08X x=%d y=%d vx=%08X vy=%08X graphic=%08X victim_x=%d victim_y=%d victim_pose=%08X owner_x=%d owner_y=%d",
        frame,frame-launch,child,signed(p:read_u16(child+0x90)),signed(p:read_u16(child+0xb0)),
        p:read_u32(child+0x40),p:read_u32(child+0x60),p:read_u32(child+0x1a0),
        signed(p:read_u16(victim+0x90)),signed(p:read_u16(victim+0xb0)),p:read_u32(victim+0x1d0),
        signed(p:read_u16(owner+0x90)),signed(p:read_u16(owner+0xb0))))
    if (frame-launch)%3==0 then
        manager.machine.video:snapshot()
        manager.machine.screens[":screen"]:snapshot(string.format("original_sonya_contact_%03d.png",frame-launch))
    end
end)
