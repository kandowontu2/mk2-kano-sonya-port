-- Whole native jumps, using only ordinary controls and read-only observations.
-- Launch from the port root with both players selected by the existing harness.
assert((os.getenv("MK2KS_TEST_LEG") or "")=="", "Clear leg mode for jump regression")
assert((os.getenv("MK2KS_TEST_SQUARE") or "")=="", "Clear square mode for jump regression")
assert((os.getenv("MK2KS_TEST_BALL") or "")=="", "Clear cannonball mode for jump regression")
assert(os.getenv("MK2KS_TEST_PROJECTILES")~="1", "Clear projectile mode for jump regression")
dofile("mk2ks_selector_exit_test.lua")

local frame,hud_frame=0,nil
local program,screen,up
local samples={{},{}}
local events={{},{}}
local taps={}
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
local starts={180,380}
local originals={kano={id=17,first=0xfe8282c0,middle=0xfe828320,tucked=0xfe828380},
    sonya={id=18,first=0xfe835bc0,middle=0xfe835c20,tucked=0xfe835c80}}
for _,name in ipairs(names) do assert(originals[name], "Jump test needs Kano and Sonya") end

emu.register_frame(function()
    frame=frame+1
    if not program then
        program=manager.machine.devices[":maincpu"].spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        up={high["P1 Up"],high["P2 Up"]}
        for _,definition in ipairs({{0xff82f5b0,"landing"},{0xff82f670,"landed"}}) do
            taps[#taps+1]=program:install_read_tap(definition[1],definition[1]+15,"native jump "..definition[2],
                function(offset,data,mask)
                    if not hud_frame then return end
                    local actor=manager.machine.devices[":maincpu"].state.A8.value
                    for side,pointer in ipairs({0x01060220,0x01060df0}) do
                        if actor==program:read_u32(pointer) then events[side][definition[2]]=frame end
                    end
                end)
        end
    end
    if not hud_frame then
        local pixels,width=screen:pixels()
        if width~=400 then return end
        local function bar(left)
            local count=0
            for x=left,left+60 do
                local c=string.unpack("<I4",pixels,(30*width+x)*4+1)
                local r,g,b=(c>>16)&255,(c>>8)&255,c&255
                if g>60 and g>r*3//2 and g>b*3//2 then count=count+1 end
            end
            return count>=55
        end
        if frame>900 and bar(110) and bar(220) then hud_frame=frame end
        return
    end
    local age=frame-hud_frame
    for side,start in ipairs(starts) do
        if age>=start and age<start+3 then up[side]:set_value(1) end
        if age>=start-1 and age<=start+80 then
            local actor=program:read_u32(side==1 and 0x01060220 or 0x01060df0)
            local y=program:read_u16(actor+0xb0)
            if y>=0x8000 then y=y-0x10000 end
            local sample={y=y,vy=program:read_u32(actor+0x60),
                vx=program:read_u32(actor+0x40),pose=program:read_u32(actor+0x1d0),
                id=program:read_u16(actor+0x1f0)}
            samples[side][age-start]=sample
            print(string.format("MK2KS_JUMP_STATE side=%d age=%d id=%d y=%d vx=%08X vy=%08X pose=%08X",
                side,age-start,sample.id,sample.y,sample.vx,sample.vy,sample.pose))
        end
    end
end)

emu.register_stop(function()
    local failures=0
    for side,rows in ipairs(samples) do
        local expected=originals[names[side]]
        local baseline,last=rows[-1],rows[80]
        local errors,air_fields=0,0
        local phases={}
        local previous
        local function require_jump(value) if not value then errors=errors+1 end end
        require_jump(baseline and last)
        if baseline and last then
            for age=0,80 do
                local s=rows[age]
                require_jump(s and s.id==expected.id and s.vx==0)
                if s then
                    if s.y<baseline.y then
                        air_fields=air_fields+1
                        require_jump(s.pose==expected.middle or s.pose==expected.tucked)
                    end
                    local pose=(s.pose==expected.middle or s.pose==expected.tucked or s.pose==expected.first) and s.pose or nil
                    if pose and pose~=previous then phases[#phases+1]={pose=pose,first=age,fields=0} end
                    if pose then phases[#phases].fields=phases[#phases].fields+1 end
                    previous=pose
                end
            end
            require_jump(last.y==baseline.y and last.vx==0 and last.vy==0)
            require_jump(air_fields==38)
            require_jump(#phases==4)
            for index,pose in ipairs({expected.middle,expected.tucked,expected.middle,expected.first}) do
                require_jump(phases[index] and phases[index].pose==pose)
            end
            -- MKII native jump advances airborne poses at cadence 4. The
            -- landing script lasts 6 fields; the final sprite remains for
            -- one additional native ready-to-stance scheduling field.
            require_jump(phases[1] and phases[1].fields==4)
            require_jump(phases[2] and phases[2].fields==34)
            require_jump(phases[3] and phases[3].fields==3)
            require_jump(phases[4] and phases[4].fields==4)
            require_jump(events[side].landing and events[side].landed and
                events[side].landed-events[side].landing==6)
            if phases[1] then
                for elapsed=0,37 do
                    local s=rows[phases[1].first+elapsed]
                    local ticks=elapsed+1
                    local y=math.floor(baseline.y-10*ticks+0.25*ticks*(ticks+1))
                    local vy=(-10*65536+ticks*32768)&0xffffffff
                    require_jump(s and s.y==y and s.vy==vy)
                end
            end
        end
        for index,phase in ipairs(phases) do
            print(string.format("MK2KS_JUMP_PHASE side=%d index=%d pose=%08X first=%d fields=%d",
                side,index,phase.pose,phase.first,phase.fields))
        end
        print(string.format("MK2KS_JUMP_RESULT pass=%s side=%d fighter=%s airborne_fields=%d errors=%d",
            tostring(errors==0),side,names[side],air_fields,errors))
        print(string.format("MK2KS_JUMP_NATIVE side=%d landing=%d landed=%d",
            side,events[side].landing or -1,events[side].landed or -1))
        if errors>0 then failures=failures+1 end
    end
    print(string.format("MK2KS_JUMP_SUITE pass=%s failures=%d",tostring(failures==0),failures))
    for _,tap in ipairs(taps) do tap:remove() end
end)
