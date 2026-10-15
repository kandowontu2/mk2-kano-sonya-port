-- Physical held/released joystick reference. Never writes game/CPU state.
local classic=os.getenv('MK2_NAV_CLASSIC')=='1'
if not classic then dofile('mk2ks_native_shang_drain_startup.lua')else
    local main=assert(manager.machine.memory.regions[':maincpu']);local done=false
    emu.register_frame_done(function()
        if done then return end;done=true
        for offset=0,0xfffff,4096 do
            local hex={};for i=0,4095 do hex[#hex+1]=string.format('%02x',main:read_u8(offset+i))end
            print(string.format('MK2_DRAIN_STARTUP kind=high start=0 offset=%d bytes=4096 writes=0 assistance=none hex=%s',offset,table.concat(hex)))
        end
        print('MK2_DRAIN_STARTUP_COMPLETE writes=0 assistance=none')
    end)
end
local frame,css,exit_frame,hud_frame,combat=0,0,0,0,0
local fields,screen,program,pixels,width
local snapshots=0
local desired=classic and {1,9}or{17,18}
local function pixel(x,y)return string.unpack('<I4',pixels,(y*width+x)*4+1)&0xffffff end
local function header()
    local count,early=0,0
    for y=0,24,2 do for x=40,360,2 do
        local v=pixel(x,y);local r,g,b=(v>>16)&255,(v>>8)&255,v&255
        if r>175 and g>140 and b<100 then count=count+1;if y==4 then early=early+1 end end
    end end
    return count,early
end
local function hud()
    for _,left in ipairs({110,220})do
        local count=0
        for x=left,left+60 do
            local v=pixel(x,30);local r,g,b=(v>>16)&255,(v>>8)&255,v&255
            if(g>60 and g>r*3//2 and g>b*3//2)or(r>60 and r>g*3//2 and r>b*3//2)then count=count+1 end
        end
        if count<55 then return false end
    end
    return true
end
local function pulse(name,age,start)if age>=start and age<start+4 then fields[name]:set_value(1)end end
local function actor(side)
    local ptr=program:read_u32(side==1 and 0x01060220 or 0x01060df0)
    return ptr,ptr>=0x01000000 and ptr<0x01100000 and program:read_u16(ptr+0x1f0)or 0xffff
end
local function emit(label)
    snapshots=snapshots+1
    local ptr=program:read_u32(0x0105d480);local seen,n={},0
    while ptr~=0 do
        assert(ptr>=0x01000000 and ptr<0x01100000 and not seen[ptr]and n<240);seen[ptr]=true;n=n+1
        print(string.format('MK2_NAV_OBJECT seq=%d label=%s frame=%d order=%d actor=%08X z=%08X x=%04X y=%04X descriptor=%08X id=%04X next=%08X writes=0 assistance=none',
            snapshots,label,frame,n,ptr,program:read_u32(ptr+0xc0),program:read_u16(ptr+0x90),program:read_u16(ptr+0xb0),
            program:read_u32(ptr+0x1a0),program:read_u16(ptr+0x1f0),program:read_u32(ptr)))
        ptr=program:read_u32(ptr)
    end
    print(string.format('MK2_NAV_LIST_COMPLETE seq=%d label=%s frame=%d count=%d writes=0 assistance=none',snapshots,label,frame,n))
    local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400)
    print(string.format('MK2_NAV_FRAME seq=%d label=%s frame=%d width=400 height=254 bytes=406400 writes=0 assistance=none hex=%s',
        snapshots,label,frame,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local ports=manager.machine.ioport.ports;local high,low,system=ports[':IN0'].fields,ports[':IN2'].fields,ports[':IN1'].fields
        fields={coin=system['Coin 1'],coin2=system['Coin 2'],start=system['1 Player Start'],start2=system['2 Players Start'],
            hp=high['P1 High Punch'],p2hp=high['P2 High Punch'],lp=low['P1 Low Punch'],
            left=high['P1 Left'],right=high['P1 Right'],p2left=high['P2 Left'],p2right=high['P2 Right']}
        screen=manager.machine.screens[':screen'];program=manager.machine.devices[':maincpu'].spaces['program']
    end
    for _,field in pairs(fields)do field:clear_value()end
    if frame>=300 and frame<304 then fields.hp:set_value(1)end
    pixels,width=screen:pixels();assert(width==400 and #pixels==406400)
    if css==0 and frame>=600 then local age=(frame-600)%300;pulse('coin',age,0);pulse('coin2',age,8);pulse('start',age,20)end
    local yellow,early=header();local is_css=yellow>=400 and yellow<=430 and early>=10
    if css==0 and frame>700 and is_css then css=frame;print('MK2_HELD_CSS frame='..frame)end
    if css>0 and exit_frame==0 then
        local age=frame-css;pulse('coin',age,0);pulse('coin2',age,8);pulse('start2',age,20)
        local input1,input2='none','none'
        if age>=65 and age<113 then input1='right';input2='left'
        elseif age>=125 and age<173 then input1='left';input2='right'
        elseif(age>=185 and age<189)or(age>=197 and age<201)then input1='right';input2='left'
        elseif(age>=209 and age<213)or(age>=221 and age<225)then input1='left';input2='right'
        elseif age>=250 and age<346 and(age-250)%12<4 then
            if program:read_u16(0x01060280)~=desired[1]then input1='left'end
            if program:read_u16(0x01060e50)~=desired[2]then input2='right'end
        end
        if input1~='none'then fields[input1]:set_value(1)end
        if input2~='none'then fields['p2'..input2]:set_value(1)end
        if age>=60 and age<=360 then
            local a1,id1=actor(1);local a2,id2=actor(2)
            print(string.format('MK2_HELD_FIELD frame=%d age=%d p1=%d p2=%d actor1=%08X actor2=%08X actor_id1=%d actor_id2=%d input1=%s input2=%s css=%s writes=0 assistance=none',
                frame,age,program:read_u16(0x01060280),program:read_u16(0x01060e50),a1,a2,id1,id2,input1,input2,tostring(is_css)))
        end
        if age==60 or(age>=80 and age<=224 and(age-80)%16==0)or age==360 then emit('held_age'..age)end
        pulse('lp',age,370);pulse('p2hp',age,382)
        if age>96 and not is_css then exit_frame=frame;emit('css_exit')end
    end
    if exit_frame>0 and not is_css and hud()then
        if hud_frame==0 then hud_frame=frame;emit('match_hud')end
        local a1,id1=actor(1);local a2,id2=actor(2)
        if id1==desired[1]and id2==desired[2]and program:read_u16(0x01060280)==desired[1]and program:read_u16(0x01060e50)==desired[2]then combat=combat+1 end
        if frame==hud_frame+120 then emit('match_intro')end
    end
    if frame%600==0 then print(string.format('MK2_HELD_LIVE frame=%d css=%d exit=%d hud=%d combat=%d',frame,css,exit_frame,hud_frame,combat))end
end)
emu.register_stop(function()
    print(string.format('MK2_HELD_RESULT pass=%s classic=%s frame=%d css=%d exit=%d hud=%d combat=%d snapshots=%d writes=0 assistance=none',
        tostring(css>0 and exit_frame>0 and hud_frame>exit_frame and combat>600),tostring(classic),frame,css,exit_frame,hud_frame,combat,snapshots))
end)
