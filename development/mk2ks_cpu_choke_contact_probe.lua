-- Observe the first CPU-owned Kano choke and its native damage/recovery.
-- Selection/input is provided by the normal ladder harness; all access here
-- is read-only. Any ladder-index setup is reported by the underlying harness.
dofile("mk2ks_cpu_ladder_trace.lua")
local frame,program,cpu=0,nil,nil
local taps,event={},nil
local approach=os.getenv("MK2KS_CPU_CHOKE_APPROACH")=="1"
local left,right,approach_frames
approach_frames=0
local function actor_valid(pointer)
    return pointer>=0x01000000 and pointer<0x01100000
end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"]; program=cpu.spaces.program
        if approach then
            local high=manager.machine.ioport.ports[":IN0"].fields
            left,right=high["P1 Left"],high["P1 Right"]
            assert(left and right)
        end
        for _,address in ipairs({0xfff91400,0xfff93400,0xfff93800}) do
            taps[#taps+1]=program:install_read_tap(address,address+15,
                "CPU Kano choke contact",function(offset)
                    if offset~=address then return end
                    local player=program:read_u32(0x01060220)
                    local opponent=program:read_u32(0x01060df0)
                    if not actor_valid(player) or not actor_valid(opponent) then return end
                    if address==0xfff91400 and not event then
                        local task=cpu.state.A13.value
                        if not actor_valid(task) or program:read_u32(task+0xc0)~=opponent or
                            program:read_u16(opponent+0x1f0)~=17 then return end
                        event={start=frame,owner=opponent,task=task,victim=player,
                            victim_task=program:read_u32(0x01060260),
                            health=program:read_u16(0x010602f0),pulses=0,releases=0,recovered=false}
                        print(string.format("MK2KS_CPU_CHOKE_START frame=%d gap=%d health=%d stage=%d",
                            frame,math.abs(program:read_u16(player+0x90)-program:read_u16(opponent+0x90)),
                            event.health,program:read_u16(0x01061b30)))
                    elseif event and frame-event.start<160 and cpu.state.A8.value==event.victim then
                        if address==0xfff93400 then
                            event.pulses=event.pulses+1
                            print(string.format("MK2KS_CPU_CHOKE_PULSE frame=%d count=%d before=%d",
                                frame,event.pulses,program:read_u16(0x010602f0)))
                            if event.pulses==2 then
                                manager.machine.screens[":screen"]:snapshot("cpu_choke_paired.png")
                            end
                        elseif address==0xfff93800 then
                            event.releases=event.releases+1
                            event.release=frame
                            event.damage=event.health-program:read_u16(0x010602f0)
                            print(string.format("MK2KS_CPU_CHOKE_RELEASE frame=%d damage=%d",frame,event.damage))
                        end
                    end
                end)
        end
    end
    if approach and frame>=1450 and frame<=1850 and frame%60==0 then
        local player,opponent=program:read_u32(0x01060220),program:read_u32(0x01060df0)
        print(string.format("MK2KS_CPU_CHOKE_APPROACH_CONTEXT frame=%d mode=%d winner=%d hp=%d,%d gap=%d",
            frame,program:read_u16(0x010601d0),program:read_u16(0x01061b00),
            program:read_u16(0x010602f0),program:read_u16(0x01060ec0),
            actor_valid(player) and actor_valid(opponent) and
                math.abs(program:read_u16(player+0x90)-program:read_u16(opponent+0x90)) or -1))
    end
    -- Leave the selector harness's direction inputs intact until combat.
    if approach and program:read_u16(0x010601d0)==2 then
        left:set_value(0); right:set_value(0)
        local player,opponent=program:read_u32(0x01060220),program:read_u32(0x01060df0)
        if not event and actor_valid(player) and actor_valid(opponent) and
            program:read_u16(0x010601d0)==2 and
            program:read_u16(0x010602f0)>0 and program:read_u16(opponent+0x1f0)==17 then
            local x1,x2=program:read_u16(player+0x90),program:read_u16(opponent+0x90)
            if math.abs(x1-x2)>80 then
                (x1<x2 and right or left):set_value(1)
                approach_frames=approach_frames+1
            end
        end
    end
    if event and event.release and not event.recovered and not event.defeated and
        frame>event.release and frame-event.start<200 then
        local own=program:read_u32(0x01060df0)
        local player=program:read_u32(0x01060220)
        if own==event.owner and player==event.victim and
            program:read_u16(0x010601d0)==2 and program:read_u16(0x01061b00)==0 and
            program:read_u16(0x010602f0)>0 and
            program:read_u16(event.task+0x1f0)~=0x111 and
            actor_valid(event.victim_task) and
            program:read_u16(event.victim_task+0x1f0)==0x303 and
            program:read_u16(player+0xb0)==program:read_u16(event.victim_task+0x200) and
            program:read_u32(player+0x40)==0 and program:read_u32(player+0x60)==0 then
            event.recovered=true
            print(string.format("MK2KS_CPU_CHOKE_RECOVER frame=%d action=%04X victim_action=%04X victim_y=%d vx=0 vy=0",
                frame,program:read_u16(event.task+0x1f0),
                program:read_u16(event.victim_task+0x1f0),program:read_u16(player+0xb0)))
            manager.machine.screens[":screen"]:snapshot("cpu_choke_recovered.png")
        elseif own==event.owner and player==event.victim and
            program:read_u16(0x010601d0)==5 and program:read_u16(0x01061b00)==2 and
            program:read_u16(0x010602f0)==0 then
            -- A subsequent CPU attack can KO a low-health victim before
            -- standing recovery. Observe this same-round defeat separately;
            -- reused object/task addresses next round cannot prove recovery.
            event.defeated=true
            print(string.format("MK2KS_CPU_CHOKE_DEFEATED frame=%d age=%d winner=2 health=0",
                frame,frame-event.start))
            manager.machine.screens[":screen"]:snapshot("cpu_choke_defeated.png")
        end
    end
end)
emu.register_stop(function()
    local pass=event and event.pulses==4 and event.releases==1 and event.damage==32 and
        (event.recovered or event.defeated)
    print(string.format("MK2KS_CPU_CHOKE_CONTACT_RESULT pass=%s pulses=%d releases=%d damage=%d recovered=%s defeated=%s approach_frames=%d",
        tostring(not not pass),event and event.pulses or 0,event and event.releases or 0,
        event and event.damage or 0,tostring(event and event.recovered or false),
        tostring(event and event.defeated or false),approach_frames))
    for _,tap in ipairs(taps) do tap:remove() end
end)
