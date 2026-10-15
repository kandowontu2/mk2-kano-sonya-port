-- Input-only joined projectile contacts; taps never return replacement data.
local config=assert(...)
assert(config.native_join)
local side=config.side
local target=config.names[side]
local move=target=="kano" and "knife" or "ring"
local scenario=os.getenv("MK2KS_PROJECTILE_CONTACT") or "hit"
assert(scenario=="hit" or scenario=="block" or scenario=="miss")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local screen=manager.machine.screens[":screen"]
local slots={{actor=0x01060220,main=0x01060260,hp=0x010602f0,id=0x01060280,state=0x010601f0},
    {actor=0x01060df0,main=0x01060e30,hp=0x01060ec0,id=0x01060e50,state=0x01060dc0}}
local parser=target=="kano" and 0xffffac00 or 0xffffae00
local action=target=="kano" and 0xffffb000 or 0xffffb400
local animation=target=="kano" and 0xff0004e0 or 0xff0204e0
local taps,epoch,frame,done,errors,collecting={},nil,0,false,0,false
local generation=0
local objects,processes,retired={},{},{}
local high,low=manager.machine.ioport.ports[":IN0"].fields,manager.machine.ioport.ports[":IN2"].fields
local controls={}
for n=1,2 do
    local label="P"..n.." "
    controls[n]={down=high[label.."Down"],left=high[label.."Left"],right=high[label.."Right"],hp=high[label.."High Punch"],block=high[label.."Block"],lp=low[label.."Low Punch"]}
end
local function valid(x) return x>=0x01000000 and x<0x01100000 end
local function signed(x) return x>=0x8000 and x-0x10000 or x end
local function check(ok,label)
    if not ok then errors=errors+1;if errors<20 then print("MK2_PROJ_CONTACT_ERROR frame="..frame.." "..label) end end
end
for kind,address in pairs({parser=parser,action=action,animation=animation,child=0xff8b6530,spawn=0xff8b5fb0,
    flight=0xff8afc10,release=0xff8afe00,collision=0xff8b6ac0,contact=0xff8b6a70,cleanup=0xff8b6820,
    reaction=0xff80f6b0,recovery=0xff861350,sound=0xffa12530}) do
    taps[#taps+1]=p:install_read_tap(address,address+15,"actual projectile "..kind,function(at)
        if at~=address or not epoch or collecting then return end
        local own,victim=p:read_u32(slots[side].actor),p:read_u32(slots[3-side].actor)
        local child=objects[generation]
        if kind=="parser" or kind=="action" or kind=="animation" or kind=="child" or kind=="spawn" then
            if cpu.A8.value~=own then return end
        elseif kind=="recovery" then
            if cpu.A8.value~=own and cpu.A8.value~=victim then return end
        elseif kind=="sound" then
            if cpu.A8.value~=own and cpu.A8.value~=child then return end
        elseif cpu.A8.value~=child then return end
        if kind=="action" then generation=generation+1 end
        if kind=="child" then objects[generation]=cpu.A10.value;child=objects[generation] end
        if kind=="spawn" then
            processes[generation]=cpu.A0.value
            print(string.format("MK2_PROJ_CONTACT_OWNER frame=%d age=%d cycle=%d child=%08X process=%08X actor_owner=%08X main_owner=%08X victim=%08X victim_main=%08X writes=0",
                frame,frame-epoch,generation,child or 0,cpu.A0.value,p:read_u32(cpu.A0.value+0x230),p:read_u32(cpu.A0.value+0x250),p:read_u32(cpu.A0.value+0x140),p:read_u32(cpu.A0.value+0x170)))
        end
        if kind=="cleanup" then retired[generation]=frame end
        print(string.format("MK2_PROJ_CONTACT_EVENT frame=%d age=%d cycle=%d kind=%s entry=%08X pc=%08X a0=%08X a1=%08X a2=%08X a3=%08X a6=%08X a8=%08X a9=%08X a10=%08X a11=%08X a13=%08X child=%08X process=%08X writes=0",
            frame,frame-epoch,generation,kind,address,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A6.value,cpu.A8.value,cpu.A9.value,cpu.A10.value,cpu.A11.value,cpu.A13.value,child or 0,processes[generation] or 0))
    end)
