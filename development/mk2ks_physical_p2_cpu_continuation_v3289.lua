-- Natural cold P1-human/P2-CPU ladder. Inputs only; CPU choices are never supplied.
for _,name in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
    assert(not os.getenv(name),'Natural pair probe cannot use '..name)
end
-- Physical roles remain explicit: every flag/health slot is the real machine slot.
local cpu_slot,human_slot=2,1
local selection_frame,selection_css,selection_exit,selection_checks,selection_errors=0,nil,nil,0,0
local human=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local human_id=assert(({kano=17,sonya=18,liu_kang=1,cage=2,baraka=3,kitana=4,
    kung_lao=0,mileena=5,shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11})[human])
assert(human=='kano' or human=='sonya','This cold native UI route covers the two added humans')
local native_direction=human=='kano'and'Left'or'Right'
local stock_direction=human=='kano'and'Right'or'Left'
local route={}
for i=1,(human=='sonya'and 4 or 1)do route[#route+1]={native_direction,12+(i-1)*12}end
for _,step in ipairs({{stock_direction,72},{native_direction,96},{stock_direction,120},{native_direction,144},
    {'Down',168},{'Up',192},{native_direction,216}})do route[#route+1]=step end
local boot=tonumber(os.getenv('MK2KS_TEST_BOOT_FRAME')or'604')
assert(boot>=600 and boot<=1500)
local confirm_age=tonumber(os.getenv('MK2KS_CPU_PAIR_CONFIRM_AGE')or'264')
assert(confirm_age>=96 and confirm_age<=370,'Only actual selection confirmation timing')
local continuation=os.getenv('MK2KS_CPU_CONTINUATION_POLICY')or'retreat'
assert(continuation=='retreat' or continuation=='jump_guard' or continuation=='guard_hold' or continuation=='neutral_hold' or continuation=='close_on_launch','Only real human continuation buttons')
local approach=os.getenv('MK2KS_CPU_PAIR_APPROACH')or'original'
assert(approach=='original' or approach=='guard_wait' or approach=='guard_until_close','Only genuine human input strategies')
local selection_p=manager.machine.devices[':maincpu'].spaces.program
local high,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local selection_inputs={system['Coin 1'],system['1 Player Start'],high['P1 High Punch'],
    high['P1 Left'],high['P1 Right'],high['P1 Up'],high['P1 Down'],high['P1 Block']}
local initial_cpu,first_live=nil,nil
emu.register_frame(function()
    selection_frame=selection_frame+1
    for _,field in ipairs(selection_inputs)do field:clear_value()end
    if selection_frame>=300 and selection_frame<304 then high['P1 High Punch']:set_value(1)end
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
        if age<4 then system['Coin 1']:set_value(1)end
        if age>=20 and age<24 then system['1 Player Start']:set_value(1)end
    end
    if not selection_css and selection_frame>700 and css then
        selection_css=selection_frame
        print(string.format('MK2_P2CPU_SELECT_CSS frame=%d human=%s slot=1 yellow=%d early=%d writes=0 assistance=none',selection_frame,human,yellow,early))
    end
    if selection_css and not selection_exit then
        local age=selection_frame-selection_css
        for _,step in ipairs(route)do
            local direction,at=step[1],step[2]
            if age>=at and age<at+4 then high['P1 '..direction]:set_value(1)end
        end
        if(age>=54 and age<=70)or(age>=228 and age<=260)then
            selection_checks=selection_checks+1
            if selection_p:read_u16(0x01060280)~=human_id then selection_errors=selection_errors+1 end
        end
        if age==65 or age==241 then manager.machine.screens[':screen']:snapshot('p1_selection_'..age..'.png')end
        if age>=confirm_age and age<confirm_age+8 then high['P1 High Punch']:set_value(1)end
        if age>confirm_age and not css then
            selection_exit=selection_frame
            manager.machine.screens[':screen']:snapshot('p1_selection_exit.png')
        end
    end
    if selection_frame%120==0 then
        print(string.format('MK2_P2CPU_BOOT_STATE frame=%d mode=%d states=%d,%d roster=%d,%d stage=%d schedule=%08X writes=0 assistance=none',
            selection_frame,selection_p:read_u16(0x010601d0),selection_p:read_u16(0x010601f0),
            selection_p:read_u16(0x01060dc0),selection_p:read_u16(0x01060280),selection_p:read_u16(0x01060e50),
            selection_p:read_u16(0x01061b30),selection_p:read_u32(0x01061b10)))
    end
    if selection_exit and not first_live and selection_p:read_u16(0x010601d0)==2 and
        selection_p:read_u16(0x010601f0)==1 and selection_p:read_u16(0x01060dc0)==0 then
        first_live=selection_frame;initial_cpu=selection_p:read_u16(0x01060e50)
        print(string.format('MK2_P2CPU_COLD_LIVE frame=%d human=%s human_id=%d cpu_id=%d stage=%d schedule=%08X writes=0 assistance=none',
            first_live,human,human_id,initial_cpu,selection_p:read_u16(0x01061b30),selection_p:read_u32(0x01061b10)))
        manager.machine.screens[':screen']:snapshot('p1_cold_cpu_fight.png')
    end
end)
emu.register_stop(function()
    print(string.format('MK2_P2CPU_SELECT_RESULT human=%s human_id=%d css=%d exit=%d live=%d initial_cpu=%d checks=%d errors=%d writes=0 assistance=none',
        human,human_id,selection_css or -1,selection_exit or -1,first_live or -1,initial_cpu or -1,selection_checks,selection_errors))
end)
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local fields=manager.machine.ioport.ports[':IN0'].fields
local frame,cycle,complete=0,0,nil
local complete_cycle,complete_actor,complete_main,follow_regain=nil,nil,nil,nil
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
    local own,v=sample(slots[cpu_slot]),sample(slots[human_slot])
    if p:read_u16(0x010601d0)==2 and own and v and own.state==0 and v.state==1 and own.roster==own.id and v.roster==v.id and specs[own.id] then return own,v end
end
local function same(c,s,v)return c and c.actor==s.actor and c.main==s.main and c.victim==v.actor and c.vmain==v.main end
local function log(tag,text,cycle_override)print(string.format('MK2_CPU_PAIR_%s frame=%d cycle=%d %s cpu_slot=2 human_slot=1 writes=0 assistance=none',tag,frame,cycle_override or cycle,text))end
local function state(tag,s,v,cycle_override)
    local function part(a,prefix)
        local text={}
        for _,key in ipairs({'actor','main','owner','pose','list','xraw','yraw','vx','vy','gravity','flags','body','facing','trail'})do text[#text+1]=string.format('%s%s=%08X',prefix,key,a[key])end
        for _,key in ipairs({'id','roster','state','action','x','y','floor','hp'})do
            local suffix=prefix=='v' and (key=='x' or key=='y')and key..'pos' or key
            text[#text+1]=string.format('%s%s=%d',prefix,suffix,a[key])
        end
        return table.concat(text,' ')
    end
    log(tag,part(s,'')..' '..part(v,'v')..string.format(' mode=%d stage=%d schedule=%08X suppression=%d left=%d right=%d stage_floor=%d',p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u32(0x01061b10),p:read_u16(0x010619d0),p:read_i16(0x0105ecf0)+0x3a,p:read_i16(0x0105ed00)+0x15f,p:read_i16(0x0105ecd0)),cycle_override)
end
local function clean(a)
    local vx=a.vx>=0x80000000 and a.vx-0x100000000 or a.vx
    return a.y==a.floor and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 and a.body&0x0c==0 and a.trail==0 and (vx==0 or a.action==0x303 and math.abs(vx)<=0x30000)
end
-- Read-only provenance for actual native body/Main flags, including stock controls.
local bound_guards,flag_count={},0
local function bind_guards()
    if p:read_u16(0x010601d0)~=2 then return end
    for side,slot in ipairs(slots)do
        local a=sample(slot)
        if a and a.owner==a.actor then
            for _,kind in ipairs({'body','flags','action'})do
                local at=(kind=='body' and a.actor+0x160 or a.main+(kind=='action' and 0x1f0 or 0x210))
                local key=string.format('%d:%s:%08X',side,kind,at)
                if not bound_guards[key]then
                    bound_guards[key]=true
                    taps[#taps+1]=p:install_write_tap(at,at+15,'native flag provenance '..key,function(offset,data,mask)
                        if offset~=at or mask~=0xffff or flag_count>=15000 or p:read_u16(0x010601d0)~=2 then return end
                        local current=sample(slot)
                        if not current or current.actor~=a.actor or current.main~=a.main or current.owner~=a.actor then return end
                        flag_count=flag_count+1
                        log('FLAG',string.format('slot=%d kind=%s at=%08X before=%04X after=%04X pc=%08X a8=%08X a13=%08X a0=%08X a1=%08X op0=%04X op1=%04X actor=%08X main=%08X id=%d state=%d action=%d pose=%08X y=%d floor=%d vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X',
                            side,kind,at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A1.value,p:read_u16(cpu.PC.value-32),p:read_u16(cpu.PC.value-16),current.actor,current.main,current.id,current.state,current.action,current.pose,current.y,current.floor,current.vx,current.vy,current.gravity,current.flags,current.body))
                    end)
                end
            end
        end
    end
end
local entries={step=0xfff89400,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,recovery=0xff861350,regained=0xff861500}
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
        local c=cycles[cycle]
        if complete and s.actor==complete_actor and s.main==complete_main and
           cpu.A8.value==s.actor and cpu.A13.value==s.main and not follow_regain then
            if kind=='recovery' or kind=='regained' then
                log('FOLLOW_READY_INSTRUCTION',string.format('kind=%s entry=%08X pc=%08X actor=%08X main=%08X a8=%08X a13=%08X',
                    kind,address,cpu.PC.value,s.actor,s.main,cpu.A8.value,cpu.A13.value),complete_cycle)
                if kind=='regained' then
                    follow_regain=frame;state('FOLLOW_REGAIN',s,v,complete_cycle)
                    manager.machine.screens[':screen']:snapshot('cpu_followup_regain.png')
                end
            end
        end
        if not same(c,s,v)or c.closed then return end
        if kind=='intro' or kind=='attack' or kind=='step' or kind=='action'then
            if cpu.A8.value~=s.actor or cpu.A13.value~=s.main then return end
            if kind=='step'then
                if s.action~=spec.state or p:read_u32(cpu.A9.value)==0 then return end
                c.steps=c.steps+1;c.paired=c.paired or frame
                manager.machine.screens[':screen']:snapshot(string.format('cpu_pair_%d_step_%d.png',cycle,c.steps))
            end
        elseif kind=='regained'then
            if not c.release then return end
            if cpu.A8.value==s.actor and cpu.A13.value==s.main then
                if c.own_regain then return end
                kind='own_regain';c.own_regain=frame;state('OWN_REGAIN',s,v)
            elseif cpu.A8.value==v.actor and cpu.A13.value==v.main then
                if c.victim_regain then return end
                kind='victim_regain';c.victim_regain=frame;state('VICTIM_REGAIN',s,v)
            else return end
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
        if side==human_slot and same(c,s,v)and c.paired and not c.closed then c.damage=c.damage+before-after end
    end)
end
-- Independent real post-grab special entry and shared continuation observations.
local follow_moves={[0xfff8cc00]='blade',[0xfff9a400]='bicycle',
    [0xffffca00]='square',[0xffffb000]='knife',[0xffffb400]='ring',[0xffffde00]='ball'}
local follow_shared={fall=0xff876660,fling=0xff876650,landing=0xff876420,trail_cleanup=0xff83efd0}
local function follow_instruction(kind,move,address)
    local s,v=live();if not s then return end
    local c=cycles[cycle]
    if not same(c,s,v) or not c.own_regain or frame<=c.own_regain or
       (follow_regain and frame>=follow_regain) or
       cpu.A8.value~=s.actor or cpu.A13.value~=s.main then return end
    log('FOLLOW_INSTRUCTION',string.format('kind=%s move=%s entry=%08X pc=%08X actor=%08X main=%08X a8=%08X a13=%08X a0=%08X a1=%08X a2=%08X a3=%08X a6=%08X trail=%08X',
        kind,move,address,cpu.PC.value,s.actor,s.main,cpu.A8.value,cpu.A13.value,
        cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A6.value,s.trail))
    if kind=='action' then state('FOLLOW_ENTRY',s,v) end
end
for address,move in pairs(follow_moves)do
    taps[#taps+1]=p:install_read_tap(address,address+15,'post-grab own action '..move,function(at)
        if at==address and cpu.PC.value==address+16 then follow_instruction('action',move,address)end
    end)
end
for kind,address in pairs(follow_shared)do
    taps[#taps+1]=p:install_read_tap(address,address+15,'post-grab native continuation '..kind,function(at)
        if at==address and cpu.PC.value==address+16 then follow_instruction(kind,'shared',address)end
    end)
end
emu.register_frame(function()
    frame=frame+1
    if first_live and frame>=first_live+1800 then manager.machine:exit();return end
    bind_guards()
    if frame==1 then
        for order=0,5 do
            local roster_table=p:read_u32(0xff8a11f0);local list=p:read_u32(roster_table+order*32);local ids={}
            for n=0,16 do ids[#ids+1]=p:read_u16(list+n*16)end
            log('ROM',string.format('table=%08X order=%d list=%08X ids=%s',roster_table,order,list,table.concat(ids,',')))
        end
    end
    local s,v=live();if not s then return end
    state('FIELD',s,v)
    fields['P1 Left']:set_value(0);fields['P1 Right']:set_value(0)
    local c=cycles[cycle]
    if same(c,s,v) and not c.closed and c.own_regain and c.victim_regain and s.hp>0 and v.hp>0then
        c.closed=true
        if c.steps==specs[s.id].steps and c.damage==specs[s.id].damage and c.release and (s.id~=17 or c.pulses==4)then
            state('COMPLETE',s,v);complete=frame
            complete_cycle=cycle;complete_actor=s.actor;complete_main=s.main
            manager.machine.screens[':screen']:snapshot('cpu_pair_complete.png')
        else state('INCOMPLETE',s,v)end
    end
    if complete then
        fields['P1 Block']:set_value(1)
        state('FOLLOW_FIELD',s,v,complete_cycle)
        -- v1997 extends the actual physical match instead of quitting at the
        -- first ordinary regain. Only human buttons change after the first grab.
        fields['P1 Left']:set_value(0);fields['P1 Right']:set_value(0)
        fields['P1 Up']:set_value(0);fields['P1 Down']:set_value(0)
        fields['P1 Block']:set_value(1)
        local gap=math.abs(s.x-v.x)
        local controllable=v.hp>0 and s.hp>0 and v.y==v.floor and
            v.vy==0 and v.gravity==0 and v.flags&0x1c==0 and v.body&0x0c==0
        if controllable and gap<220 and continuation~='guard_hold' and continuation~='neutral_hold' and continuation~='close_on_launch' then
            fields['P1 Block']:set_value(0)
            fields['P1 '..(v.x<s.x and 'Left' or 'Right')]:set_value(1)
        end
        if controllable and continuation=='jump_guard' and (frame-first_live)%90<8 then
            fields['P1 Block']:set_value(0);fields['P1 Up']:set_value(1)
        end
        if controllable and continuation=='neutral_hold' then fields['P1 Block']:set_value(0)end
        if controllable and continuation=='close_on_launch' then
            fields['P1 Block']:set_value(0)
            local advancing=s.action==0x204 and gap>68
            local guarding=s.action==0x204 and gap<=68
            if advancing then fields['P1 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)end
            if guarding then fields['P1 Block']:set_value(1)end
            log('LAUNCH_RESPONSE',string.format('policy=%s cpu_action=%04X gap=%d advancing=%d guarding=%d',
                continuation,s.action,gap,advancing and 1 or 0,guarding and 1 or 0))
        end
        log('CONTINUATION_INPUT',string.format('policy=%s gap=%d controllable=%d jump=%d',
            continuation,gap,controllable and 1 or 0,
            controllable and continuation=='jump_guard'and(frame-first_live)%90<8 and 1 or 0))
    elseif same(c,s,v) and c.victim_ready and v.hp>0 and s.hp>0 and
        v.y==v.floor and v.vy==0 and v.gravity==0 and v.flags&0x1c==0 and
        v.body&0x0c==0 and v.trail==0 and math.abs(s.x-v.x)<170 then
        -- A genuine recovered human backstep leaves the CPU free to choose its
        -- next action. Do not alter its guard, velocity, timer or readiness.
        local direction=v.x<s.x and 'Left' or 'Right'
        fields['P1 '..direction]:set_value(1)
        log('INPUT',string.format('buttons=%s gap=%d phase=recovered_backstep',direction,math.abs(s.x-v.x)))
    elseif not c or c.closed or not c.paired then
        if (approach=='guard_wait' or approach=='guard_until_close') and v.hp>0 and s.hp>0 then
            -- Real standing guard lets the original CPU approach/choose. This
            -- preserves human health for a whole grab without guest writes or
            -- prescribing the CPU's character, move, position or random seed.
            local gap=math.abs(s.x-v.x)
            local guarding=approach=='guard_wait' or gap>110
            if guarding then fields['P1 Block']:set_value(1)end
            log('INPUT',string.format('buttons=%s gap=%d phase=%s',guarding and 'Block' or 'Neutral',gap,approach))
        elseif v.hp>0 and s.hp>0 and clean(v) and math.abs(s.x-v.x)>76 then
            fields['P1 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)
            log('INPUT',string.format('buttons=%s gap=%d',v.x<s.x and 'Right' or 'Left',math.abs(s.x-v.x)))
        end
    end
end)
emu.register_stop(function()
    log('RESULT',string.format('schema=9 cycles=%d complete=%d follow_regain=%d scope=natural_P2_CPU_extended_human_continuation_diagnostic_not_accepted_special_or_full_goal',cycle,complete or -1,follow_regain or -1))
    for _,tap in ipairs(taps)do tap:remove()end
end)
