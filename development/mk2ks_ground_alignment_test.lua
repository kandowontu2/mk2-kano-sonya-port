-- Real selection/input and read-only floor/sprite geometry observation.
dofile("mk2ks_selector_exit_test.lua")
local frame,program,screen=0,nil,nil
local seen={{},{}}
local fields,checks,errors=nil,0,0
local jumped={false,false}
local phases={}
local anchors={[4]=133,[8]=131,[17]=134,[18]=135}
local contacts={[4]=5,[8]=8,[17]=5,[18]=5}
local ids={kano=17,sonya=18,kitana=4,sub_zero=8}
local expected={assert(ids[os.getenv("MK2KS_TEST_FIGHTER")]),assert(ids[os.getenv("MK2KS_P2_FIGHTER")])}
local arc_snapshots=os.getenv("MK2KS_GROUND_ARC_SNAPSHOTS")=="1"
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function check(value,label)
    checks=checks+1
    if not value then errors=errors+1;if errors<=12 then print("MK2KS_GROUND_ERROR "..label) end end
end
emu.register_frame(function()
    frame=frame+1
    if not program then
        program=manager.machine.devices[":maincpu"].spaces.program
        screen=manager.machine.screens[":screen"]
        fields=manager.machine.ioport.ports[":IN0"].fields
    end
    if frame>=1500 and frame<1503 then fields["P1 Up"]:set_value(1) end
    if frame>=1700 and frame<1703 then fields["P2 Up"]:set_value(1) end
    if frame>=1900 and frame<1912 then fields["P1 Down"]:set_value(1);fields["P2 Down"]:set_value(1) end
    if frame>=2020 and frame<2032 then fields["P1 Right"]:set_value(1);fields["P2 Left"]:set_value(1) end
    if frame<1400 or frame>2160 then return end
    local phase=frame<=1480 and "stance" or frame>=1800 and frame<=1880 and "landed" or
        frame>=1960 and frame<=1980 and "uncrouched" or frame>=2080 and "walked" or nil
    for side,pointer in ipairs({0x01060220,0x01060df0}) do
        local actor=program:read_u32(pointer)
        if actor>=0x01000000 and actor<0x01100000 then
            local process=program:read_u32(side==1 and 0x01060260 or 0x01060e30)
            local floor=signed(program:read_u16(process+0x200))
            local y=signed(program:read_u16(actor+0xb0))
            if frame==1530 or frame==1730 then
                print(string.format("MK2KS_GROUND_AIR frame=%d side=%d id=%d jump=%d y=%d floor=%d",
                    frame,side,program:read_u16(actor+0x1f0),floor-y,y,floor))
            end
            if arc_snapshots and (side==1 and frame>=1510 and frame<=1560 and frame%5==0 or
                side==2 and frame>=1710 and frame<=1760 and frame%5==0) then
                print(string.format("MK2KS_SHADOW_ARC frame=%d side=%d id=%d jump=%d",
                    frame,side,program:read_u16(actor+0x1f0),floor-y))
                screen:snapshot(string.format("shadow_arc_side%d_frame%d.png",side,frame))
            end
            if y<floor then jumped[side]=true end
            local pose=program:read_u32(actor+0x1d0)
            if os.getenv("MK2KS_GROUND_CROUCH_TRACE")=="1" and side==1 and
                frame>=1898 and frame<=1960 and frame%2==0 then
                print(string.format("MK2KS_CROUCH_MOTION frame=%d id=%d action=%04X pose=%08X y=%d floor=%d",
                    frame,program:read_u16(actor+0x1f0),
                    program:read_u16(process+0x1f0),pose,y,floor))
                if frame>=1908 and frame<=1940 then
                    screen:snapshot(string.format("crouch_motion_frame%d.png",frame))
                end
            end
            if phase then
                local id=program:read_u16(actor+0x1f0)
                local stage=signed(program:read_u16(0x0105ecd0))
                check(id==expected[side],"actual selected identity")
                check(y==floor and floor==stage-anchors[expected[side]],"grounded physical origin uses corrected anchor")
                local bottom=-32768
                local cache=program:read_u32(actor+0x1a0)
                for part=0,15 do
                    local at=cache+part*0x70
                    local source=program:read_u32(at)
                    if source==0 then break end
                    bottom=math.max(bottom,y-signed(program:read_u16(at+0x60))+program:read_u16(at+0x30))
                end
                check(bottom-stage==contacts[expected[side]],"actual displayed stance meets stock-referenced contact line")
                phases[phase]=true
                if not seen[side][phase..pose] then
                    seen[side][phase..pose]=true
                    print(string.format("MK2KS_GROUND_CONTACT frame=%d phase=%s side=%d id=%d y=%d floor=%d stage=%d bottom=%d pose=%08X",
                        frame,phase,side,id,y,floor,stage,bottom,pose))
                end
            end
        else check(false,"valid live actor") end
    end
    if frame==1450 or frame==1530 or frame==1730 or frame==1850 or
        frame==1970 or frame==2120 then screen:snapshot() end
end)
emu.register_stop(function()
    for side=1,2 do check(jumped[side],"both real jumps exercised") end
    for _,phase in ipairs({"stance","landed","uncrouched","walked"}) do check(phases[phase],"observed "..phase) end
    check(checks>1500,"full stance and recovery observation")
    print(string.format("MK2KS_GROUND_RESULT pass=%s checks=%d errors=%d",tostring(errors==0),checks,errors))
end)
