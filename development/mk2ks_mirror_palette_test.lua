-- Ordinary mirror selections/actions; read-only native palette/identity checks.
local fighter=os.getenv("MK2KS_TEST_FIGHTER")
assert(fighter=="kano" or fighter=="sonya", "Choose a custom mirror fighter")
assert(os.getenv("MK2KS_P2_FIGHTER")==fighter, "Both players must select the same fighter")
assert(os.getenv("MK2KS_TWO_PLAYER")=="1", "Mirror palette test requires two players")
local leg_mode=os.getenv("MK2KS_TEST_LEG") or ""
assert(leg_mode=="" or (fighter=="sonya" and leg_mode=="near"), "Only an optional Sonya mirror grab is supported")
dofile("mk2ks_selector_exit_test.lua")

local frame,hud_frame=0,nil
local program,screen,controls
local checks,errors,alt_fields=0,0,0
local pointers={0x01060220,0x01060df0}
local id=fighter=="kano" and 17 or 18
-- Original MK3 primary/alternate palette table entries, relocated donor area.
local donor=fighter=="kano" and {0xfec95de0,0xfec961f0} or {0xfec96790,0xfec96ba0}
local function require_palette(condition,label)
    checks=checks+1
    if not condition then
        errors=errors+1
        if errors<=12 then print("MK2KS_MIRROR_ERROR "..label) end
    end
end
emu.register_frame(function()
    frame=frame+1
    if not program then
        program=manager.machine.devices[":maincpu"].spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        controls={{high["P1 Up"],high["P1 High Punch"]},{high["P2 Up"],high["P2 High Punch"]}}
    end
    if not hud_frame then
        local pixels,width=screen:pixels()
        if width~=400 then return end
        local green=0
        for x=20,380 do
            local c=string.unpack("<I4",pixels,(30*width+x)*4+1)
            local r,g,b=(c>>16)&255,(c>>8)&255,c&255
            if g>100 and g>r*3//2 and g>b*3//2 then green=green+1 end
        end
        if green>250 and program:read_u16(0x01060280)==id and program:read_u16(0x01060e50)==id then hud_frame=frame end
        return
    end
    local age=frame-hud_frame
    if leg_mode=="" then for side=1,2 do
        for action=1,2 do
            local first=180+(side-1)*100+(action-1)*220
            if age==first then controls[side][action]:set_value(1) end
            if age==first+3 then controls[side][action]:clear_value() end
        end
    end end
    if age<160 or age>700 or age%30~=10 then return end
    local base_table=program:read_u32(0xff906f40)
    local alt_table=program:read_u32(0xff907060)
    local records={program:read_u32(base_table+id*32),program:read_u32(alt_table+id*32)}
    require_palette(records[1]~=records[2],"primary and alternate record alias")
    local alt_count=0
    for side,pointer in ipairs(pointers) do
        local actor=program:read_u32(pointer)
        local alternate=(program:read_u16(actor+0x160)&0x40)~=0
        if alternate then alt_count=alt_count+1;alt_fields=alt_fields+1 end
        local variant=alternate and 2 or 1
        local palette=program:read_u16(actor+0x140)&0x7f00
        local mismatches=0
        -- 6-bit body pixels use entries 1..63. The transparent zero is ignored.
        for color=1,63 do
            local expected=program:read_u16(donor[variant]+16+color*16)&0x7fff
            local actual=program:read_u16(0x01800000+(palette+color)*16)&0x7fff
            if actual~=expected then mismatches=mismatches+1 end
        end
        require_palette(program:read_u16(actor+0x1f0)==id,"actor identity changed")
        require_palette(mismatches==0,"side "..side.." palette mismatches "..mismatches)
        print(string.format("MK2KS_MIRROR_STATE age=%d side=%d id=%d alternate=%s palette=%04X mismatches=%d",
            age,side,id,tostring(alternate),palette,mismatches))
    end
    require_palette(alt_count==1,"exactly one mirror must use the native alternate flag")
    if age==160 or age==400 or age==700 then manager.machine.video:snapshot() end
end)
emu.register_stop(function()
    print(string.format("MK2KS_MIRROR_RESULT pass=%s fighter=%s checks=%d errors=%d alternate_fields=%d",
        tostring(checks>=100 and errors==0 and alt_fields>=15),fighter,checks,errors,alt_fields))
end)
