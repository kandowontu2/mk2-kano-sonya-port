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
local cpu=manager.machine.devices[':maincpu'].state
local fields=manager.machine.ioport.ports[':IN0'].fields
local frame,cycle,complete=0,0,nil
local taps,cycles={},{}
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
             {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local specs={
    [17]={target='kano',action=0xfff91400,intro=0xfff94000,attack=0xfff94800,release=0xfff93800,pulse=0xfff93400,steps=22,damage=32,state=0x111},
    [18]={target='sonya',action=0xfff80800,intro=0xfff83000,attack=0xfff83800,release=0xfff82200,steps=5,damage=35,state=0x110}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(slot)
    local a,m=p:read_u32(slot.actor),p:read_u32(slot.main)
    if not valid(a) or not valid(m)then return end
    return {actor=a,main=m,id=p:read_u16(a+0x1f0),roster=p:read_u16(slot.id),state=p:read_u16(slot.state),owner=p:read_u32(m+0xc0),
        action=p:read_u16(m+0x1f0),pose=p:read_u32(a+0x1d0),list=p:read_u32(a+0x1a0),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
        xraw=p:read_u32(a+0x80),yraw=p:read_u32(a+0xa0),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),
        flags=p:read_u16(m+0x210),body=p:read_u16(a+0x160),facing=p:read_u16(a+0xf0),trail=p:read_u32(m+0x190),hp=p:read_u16(slot.hp)}
end
local function live()
    local own,v=sample(slots[1]),sample(slots[2])
    if p:read_u16(0x010601d0)==2 and own and v and own.state==0 and v.state==1 and own.roster==own.id and v.roster==v.id and specs[own.id] then return own,v end
end
local function same(c,s,v)return c and c.actor==s.actor and c.main==s.main and c.victim==v.actor and c.vmain==v.main end
local function log(tag,text)print(string.format('MK2_CPU_PAIR_%s frame=%d cycle=%d %s cpu_slot=1 human_slot=2 writes=0 assistance=none',tag,frame,cycle,text))end
local function state(tag,s,v)
    local function part(a,prefix)
        local text={}
        for _,key in ipairs({'actor','main','owner','pose','list','xraw','yraw','vx','vy','gravity','flags','body','facing','trail'})do text[#text+1]=string.format('%s%s=%08X',prefix,key,a[key])end
        for _,key in ipairs({'id','roster','state','action','x','y','floor','hp'})do
            local suffix=prefix=='v' and (key=='x' or key=='y')and key..'pos' or key
            text[#text+1]=string.format('%s%s=%d',prefix,suffix,a[key])
        end
        return table.concat(text,' ')
    end
    log(tag,part(s,'')..' '..part(v,'v')..string.format(' mode=%d stage=%d schedule=%08X suppression=%d left=%d right=%d',p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u32(0x01061b10),p:read_u16(0x010619d0),p:read_i16(0x0105ecf0)+0x3a,p:read_i16(0x0105ed00)+0x15f))
end
local function clean(a)
    local vx=a.vx>=0x80000000 and a.vx-0x100000000 or a.vx
    return a.y==a.floor and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 and a.body&0x0c==0 and a.trail==0 and (vx==0 or a.action==0x303 and math.abs(vx)<=0x30000)
end
local entries={step=0xfff89400,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,recovery=0xff861350}
for id,spec in pairs(specs)do for _,kind in ipairs({'action','intro','attack','release','pulse'})do if spec[kind]then entries[kind..'_'..id]=spec[kind]end end end
for entry_kind,address in pairs(entries)do
    taps[#taps+1]=p:install_read_tap(address,address+15,'actual native CPU pair '..entry_kind,function(at,data)
        local descriptor=entry_kind:match('^intro_')or entry_kind:match('^attack_')
        if at~=address or(not descriptor and cpu.PC.value~=address+16)or(descriptor and cpu.PC.value<0xff800000)then return end
        local s,v=live();if not s then return end
        local kind=entry_kind:match('^(%a+)');local spec=specs[s.id]
        local requested=tonumber(entry_kind:match('_(%d+)$'));if requested and requested~=s.id then return end
        if kind=='action' then
            if cpu.A8.value~=s.actor or cpu.A13.value~=s.main then return end
            cycle=cycle+1;cycles[cycle]={start=frame,actor=s.actor,main=s.main,victim=v.actor,vmain=v.main,id=s.id,steps=0,damage=0,pulses=0}
            state('ENTRY',s,v)
        end
        local c=cycles[cycle];if not same(c,s,v)or c.closed then return end
        if kind=='intro' or kind=='attack' or kind=='step' or kind=='action'then
            if cpu.A8.value~=s.actor or cpu.A13.value~=s.main then return end
            if kind=='step'then
                if s.action~=spec.state or p:read_u32(cpu.A9.value)==0 then return end
                c.steps=c.steps+1;c.paired=c.paired or frame
                manager.machine.screens[':screen']:snapshot(string.format('cpu_pair_%d_step_%d.png',cycle,c.steps))
            end
        elseif kind=='recovery'then
            if cpu.A8.value==s.actor and cpu.A13.value==s.main then kind='own_ready';c.own_ready=c.own_ready or frame
            elseif cpu.A8.value==v.actor and cpu.A13.value==v.main and c.release then kind='victim_ready';c.victim_ready=c.victim_ready or frame
            else return end
        else
            if not c.paired or cpu.A8.value~=v.actor then return end
            if kind=='release'then c.release=frame
            elseif kind=='pulse'then c.pulses=c.pulses+1
            elseif kind=='damage' and s.id==18 and not c.release then return end
        end
        log('EVENT',string.format('kind=%s entry=%08X pc=%08X actor=%08X main=%08X victim=%08X vmain=%08X a8=%08X a13=%08X a0=%08X a1=%08X a2=%08X a3=%08X a9=%08X a10=%08X group=%08X word=%04X steps=%d',kind,address,cpu.PC.value,s.actor,s.main,v.actor,v.main,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A9.value,cpu.A10.value,kind=='step' and p:read_u32(cpu.A9.value)or 0,descriptor and(data&0xffff)or 0,c.steps))
    end)
end
for side,slot in ipairs(slots)do
    taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'CPU pair health ledger',function(at,data,mask)
        if mask~=0xffff then return end
        local s,v=live();if not s then return end
        local c=cycles[cycle];local before,after=p:read_u16(at),data&0xffff
        log('HEALTH',string.format('slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X',side,before,after,cpu.PC.value,cpu.A8.value,cpu.A13.value))
        if side==2 and same(c,s,v)and c.paired and not c.closed then c.damage=c.damage+before-after end
    end)
end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        for order=0,5 do
            local roster_table=p:read_u32(0xff8a11f0);local list=p:read_u32(roster_table+order*32);local ids={}
            for n=0,16 do ids[#ids+1]=p:read_u16(list+n*16)end
            log('ROM',string.format('table=%08X order=%d list=%08X ids=%s',roster_table,order,list,table.concat(ids,',')))
        end
    end
    local s,v=live();if not s then return end
    state('FIELD',s,v)
    fields['P2 Left']:set_value(0);fields['P2 Right']:set_value(0)
    local c=cycles[cycle]
    if same(c,s,v) and not c.closed and c.own_ready and c.victim_ready and clean(s)and clean(v)then
        c.closed=true
        if c.steps==specs[s.id].steps and c.damage==specs[s.id].damage and c.release and (s.id~=17 or c.pulses==4)then
            state('COMPLETE',s,v);complete=frame
            manager.machine.screens[':screen']:snapshot('cpu_pair_complete.png')
        else state('INCOMPLETE',s,v)end
    end
    if complete then
        fields['P2 Block']:set_value(1)
        if frame>=complete+30 then manager.machine:exit()end
    elseif same(c,s,v) and c.victim_ready and v.hp>0 and s.hp>0 and
        v.y==v.floor and v.vy==0 and v.gravity==0 and v.flags&0x1c==0 and
        v.body&0x0c==0 and v.trail==0 and math.abs(s.x-v.x)<170 then
        -- A genuine recovered human backstep leaves the CPU free to choose its
        -- next action. Do not alter its guard, velocity, timer or readiness.
        local direction=v.x<s.x and 'Left' or 'Right'
        fields['P2 '..direction]:set_value(1)
        log('INPUT',string.format('buttons=%s gap=%d phase=recovered_backstep',direction,math.abs(s.x-v.x)))
    elseif not c or c.closed or not c.paired then
        if v.hp>0 and s.hp>0 and clean(v) and math.abs(s.x-v.x)>76 then
            fields['P2 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)
            log('INPUT',string.format('buttons=%s gap=%d',v.x<s.x and 'Right' or 'Left',math.abs(s.x-v.x)))
        end
    end
end)
emu.register_stop(function()
    log('RESULT',string.format('schema=3 cycles=%d complete=%d scope=natural_P1_CPU_paired_trace_not_all_victims_pixels_audio_or_full_goal',cycle,complete or -1))
    for _,tap in ipairs(taps)do tap:remove()end
end)
