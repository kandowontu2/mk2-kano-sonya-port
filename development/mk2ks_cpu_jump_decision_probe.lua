-- Natural cold P2-human/P1-CPU ladder. Inputs only; CPU choices are never supplied.
for _,name in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
    assert(not os.getenv(name),'Natural pair probe cannot use '..name)
end
-- Cold P2-only campaign: real coin/start/selection inputs, never a joined proxy.
local selection_frame,selection_css,selection_exit,selection_checks,selection_errors=0,nil,nil,0,0
local human=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local human_id=assert(({kano=17,sonya=18,liu_kang=1,cage=2,baraka=3,kitana=4,
    kung_lao=0,mileena=5,shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11})[human])
local routes={sonya={'Right'},kano={'Left','Left','Left','Left'},liu_kang={'Left','Left','Left'},
    cage={'Left'},kung_lao={'Left','Left'},reptile={},jax={'Down'},kitana={'Left','Down'},
    shang_tsung={'Left','Left','Down'},sub_zero={'Left','Left','Left','Down'},
    raiden={'Down','Down'},scorpion={'Left','Down','Down'},baraka={'Left','Left','Down','Down'},
    mileena={'Left','Left','Left','Down','Down'}}
local boot=tonumber(os.getenv('MK2KS_TEST_BOOT_FRAME')or'601')
assert(boot>=600 and boot<=1500)
local selection_p=manager.machine.devices[':maincpu'].spaces.program
local high,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local selection_inputs={system['Coin 2'],system['2 Players Start'],high['P2 High Punch'],
    high['P2 Left'],high['P2 Right'],high['P2 Up'],high['P2 Down'],high['P2 Block']}
