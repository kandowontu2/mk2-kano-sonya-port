-- Native CPU morph diagnosis. Source stage/health assistance is explicit;
-- random values, target IDs, poses, actor coordinates and processes are READ ONLY.
-- P1 health assistance below remains explicitly confined to this stage fixture.
dofile('mk2ks_cpu_ladder_trace.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,taps,actors=0,{},{}
local choices,forms,restores={}, {[17]=0,[18]=0}, {[17]=0,[18]=0}
local groups,errors,fields,pending,health_writes={},0,0,{},0
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function native(a,m)
    return valid(a) and valid(m) and a==p:read_u32(0x01060df0) and m==p:read_u32(0x01060e30) and
        p:read_u16(0x01060dc0)==0 and p:read_u16(0x01060e50)==6 and p:read_u16(0x01061b30)==14
end
local function log(tag,extra)
    print(string.format('MK2_SHANG_ROSTER_%s frame=%d %s writes=0',tag,frame,extra))
end
local function code(at,tag,fn)
    taps[#taps+1]=p:install_read_tap(at,at+15,'native morph '..tag,function()
        if cpu.PC.value==at+16 and native(cpu.A8.value,cpu.A13.value) then fn(cpu.A8.value,cpu.A13.value) end
    end)
end
code(0xff86e280,'rng',function(a,m)
    log('RNG',string.format('actor=%08X main=%08X bound=%d pc=%08X',a,m,cpu.A0.value,cpu.PC.value))
end)
code(0xff86e480,'choice',function(a,m)
    local id=cpu.A9.value;choices[id]=(choices[id] or 0)+1
    actors[a]=actors[a] or {main=m}
    actors[a].choice=id
    log('CHOICE',string.format('actor=%08X main=%08X id=%d pc=%08X roster=6 state=0 stage=14',a,m,id,cpu.PC.value))
end)
code(0xff86e580,'lookup',function(a,m)
    log('LOOKUP',string.format('actor=%08X main=%08X choice=%d root=%08X pc=%08X',a,m,(actors[a] or {}).choice or -1,cpu.A9.value,cpu.PC.value))
end)
code(0xffa16300,'restore begin',function(a,m)
    log('RESTORE_BEGIN',string.format('actor=%08X main=%08X id=%d pc=%08X',a,m,p:read_u16(a+0x1f0),cpu.PC.value))
end)
code(0xffa16440,'restore lookup',function(a,m)
    log('RESTORE_LOOKUP',string.format('actor=%08X main=%08X id=%d root=%08X pc=%08X',a,m,p:read_u16(a+0x1f0),cpu.A0.value,cpu.PC.value))
end)
code(0xff838790,'group',function(a,m)
    local group=cpu.A0.value
    if group>=0xff0c4000 and group<0xff0c4240 then
        groups[group]=(groups[group] or 0)+1
        log('GROUP',string.format('actor=%08X main=%08X group=%08X pc=%08X choice=%d',a,m,group,cpu.PC.value,(actors[a] or {}).choice or -1))
        pending[#pending+1]={at=frame+1,group=group}
    end
end)
code(0xff907510,'palette',function(a,m)
    if cpu.A0.value==0xff0c0800 or cpu.A0.value==0xff0c1000 then
        log('PALETTE',string.format('actor=%08X main=%08X palette=%08X pc=%08X',a,m,cpu.A0.value,cpu.PC.value))
    end
end)
code(0xff841090,'body palette',function(a,m)
    local id=p:read_u16(a+0x1f0)
    if id==17 or id==18 or (actors[a] or {}).choice==17 or (actors[a] or {}).choice==18 then
        log('BODY_PALETTE',string.format('actor=%08X main=%08X id=%d palette=%08X pc=%08X main_flags=%08X',a,m,id,cpu.A0.value,cpu.PC.value,p:read_u32(m+0x210)))
    end
end)
code(0xff861350,'ready',function(a,m)
    log('READY',string.format('actor=%08X main=%08X id=%d action=%04X a12=%08X pc=%08X',a,m,p:read_u16(a+0x1f0),p:read_u16(m+0x1f0),cpu.A12.value,cpu.PC.value))
end)
code(0xff838460,'morph timer check',function(a,m)
    log('TIMER_CHECK',string.format('actor=%08X main=%08X id=%d pc=%08X',a,m,p:read_u16(a+0x1f0),cpu.PC.value))
end)
code(0xff83c870,'native animation timing',function(a,m)
    log('TIMING',string.format('actor=%08X main=%08X id=%d rate=%08X list=%08X pc=%08X',a,m,p:read_u16(a+0x1f0),cpu.A0.value,cpu.A9.value,cpu.PC.value))
end)
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local ids={};for i=0,13 do ids[#ids+1]=p:read_u16(0xfffc8200+i*16) end
        log('ROM',string.format('random=%04X map=%s lookup=%08X scope=diagnostic_stage14_P1_health_assistance_not_natural_tower',p:read_u16(0xff86e270),table.concat(ids,','),p:read_u32(0xff86e560)))
        local rate_table=p:read_u32(0xff9b5390)
        local stock={};for i=0,16 do stock[#stock+1]=string.format('%08X',p:read_u32(rate_table+i*32)) end
        log('TURN_TABLE',string.format('human=%08X cpu=%08X kano=%08X sonya=%08X stock=%s',p:read_u32(0xff8700d0),rate_table,p:read_u32(rate_table+17*32),p:read_u32(rate_table+18*32),table.concat(stock,',')))
        assert(p:read_u16(0xff86e270)==0x19c0,'Fourteen native morph choices missing')
    end
    local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
    if native(a,m) then
        -- Explicit stage-only fallback; the base helper also logs its own
        -- health assistance. Neither writes CPU identity or a morph target.
        local human=p:read_u32(0x01060220)
        local hp=p:read_u16(0x010602f0)
        if p:read_u16(0x010601f0)==1 and
            p:read_u16(0x01060280)==17 and valid(human) and p:read_u16(human+0x1f0)==17 and hp>0 and hp<161 then
            health_writes=health_writes+1
            print(string.format('MK2_SHANG_FIXTURE_HEALTH frame=%d address=010602F0 old=%d new=161 count=%d mode=%d state=1 roster=17 actor=%08X id=17 cpu_roster=6 cpu_state=0 stage=14 scope=stage14_P1_only',frame,hp,health_writes,p:read_u16(0x010601d0),human))
            p:write_u16(0x010602f0,161)
        end
        if frame%60==0 then log('STAGE',string.format('mode=%d p1_state=%d p1_roster=%d p1_actor=%08X p1_id=%d p1_hp=%d cpu_actor=%08X cpu_main=%08X cpu_id=%d cpu_roster=6 cpu_state=0 stage=14',p:read_u16(0x010601d0),p:read_u16(0x010601f0),p:read_u16(0x01060280),human,valid(human) and p:read_u16(human+0x1f0) or -1,hp,a,m,p:read_u16(a+0x1f0))) end
        if not actors[a] or not actors[a].tap then
            actors[a]=actors[a] or {main=m}
            actors[a].tap=p:install_write_tap(a+0x1f0,a+0x1ff,'native actual morph stores',function(at,data,mask)
                if not native(a,m) or mask~=0xffff or cpu.A8.value~=a or cpu.A13.value~=m then return end
                local old,id,pc=p:read_u16(a+0x1f0),data&0xffff,cpu.PC.value
                log('STORE',string.format('actor=%08X main=%08X old=%d id=%d pc=%08X a9=%08X a0=%08X',a,m,old,id,pc,cpu.A9.value,cpu.A0.value))
                if pc==0xff86e670 and (id==17 or id==18) then
                    forms[id]=forms[id]+1;actors[a].form=id
                    if actors[a].choice~=id then errors=errors+1 end
                    pending[#pending+1]={at=frame+2,form=id}
                elseif pc==0xffa16700 and id==6 and (old==17 or old==18) then
                    restores[old]=restores[old]+1;actors[a].form=nil;actors[a].restored_at=frame;actors[a].restored_from=old
                    pending[#pending+1]={at=frame+2,restore=old}
                elseif id~=6 and id>11 and id~=17 and id~=18 then errors=errors+1 end
            end)
            taps[#taps+1]=p:install_write_tap(m+0x1f0,m+0x22f,'morph action and flags diagnosis',function(at,data,mask)
                if not native(a,m) then return end
                local id=p:read_u16(a+0x1f0)
                if id~=17 and id~=18 then return end
                local regs={}
                for i=0,14 do regs[#regs+1]=string.format('a%d=%08X',i,cpu['A'..i].value) end
                log('PROCESS_WRITE',string.format('actor=%08X main=%08X id=%d address=%08X old=%08X data=%08X mask=%08X pc=%08X %s',a,m,id,at,p:read_u32(at),data,mask,cpu.PC.value,table.concat(regs,' ')))
            end)
        end
        local id=p:read_u16(a+0x1f0)
        local record=actors[a]
        if id==6 and record.restored_at and frame<=record.restored_at+120 then
            log('RESTORED_FIELD',string.format('actor=%08X main=%08X from=%d age=%d id=6 roster=6 state=0 stage=14 mode=%d action=%04X pose=%08X y=%d floor=%d vx=%08X vy=%08X body=%04X trail=%08X',a,m,record.restored_from,frame-record.restored_at,p:read_u16(0x010601d0),p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),p:read_i16(a+0xb0),p:read_i16(m+0x200),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u16(a+0x160),p:read_u32(m+0x190)))
        end
        if id==17 or id==18 then
            fields=fields+1
            log('FIELD',string.format('actor=%08X main=%08X id=%d roster=6 state=0 stage=14 mode=%d action=%04X pose=%08X list=%08X x=%d y=%d floor=%d vx=%08X vy=%08X flags=%04X body=%04X trail=%08X health=%d',a,m,id,p:read_u16(0x010601d0),p:read_u16(m+0x1f0),p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_i16(a+0x90),p:read_i16(a+0xb0),p:read_i16(m+0x200),p:read_u32(a+0x40),p:read_u32(a+0x60),p:read_u16(a+0xf0),p:read_u16(a+0x160),p:read_u32(m+0x190),p:read_u16(0x01060ec0)))
            if fields==60 or fields==200 or fields==540 then manager.machine.screens[':screen']:snapshot(string.format('shang_live_%d_%d.png',id,frame)) end
            if fields<140 or fields%60==0 then
                local saved={};for at=0x30,0x100,0x10 do saved[#saved+1]=string.format('m%03X=%04X',at,p:read_u16(m+at)) end
                log('SAVED_TASK',string.format('actor=%08X main=%08X id=%d %s',a,m,id,table.concat(saved,' ')))
            end
        end
    end
    for _,s in ipairs(pending) do
        if s.at==frame then manager.machine.screens[':screen']:snapshot(string.format('shang_%s_%d_%d.png',s.form and 'form' or s.restore and 'restore' or 'transition',s.form or s.restore or s.group,frame)) end
    end
end)
emu.register_stop(function()
    log('RESULT',string.format('kano=%d sonya=%d restore_kano=%d restore_sonya=%d fields=%d errors=%d fixture_health_writes=%d scope=diagnostic_native_random_morph_not_human_commands_or_full_goal',forms[17],forms[18],restores[17],restores[18],fields,errors,health_writes))
    for _,tap in ipairs(taps) do tap:remove() end
    for _,record in pairs(actors) do if record.tap then record.tap:remove() end end
end)
