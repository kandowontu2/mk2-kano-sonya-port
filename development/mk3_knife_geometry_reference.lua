-- Original MK3 reference: real inputs and read-only taps, no memory assistance.
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local frame,pulses,taps,collecting=0,{},{},false
local fields=manager.machine.ioport.ports[":IN0"].fields
local system=manager.machine.ioport.ports[":IN2"].fields
local scenario=os.getenv("MK3_KNIFE_GUARD") or "duck"
local sonya=os.getenv("MK3_PROJECTILE_TARGET")=="sonya"
local identity=sonya and 1 or 0
local low=manager.machine.ioport.ports[":IN1"].fields
local function pulse(field,first,hold) pulses[#pulses+1]={field,first,first+(hold or 4)} end
for base=360,1320,480 do
    pulse(system["Coin 1"],base);pulse(system["1 Player Start"],base+20)
    if sonya then pulse(fields["P1 Down"],base+240)
    else for _,age in ipairs({180,220,260}) do pulse(fields["P1 Right"],base+age) end end
    pulse(fields["P1 High Punch"],base+320)
end
for _,age in ipairs({2960,2980,3000}) do pulse(system["Coin 2"],age) end
pulse(system["2 Players Start"],3020)
if sonya then pulse(fields["P1 Down"],3090)
else for _,age in ipairs({3060,3090,3120}) do pulse(fields["P1 Right"],age) end end
pulse(fields["P1 High Punch"],3160);pulse(fields["P2 High Punch"],3180)
for _,first in ipairs({3900,4140}) do
    pulse(fields["P1 Down"],first,3);pulse(fields[sonya and "P1 Right" or "P1 Left"],first+5,3)
    pulse(sonya and low["P1 Low Punch"] or fields["P1 High Punch"],first+6,3)
    if scenario~="hit" then pulse(fields[scenario=="duck" and "P2 Down" or "P2 Block"],first-40,180) end
end
local function signed(x)return x>=0x8000 and x-0x10000 or x end
for kind,address in pairs({lookup=0xffa516c0,rectangle=0xffa5cc30}) do
    taps[#taps+1]=p:install_read_tap(address,address+15,"original knife "..kind,function(at)
        if at~=address or collecting or frame<3890 or frame>4400 or p:read_u16(cpu.A8.value+0x1f0)~=identity then return end
        print(string.format("MK3_KNIFE_GEOMETRY frame=%d kind=%s pc=%08X actor=%08X process=%08X a0=%08X a2=%08X a3=%08X a4=%08X a5=%08X x=%d y=%d writes=0",
            frame,kind,cpu.PC.value,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A2.value,cpu.A3.value,cpu.A4.value,cpu.A5.value,signed(p:read_u16(cpu.A8.value+0x90)),signed(p:read_u16(cpu.A8.value+0xb0))))
        if kind=="lookup" then
            print(string.format("MK3_KNIFE_DESCRIPTOR address=%08X edge=%d top=%d width=%d height=%d writes=0",cpu.A0.value,
                signed(p:read_u16(cpu.A0.value)),signed(p:read_u16(cpu.A0.value+16)),p:read_u16(cpu.A0.value+32),p:read_u16(cpu.A0.value+48)))
        end
    end)
end
for side,address in ipairs({0x01060a40,0x010615f0}) do
    taps[#taps+1]=p:install_write_tap(address,address+15,"original knife health",function(at,data)
        if at==address and frame>=3890 and p:read_u16(address)~=(data&0xffff) then
            print(string.format("MK3_KNIFE_HEALTH frame=%d slot=%d before=%d after=%d pc=%08X actor=%08X process=%08X writes=0",frame,side,p:read_u16(address),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value))
        end
    end)
end
emu.register_frame(function()
    collecting=true;frame=frame+1
    for _,v in ipairs(pulses) do if frame==v[2] then v[1]:set_value(1) end;if frame==v[3] then v[1]:set_value(0) end end
    if frame>=3890 and frame<=4400 then
        for side,address in ipairs({0x010609b0,0x01061560}) do
            local actor=p:read_u32(address)
            if actor>=0x01000000 and actor<0x01400000 then
                print(string.format("MK3_KNIFE_FIELD frame=%d slot=%d actor=%08X id=%d x=%d y=%d pose=%08X writes=0",frame,side,actor,p:read_u16(actor+0x1f0),signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0)),p:read_u32(actor+0x1d0)))
            end
        end
    end
    if frame==3100 or frame==3800 or frame==3930 or frame==3960 then manager.machine.screens[":screen"]:snapshot("knife_ref_"..frame..".png") end
    if frame==4500 then manager.machine:exit() end
    collecting=false
end)
emu.register_stop(function()for _,tap in ipairs(taps) do tap:remove() end end)
