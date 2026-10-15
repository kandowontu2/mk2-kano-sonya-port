-- Physical selection navigation. All game, register and memory observations
-- are passive. No cheats, savestates, screenshots or forced combat outcomes.
dofile('mk2ks_native_shang_drain_startup.lua')
local plans = {
    assert(load(assert(os.getenv('MK2KS_NAV_P1')), 'physical-p1-plan', 't', {}))(),
    assert(load(assert(os.getenv('MK2KS_NAV_P2')), 'physical-p2-plan', 't', {}))()
}
local direction = assert(os.getenv('MK2KS_NAV_DIRECTION'))
local frame, css, exit_frame, hud_frame, combat_fields = 0, 0, 0, 0, 0
local fields, screen, program, pixels, width
local checks, errors, snapshots = 0, 0, 0
local ended = false
local roster = {0x01060280, 0x01060e50}
local actors = {0x01060220, 0x01060df0}
local finish_age = 65 + math.max(#plans[1], #plans[2]) * 12 + 16

local function pixel(x, y)
    return string.unpack('<I4', pixels, (y * width + x) * 4 + 1) & 0xffffff
end
local function header()
    local count, early = 0, 0
    for y=0,24,2 do for x=40,360,2 do
        local v=pixel(x,y);local r,g,b=(v>>16)&255,(v>>8)&255,v&255
        if r>175 and g>140 and b<100 then count=count+1;if y==4 then early=early+1 end end
    end end
    return count,early
end
local function hud()
    for _,left in ipairs({110,220}) do
        local count=0
        for x=left,left+60 do
            local v=pixel(x,30);local r,g,b=(v>>16)&255,(v>>8)&255,v&255
            if (g>60 and g>r*3//2 and g>b*3//2)or(r>60 and r>g*3//2 and r>b*3//2)then count=count+1 end
        end
        if count<55 then return false end
    end
    return true
end
local function pulse(name,age,start)
    if age>=start and age<start+4 then fields[name]:set_value(1)end
end
local function read_actor(side)
    local ptr=program:read_u32(actors[side])
    return ptr,ptr>=0x01000000 and ptr<0x01100000 and program:read_u16(ptr+0x1f0)or 0xffff
end
local function emit(label)
    snapshots=snapshots+1
    local ptr=program:read_u32(0x0105d480);local seen,n={},0
    while ptr~=0 do
        assert(ptr>=0x01000000 and ptr<0x01100000 and not seen[ptr]and n<240)
        seen[ptr]=true;n=n+1
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
        local ports=manager.machine.ioport.ports
        local high,system,low=ports[':IN0'].fields,ports[':IN1'].fields,ports[':IN2'].fields
        fields={coin=system['Coin 1'],coin2=system['Coin 2'],start=system['1 Player Start'],start2=system['2 Players Start'],
            hp=high['P1 High Punch'],p2hp=high['P2 High Punch'],lp=low['P1 Low Punch'],p2lp=low['P2 Low Punch']}
        for side=1,2 do for _,move in ipairs({'Up','Down','Left','Right'})do
            fields[(side==1 and ''or'p2')..move:lower()]=high['P'..side..' '..move]
        end end
        screen=manager.machine.screens[':screen'];program=manager.machine.devices[':maincpu'].spaces['program']
    end
    for _,field in pairs(fields)do field:clear_value()end
    if frame>=300 and frame<304 then fields.hp:set_value(1)end
    pixels,width=screen:pixels();assert(width==400 and #pixels==406400)
    if css==0 and frame>=600 then
        local age=(frame-600)%300;pulse('coin',age,0);pulse('coin2',age,8);pulse('start',age,20)
    end
    local yellow,early=header();local is_css=yellow>=400 and yellow<=430 and early>=10
    if css==0 and frame>700 and is_css then css=frame;print('MK2_NAV_CSS frame='..frame)end
    if css>0 and exit_frame==0 then
        local age=frame-css
        pulse('coin',age,0);pulse('coin2',age,8);pulse('start2',age,20)
        if age==60 then emit('initial_joined')end
        for side,plan in ipairs(plans)do
            local prefix=side==1 and ''or'p2'
            local index=(age-65)//12+1;local phase=(age-65)%12
            if index>=1 and index<=#plan then
                local step=plan[index]
                if phase<4 then fields[prefix..step[2]]:set_value(1)end
                if phase==10 then
                    local observed=program:read_u16(roster[side]);local ptr,id=read_actor(side)
                    local okay=is_css and observed==step[3]and id==step[3]
                    checks=checks+1;if not okay then errors=errors+1 end
                    print(string.format('MK2_NAV_STEP frame=%d age=%d side=%d index=%d origin=%d direction=%s expected=%d observed=%d actor=%08X actor_id=%d test=%s css=%s pass=%s writes=0 assistance=none',
                        frame,age,side,index,step[1],step[2],step[3],observed,ptr,id,tostring(step[4]),tostring(is_css),tostring(okay)))
                    if step[4]then emit('edge_p'..side..'_'..step[1]..'_'..step[2])end
                end
            end
        end
        pulse('lp',age,finish_age);pulse('p2hp',age,finish_age+12)
        if age>96 and not is_css then exit_frame=frame;emit('css_exit');print('MK2_NAV_EXIT frame='..frame..' age='..age)end
    end
    if exit_frame>0 and not is_css and hud()then
        if hud_frame==0 then hud_frame=frame;emit('native_match_hud')end
        local p1,id1=read_actor(1);local p2,id2=read_actor(2)
        if id1==17 and id2==18 and program:read_u16(roster[1])==17 and program:read_u16(roster[2])==18 then combat_fields=combat_fields+1 end
        if frame==hud_frame+120 then emit('native_match_intro')end
    end
    if frame%600==0 then print(string.format('MK2_NAV_LIVE frame=%d css=%d exit=%d hud=%d checks=%d errors=%d',frame,css,exit_frame,hud_frame,checks,errors))end
end)
emu.register_stop(function()
    if ended then return end;ended=true
    local wanted=#plans[1]+#plans[2]
    print(string.format('MK2_NAV_RESULT pass=%s direction=%s frame=%d css=%d exit=%d hud=%d checks=%d expected_checks=%d errors=%d combat_fields=%d snapshots=%d writes=0 assistance=none',
        tostring(css>0 and exit_frame>0 and hud_frame>exit_frame and checks==wanted and errors==0 and combat_fields>600),
        direction,frame,css,exit_frame,hud_frame,checks,wanted,errors,combat_fields,snapshots))
end)