end
for n,slot in ipairs(slots) do
    taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,"original projectile health",function(at,data)
        if at~=slot.hp or not epoch then return end
        local before,after=p:read_u16(slot.hp),data&0xffff;if before==after then return end
        print(string.format("MK2_PROJ_CONTACT_HEALTH frame=%d age=%d cycle=%d slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X writes=0",
            frame,frame-epoch,generation,n,before,after,cpu.PC.value,cpu.A8.value,cpu.A13.value))
    end)
end
taps[#taps+1]=p:install_read_tap(0xff835b70,0xff835b7f,"native projectile rectangles",function(at)
    if at~=0xff835b70 or not epoch or collecting or cpu.A8.value~=objects[generation] then return end
    print(string.format("MK2_PROJ_CONTACT_GEOMETRY frame=%d age=%d cycle=%d child=%08X process=%08X victim_min=%08X victim_max=%08X attack_min=%08X attack_max=%08X writes=0",
        frame,frame-epoch,generation,cpu.A8.value,cpu.A13.value,cpu.A2.value,cpu.A3.value,cpu.A4.value,cpu.A5.value))
end)
local function pulse(n,key,age,first,hold)
    if age>=first and age<first+(hold or 3) then
        controls[n][key]:set_value(1)
        print(string.format("MK2_PROJ_CONTACT_CONTROL frame=%d age=%d slot=%d button=%s value=1 writes=0",frame,age,n,key))
    end
