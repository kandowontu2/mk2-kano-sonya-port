-- Actual cold two-human selection and airborne Block commands. No guest writes.
for _,name in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
    assert(not os.getenv(name),'Human air probe cannot use '..name)
end
assert(os.getenv('MK2KS_TWO_PLAYER')=='1')
dofile('mk2ks_selector_exit_test.lua')
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_AIR_SIDE')))
local delay=assert(tonumber(os.getenv('MK2KS_HUMAN_AIR_DELAY')))
local attacker=assert(os.getenv('MK2KS_HUMAN_AIR_ATTACKER'))
local victim=assert(os.getenv('MK2KS_HUMAN_AIR_VICTIM'))
local aid=assert(({kano=17,jax=11})[attacker])
local vid=assert(({sonya=18,sub_zero=8,kano=17})[victim])
assert(side==1 or side==2);assert(delay>=2 and delay<=32)
local p=manager.machine.devices[':maincpu'].spaces.program
local regs=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
             {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local fields={}
for n=1,2 do
    local high=manager.machine.ioport.ports[':IN0'].fields
    fields[n]={}
    for _,name in ipairs({'Up','Down','Left','Right','Block','High Punch','High Kick'})do fields[n][name]=high['P'..n..' '..name]end
end
local frame,match,jump,command,caught,own_ready,victim_ready,complete=0,nil,nil,nil,nil,nil,nil,nil
local close_ready,followup=nil,nil
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(n)
    local slot=slots[n];local a,m=p:read_u32(slot.actor),p:read_u32(slot.main)
    if not valid(a)or not valid(m)then return end
    return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(slot.id),state=p:read_u16(slot.state),
        x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),action=p:read_u16(m+0x1f0),hp=p:read_u16(slot.hp),
        xraw=p:read_u32(a+0x80),yraw=p:read_u32(a+0xa0),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),
        pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),body=p:read_u16(a+0x160),trail=p:read_u32(m+0x190),callback=p:read_u32(m+0x290)}
