-- Read-only continuous port contact evidence. No geometric acceptance claim.
dofile("mk2ks_finish_range_test.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local side=tonumber(os.getenv("MK2_TRACE_NATIVE_FINISH_SIDE") or "1")
assert(os.getenv("MK2_TRACE_NATIVE_FINISH")=="sonya")
local frame,start,observed=0,nil,0
local own_ptr=side==1 and 0x01060220 or 0x01060df0
local victim_ptr=side==1 and 0x01060df0 or 0x01060220
local process_ptr=side==1 and 0x01060260 or 0x01060e30
local tap=p:install_read_tap(0xfffab200,0xfffab20f,"Sonya port contact start",function(offset)
    if offset==0xfffab200 and cpu.A8.value==p:read_u32(own_ptr) then start=frame end
end)
local tick_tap=p:install_read_tap(0xfffbed00,0xfffbed0f,"Sonya native world tick",function(offset)
    if offset~=0xfffbed00 or not start or cpu.A8.value~=p:read_u32(own_ptr) then return end
    print(string.format("MK2_SONYA_NATIVE_TICK frame=%d age=%d actor=%08X process=%08X vx=%08X vy=%08X sequence=%08X loop=%d",
        frame,cpu.A6.value+1,cpu.A8.value,cpu.A13.value,cpu.A2.value,cpu.A3.value,cpu.A9.value,cpu.A11.value))
end)
local function valid(v) return v>=0x01000000 and v<0x01100000 end
local function signed(v) return v>=0x8000 and v-0x10000 or v end
local cleanup_tap=p:install_read_tap(0xff83efd0,0xff83efdf,"Sonya projectile contact retirement",function(offset)
    if offset~=0xff83efd0 or not start or cpu.A8.value~=p:read_u32(own_ptr) then return end
    local child=p:read_u32(cpu.A13.value+0x190)
    if not valid(child) or p:read_u16(child+0xc0)~=0x51 then return end
    local victim=p:read_u32(victim_ptr)
    if not valid(victim) then return end
    print(string.format("MK2_SONYA_NATIVE_CONTACT frame=%d age=%d actor=%08X child=%08X x=%d y=%d target_x=%d target_y=%d graphic=%08X flags=%04X",
        frame,cpu.A6.value,cpu.A8.value,child,signed(p:read_u16(child+0x90)),signed(p:read_u16(child+0xb0)),
        signed(p:read_u16(victim+0x90)),signed(p:read_u16(0x0105ecd0))-88,p:read_u32(child+0x1a0),p:read_u16(child+0xf0)))
end)
emu.register_frame(function()
    frame=frame+1
    assert(tap and tick_tap and cleanup_tap)
    if not start or frame-start<40 or frame-start>180 then return end
    local own,victim,process=p:read_u32(own_ptr),p:read_u32(victim_ptr),p:read_u32(process_ptr)
    if not valid(own) or not valid(victim) or not valid(process) then return end
    local child=p:read_u32(process+0x190)
    local present=valid(child) and p:read_u16(child+0xc0)==0x51
    observed=observed+1
    print(string.format("MK2_SONYA_CONTACT_FRAME frame=%d action_age=%d side=%d child=%08X present=%s owner_x=%d owner_y=%d victim_x=%d victim_y=%d victim_pose=%08X child_x=%d child_y=%d child_graphic=%08X flags=%04X",
        frame,frame-start,side,child,tostring(present),signed(p:read_u16(own+0x90)),signed(p:read_u16(own+0xb0)),
        signed(p:read_u16(victim+0x90)),signed(p:read_u16(victim+0xb0)),p:read_u32(victim+0x1d0),
        present and signed(p:read_u16(child+0x90)) or 0,present and signed(p:read_u16(child+0xb0)) or 0,
        present and p:read_u32(child+0x1a0) or 0,present and p:read_u16(child+0xf0) or 0))
    if (frame-start)%3==0 or frame-start==115 or frame-start==116 then
        manager.machine.screens[":screen"]:snapshot(string.format("port_sonya_contact_side%d_%03d.png",side,frame-start))
    end
end)
emu.register_stop(function()
    print(string.format("MK2_SONYA_CONTACT_CAPTURE complete=%s frames=%d fidelity_verified=false",
        tostring(observed==141),observed))
end)
