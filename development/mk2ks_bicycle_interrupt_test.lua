-- Counter a real bicycle startup with a native uppercut, recover, and retry.
-- The observer never writes character, process, health, position, or ROM state.
assert(os.getenv("MK2KS_TWO_PLAYER")=="1")
dofile("mk2ks_selector_exit_test.lua")
local side=tonumber(os.getenv("MK2KS_BICYCLE_SIDE") or "1")
-- Strike after entry but before the displaced startup drops below the uppercut.
local delay=tonumber(os.getenv("MK2KS_BICYCLE_INTERRUPT_DELAY") or tostring(10-side))
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
assert((side==1 or side==2) and names[side]=="sonya")
local ids={kano=17,sonya=18}
local victim_id=assert(ids[names[3-side]])
local frame,hud,command,retry,settle=0,nil,nil,nil,nil
local baseline,interrupted,last,hit_frame
local cpu,program,screen,buttons,direction
local pointers={0x01060220,0x01060df0}
local processes={0x01060260,0x01060e30}
local health={0x010602f0,0x01060ec0}
local taps,events,ready={},{entries={},collisions={},ticks={},releases={} },{{},{}}
local errors,palettes=0,0
local function check(condition,label)
    if not condition then errors=errors+1;if errors<=40 then print("MK2KS_BICYCLE_INTERRUPT_ERROR "..label) end end
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function sample(index)
    local actor=program:read_u32(pointers[index])
    local process=program:read_u32(processes[index])
    return {id=program:read_u16(actor+0x1f0),action=program:read_u16(process+0x1f0),
        x=signed(program:read_u16(actor+0x90)),y=signed(program:read_u16(actor+0xb0)),
        floor=signed(program:read_u16(process+0x200)),vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60),
        gravity=program:read_u32(actor+0x20),trail=program:read_u32(process+0x190),health=program:read_u16(health[index])}
end
local function press(index,key) buttons[index][key]:set_value(1) end
local function input(at)
    local age=frame-at
    local back=direction=="right" and "left" or "right"
    if (age>=0 and age<3) or (age>=6 and age<9) then press(side,back) end
    if age>=12 and age<15 then press(side,"down") end
    if age>=13 and age<16 then press(side,"hk") end
end
local function check_palettes()
    local alternates=0
    for index,name in ipairs(names) do
        local donors=name=="kano" and {0xfec95de0,0xfec961f0} or {0xfec96790,0xfec96ba0}
        local actor=program:read_u32(pointers[index])
        local alternate=(program:read_u16(actor+0x160)&0x40)~=0
        if alternate then alternates=alternates+1 end
        local bank=program:read_u16(actor+0x140)&0x7f00
        local mismatches=0
        for color=1,63 do
            if (program:read_u16(0x01800000+(bank+color)*16)&0x7fff)~=
               (program:read_u16(donors[alternate and 2 or 1]+16+color*16)&0x7fff) then mismatches=mismatches+1 end
        end
        check(mismatches==0,"native palette side "..index);palettes=palettes+1
    end
    check(alternates==(names[1]==names[2] and 1 or 0),"native mirror outfit count")
