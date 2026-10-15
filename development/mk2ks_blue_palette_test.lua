-- Normal two-player selection and special inputs. All memory access is read-only.
dofile("mk2ks_selector_exit_test.lua")
local effect=assert(os.getenv("MK2KS_BLUE_EFFECT"))
local victim=assert(os.getenv("MK2KS_BLUE_VICTIM"))
local side=assert(tonumber(os.getenv("MK2KS_BLUE_SIDE")))
assert(effect=="freeze" or effect=="shock")
assert(side==1 or side==2)
local ids={kano=17,sonya=18,cage=2}
local id=assert(ids[victim])
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local screen=manager.machine.screens[":screen"]
local controls={}
for _,port in ipairs({":IN0",":IN2"}) do
    for name,field in pairs(manager.machine.ioport.ports[port].fields) do controls[name]=field end
end
local pointers={0x01060220,0x01060df0}
local frame,start,checks,errors=0,nil,0,0
local blue_queues,blue_fields,restores,bad_queues=0,0,0,0
local lookups,normal_fields=0,0
local last_blue,last_restore=-1000,-1000
local donor={ [17]=0xfea66010,[18]=0xfea643a0 }
local table_address,record,normal_records
local taps={}
local function check(ok,label)
    checks=checks+1
    if not ok then
        errors=errors+1
        if errors<=15 then print("MK2_BLUE_ERROR "..label) end
    end
end
local function valid(actor) return actor>=0x01000000 and actor<0x01100000 end
local function live()
    return start and frame-start<1300 and p:read_u16(0x010601d0)==2
end
taps[1]=p:install_read_tap(0xff80c6b0,0xff80c6bf,"owned blue palette enqueue",function(at)
    if at~=0xff80c6b0 or not live() then return end
    local source,pen,count=cpu.A0.value,cpu.A1.value&0xffff,cpu.A2.value&0xffff
    if count>256 or source<0x01000000 then
        bad_queues=bad_queues+1
        check(false,string.format("invalid enqueue source=%08X pen=%04X count=%d",source,pen,count))
    end
    if source==record+16 then
        blue_queues=blue_queues+1;last_blue=frame
        check(count==64,"native blue copy has exactly 64 colours")
        print(string.format("MK2_BLUE_QUEUE frame=%d effect=%s victim=%s side=%d source=%08X pen=%04X count=%d",
            frame,effect,victim,side,source,pen,count))
    elseif blue_queues>0 and (source==normal_records[1]+16 or source==normal_records[2]+16) then
        restores=restores+1;last_restore=frame
        print(string.format("MK2_BLUE_RESTORE frame=%d source=%08X pen=%04X count=%d",frame,source,pen,count))
    end
end)
taps[2]=p:install_read_tap(effect=="freeze" and 0xff910960 or 0xff8dad90,
    effect=="freeze" and 0xff91096f or 0xff8dad9f,"native blue palette selection",function(at)
    if at==(effect=="freeze" and 0xff910960 or 0xff8dad90) and live() then
        lookups=lookups+1
        print(string.format("MK2_BLUE_LOOKUP frame=%d effect=%s victim=%s side=%d pc=%08X",frame,effect,victim,side,cpu.PC.value))
    end
end)
emu.register_frame(function()
    frame=frame+1
    assert(#taps==2)
    if not table_address then
        table_address=p:read_u32(0xff910970)
        check(table_address==p:read_u32(0xff8dada0),"shock and freeze use the same table")
        for stock=0,16 do
            check(p:read_u32(table_address+stock*32)==p:read_u32(0xff9109e0+stock*32),"stock row "..stock.." unchanged")
        end
        record=p:read_u32(table_address+id*32)
        check(record>=0xff800000 and record<=0xfffff000,"blue record is ROM-owned")
        if record>=0xff800000 then
            check(p:read_u16(record)==64,"blue record count")
            check(p:read_u16(record+16)==0,"transparent entry")
            if donor[id] then for color=0,63 do
                check(p:read_u16(record+16+color*16)==p:read_u16(donor[id]+16+color*16),"original frozen colour "..color)
            end end
        end
        normal_records={p:read_u32(p:read_u32(0xff906f40)+id*32),p:read_u32(p:read_u32(0xff907060)+id*32)}
        print(string.format("MK2_BLUE_TABLE effect=%s victim=%s side=%d table=%08X record=%08X",effect,victim,side,table_address,record))
    end
    local actor=p:read_u32(pointers[side])
    local attacker=p:read_u32(pointers[3-side])
    if not start then
        if frame>1200 and p:read_u16(0x010601d0)==2 and valid(actor) and valid(attacker) and
            p:read_u16(actor+0x1f0)==id and p:read_u16(attacker+0x1f0)==(effect=="freeze" and 8 or 7) then
            start=frame
            screen:snapshot("blue_before.png")
        end
        return
    end
    local age=frame-start
    if age>1300 then return end
    for player=1,2 do for _,name in ipairs({"Up","Down","Left","Right","High Punch","Low Punch","High Kick","Low Kick","Block"}) do
        controls["P"..player.." "..name]:clear_value()
    end end
    if not live() or not valid(actor) or not valid(attacker) then return end
    check(p:read_u16(actor+0x1f0)==id,"victim retains its own identity")
    local prefix="P"..(3-side).." "
    local forward=p:read_u16(attacker+0x90)<p:read_u16(actor+0x90) and "Right" or "Left"
    local direction=forward -- Both native MKII projectiles use Down, Forward + LP.
    local phase=(age-60)%260
    if age>=60 and age<1100 then
        if phase<3 then controls[prefix.."Down"]:set_value(1) end
        if phase>=5 and phase<8 then controls[prefix..direction]:set_value(1) end
        if phase>=6 and phase<9 then controls[prefix.."Low Punch"]:set_value(1) end
    end
    if frame>last_blue and blue_queues>0 then
        local bank=p:read_u16(actor+0x140)&0x7f00
        local mismatches,normal_mismatches=0,0
        local variant=(p:read_u16(actor+0x160)&0x40)~=0 and 2 or 1
        for color=1,63 do
            if p:read_u16(0x01800000+(bank+color)*16)&0x7fff~=p:read_u16(record+16+color*16)&0x7fff then mismatches=mismatches+1 end
            if p:read_u16(0x01800000+(bank+color)*16)&0x7fff~=p:read_u16(normal_records[variant]+16+color*16)&0x7fff then normal_mismatches=normal_mismatches+1 end
        end
        if mismatches==0 then
            blue_fields=blue_fields+1
            if blue_fields==10 then screen:snapshot("blue_active.png") end
        end
        if blue_fields>10 and normal_mismatches==0 then
            normal_fields=normal_fields+1
            if normal_fields==10 then screen:snapshot("blue_restored.png") end
        end
    end
    if frame==last_restore+3 then screen:snapshot("blue_restored.png") end
end)
emu.register_stop(function()
    check(start~=nil,"actual selected match began")
    check(blue_queues>=1 and lookups>=2,"repeated native special activation")
    check(blue_fields>=10,"rendered owned blue colours")
    check(normal_fields>=10,"native normal-palette restoration (cached records need no enqueue)")
    print(string.format("MK2_BLUE_RESULT pass=%s effect=%s victim=%s side=%d checks=%d errors=%d blue_queues=%d lookups=%d blue_fields=%d normal_fields=%d restores=%d bad_queues=%d writes=0 assistance=none",
        tostring(errors==0),effect,victim,side,checks,errors,blue_queues,lookups,blue_fields,normal_fields,restores,bad_queues))
end)
