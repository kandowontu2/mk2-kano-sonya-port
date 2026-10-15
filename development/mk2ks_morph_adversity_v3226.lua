-- Native controls only. No guest-memory, identity, timer or coordinate writes.
local side=tonumber(os.getenv('MK2KS_HUMAN_SHANG_SIDE') or '1')
local target=assert(os.getenv('MK2KS_HUMAN_SHANG_TARGET'))
local phase=assert(os.getenv('MK2KS_MORPH_ADVERSITY_PHASE'))
assert(({forward=true,formed=true,reverse=true,ko=true,repeat_morph=true})[phase])
local form= os.getenv('MK2KS_MORPH_ADVERSITY_FORM')or'added'
assert(({added=true,stock_cage=true,stock_kitana=true})[form])
local profile='adversity_'..phase
for _,key in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do assert(not os.getenv(key),'No guest assistance')end
local attack_due,choice_frame,form_frame,reverse_frame=nil,nil,nil,nil
local attack_count=0
assert((side==1 or side==2) and (target=='kano' or target=='sonya'))
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local high=manager.machine.ioport.ports[':IN0'].fields
local low=manager.machine.ioport.ports[':IN2'].fields
local f={}
for slot=1,2 do
    for _,key in ipairs({'Up','Down','Left','Right','High Punch','Low Punch','Block','Block 2','High Kick','Low Kick'}) do
        local name='P'..slot..' '..key
        f[name]=assert(high[name] or low[name], 'Missing native input: '..name)
    end
end
local sys=manager.machine.ioport.ports[':IN1'].fields
local slots={{state=0x010601f0,roster=0x01060280,actor=0x01060220,main=0x01060260,hp=0x010602f0},
             {state=0x01060dc0,roster=0x01060e50,actor=0x01060df0,main=0x01060e30,hp=0x01060ec0}}
local keys={'Up','Down','Left','Right','High Punch','Low Punch','Block','Block 2','High Kick','Low Kick'}
local frame,css,match,actor,main,forms,restores,errors=0,nil,nil,nil,nil,0,0,0
local taps,pending={},{}
local identity=({stock_cage=2,stock_kitana=4})[form]or(target=='kano'and 17 or 18)
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function owned(a,m)
    return match and a==actor and p:read_u32(slots[side].actor)==a and p:read_u32(slots[side].main)==main and
        p:read_u16(slots[side].state)==1 and p:read_u16(slots[side].roster)==6 and
        (m==main or valid(m) and p:read_u32(m+0x290)==main)
end
local function log(tag,s)print(string.format('MK2_HUMAN_SHANG_%s frame=%d side=%d target=%s profile=%s form=%s %s writes=0',tag,frame,side,target,profile,form,s))end
local function tap(at,tag,fn)
    taps[#taps+1]=p:install_read_tap(at,at+15,tag,function()
        if cpu.PC.value==at+16 and owned(cpu.A8.value,cpu.A13.value) then fn() end
    end)
