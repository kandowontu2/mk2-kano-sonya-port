-- Read-only contact capture. Reused harness drives inputs and round health;
-- this observer does not align actors, change palettes or force actions.
dofile("mk2ks_finish_state_trace.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local side=tonumber(os.getenv("MK2_TRACE_NATIVE_FINISH_SIDE") or "1")
local own_ptr=side==1 and 0x01060220 or 0x01060df0
local victim_ptr=side==1 and 0x01060df0 or 0x01060220
local poses={0xfe9b2d10,0xfe9b2db0,0xfe9b2e50,0xfe9b2ef0,0xfe9b2f70,0xfe9b2fb0}
local frame,seen,captured,pending=0,{},0,{}
local skeleton_checks,skeleton_errors=0,0
local function signed(v) return v>=0x8000 and v-0x10000 or v end
emu.register_frame(function()
    frame=frame+1
    local own,victim=p:read_u32(own_ptr),p:read_u32(victim_ptr)
    if own<0x01000000 or own>=0x01100000 or victim<0x01000000 or victim>=0x01100000 then return end
    if p:read_u16(own+0x1f0)~=17 or p:read_u16(victim+0x1f0)~=18 then return end
    local pose=p:read_u32(victim+0x1d0)
    local own_pose=p:read_u32(own+0x1d0)
    if own_pose>=0xfe9b26d0 and own_pose<=0xfe9b2810 then
        local process=p:read_u32(side==1 and 0x01060260 or 0x01060e30)
        local child=process>=0x01000000 and process<0x01100000 and p:read_u32(process+0x190) or 0
        if child>=0x01000000 and child<0x01100000 then
            local own_flip=p:read_u16(own+0xf0)&0x10
            local child_flip=p:read_u16(child+0xf0)&0x10
            skeleton_checks=skeleton_checks+1
            if own_flip~=child_flip or p:read_u16(own+0x90)~=p:read_u16(child+0x90) or
               p:read_u16(own+0xb0)~=p:read_u16(child+0xb0) then
                skeleton_errors=skeleton_errors+1
                if skeleton_errors<=3 then print(string.format("MK2_CONTACT_FACING_ERROR frame=%d side=%d own_flip=%04X child_flip=%04X",frame,side,own_flip,child_flip)) end
            end
        else skeleton_errors=skeleton_errors+1 end
    end
    for index,expected in ipairs(poses) do
        if pose==expected and not seen[index] then
            seen[index]=frame
            pending[frame+3]=index
            print(string.format("MK2_CONTACT_PHASE frame=%d side=%d phase=%d own=%08X victim=%08X x=%d,%d y=%d,%d flags=%04X,%04X",
                frame,side,index-1,p:read_u32(own+0x1d0),pose,
                signed(p:read_u16(own+0x90)),signed(p:read_u16(victim+0x90)),
                signed(p:read_u16(own+0xb0)),signed(p:read_u16(victim+0xb0)),
                p:read_u16(own+0x160),p:read_u16(victim+0x160)))
        end
    end
    if pending[frame] then
        local index=pending[frame]
        if pose~=poses[index] then error("Contact pose did not survive the render delay") end
        manager.machine.screens[":screen"]:snapshot(string.format("port_contact_side%d_phase_%02d.png",side,index-1))
        captured=captured+1
        pending[frame]=nil
    end
end)
emu.register_stop(function()
    print(string.format("MK2_CONTACT_CAPTURE_RESULT complete=%s snapshots=%d fidelity_verified=false",tostring(captured==6),captured))
    print(string.format("MK2_CONTACT_FACING_RESULT pass=%s checks=%d errors=%d",
        tostring(skeleton_checks>=100 and skeleton_errors==0),skeleton_checks,skeleton_errors))
end)
