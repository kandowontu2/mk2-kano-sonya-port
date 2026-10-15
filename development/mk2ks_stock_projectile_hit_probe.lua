-- Stock MKII Liu Kang projectile comparison for the port's hit effect.
-- Uses only real P1 inputs; no fighter state, position or health writes.
dofile("mk2ks_selector_exit_test.lua")

local frame, program, screen, controls = 0, nil, nil, nil
local first_ready, last_health, hits = nil, nil, 0
local victim_id=({kitana=4,sonya=18})[os.getenv("MK2KS_STOCK_PROJECTILE_VICTIM") or "kitana"]
assert(victim_id,"Choose stock Kitana or imported Sonya as the victim")
local function pulse(field, age, start)
    if age >= start and age < start + 3 then field:set_value(1) end
end

emu.register_frame(function()
    frame=frame+1
    if not program then
        program=manager.machine.devices[":maincpu"].spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        controls={left=high["P1 Left"],right=high["P1 Right"],hp=high["P1 High Punch"]}
    end
    local p1,p2=program:read_u32(0x01060220),program:read_u32(0x01060df0)
    if p1<0x01000000 or p1>=0x01100000 or p2<0x01000000 or p2>=0x01100000 or
        program:read_u16(p1+0x1f0)~=1 or program:read_u16(p2+0x1f0)~=victim_id then return end
    local h1,h2=program:read_u16(0x010602f0),program:read_u16(0x01060ec0)
    if h1==0 or h2==0 then return end
    if not first_ready and h1==161 and h2==161 then
        first_ready=frame
        last_health=h2
        print(string.format("MK2KS_STOCK_PROJECTILE_READY frame=%d p1=%08X p2=%08X victim_id=%d",
            frame,p1,p2,victim_id))
    end
    if not first_ready then return end
    local age=frame-first_ready
    local x1,x2=program:read_u16(p1+0x90),program:read_u16(p2+0x90)
    local forward=x1<x2 and controls.right or controls.left
    for _,start in ipairs({220,330,440,550,660,770}) do
        pulse(forward,age,start)
        pulse(forward,age,start+8)
        pulse(controls.hp,age,start+16)
    end
    if age>=210 and age<=850 and age%4==0 then
        screen:snapshot(string.format("stock_projectile_age%04d.png",age))
    end
    if last_health and h2<last_health then
        hits=hits+1
        print(string.format("MK2KS_STOCK_PROJECTILE_HIT frame=%d age=%d health=%d->%d x=%d,%d",
            frame,age,last_health,h2,x1,x2))
        screen:snapshot(string.format("stock_projectile_hit%02d_age%04d.png",hits,age))
    end
    last_health=h2
end)

emu.register_stop(function()
    print(string.format("MK2KS_STOCK_PROJECTILE_RESULT ready=%s hits=%d",
        tostring(first_ready~=nil),hits))
end)