end
tap(0xfffc8800,'kano parser',function()log('PARSER','kind=kano actor='..string.format('%08X',cpu.A8.value)..' event='..string.format('%08X',cpu.A13.value))end)
tap(0xfffc9000,'sonya LP parser',function()log('PARSER','kind=sonya_lp actor='..string.format('%08X',cpu.A8.value)..' event='..string.format('%08X',cpu.A13.value))end)
tap(0xfffc9100,'sonya Block parser',function()log('PARSER','kind=sonya_block actor='..string.format('%08X',cpu.A8.value)..' event='..string.format('%08X',cpu.A13.value))end)
tap(0xff8771f0,'native eligibility gate',function()log('GATE',string.format('actor=%08X event=%08X entry=%08X pc=%08X',cpu.A8.value,cpu.A13.value,cpu.A7.value,cpu.PC.value))end)
tap(0xff86e480,'native forward morph',function()choice_frame=frame;if phase=='forward'and not attack_due then attack_due=frame+2 end;log('CHOICE',string.format('actor=%08X main=%08X id=%d pc=%08X',actor,main,cpu.A9.value,cpu.PC.value))end)
tap(0xff86e580,'native forward lookup',function()log('LOOKUP',string.format('actor=%08X main=%08X root=%08X pc=%08X',actor,main,cpu.A9.value,cpu.PC.value))end)
tap(0xffa16300,'native restoration',function()reverse_frame=frame;if phase=='reverse'and not attack_due then attack_due=frame+2 end;log('RESTORE_BEGIN',string.format('actor=%08X main=%08X id=%d pc=%08X',actor,main,p:read_u16(actor+0x1f0),cpu.PC.value))end)
tap(0xffa16440,'native reverse lookup',function()log('RESTORE_LOOKUP',string.format('actor=%08X main=%08X root=%08X pc=%08X',actor,main,cpu.A0.value,cpu.PC.value))end)
tap(0xff838790,'native transition group',function()
    if cpu.A0.value>=0xff0c4000 and cpu.A0.value<0xff0c4240 then log('GROUP',string.format('actor=%08X main=%08X group=%08X pc=%08X',actor,main,cpu.A0.value,cpu.PC.value))end
end)
tap(0xff907510,'native morph palette',function()
    if cpu.A0.value==0xff0c0800 or cpu.A0.value==0xff0c1000 then log('PALETTE',string.format('actor=%08X main=%08X palette=%08X pc=%08X',actor,main,cpu.A0.value,cpu.PC.value))end
end)
tap(0xffffb000,'Kano knife action',function()log('PROJECTILE_ACTION',string.format('actor=%08X main=%08X entry=FFFFB000 id=%d',actor,main,p:read_u16(actor+0x1f0)))end)
tap(0xffffb400,'Sonya ring action',function()log('PROJECTILE_ACTION',string.format('actor=%08X main=%08X entry=FFFFB400 id=%d',actor,main,p:read_u16(actor+0x1f0)))end)
tap(0xfffc5800,'Kano knife create',function()log('PROJECTILE_CREATE',string.format('actor=%08X main=%08X entry=FFFC5800 id=%d',actor,main,p:read_u16(actor+0x1f0)))end)
tap(0xfffc5c00,'Sonya ring create',function()log('PROJECTILE_CREATE',string.format('actor=%08X main=%08X entry=FFFC5C00 id=%d',actor,main,p:read_u16(actor+0x1f0)))end)
for n,sl in ipairs(slots)do
 taps[#taps+1]=p:install_write_tap(sl.hp,sl.hp+15,'actual adversity native health',function(at,data,mask)
  if match then log('HEALTH',string.format('slot=%d before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X',n,p:read_u16(sl.hp),data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))end
 end)
