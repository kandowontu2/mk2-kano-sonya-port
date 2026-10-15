-- Natural ladder and ordinary human inputs only. All observations are read-only.
for _,name in ipairs({"MK2KS_DIAGNOSTIC_CPU_ID","MK2KS_DIAGNOSTIC_LADDER_INDEX",
    "MK2KS_DIAGNOSTIC_CPU_HEALTH","MK2KS_DIAGNOSTIC_P1_REGEN","MK2KS_DIAGNOSTIC_ALL_STAGES"}) do
    assert(not os.getenv(name),"Natural CPU probe cannot use "..name)
end
dofile("mk2ks_cpu_ladder_trace.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local screen=manager.machine.screens[":screen"]
local frame,taps,collecting,fields,events=0,{},false,0,0
local captures,children={},{}
local slots={{actor=0x01060220,main=0x01060260,state=0x010601f0,id=0x01060280,hp=0x010602f0},
    {actor=0x01060df0,main=0x01060e30,state=0x01060dc0,id=0x01060e50,hp=0x01060ec0}}
local function valid(v)return v>=0x01000000 and v<0x01100000 end
local function signed(v)return v>=0x8000 and v-0x10000 or v end
local function active()
    local actor=p:read_u32(slots[2].actor)
    return p:read_u16(0x010601d0)==2 and p:read_u16(slots[1].state)==1 and
        p:read_u16(slots[2].state)==0 and valid(actor) and
        (p:read_u16(actor+0x1f0)==17 or p:read_u16(actor+0x1f0)==18)
end
for _,address in ipairs({0xfffc6000,0xfffc7000}) do
    taps[#taps+1]=p:install_read_tap(address,address+15,"natural CPU child construction",function(at)
        if at~=address or collecting or not active() then return end
        collecting=true
        local actor,main=cpu.A8.value,cpu.A13.value
        if valid(actor) and valid(main) and p:read_u32(main+0x230)==p:read_u32(slots[2].actor) then
            children[actor]=main
            print(string.format("MK2_NAT_CPU_CHILD frame=%d entry=%08X pc=%08X actor=%08X main=%08X owner=%08X id=%d writes=0",
                frame,address,cpu.PC.value,actor,main,p:read_u32(main+0x230),p:read_u16(actor+0x1f0)))
        end
        collecting=false
    end)
end
taps[#taps+1]=p:install_read_tap(0xff838790,0xff83879f,"natural CPU group execution",function(at)
    if at~=0xff838790 or collecting or not active() then return end
    collecting=true
    local actor,main=cpu.A8.value,cpu.A13.value
    if valid(actor) and valid(main) and (actor==p:read_u32(slots[2].actor) or children[actor]==main) then
        print(string.format("MK2_NAT_CPU_GROUP frame=%d pc=%08X actor=%08X main=%08X id=%d body=%d group=%08X x=%d y=%d vx=%08X vy=%08X writes=0",
            frame,cpu.PC.value,actor,main,p:read_u16(actor+0x1f0),children[actor] and 0 or 1,cpu.A0.value,
            signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),p:read_u32(actor+0x40),p:read_u32(actor+0x60)))
    end
    collecting=false
end)
taps[#taps+1]=p:install_read_tap(0xff8b6820,0xff8b682f,"natural CPU child retirement",function(at)
    if at~=0xff8b6820 or collecting then return end
    local actor=cpu.A8.value
    if children[actor] then
        print(string.format("MK2_NAT_CPU_RETIRE frame=%d pc=%08X actor=%08X main=%08X writes=0",frame,cpu.PC.value,actor,cpu.A13.value))
        children[actor]=nil
    end
end)
for _,spec in ipairs({{"ready",0xff861350},{"fling",0xff876650}}) do
    taps[#taps+1]=p:install_read_tap(spec[2],spec[2]+15,"natural CPU recovery/physics",function(at)
        if at~=spec[2] or collecting or not active() then return end
        local actor,main=cpu.A8.value,cpu.A13.value
        if actor==p:read_u32(slots[1].actor) or actor==p:read_u32(slots[2].actor) then
            print(string.format("MK2_NAT_CPU_EVENT frame=%d kind=%s entry=%08X pc=%08X actor=%08X main=%08X a0=%08X a1=%08X a2=%08X a3=%08X writes=0",
                frame,spec[1],spec[2],cpu.PC.value,actor,main,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value))
        end
    end)
