-- Cold diagnostic; completed source endings are deliberately not claimed.
assert(os.getenv("MK2KS_TWO_PLAYER")~="1")
local target=assert(os.getenv("MK2KS_TEST_FIGHTER"))
local identity=target=="kano" and 17 or 18
local side=tonumber(os.getenv("MK2KS_MOBILITY_SIDE") or "1")
assert(side==1 or side==2)
if side==1 then dofile("mk2ks_selector_exit_test.lua") end
local joined=dofile("mk2ks_restart_lifecycle.lua")(target,side,{driver="mobility_contact"})
local p=manager.machine.devices[":maincpu"].spaces.program
local frame,match,started,css,route=0,nil,false,nil,{}
local slots={{actor=0x01060220,state=0x010601f0,id=0x01060280,hp=0x010602f0},
    {actor=0x01060df0,state=0x01060dc0,id=0x01060e50,hp=0x01060ec0}}
local fields=manager.machine.ioport.ports[":IN0"].fields
local system=manager.machine.ioport.ports[":IN1"].fields
local coords={[17]={0,0},[1]={1,0},[0]={2,0},[2]={3,0},[9]={4,0},[18]={5,0},
    [8]={1,1},[6]={2,1},[4]={3,1},[11]={4,1},[5]={1,2},[3]={2,2},[10]={3,2},[7]={4,2}}
emu.register_frame(function()
    frame=frame+1
    if side==2 and not match then
        for _,key in ipairs({"Up","Down","Left","Right","High Punch","Block"}) do fields["P2 "..key]:set_value(0) end
        local boot_age=(frame-600)%120
        system["Coin 2"]:set_value(frame>=600 and not css and (boot_age<5 or boot_age>=20 and boot_age<25) and 1 or 0)
        system["2 Players Start"]:set_value(frame>=600 and not css and boot_age>=40 and boot_age<45 and 1 or 0)
        if not css and frame>700 and p:read_u16(0x010601d0)==4 and p:read_u16(slots[2].state)==3 then
            css=frame
            local from,to=assert(coords[p:read_u16(slots[2].id)]),coords[identity]
            for _=1,from[2] do route[#route+1]="Up" end
            for _=1,math.abs(to[1]-from[1]) do route[#route+1]=to[1]<from[1] and "Left" or "Right" end
            for _=1,to[2] do route[#route+1]="Down" end
        end
        if css then
            local age=frame-css
            for index,key in ipairs(route) do local first=80+(index-1)*12;if age>=first and age<first+5 then fields["P2 "..key]:set_value(1) end end
            if age>=200 and age<208 then fields["P2 High Punch"]:set_value(1) end
        end
        if frame==3000 then print("MK2_MOB_COLD_ERROR actual P2 start timed out");manager.machine:exit() end
    end
    local own,other=slots[side],slots[3-side]
    local actor=p:read_u32(own.actor)
    if not match and p:read_u16(0x010601d0)==2 and p:read_u16(own.state)==1 and p:read_u16(other.state)==0 and
        p:read_u16(own.id)==identity and p:read_u16(own.hp)==161 and actor>=0x01000000 and actor<0x01100000 and p:read_u16(actor+0x1f0)==identity then
        match=frame;print("MK2_MOB_COLD_MATCH frame="..frame.." scope=cold_diagnosis_not_post_ending")
    end
    if match and not started and frame-match==600 then started=true;joined.begin(frame) end
    if started then joined.drive(frame)
    elseif match and frame-match>=100 then fields["P"..side.." Block"]:set_value(1) end
end)