local initial_cpu,first_live=nil,nil
emu.register_frame(function()
    selection_frame=selection_frame+1
    for _,field in ipairs(selection_inputs)do field:clear_value()end
    if selection_frame>=300 and selection_frame<304 then high['P2 High Punch']:set_value(1)end
    local pixels,width=manager.machine.screens[':screen']:pixels()
    local yellow,early=0,0
    if width==400 and #pixels>=400*254*4 then
        for y=0,24,2 do for x=40,360,2 do
            local rgb=string.unpack('<I4',pixels,(y*width+x)*4+1)
            local r,g,b=(rgb>>16)&255,(rgb>>8)&255,rgb&255
            if r>175 and g>140 and b<100 then yellow=yellow+1;if y==4 then early=early+1 end end
        end end
    end
    local css=yellow>=400 and yellow<=430 and early>=10
    if not selection_css and selection_frame>=boot then
        local age=(selection_frame-boot)%300
        if age<4 then system['Coin 2']:set_value(1)end
        if age>=20 and age<24 then system['2 Players Start']:set_value(1)end
    end
    if not selection_css and selection_frame>700 and css then
        selection_css=selection_frame
        print(string.format('MK2_P1CPU_SELECT_CSS frame=%d human=%s slot=2 yellow=%d early=%d writes=0 assistance=none',selection_frame,human,yellow,early))
    end
    if selection_css and not selection_exit then
        local age=selection_frame-selection_css
        for index,direction in ipairs(routes[human])do
            local at=12+(index-1)*12
            if age>=at and age<at+4 then high['P2 '..direction]:set_value(1)end
        end
        if age>=65 and age<=103 then
            selection_checks=selection_checks+1
            if selection_p:read_u16(0x01060e50)~=human_id then selection_errors=selection_errors+1 end
        end
        if age==65 or age==81 then manager.machine.screens[':screen']:snapshot('p2_selection_'..age..'.png')end
        if age>=96 and age<104 then high['P2 High Punch']:set_value(1)end
        if age>96 and not css then
            selection_exit=selection_frame
            manager.machine.screens[':screen']:snapshot('p2_selection_exit.png')
        end
    end
    if selection_frame%120==0 then
        print(string.format('MK2_P1CPU_BOOT_STATE frame=%d mode=%d states=%d,%d roster=%d,%d stage=%d schedule=%08X writes=0 assistance=none',
            selection_frame,selection_p:read_u16(0x010601d0),selection_p:read_u16(0x010601f0),
            selection_p:read_u16(0x01060dc0),selection_p:read_u16(0x01060280),selection_p:read_u16(0x01060e50),
            selection_p:read_u16(0x01061b30),selection_p:read_u32(0x01061b10)))
    end
    if selection_exit and not first_live and selection_p:read_u16(0x010601d0)==2 and
        selection_p:read_u16(0x010601f0)==0 and selection_p:read_u16(0x01060dc0)==1 then
        first_live=selection_frame;initial_cpu=selection_p:read_u16(0x01060280)
        print(string.format('MK2_P1CPU_COLD_LIVE frame=%d human=%s human_id=%d cpu_id=%d stage=%d schedule=%08X writes=0 assistance=none',
            first_live,human,human_id,initial_cpu,selection_p:read_u16(0x01061b30),selection_p:read_u32(0x01061b10)))
        manager.machine.screens[':screen']:snapshot('p2_cold_cpu_fight.png')
    end
end)
emu.register_stop(function()
    print(string.format('MK2_P1CPU_SELECT_RESULT human=%s human_id=%d css=%d exit=%d live=%d initial_cpu=%d checks=%d errors=%d writes=0 assistance=none',
        human,human_id,selection_css or -1,selection_exit or -1,first_live or -1,initial_cpu or -1,selection_checks,selection_errors))
end)
local p=manager.machine.devices[':maincpu'].spaces.program
local regs=manager.machine.devices[':maincpu'].state
local fields={}
for _,port in ipairs({':IN0',':IN2'})do for key,field in pairs(manager.machine.ioport.ports[port].fields)do fields[key]=field end end
local frame,events,actions=0,0,0
local strategy=os.getenv('MK2KS_AIR_STRATEGY')or'jump'
assert(strategy=='projectile'or strategy=='retreat')
local taps={}
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
             {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(slot)
    local a,m=p:read_u32(slot.actor),p:read_u32(slot.main)
    if not valid(a)or not valid(m)then return end
    return {actor=a,main=m,id=p:read_u16(a+0x1f0),roster=p:read_u16(slot.id),
        owner=p:read_u32(m+0xc0),state=p:read_u16(slot.state),action=p:read_u16(m+0x1f0),
        x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
        vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),
        pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),body=p:read_u16(a+0x160),hp=p:read_u16(slot.hp)}
end
local function live()
    local a,b=sample(slots[1]),sample(slots[2])
    if p:read_u16(0x010601d0)==2 and a and b and a.state==0 and b.state==1 then return a,b end