end
for _,spec in ipairs({{17,"knife",0xffffb000},{17,"ball",0xffffde00},{17,"blade",0xfff8cc00},
    {17,"choke",0xfff91400},{18,"ring",0xffffb400},{18,"square",0xffffca00},
    {18,"bicycle",0xfff9a400},{18,"leg",0xfff80800}}) do
    taps[#taps+1]=p:install_read_tap(spec[3],spec[3]+15,"natural CPU complete action start",function(at)
        if at~=spec[3] or collecting or not active() then return end
        collecting=true
        local main,actor=cpu.A13.value,p:read_u32(slots[2].actor)
        if valid(main) and main==p:read_u32(slots[2].main) and p:read_u32(main+0xc0)==actor and p:read_u16(actor+0x1f0)==spec[1] then
            events=events+1
            local stage,schedule=p:read_u16(0x01061b30),p:read_u32(0x01061b10)
            print(string.format("MK2_NAT_CPU_ENTRY frame=%d serial=%d id=%d move=%s entry=%08X pc=%08X actor=%08X main=%08X a8=%08X stage=%d schedule=%08X mode=%d state=%d roster=%d scheduled=%d human_state=%d human_roster=%d writes=0",
                frame,events,spec[1],spec[2],spec[3],cpu.PC.value,actor,main,cpu.A8.value,stage,schedule,
                p:read_u16(0x010601d0),p:read_u16(slots[2].state),p:read_u16(slots[2].id),p:read_u16(schedule+stage*16),
                p:read_u16(slots[1].state),p:read_u16(slots[1].id)))
            if events<=12 then for _,age in ipairs({8,18,40,80}) do captures[frame+age]={events,spec[2],age} end end
        end
        collecting=false
    end)
end
for side,slot in ipairs(slots) do
    taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,"natural CPU native health",function(at,data,mask)
        if collecting or not active() then return end
        collecting=true
        print(string.format("MK2_NAT_CPU_HEALTH frame=%d slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X writes=0",
            frame,side,p:read_u16(slot.hp),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value))
        collecting=false
    end)
end
emu.register_frame(function()
    frame=frame+1
    if not active() then return end
    fields=fields+1
    local stage,schedule=p:read_u16(0x01061b30),p:read_u32(0x01061b10)
    local scheduled=schedule>=0xff800000 and p:read_u16(schedule+stage*16) or 65535
    for side,slot in ipairs(slots) do
        local actor,main=p:read_u32(slot.actor),p:read_u32(slot.main)
        if valid(actor) and valid(main) then
            print(string.format("MK2_NAT_CPU_FIELD frame=%d slot=%d mode=2 stage=%d schedule=%08X scheduled=%d actor=%08X main=%08X owner=%08X state=%d roster=%d id=%d hp=%d action=%04X pose=%08X list=%08X x=%d y=%d floor=%d xraw=%08X yraw=%08X vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X trail=%08X child=%08X writes=0",
                frame,side,stage,schedule,scheduled,actor,main,p:read_u32(main+0xc0),p:read_u16(slot.state),p:read_u16(slot.id),
                p:read_u16(actor+0x1f0),p:read_u16(slot.hp),p:read_u16(main+0x1f0),p:read_u32(actor+0x1d0),p:read_u32(actor+0x1a0),
                signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),signed(p:read_u16(main+0x200)),
                p:read_u32(actor+0x80),p:read_u32(actor+0xa0),p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u32(actor+0x20),
                p:read_u16(main+0x210),p:read_u16(actor+0x160),p:read_u32(main+0x190),p:read_u32(main+0x190)))
        end
    end
    if captures[frame] then
        local c=captures[frame]
        screen:snapshot(string.format("nat_cpu_%d_%s_%d.png",c[1],c[2],c[3]))
    end
    for actor,main in pairs(children) do
        print(string.format("MK2_NAT_CPU_EFFECT frame=%d actor=%08X main=%08X owner=%08X id=%d type=%d action=%04X pose=%08X x=%d y=%d xraw=%08X yraw=%08X vx=%08X vy=%08X velocity_parameter=%08X flags=%04X writes=0",
            frame,actor,main,p:read_u32(main+0x230),p:read_u16(actor+0x1f0),p:read_u16(actor+0xc0),p:read_u16(main+0x1f0),
            p:read_u32(actor+0x1d0),signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),
            p:read_u32(actor+0x80),p:read_u32(actor+0xa0),p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u32(main+0x250),p:read_u16(actor+0xf0)))
    end
end)
emu.register_stop(function()
    local live_children=0;for _ in pairs(children) do live_children=live_children+1 end
    print(string.format("MK2_NAT_CPU_RESULT frames=%d active_fields=%d entries=%d writes=0 schema=4 live_children=%d",frame,fields,events,live_children))
    for _,tap in ipairs(taps) do tap:remove() end
end)
