-- Reusable input-only cold P2 selection; no guest writes or joined proxy.
for _,name in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
    assert(not os.getenv(name),'Natural selection cannot use '..name)
end
local frame,css_at,exit_at,checks,errors,first_live,initial_cpu=0,nil,nil,0,0,nil,nil
local human=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local identity=assert(({kano=17,sonya=18,liu_kang=1,cage=2,baraka=3,kitana=4,kung_lao=0,mileena=5,shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11})[human])
local routes={sonya={'Right'},kano={'Left','Left','Left','Left'},liu_kang={'Left','Left','Left'},cage={'Left'},kung_lao={'Left','Left'},reptile={},jax={'Down'},kitana={'Left','Down'},shang_tsung={'Left','Left','Down'},sub_zero={'Left','Left','Left','Down'},raiden={'Down','Down'},scorpion={'Left','Down','Down'},baraka={'Left','Left','Down','Down'},mileena={'Left','Left','Left','Down','Down'}}
local boot=tonumber(os.getenv('MK2KS_TEST_BOOT_FRAME')or'604');assert(boot>=600 and boot<=1500)
local p=manager.machine.devices[':maincpu'].spaces.program
local high,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local inputs={system['Coin 2'],system['2 Players Start'],high['P2 High Punch'],high['P2 Left'],high['P2 Right'],high['P2 Up'],high['P2 Down'],high['P2 Block']}
emu.register_frame(function()
    frame=frame+1;for _,field in ipairs(inputs)do field:clear_value()end
    if frame>=300 and frame<304 then high['P2 High Punch']:set_value(1)end
    local pixels,width=manager.machine.screens[':screen']:pixels();local yellow,early=0,0
    if width==400 and #pixels>=400*254*4 then
        for y=0,24,2 do for x=40,360,2 do
            local rgb=string.unpack('<I4',pixels,(y*width+x)*4+1)
            if ((rgb>>16)&255)>175 and ((rgb>>8)&255)>140 and (rgb&255)<100 then yellow=yellow+1;if y==4 then early=early+1 end end
        end end
    end
    local css=yellow>=400 and yellow<=430 and early>=10
    if not css_at and frame>=boot then
        local age=(frame-boot)%300
        if age<4 then system['Coin 2']:set_value(1)end
        if age>=20 and age<24 then system['2 Players Start']:set_value(1)end
    end
    if not css_at and frame>700 and css then
        css_at=frame;print(string.format('MK2_P1CPU_SELECT_CSS frame=%d human=%s slot=2 yellow=%d early=%d writes=0 assistance=none',frame,human,yellow,early))
    end
    if css_at and not exit_at then
        local age=frame-css_at
        for i,direction in ipairs(routes[human])do local at=12+(i-1)*12;if age>=at and age<at+4 then high['P2 '..direction]:set_value(1)end end
        if age>=65 and age<=103 then checks=checks+1;if p:read_u16(0x01060e50)~=identity then errors=errors+1 end end
        if age==65 or age==81 then manager.machine.screens[':screen']:snapshot('p2_selection_'..age..'.png')end
        if age>=96 and age<104 then high['P2 High Punch']:set_value(1)end
        if age>96 and not css then exit_at=frame;manager.machine.screens[':screen']:snapshot('p2_selection_exit.png')end
    end
    if exit_at and not first_live and p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==0 and p:read_u16(0x01060dc0)==1 then
        first_live=frame;initial_cpu=p:read_u16(0x01060280)
        print(string.format('MK2_P1CPU_COLD_LIVE frame=%d human=%s human_id=%d cpu_id=%d stage=%d schedule=%08X writes=0 assistance=none',frame,human,identity,initial_cpu,p:read_u16(0x01061b30),p:read_u32(0x01061b10)))
        manager.machine.screens[':screen']:snapshot('p2_cold_cpu_fight.png')
    end
end)
emu.register_stop(function()
    print(string.format('MK2_P1CPU_SELECT_RESULT human=%s human_id=%d css=%d exit=%d live=%d initial_cpu=%d checks=%d errors=%d writes=0 assistance=none',human,identity,css_at or-1,exit_at or-1,first_live or-1,initial_cpu or-1,checks,errors))
end)
return {frame=function()return frame end,first_live=function()return first_live end,initial_cpu=function()return initial_cpu end}