end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        buttons={}
        for index=1,2 do
            local prefix="P"..index.." "
            buttons[index]={left=high[prefix.."Left"],right=high[prefix.."Right"],down=high[prefix.."Down"],
                hp=high[prefix.."High Punch"],hk=high[prefix.."High Kick"]}
        end
        for _,event in ipairs({{0xfff9a400,"entries",side},{0xfff9ee00,"collisions",side},
                              {0xfff9d000,"ticks",side},{0xfff9e000,"releases",3-side}}) do
            taps[#taps+1]=program:install_read_tap(event[1],event[1]+15,"interrupted bicycle event",function()
                if command and frame>=command and cpu.state.A8.value==program:read_u32(pointers[event[3]]) then
                    local list=events[event[2]];list[#list+1]=frame
                    if event[2]~="ticks" then print(string.format("MK2KS_BICYCLE_INTERRUPT_EVENT kind=%s frame=%d",event[2],frame)) end
                end
            end)
        end
        taps[#taps+1]=program:install_read_tap(0xff861350,0xff86135f,"interrupted bicycle ready",function()
            if not command then return end
            for index,pointer in ipairs(pointers) do
                if cpu.state.A8.value==program:read_u32(pointer) then ready[index][#ready[index]+1]=frame end
            end
        end)
        taps[#taps+1]=program:install_write_tap(health[side],health[side]+15,"actual bicycle counter damage",function(offset,data)
            if baseline and not interrupted and (data&0xffff)<baseline[1].health then
                hit_frame=frame;print("MK2KS_BICYCLE_INTERRUPT_HIT frame="..frame)
            end
        end)
    end
    if not hud then
        local pixels,width=screen:pixels()
        if width~=400 or frame<900 then return end
        local green=0
        for x=20,380 do
            local c=string.unpack("<I4",pixels,(30*width+x)*4+1)
            local r,g,b=(c>>16)&255,(c>>8)&255,c&255
            if g>100 and g>r*3//2 and g>b*3//2 then green=green+1 end
        end
        if green>250 then hud=frame end
        return
    end
    if frame<hud+180 or last then return end
    local own,victim=sample(side),sample(3-side)
    if not command then
        if math.abs(own.x-victim.x)>68 then
            press(side,own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then
                command=frame+20;baseline={own,victim};settle=nil
                direction=own.x<victim.x and "right" or "left";check_palettes()
                print(string.format("MK2KS_BICYCLE_INTERRUPT_COMMAND frame=%d delay=%d x=%d,%d",command,delay,own.x,victim.x))
            end
        end
        return
    end
    input(command)
    local age=frame-command
    if age>=delay-8 and age<delay+4 then press(3-side,"down") end
    if age>=delay and age<delay+4 then press(3-side,"hp") end
    if age>=6 and age<=80 and age%2==0 then
        print(string.format("MK2KS_BICYCLE_INTERRUPT_STATE age=%d health=%d,%d action=%04X,%04X x=%d,%d y=%d,%d",
            age,own.health,victim.health,own.action,victim.action,own.x,victim.x,own.y,victim.y))
    end
    if age==24 or age==50 then manager.machine.video:snapshot() end
    if age==200 then
        interrupted={own,victim,entries=#events.entries,collisions=#events.collisions,ticks=#events.ticks,releases=#events.releases}
        check_palettes()
        print(string.format("MK2KS_BICYCLE_INTERRUPT_RECOVERED entries=%d collisions=%d ticks=%d releases=%d health=%d,%d",
            interrupted.entries,interrupted.collisions,interrupted.ticks,interrupted.releases,own.health,victim.health))
    end
    if interrupted and not retry then
        if math.abs(own.x-victim.x)>68 then
            press(side,own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then
                retry=frame+20;direction=own.x<victim.x and "right" or "left"
                print("MK2KS_BICYCLE_INTERRUPT_RETRY frame="..retry)
            end
        end
    elseif retry then
        input(retry)
        if frame==retry+45 then check_palettes();manager.machine.video:snapshot() end
        if frame==retry+200 then last={own,victim};check_palettes();manager.machine.video:snapshot() end
    end
end)
emu.register_stop(function()
    check(#taps==6,"all observers installed")
    check(baseline and interrupted and last,"interrupt and retry both completed")
    if baseline and interrupted and last then
        check(interrupted.entries==1 and interrupted.ticks==0 and interrupted.releases==0,"active startup interrupted before paired flight")
        check(hit_frame and events.entries[1] and hit_frame>=events.entries[1] and hit_frame<command+40,"counter hit after bicycle actually started")
        check(interrupted[1].health==baseline[1].health-40 and interrupted[2].health==baseline[2].health,"actual uppercut damaged only Sonya")
        check(#events.entries==2 and #events.ticks>=16 and #events.ticks<=48 and #events.releases==1,"retry executes one full paired bicycle")
        check(last[1].health==interrupted[1].health and last[2].health==interrupted[2].health-22,"retry damages only victim by 22")
        for _,phase in ipairs({interrupted,last}) do
            for index,s in ipairs(phase) do
                check(s.id==(index==1 and 18 or victim_id),"true identities preserved")
                check(s.action~=0x204 and s.action~=0x214 and s.action~=0x215 and s.trail==0,"bicycle states and attached object cleared")
                check(s.y==s.floor and s.vx==0 and s.vy==0 and s.gravity==0,"grounded recovery with no residual motion")
            end
        end
        check(#ready[side]>0 and #ready[3-side]>0,"both native ready continuations")
    end
    print(string.format("MK2KS_BICYCLE_INTERRUPT_RESULT pass=%s side=%d victim=%s delay=%d entries=%d collisions=%d ticks=%d releases=%d palettes=%d errors=%d",
        tostring(errors==0),side,names[3-side],delay,#events.entries,#events.collisions,#events.ticks,#events.releases,palettes,errors))
    for _,tap in ipairs(taps) do tap:remove() end
end)
