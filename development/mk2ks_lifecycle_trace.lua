-- Optional read-only evidence for real-input blade/bicycle lifecycle drivers.
-- Every tap returns nil: no guest data, state or health is substituted.
return function(move,side,names,context)
    assert(move=="blade" or move=="bicycle")
    local p=manager.machine.devices[":maincpu"].spaces.program
    local cpu=manager.machine.devices[":maincpu"].state
    local slots={{actor=0x01060220,main=0x01060260,hp=0x010602f0,id=0x01060280,state=0x010601f0},
        {actor=0x01060df0,main=0x01060e30,hp=0x01060ec0,id=0x01060e50,state=0x01060dc0}}
    local taps,vx_observed={},{}
    local function valid(x) return x>=0x01000000 and x<0x01100000 end
    local function signed(x) return x>=0x8000 and x-0x10000 or x end
    print(string.format("MK2_LIFE_TRACE_BOOT move=%s side=%d names=%s,%s writes=0",move,side,names[1],names[2]))
    local entries=move=="blade" and {action=0xfff8cc00,strike=0xfff8e400,create=0xfff8d800,step=0xfff8e000,
        hurt=0xfff90000,blood_request=0xff9a5b00,blood_start=0xff9a7f70,blood_allocate=0xff9aff00,
        blood_insert=0xff83f610,blood_cleanup=0xff9b0e50,recovery=0xff861350} or
        {action=0xfff9a400,tick=0xfff9d000,release=0xfff9e000,strike=0xfff9ee00,
        animation=0xff83bb00,fling=0xff876650,recovery=0xff861350}
    for kind,address in pairs(entries) do
        taps[#taps+1]=p:install_read_tap(address,address+15,"lifecycle evidence "..kind,function(at)
            local frame,cycle,age=context()
            if at~=address or not cycle or age<0 then return end
            local own,victim=p:read_u32(slots[side].actor),p:read_u32(slots[3-side].actor)
            local actor=cpu.A8.value
            if kind=="action" or kind=="strike" or kind=="create" or kind=="step" or kind=="tick" then
                if actor~=own then return end
            elseif kind=="hurt" or kind=="release" or kind=="blood_request" then
                if actor~=victim then return end
            elseif kind=="animation" or kind=="fling" or kind=="recovery" then
                if actor~=own and actor~=victim then return end
            end
            print(string.format("MK2_LIFE_TRACE_EVENT frame=%d cycle=%d age=%d kind=%s entry=%08X pc=%08X a8=%08X a13=%08X a0=%08X a1=%08X a2=%08X a3=%08X a6=%08X a9=%08X a10=%08X a11=%08X writes=0",
                frame,cycle,age,kind,address,cpu.PC.value,actor,cpu.A13.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A6.value,cpu.A9.value,cpu.A10.value,cpu.A11.value))
        end)
    end
    for n,slot in ipairs(slots) do
        taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,"lifecycle evidence health",function(at,data)
            local frame,cycle,age=context()
            if at~=slot.hp or not cycle or age<0 then return end
            local before,after=p:read_u16(slot.hp),data&0xffff;if before==after then return end
            print(string.format("MK2_LIFE_TRACE_HEALTH frame=%d cycle=%d age=%d slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X writes=0",
                frame,cycle,age,n,before,after,cpu.PC.value,cpu.A8.value,cpu.A13.value))
        end)
    end
    emu.register_stop(function() for _,tap in ipairs(taps) do tap:remove() end end)
    return {field=function(frame,cycle,age)
        for n,slot in ipairs(slots) do
            local actor,main=p:read_u32(slot.actor),p:read_u32(slot.main)
            assert(valid(actor) and valid(main),"Actual lifecycle actor/main required")
            if move=="bicycle" and age==0 and not vx_observed[actor] then
                vx_observed[actor]=true
                local address=actor+0x40
                taps[#taps+1]=p:install_write_tap(address,address+31,"actual lifecycle horizontal velocity",function(at,data)
                    local now,generation,elapsed=context()
                    if at~=address or not generation or elapsed<0 then return end
                    local before=p:read_u32(address)
                    if before==data then return end
                    print(string.format("MK2_LIFE_TRACE_VELOCITY frame=%d cycle=%d age=%d slot=%d actor=%08X before=%08X after=%08X pc=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X x=%d left=%d right=%d writes=0",
                        now,generation,elapsed,n,actor,before,data,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A8.value,cpu.A13.value,
                        signed(p:read_u16(actor+0x90)),signed(p:read_u16(0x0105ecf0))+0x3a,signed(p:read_u16(0x0105ed00))+0x15f))
                end)
            end
            local trail=p:read_u32(main+0x190)
            print(string.format("MK2_LIFE_TRACE_FIELD frame=%d cycle=%d age=%d slot=%d actor=%08X main=%08X id=%d roster=%d state=%d action=%04X pose=%08X hp=%d x=%d y=%d floor=%d xraw=%08X yraw=%08X vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X trail=%08X descriptor=%08X suppression=%d left=%d right=%d writes=0",
                frame,cycle,age,n,actor,main,p:read_u16(actor+0x1f0),p:read_u16(slot.id),p:read_u16(slot.state),p:read_u16(main+0x1f0),p:read_u32(actor+0x1d0),p:read_u16(slot.hp),
                signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),signed(p:read_u16(main+0x200)),p:read_u32(actor+0x80),p:read_u32(actor+0xa0),p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u32(actor+0x20),p:read_u16(main+0x210),p:read_u16(actor+0x160),trail,valid(trail) and p:read_u32(trail+0x1a0) or 0,p:read_u16(0x010619d0),signed(p:read_u16(0x0105ecf0))+0x3a,signed(p:read_u16(0x0105ed00))+0x15f))
        end
    end}
end