end
local output=assert(os.getenv('MK2KS_MORPH_CAPTURE_OUT'))
local dumped=false
emu.register_frame(function()
 if dumped then return end
 dumped=true;local words={}
 for address=0xff800000,0xfffffff0,16 do words[#words+1]=string.pack('<I2',p:read_u16(address))end
 local raw=table.concat(words);assert(#raw==0x100000)
 local file=assert(io.open(output..'/guest_maincpu.bin','wb'));file:write(raw);file:close()
 print('MK2_MORPH_GUEST frame=1 bytes=1048576 start=FF800000 stop=100000000 writes=0')
end)

local function pulse(field,age,start,length)field:set_value(age>=start and age<start+(length or 4) and 1 or 0)end
emu.register_frame(function()
    frame=frame+1
    for _,k in ipairs(keys) do for slot=1,2 do f['P'..slot..' '..k]:set_value(0) end end
    for _,k in ipairs({'Coin 1','Coin 2','1 Player Start','2 Players Start'}) do sys[k]:set_value(0) end
    if frame==1 then log('ROM',string.format('lp=%08X block=%08X lk=%08X scope=input_only_native_human_morph_no_guest_state_assistance',p:read_u32(0xffff8e80+6*32),p:read_u32(0xffff9100+6*32),p:read_u32(0xffff9600+6*32))) end
    if not css and frame>=600 then
        local age=(frame-600)%300
        pulse(sys['Coin 1'],age,0);pulse(sys['Coin 2'],age,8);pulse(sys['1 Player Start'],age,20)
        if p:read_u16(0x010601d0)==4 and p:read_u16(slots[1].state)==3 then css=frame;log('CSS','mode=4') end
    end
    if css and not match then
        local age=frame-css
        pulse(sys['Coin 1'],age,0);pulse(sys['Coin 2'],age,8);pulse(sys['2 Players Start'],age,20)
        local routes=side==1 and {{'Right','Down'},{'Left','Left','Left','Left'}} or {{'Left'},{'Left','Left','Down'}}
        for slot=1,2 do
            for i,key in ipairs(routes[slot]) do local first=(slot==1 and 12 or 42)+(i-1)*12;if age>=first and age<first+4 then f['P'..slot..' '..key]:set_value(1) end end
            pulse(f['P'..slot..' High Punch'],age,110,8)
        end
    end
    if not match and p:read_u16(0x010601d0)==2 and p:read_u16(slots[side].state)==1 and
        p:read_u16(slots[3-side].state)==1 and p:read_u16(slots[side].roster)==6 and
        p:read_u16(slots[3-side].roster)==17 and p:read_u16(slots[1].hp)==161 and p:read_u16(slots[2].hp)==161 then
        local a,m=p:read_u32(slots[side].actor),p:read_u32(slots[side].main)
        if valid(a) and valid(m) and p:read_u16(a+0x1f0)==6 then
            match,actor,main=frame,a,m
            log('MATCH',string.format('actor=%08X main=%08X own_state=1 own_roster=6 own_id=6 other_state=1 other_roster=17 hp1=161 hp2=161',actor,main))
            taps[#taps+1]=p:install_write_tap(actor+0x1f0,actor+0x1ff,'actual human native morph stores',function(at,data,mask)
                if not owned(cpu.A8.value,cpu.A13.value) or cpu.A13.value~=main or mask~=0xffff then return end
                local old,id=p:read_u16(actor+0x1f0),data&0xffff
                log('STORE',string.format('actor=%08X main=%08X old=%d id=%d pc=%08X a9=%08X a0=%08X',actor,main,old,id,cpu.PC.value,cpu.A9.value,cpu.A0.value))
                if cpu.PC.value==0xff86e670 and old==6 and id==identity and cpu.A9.value==id then forms=forms+1;form_frame=frame;if(phase=='formed'or phase=='ko')and not attack_due then attack_due=frame+40 end;pending[#pending+1]={at=frame+60,kind='form'}
                elseif cpu.PC.value==0xffa16700 and old==identity and id==6 then restores=restores+1;pending[#pending+1]={at=frame+30,kind='restored'}
                else log('OTHER_STORE','pc='..string.format('%08X',cpu.PC.value)) end
            end)
        end
    end
    if match then
        local age=frame-match
        local command={}
        local function press(k)f['P'..side..' '..k]:set_value(1);command[#command+1]=k:gsub(' ','_')end
        local function other(k)
            f['P'..(3-side)..' '..k]:set_value(1)
            log('OPINPUT',string.format('age=%d slot=%d button=%s',age,3-side,k:gsub(' ','_')))
        end
        local own=p:read_u32(slots[side].actor)
        local opposite=p:read_u32(slots[3-side].actor)
        local flipped=valid(own)and(p:read_u16(own+0xf0)&0x10)~=0
        local back,forward=flipped and 'Right' or 'Left',flipped and 'Left' or 'Right'
        local mode=p:read_u16(0x010601d0)
        local x1=valid(own)and p:read_i16(own+0x90)or 0
        local x2=valid(opposite)and p:read_i16(opposite+0x90)or 0
        if mode==2 and age>=20 and age<90 and math.abs(x1-x2)>63 then other(x2>x1 and'Left'or'Right')end
        local morph_age=phase=='ko'and age-200 or age
        if phase=='repeat_morph'and age>=800 then morph_age=age>=1500 and age-1400 or age-700 end
        if phase=='ko'and mode==2 and age>=95 and age<114 then
            other('Down')
            if age>=106 and age<110 then
                other('High Punch')
                if age==106 then attack_count=attack_count+1;log('ATTACK',string.format('ordinal=%d slot=%d due=%d gap=%d choice=-1 form=-1 reverse=-1',attack_count,3-side,match+95,math.abs(x1-x2)))end
            end
        end
        if mode==2 and p:read_u16(slots[side].hp)>0 then
            if form=='stock_cage'then
                if morph_age>=100 and morph_age<102 or morph_age>=104 and morph_age<106 then press(back)end
                if morph_age>=108 and morph_age<110 then press('Down');press('Low Punch')end
            elseif form=='stock_kitana'then
                if morph_age>=100 and morph_age<102 or morph_age>=104 and morph_age<106 or morph_age>=108 and morph_age<110 then press('Block')end
            elseif target=='kano' then
                if morph_age>=100 and morph_age<102 then press(back)end
                if morph_age>=104 and morph_age<106 then press('Down')end
                if morph_age>=108 and morph_age<110 then press(back);press('Low Kick')end
            elseif morph_age>=100 and morph_age<108 then press('Down');press('Low Punch');press('Block')end
        end
        if mode==2 and p:read_u16(slots[side].hp)>0 then
            if phase=='forward'and age>=90 and(not attack_due or frame<attack_due+8) then other('Down')end
            if phase=='reverse'and form_frame and frame>=form_frame+496 and(not attack_due or frame<attack_due+8) then other('Down')end
            if attack_due then
                local n=frame-attack_due
                if phase=='ko'and n>=18 then
                    if math.abs(x1-x2)>63 then other(x2>x1 and'Left'or'Right')end
                    if n>=100 and math.abs(x1-x2)<=63 and p:read_i16(opposite+0xb0)==p:read_i16(p:read_u32(slots[3-side].main)+0x200)then attack_due=frame;n=0 end
                end
                local early=phase=='forward'or phase=='reverse'
                local first=early and 0 or 11
                local finish=early and 8 or 18
                if n>=0 and n<finish then other('Down')end
                if n>=first and n<first+4 then other('High Punch');if n==first then attack_count=attack_count+1;log('ATTACK',string.format('ordinal=%d slot=%d due=%d gap=%d choice=%d form=%d reverse=%d',attack_count,3-side,attack_due,math.abs(x1-x2),choice_frame or -1,form_frame or -1,reverse_frame or -1))end end
            end
        end
        if phase~='repeat_morph'and phase~='ko'and age>=1100 and age<1110 then press(forward)
        elseif phase~='repeat_morph'and phase~='ko'and age>=1140 and age<1143 then press('Up')
        elseif phase~='repeat_morph'and phase~='ko'and age>=1250 and age<1254 then press('High Punch')end
        if #command>0 then log('INPUT',string.format('age=%d actor=%08X id=%d buttons=%s facing=%s',age,actor,p:read_u16(actor+0x1f0),table.concat(command,','),flipped and 'left' or 'right')) end
        log('FIELD',string.format('age=%d actor=%08X main=%08X mode=%d state=%d roster=%d id=%d action=%04X pose=%08X x=%d y=%d floor=%d vx=%08X vy=%08X trail=%08X hp1=%d hp2=%d',age,actor,main,p:read_u16(0x010601d0),p:read_u16(slots[side].state),p:read_u16(slots[side].roster),p:read_u16(actor+0x1f0),p:read_u16(main+0x1f0),p:read_u32(actor+0x1d0),p:read_i16(actor+0x90),p:read_i16(actor+0xb0),p:read_i16(main+0x200),p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u32(main+0x190),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)))
        for n,sl in ipairs(slots)do
            local a,m=p:read_u32(sl.actor),p:read_u32(sl.main)
            if valid(a)and valid(m)then
                log('PAIR',string.format('age=%d slot=%d mode=%d actor=%08X main=%08X owner=%08X state=%d roster=%d id=%d hp=%d action=%04X pose=%08X x=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X flags=%04X body=%04X trail=%08X',
                 age,n,mode,a,m,p:read_u32(m+0xc0),p:read_u16(sl.state),p:read_u16(sl.roster),p:read_u16(a+0x1f0),p:read_u16(sl.hp),
                 p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),p:read_i16(a+0x90),p:read_i16(a+0xb0),p:read_i16(m+0x200),
                 p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u32(a+0x20),p:read_u16(m+0x210),p:read_u16(a+0x160),p:read_u32(m+0x190)))
            else log('PAIR_MISSING','age='..age..' slot='..n..' mode='..mode)end
        end
        if age%60==0 then manager.machine.screens[':screen']:snapshot(string.format('adversity_%d.png',frame))end
        if age==2400 then manager.machine:exit() end
    elseif frame>=3000 then errors=errors+1;log('ERROR','reason=no_actual_human_match');manager.machine:exit() end
    for _,s in ipairs(pending) do if s.at==frame then manager.machine.screens[':screen']:snapshot(string.format('human_shang_%s_%s_p%d_%d.png',target,s.kind,side,frame))end end
end)
emu.register_stop(function()
    log('RESULT',string.format('forms=%d restores=%d errors=%d match=%d scope=bounded_input_only_human_morph_not_complete_integration',forms,restores,errors,match or -1))
    for _,t in ipairs(taps) do t:remove() end
end)