end
local function pair()return sample(side),sample(3-side)end
local function live(a,b)return p:read_u16(0x010601d0)==2 and a and b and a.id==aid and a.roster==aid and b.id==vid and b.roster==vid and a.state==1 and b.state==1 end
local function clean(s)return s.y==s.floor and s.vx==0 and s.vy==0 and s.gravity==0 and s.flags&0x1c==0 and s.body&0x0c==0 and s.trail==0 end
local function log(tag,a,b,extra)
    local function part(s,prefix)
        local out={}
        for _,key in ipairs({'actor','main','owner','xraw','yraw','vx','vy','gravity','pose','flags','body','trail','callback'})do out[#out+1]=string.format('%s%s=%08X',prefix,key,s[key])end
        for _,key in ipairs({'id','roster','state','x','y','floor','action','hp'})do out[#out+1]=string.format('%s%s=%d',prefix,key,s[key])end
        return table.concat(out,' ')
    end
    print(string.format('MK2_HUMAN_AIR_%s frame=%d side=%d attacker=%s victim=%s delay=%d %s %s %s writes=0 assistance=none',tag,frame,side,attacker,victim,delay,part(a,'a'),part(b,'v'),extra or''))
end
local entries={0xff8643e0,0xff8b6ff0,0xfffcac00,0xff83cc20,0xfffc0680,0xfffff980,0xfffff580,0xfffff800,
    0xfffc2000,0xff83a7a0,0xfffc1c00,0xff8da830,0xff8ea320,0xff861410,0xff861500,0xff876660}
for _,address in ipairs(entries)do
    taps[#taps+1]=p:install_read_tap(address,address+15,'human air instruction provenance',function(at)
        if not match or not command or regs.PC.value~=address+16 then return end
        local a,b=pair();if not live(a,b)then return end
        if regs.A8.value~=a.actor and regs.A8.value~=b.actor then return end
        if address==0xff8b6ff0 and regs.A8.value==a.actor and regs.A13.value==a.main and not caught then
            caught=frame;log('CAUGHT',a,b,'entry=FF8B6FF0 pc=FF8B7000');screen:snapshot('human_air_caught.png')
        end
        if address==0xff861500 and caught and not complete then
            if regs.A8.value==a.actor and regs.A13.value==a.main and not own_ready then own_ready=frame;log('OWN_READY',a,b,'entry=FF861500 pc=FF861510')end
            if regs.A8.value==b.actor and regs.A13.value==b.main and not victim_ready then victim_ready=frame;log('VICTIM_READY',a,b,'entry=FF861500 pc=FF861510')end
        end
        log('EVENT',a,b,string.format('entry=%08X pc=%08X a0=%08X a1=%08X a2=%08X a3=%08X a6=%08X a8=%08X a10=%08X a13=%08X',address,regs.PC.value,regs.A0.value,regs.A1.value,regs.A2.value,regs.A3.value,regs.A6.value,regs.A8.value,regs.A10.value,regs.A13.value))
    end)
end
for slot,info in ipairs(slots)do
    taps[#taps+1]=p:install_write_tap(info.hp,info.hp+15,'human air native health',function(at,data,mask)
        if not match or mask~=0xffff then return end
        local a,b=pair();if not live(a,b)then return end
        log('HEALTH',a,b,string.format('slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X',slot,p:read_u16(at),data&0xffff,regs.PC.value,regs.A8.value,regs.A13.value))
    end)
end
local function input(slot,name,a,b)
    fields[slot][name]:set_value(1)
    log('INPUT',a,b,string.format('slot=%d button=%s',slot,name:gsub(' ','_')))
end
emu.register_frame(function()
    frame=frame+1
    local a,b=pair()
    if not match then
        if frame>1200 and live(a,b) and a.hp==161 and b.hp==161 and clean(a) and clean(b)then
            match=frame;log('MATCH',a,b);screen:snapshot('human_air_match.png')
            -- Only observe actual original stores. Never replace their values.
            for role,s in ipairs({a,b})do
                for _,spec in ipairs({{s.actor+0x160,'body'},{s.main+0x210,'flags'}})do
                    taps[#taps+1]=p:install_write_tap(spec[1],spec[1]+15,'native human air locks',function(at,data,mask)
                        if mask~=0xffff or not command then return end
                        local own,other=pair();if not live(own,other)then return end
                        log('LOCK',own,other,string.format('role=%d kind=%s at=%08X before=%04X after=%04X pc=%08X a8=%08X a13=%08X',role,spec[2],at,p:read_u16(at),data&0xffff,regs.PC.value,regs.A8.value,regs.A13.value))
                    end)
                end
            end
        elseif frame>=3000 then print('MK2_HUMAN_AIR_ERROR reason=no_actual_selected_match writes=0 assistance=none');manager.machine:exit()end
    end
    if not match then return end
    if not live(a,b)then print('MK2_HUMAN_AIR_ERROR reason=lost_actual_pair writes=0 assistance=none');manager.machine:exit();return end
    for n=1,2 do for _,field in pairs(fields[n])do field:set_value(0)end end
    log('FIELD',a,b)
    if not jump then
        if frame-match>=180 then
            if math.abs(a.x-b.x)>63 then input(side,a.x<b.x and 'Right'or'Left',a,b);close_ready=nil
            elseif clean(a) and clean(b)then
                close_ready=close_ready or frame
                if frame-close_ready>=30 then jump=frame;command=jump+delay;log('JUMP',a,b,'command='..command)end
            else close_ready=nil end
        end
    end
    if jump then
        if frame>=jump and frame<jump+3 then input(1,'Up',a,b);input(2,'Up',a,b)end
        if frame>=command and frame<command+6 then input(side,'Block',a,b)end
        if own_ready and victim_ready and not complete and clean(a)and clean(b)then
            complete=frame;followup=frame+16;log('COMPLETE',a,b,'followup='..followup);screen:snapshot('human_air_complete.png')
        end
        if followup and frame>=followup then
            local age=frame-followup
            for n=1,2 do
                local me,other=n==side and a or b,n==side and b or a
                if age<8 then input(n,me.x<other.x and 'Right'or'Left',a,b)
                elseif age>=40 and age<43 then input(n,'Up',a,b)
                elseif age>=112 and age<115 then input(n,'High Punch',a,b)
                elseif age>=136 and age<142 then input(n,'Block',a,b)end
            end
            if age==160 then log('FINAL',a,b);screen:snapshot('human_air_final.png');manager.machine:exit()end
        end
        if caught and frame-caught<=100 and (frame-caught)%8==0 then screen:snapshot('human_air_pose_'..(frame-caught)..'.png')end
        if not complete and frame-jump>=240 then log('FAILED',a,b,'reason=no_full_native_recovery');manager.machine:exit()end
    end
end)
emu.register_stop(function()
    print(string.format('MK2_HUMAN_AIR_RESULT match=%d jump=%d command=%d caught=%d own_ready=%d victim_ready=%d complete=%d followup=%d final=%d side=%d attacker=%s victim=%s delay=%d writes=0 assistance=none scope=diagnostic_independent_verification_pending',match or-1,jump or-1,command or-1,caught or-1,own_ready or-1,victim_ready or-1,complete or-1,followup or-1,frame,side,attacker,victim,delay))
    for _,tap in ipairs(taps)do tap:remove()end
end)
