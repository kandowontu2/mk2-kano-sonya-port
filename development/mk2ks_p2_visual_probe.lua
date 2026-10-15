-- Read-only adjacent-frame evidence for the unusual Raiden-stage winner image.
dofile("mk2ks_p2_campaign_probe.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local screen=manager.machine.screens[":screen"]
local frame,start=0,nil
local taps={}
local fighter=assert(os.getenv("MK2KS_P2_FIGHTER"))
local id=fighter=="kano" and 17 or 18
local entry=0xfffef800+id*32
taps[1]=p:install_read_tap(entry,entry+15,"P2 native winner adjacent frames",function(at)
    if at==entry and p:read_u16(0x01061b30)==1 and p:read_u16(0x01060dc0)==1 and
        p:read_u16(0x010602f0)==0 and p:read_u16(0x01060ec0)>0 then
        start=frame
        print(string.format("MK2_P2_VISUAL_WIN frame=%d fighter=%s stage=1 pc=%08X",frame,fighter,cpu.PC.value))
    end
end)
emu.register_frame(function()
    frame=frame+1
    assert(#taps==1)
    if start then
        local age=frame-start
        if age==1 or age==20 or age==40 or age==60 or age==80 or age==100 or age==120 then
            screen:snapshot(string.format("p2_visual_%s_age_%03d.png",fighter,age))
            local pixels,width=screen:pixels()
            local colors={}
            for _,point in ipairs({{10,100},{200,100},{390,100},{200,200}}) do
                colors[#colors+1]=string.format("%06X",string.unpack("<I4",pixels,(point[2]*width+point[1])*4+1)&0xffffff)
            end
            print(string.format("MK2_P2_VISUAL_FRAME frame=%d age=%d fighter=%s stage=%d colors=%s",
                frame,age,fighter,p:read_u16(0x01061b30),table.concat(colors,",")))
        end
    end
end)