end
local function observe_and_drive()
    frame=config.now()
    if not config.active() or done then return end
    config.clear_controls()
    if not epoch then
        epoch=frame
        print(string.format("MK2_PROJ_CONTACT_BEGIN frame=%d target=%s side=%d move=%s scenario=%s writes=0",frame,target,side,move,scenario))
        local root=p:read_u32(animation)
        print(string.format("MK2_PROJ_CONTACT_ROM parser=%08X action=%08X animation=%08X first=%04X mask=%04X opcode=%04X root=%08X writes=0",parser,action,animation,p:read_u16(parser),p:read_u16(parser+16),p:read_u16(action),root))
        for i=0,9 do print(string.format("MK2_PROJ_CONTACT_POSE index=%d value=%08X writes=0",i,p:read_u32(root+i*32))) end
        local attack_root=p:read_u32(0xfffe6000+(target=="kano" and 17 or 18)*32)
        for i=0,3 do
            local desc=p:read_u32(attack_root+(16+i)*32)
            print(string.format("MK2_PROJ_CONTACT_DESCRIPTOR phase=%d address=%08X edge=%d top=%d width=%d height=%d reaction=%04X damage=%04X writes=0",
                i,desc,signed(p:read_u16(desc)),signed(p:read_u16(desc+16)),p:read_u16(desc+32),p:read_u16(desc+48),p:read_u16(desc+64),p:read_u16(desc+80)))
        end
        for _,i in ipairs({0,1,2,3,5,6}) do
            local group=p:read_u32(root+i*32)
            local component=p:read_u32(group)
            print(string.format("MK2_PROJ_CONTACT_COMPONENT index=%d group=%08X address=%08X width=%d height=%d dx=%d dy=%d writes=0",
                i,group,component,p:read_u16(component),p:read_u16(component+16),signed(p:read_u16(component+32)),signed(p:read_u16(component+48))))
        end
        local checksum=0x811c9dc5
        for at=0xff8eba90,0xff8f3bd0,16 do checksum=((checksum~p:read_u16(at))*0x01000193)&0xffffffff end
        print(string.format("MK2_PROJ_CONTACT_STOCK start=%08X finish=%08X checksum=%08X writes=0",0xff8eba90,0xff8f3be0,checksum))
    end
    local age=frame-epoch
    local own,victim=p:read_u32(slots[side].actor),p:read_u32(slots[3-side].actor)
    check(valid(own) and valid(victim),"two actual fighters")
    if not valid(own) or not valid(victim) then return end
    local forward=signed(p:read_u16(own+0x90))<signed(p:read_u16(victim+0x90)) and "right" or "left"
    local direction=target=="sonya" and forward or (forward=="right" and "left" or "right")
    for _,first in ipairs({180,380}) do
        pulse(side,"down",age,first);pulse(side,direction,age,first+5);pulse(side,target=="kano" and "hp" or "lp",age,first+6)
        if scenario=="block" then pulse(3-side,"block",age,first-20,160) end
        if scenario=="miss" then pulse(3-side,"down",age,first-20,160) end
    end
    for n,slot in ipairs(slots) do
        local actor,main=p:read_u32(slot.actor),p:read_u32(slot.main)
        check(valid(main),"native main")
        print(string.format("MK2_PROJ_CONTACT_FIELD frame=%d age=%d slot=%d actor=%08X main=%08X id=%d roster=%d state=%d action=%04X pose=%08X hp=%d x=%d y=%d floor=%d xraw=%08X yraw=%08X vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X trail=%08X writes=0",
            frame,age,n,actor,main,p:read_u16(actor+0x1f0),p:read_u16(slot.id),p:read_u16(slot.state),p:read_u16(main+0x1f0),p:read_u32(actor+0x1d0),p:read_u16(slot.hp),
            signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),signed(p:read_u16(main+0x200)),p:read_u32(actor+0x80),p:read_u32(actor+0xa0),
            p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u32(actor+0x20),p:read_u16(main+0x210),p:read_u16(actor+0x160),p:read_u32(main+0x190)))
    end
    for cycle,child in pairs(objects) do
        local process=processes[cycle]
        if valid(child) and not retired[cycle] and process and valid(process) then
            local desc=p:read_u32(process+0x100)
            local component=p:read_u32(child+0x1a0)
            local cx,cy=signed(p:read_u16(child+0x90)),signed(p:read_u16(child+0xb0))
            local cw,ch=p:read_u16(component+0x20),p:read_u16(component+0x30)
            local dx,dy=signed(p:read_u16(component+0x50)),signed(p:read_u16(component+0x60))
            print(string.format("MK2_PROJ_CONTACT_RENDER frame=%d age=%d cycle=%d component=%08X width=%d height=%d dx=%d dy=%d left=%d top=%d right=%d bottom=%d writes=0",
                frame,age,cycle,component,cw,ch,dx,dy,cx-dx,cy-dy,cx-dx+cw,cy-dy+ch))
            print(string.format("MK2_PROJ_CONTACT_EFFECT frame=%d age=%d cycle=%d child=%08X process=%08X id=%d type=%d actor_owner=%08X velocity_parameter=%08X parent_child=%08X action=%04X pose=%08X x=%d y=%d xraw=%08X yraw=%08X vx=%08X vy=%08X flags=%04X palette=%08X descriptor=%08X damage=%04X writes=0",
                frame,age,cycle,child,process,p:read_u16(child+0x1f0),p:read_u16(child+0xc0),p:read_u32(process+0x230),p:read_u32(process+0x250),p:read_u32(p:read_u32(slots[side].main)+0x190),
                p:read_u16(process+0x1f0),p:read_u32(child+0x1d0),signed(p:read_u16(child+0x90)),signed(p:read_u16(child+0xb0)),p:read_u32(child+0x80),p:read_u32(child+0xa0),p:read_u32(child+0x40),p:read_u32(child+0x60),p:read_u16(child+0xf0),p:read_u32(child+0x1c0),desc,
                desc>=0xff800000 and p:read_u16(desc+80) or 0))
        end
    end
    if age==200 or age==210 or age==225 or age==410 or age==440 or age==560 then screen:snapshot("proj_contact_"..age..".png") end
    if age==600 then
        check(generation==2 and retired[1] and retired[2],"two actual spawned/retired projectiles")
        print(string.format("MK2_PROJ_CONTACT_RESULT frame=%d pass=%s target=%s side=%d move=%s scenario=%s cycles=%d fields=601 errors=%d writes=0",frame,tostring(errors==0),target,side,move,scenario,generation,errors))
        done=true;config.complete(frame,errors==0);manager.machine:exit()
    end
end
emu.register_frame(function() collecting=true;observe_and_drive();collecting=false end)
emu.register_stop(function() for _,tap in ipairs(taps) do tap:remove() end end)
