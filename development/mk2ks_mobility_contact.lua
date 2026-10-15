-- Real native joined-game controls and read-only complete contact observations.
local config=assert(...)
assert(config.native_join)
local side=config.side
local target=config.names[side]
local move=target=="kano" and "ball" or "square"
local scenario=os.getenv("MK2KS_MOBILITY_CONTACT") or "hit"
assert(scenario=="hit" or scenario=="block" or scenario=="miss")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local screen=manager.machine.screens[":screen"]
local slots={{actor=0x01060220,main=0x01060260,hp=0x010602f0,id=0x01060280,state=0x010601f0},
    {actor=0x01060df0,main=0x01060e30,hp=0x01060ec0,id=0x01060e50,state=0x01060dc0}}
local spec=target=="kano" and {parser=0xffffdb00,action=0xffffde00,attack=0xffffec00,animation=0xff0000e0,state=0x20b,projectile=0xffffb000} or
    {parser=0xffffc800,action=0xffffca00,attack=0xffffda00,animation=0xff0203c0,state=0x207,projectile=0xffffb400}
local taps,epoch,start,frame,done,errors={},nil,nil,0,false,0
local collecting=false
local counts={action=0,attack=0,animation=0,fling=0,recovery=0,projectile=0}
local high,low=manager.machine.ioport.ports[":IN0"].fields,manager.machine.ioport.ports[":IN2"].fields
local controls={}
for n=1,2 do
    local label="P"..n.." "
    controls[n]={up=high[label.."Up"],down=high[label.."Down"],left=high[label.."Left"],right=high[label.."Right"],
        hp=high[label.."High Punch"],block=high[label.."Block"],lp=low[label.."Low Punch"],lk=low[label.."Low Kick"]}
end
local function valid(x) return x>=0x01000000 and x<0x01100000 end
local function signed(x) return x>=0x8000 and x-0x10000 or x end
local function check(ok,label)
    if not ok then errors=errors+1;if errors<20 then print("MK2_MOB_CONTACT_ERROR frame="..frame.." "..label) end end
end
local function event(kind,address)
    taps[#taps+1]=p:install_read_tap(address,address+15,"native mobility contact "..kind,function(at)
        if at~=address or not epoch or collecting then return end
        local own,victim=p:read_u32(slots[side].actor),p:read_u32(slots[3-side].actor)
        if kind~="fling" and kind~="recovery" and cpu.A8.value~=own then return end
        if (kind=="fling" or kind=="recovery") and cpu.A8.value~=own and cpu.A8.value~=victim then return end
        if kind=="action" then start=frame end
        if counts[kind] then counts[kind]=counts[kind]+1 end
        print(string.format("MK2_MOB_CONTACT_EVENT frame=%d age=%d kind=%s entry=%08X pc=%08X a8=%08X a13=%08X a0=%08X a1=%08X a2=%08X a3=%08X a6=%08X a9=%08X a11=%08X writes=0",
            frame,frame-epoch,kind,address,cpu.PC.value,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A6.value,cpu.A9.value,cpu.A11.value))
    end)
end
for kind,address in pairs({parser=spec.parser,action=spec.action,attack=spec.attack,animation=spec.animation,
    fling=0xff876650,recovery=0xff861350,projectile=spec.projectile}) do event(kind,address) end
if target=="kano" then event("elapsed",0xffffdb60) end
for n,slot in ipairs(slots) do
    taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,"mobility native health",function(at,data)
        if at~=slot.hp or not epoch then return end
        local before,after=p:read_u16(slot.hp),data&0xffff;if before==after then return end
        print(string.format("MK2_MOB_CONTACT_HEALTH frame=%d age=%d slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X writes=0",
            frame,frame-epoch,n,before,after,cpu.PC.value,cpu.A8.value,cpu.A13.value))
    end)
end
local function pulse(n,key,age,first,hold)
    if age>=first and age<first+(hold or 3) then
        controls[n][key]:set_value(1)
        print(string.format("MK2_MOB_CONTACT_CONTROL frame=%d age=%d slot=%d button=%s value=1 writes=0",frame,age,n,key))
    end
