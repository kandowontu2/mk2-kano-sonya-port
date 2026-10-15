-- ORIGINAL MK3 asset reference only. Not loaded by the port.
-- Explicit diagnostic assistance changes only the native attract BIO choice.
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local screen=manager.machine.screens[":screen"]
local fighter=os.getenv("MK3_BIO_FIGHTER") or "kano"
local identity=assert(({kano=0,sonya=1})[fighter])
local frame,ready,writes=0,nil,0
local taps={}
taps[1]=p:install_read_tap(0xff96ed50,0xff96ed5f,"original native bio choice",function(at)
    if at~=0xff96ed50 or ready then return end
    local old=p:read_u16(0x010623f0)
    p:write_u16(0x010623f0,identity)
    writes=writes+1
    print(string.format("MK3_BIO_CHOICE_ASSIST frame=%d old=%d new=%d address=010623F0",frame,old,identity))
end)
taps[2]=p:install_read_tap(0xff96f0f0,0xff96f0ff,"original completed native bio",function(at)
    if at~=0xff96f0f0 or ready then return end
    assert(p:read_u16(0x010623f0)==identity,"Original bio chooser did not retain fighter")
    ready=frame
    print(string.format("MK3_BIO_READY frame=%d fighter=%s identity=%d pc=%08X",frame,fighter,identity,cpu.PC.value))
end)
emu.register_frame(function()
    frame=frame+1
    assert(#taps==2,"Retain both original native asset observer handles")
    if frame==1 then
        print("MK3_BIO_REFERENCE assistance=attract_bio_choice_only port_loaded=false")
        local pointer=p:read_u32(0xff928740+13*48+16)
        print(string.format("MK3_BIO_BACKGROUND script=%08X",pointer))
        for index=0,31 do
            print(string.format("MK3_BIO_SCRIPT at=%08X value=%08X",pointer+index*32,p:read_u32(pointer+index*32)))
        end
    end
    if ready then
        local age=frame-ready
        if age==20 or age==120 or age==240 then
            screen:snapshot(string.format("mk3_bio_%s_%03d.png",fighter,age))
            print(string.format("MK3_BIO_CAPTURE frame=%d age=%d",frame,age))
        end
        if age==270 then manager.machine:exit() end
    end
end)
emu.register_stop(function()
    print(string.format("MK3_BIO_RESULT fighter=%s ready=%s choice_writes=%d frames=%d",fighter,tostring(ready),writes,frame))
end)