end
local function log(tag,a,b,extra)
    local function part(s,prefix)
        local items={}
        for _,key in ipairs({'actor','main','owner','vx','vy','gravity','pose','flags','body'})do items[#items+1]=string.format('%s%s=%08X',prefix,key,s[key])end
        for _,key in ipairs({'id','roster','state','action','x','y','floor','hp'})do items[#items+1]=string.format('%s%s=%d',prefix,key,s[key])end
        return table.concat(items,' ')
    end
    print(string.format('MK2_CPU_AIR_%s frame=%d %s %s %s cpu_slot=1 human_slot=2 writes=0 assistance=none',tag,frame,part(a,'c'),part(b,'h'),extra or''))
end
for _,address in ipairs({0xff9beef0,0xff9bef40,0xff9bf050,0xff9bf1c0,0xff8b6ff0,0xff861500,
    0xfffff580,0xfffff980,0xfffc2000,0xfffc8700,0xfffc8780,0xfffc87b0,0xff9becd0,0xff9c8180,0xff9c8170,0xff9c7b20,0xff9c7910,0xff9c77b0,0xff9c7cf0,0xff9c8260,0xff9bea10,0xff9be790})do
    taps[#taps+1]=p:install_read_tap(address,address+15,'CPU aerial provenance',function(at,data)
        if regs.PC.value~=address+16 then return end
        local a,b=live();if not a then return end
        if address==0xff861500 and (regs.A8.value~=a.actor and regs.A8.value~=b.actor)then return end
        events=events+1
        if address==0xff8b6ff0 then actions=actions+1;manager.machine.screens[':screen']:snapshot('cpu_air_action_'..actions..'.png')end
        log('EVENT',a,b,string.format('entry=%08X pc=%08X a0=%08X a1=%08X a3=%08X a6=%08X a8=%08X a10=%08X a13=%08X',address,regs.PC.value,regs.A0.value,regs.A1.value,regs.A3.value,regs.A6.value,regs.A8.value,regs.A10.value,regs.A13.value))
    end)
end
local lookups=0
taps[#taps+1]=p:install_read_tap(0xff83b840,0xff83b84f,'native indexed CPU callback',function(at,data)
    if regs.PC.value~=0xff83b850 or regs.A1.value<0xff9b0000 or regs.A1.value>=0xff9d0000 then return end
    local a,b=live();if not a or lookups>=3000 then return end
    lookups=lookups+1
    log('LOOKUP',a,b,string.format('pc=%08X table=%08X row=%08X a8=%08X a13=%08X',regs.PC.value,regs.A1.value,regs.A0.value,regs.A8.value,regs.A13.value))
end)
for side,slot in ipairs(slots)do
    taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'native aerial health',function(at,data,mask)
        local a,b=live();if not a or mask~=0xffff then return end
        log('HEALTH',a,b,string.format('slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X',side,p:read_u16(at),data&0xffff,regs.PC.value,regs.A8.value,regs.A13.value))
    end)
end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        for _,range in ipairs({{0xff9beef0,0xff9bf2c0},{0xfffc8700,0xfffc8800}})do
            local words={}
            for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
            print(string.format('MK2_CPU_AIR_ROM start=%08X stop=%08X words=%s writes=0 assistance=none',range[1],range[2],table.concat(words,',')))
        end
        print('MK2_CPU_AIR_STRATEGY strategy='..strategy..' writes=0 assistance=none')
    end
    local a,b=live();if not a then return end
    fields['P2 Left']:set_value(0);fields['P2 Right']:set_value(0);fields['P2 Up']:set_value(0)
    log('FIELD',a,b,string.format('stage=%d schedule=%08X',p:read_u16(0x01061b30),p:read_u32(0x01061b10)))
    fields['P2 Down']:set_value(0);fields['P2 Low Punch']:set_value(0);fields['P2 Block']:set_value(0)
    if b.hp>0 and a.hp>0 and b.y==b.floor and b.vy==0 and b.gravity==0 and b.flags&0x1c==0 and b.body&0x0c==0 then
        local forward=b.x<a.x and 'Right' or'Left'
        local backward=b.x<a.x and 'Left' or'Right'
        local gap=math.abs(a.x-b.x)
        local keys={}
        if a.y<a.floor and gap<160 then
            keys={'Up',forward}
        elseif gap<200 then
            keys={backward}
        elseif strategy=='projectile' then
            local age=frame%120
            if age<4 then keys={'Down'}
            elseif age>=6 and age<10 then keys={forward}
            elseif age>=12 and age<16 then keys={'Low Punch'}end
        elseif frame%120<4 then
            keys={'Up'}
        end
        for _,key in ipairs(keys)do fields['P2 '..key]:set_value(1)end
        if #keys>0 then log('INPUT',a,b,'buttons='..table.concat(keys,'+'))end
    end
    if actions>0 and frame%30==0 then manager.machine.screens[':screen']:snapshot('cpu_air_field_'..frame..'.png')end
end)
emu.register_stop(function()
    print(string.format('MK2_CPU_AIR_RESULT schema=1 events=%d actions=%d writes=0 assistance=none scope=diagnostic_not_full_pair_acceptance',events,actions))
    for _,tap in ipairs(taps)do tap:remove()end
end)