end
local function observe_and_drive()
    frame=config.now()
    if not config.active() or done then return end
    config.clear_controls()
    if not epoch then
        epoch=frame
        for n,slot in ipairs(slots) do
            local actor=p:read_u32(slot.actor);local address=actor+0x40
            taps[#taps+1]=p:install_write_tap(address,address+31,"original mobility boundary velocity",function(at,data)
                if at~=address then return end
                local before=p:read_u32(address);if before==data then return end
                local other=p:read_u32(slots[3-n].actor)
                print(string.format("MK2_MOB_CONTACT_VELOCITY frame=%d age=%d slot=%d actor=%08X before=%08X after=%08X pc=%08X a2=%08X a5=%08X a6=%08X a7=%08X a8=%08X a9=%08X a13=%08X b4=%08X request=%08X x=%d tx=%d left=%d right=%d writes=0",
                    frame,frame-epoch,n,actor,before,data,cpu.PC.value,cpu.A2.value,cpu.A5.value,cpu.A6.value,cpu.A7.value,cpu.A8.value,cpu.A9.value,cpu.A13.value,cpu.B4.value,
                    p:read_u32(n==1 and 0x010602d0 or 0x01060ea0),signed(p:read_u16(actor+0x90)),signed(p:read_u16(other+0x90)),
                    signed(p:read_u16(0x0105ecf0))+0x3a,signed(p:read_u16(0x0105ed00))+0x15f))
            end)
        end
        print(string.format("MK2_MOB_CONTACT_BEGIN frame=%d move=%s target=%s side=%d scenario=%s writes=0",frame,move,target,side,scenario))
        print(string.format("MK2_MOB_CONTACT_DESCRIPTOR frame=%d move=%s values=%d,%d,%d,%d,%04X,%04X,%d,%d,%d writes=0",frame,move,
            p:read_u16(spec.attack),p:read_u16(spec.attack+16),p:read_u16(spec.attack+32),p:read_u16(spec.attack+48),
            p:read_u16(spec.attack+64),p:read_u16(spec.attack+80),p:read_u16(spec.attack+96),p:read_u16(spec.attack+112),p:read_u16(spec.attack+128)))
        -- Own ROM animation entries, observed without replacement.
        local root=p:read_u32(spec.animation)
        print(string.format("MK2_MOB_CONTACT_ROOT move=%s table=%08X root=%08X writes=0",move,spec.animation,root))
        for index=0,(target=="kano" and 10 or 5) do
            print(string.format("MK2_MOB_CONTACT_POSE move=%s index=%d value=%08X writes=0",move,index,p:read_u32(root+index*32)))
        end
    end
    local age=frame-epoch
    local own,victim=p:read_u32(slots[side].actor),p:read_u32(slots[3-side].actor)
    check(valid(own) and valid(victim),"both actual actors")
    if not valid(own) or not valid(victim) then return end
    local forward=signed(p:read_u16(own+0x90))<signed(p:read_u16(victim+0x90)) and "right" or "left"
    local back=forward=="right" and "left" or "right"
    if target=="kano" then
        pulse(side,"lk",age,180,81)
        if scenario=="block" then pulse(3-side,"block",age,220,180) end
        if scenario=="miss" then pulse(3-side,"down",age,220,180) end
    else
        pulse(side,forward,age,180);pulse(side,back,age,185);pulse(side,"hp",age,186)
        if scenario=="hit" then pulse(3-side,"up",age,193) end
        if scenario=="block" then pulse(3-side,"block",age,160,150) end
        if scenario=="miss" then pulse(3-side,forward,age,140,40) end
    end
    -- Actual subsequent native projectile action, not merely an idle sample.
    local followup=450
    pulse(side,"down",age,followup);pulse(side,target=="kano" and back or forward,age,followup+5)
    pulse(side,target=="kano" and "hp" or "lp",age,followup+6)
    for n,slot in ipairs(slots) do
        local actor,main=p:read_u32(slot.actor),p:read_u32(slot.main)
        check(valid(main) and p:read_u16(actor+0x1f0)==(config.names[n]=="kano" and 17 or 18) and p:read_u16(slot.state)==1,"canonical actual actor/controller")
        print(string.format("MK2_MOB_CONTACT_FIELD frame=%d age=%d slot=%d actor=%08X main=%08X id=%d roster=%d state=%d action=%04X pose=%08X hp=%d x=%d y=%d floor=%d xraw=%08X yraw=%08X vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X trail=%08X writes=0",
            frame,age,n,actor,main,p:read_u16(actor+0x1f0),p:read_u16(slot.id),p:read_u16(slot.state),p:read_u16(main+0x1f0),p:read_u32(actor+0x1d0),p:read_u16(slot.hp),
            signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),signed(p:read_u16(main+0x200)),p:read_u32(actor+0x80),p:read_u32(actor+0xa0),
            p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u32(actor+0x20),p:read_u16(main+0x210),p:read_u16(actor+0x160),p:read_u32(main+0x190)))
    end
    if start and (frame-start==8 or frame-start==18 or frame-start==40) then screen:snapshot("mob_contact_"..(frame-start)..".png") end
    if age==440 then screen:snapshot("mob_contact_ready.png") end
    if age==600 then
        check(counts.action==1 and counts.attack>0 and counts.recovery>0 and counts.projectile>0,"actual contact and subsequent native control")
        print(string.format("MK2_MOB_CONTACT_RESULT frame=%d pass=%s move=%s target=%s side=%d scenario=%s fields=601 errors=%d writes=0",frame,tostring(errors==0),move,target,side,scenario,errors))
        done=true;config.complete(frame,errors==0);manager.machine:exit()
    end
end
emu.register_frame(function()
    -- Program-space reads by Lua also invoke read taps. They are evidence
    -- collection, not CPU execution, and must not fabricate native events.
    collecting=true
    observe_and_drive()
    collecting=false
end)
emu.register_stop(function() for _,tap in ipairs(taps) do tap:remove() end end)
