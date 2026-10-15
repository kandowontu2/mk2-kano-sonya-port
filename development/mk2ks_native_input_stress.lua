-- Deterministic two-human controller stress on the real Kano/Sonya IDs.
-- The selector harness owns character selection and its existing display,
-- identity, name, cleanup, and stall checks. This layer writes inputs only.
assert(os.getenv("MK2KS_TWO_PLAYER") == "1")
dofile("mk2ks_selector_exit_test.lua")

local frame, active, first, program, controls = 0, 0, nil, nil, nil
local expected = {
    kano = 17, sonya = 18,
}
local p1_id = assert(expected[os.getenv("MK2KS_TEST_FIGHTER")])
local p2_id = assert(expected[os.getenv("MK2KS_P2_FIGHTER")])
assert(p1_id ~= p2_id)
local min_x, max_x = {0xffff,0xffff}, {0,0}
local changes, last_action, identity_errors = {0,0}, {nil,nil}, 0
local health_drops = {0,0}
local last_health = {nil,nil}
local function signed(word) return word >= 0x8000 and word-0x10000 or word end

emu.register_frame(function()
    frame=frame+1
    if not program then
        program=manager.machine.devices[":maincpu"].spaces.program
        local high=manager.machine.ioport.ports[":IN0"].fields
        local low=manager.machine.ioport.ports[":IN2"].fields
        controls={}
        for side=1,2 do
            local prefix="P"..side.." "
            controls[side]={
                left=high[prefix.."Left"],right=high[prefix.."Right"],
                up=high[prefix.."Up"],down=high[prefix.."Down"],
                hp=high[prefix.."High Punch"],hk=high[prefix.."High Kick"],
                lp=low[prefix.."Low Punch"],lk=low[prefix.."Low Kick"],
                block=high[prefix.."Block"]}
        end
    end
    local p1=program:read_u32(0x01060220)
    local p2=program:read_u32(0x01060df0)
    local valid=p1>=0x01000000 and p1<0x01100000 and
        p2>=0x01000000 and p2<0x01100000
    local ids=valid and {program:read_u16(p1+0x1f0),program:read_u16(p2+0x1f0)} or nil
    local combat=valid and program:read_u16(0x01061b00)==0 and
        program:read_u16(0x010602f0)>0 and program:read_u16(0x01060ec0)>0 and
        program:read_u16(0x01060280)==p1_id and
        program:read_u16(0x01060e50)==p2_id
    if not combat then
        if first then
            for _,set in ipairs(controls) do
                for _,field in pairs(set) do field:clear_value() end
            end
        end
        return
    end
    if not first then
        first=frame
        print(string.format("MK2KS_INPUT_STRESS_ENTER frame=%d ids=%d,%d",frame,p1_id,p2_id))
        manager.machine.video:snapshot()
    end
    active=active+1
    if ids[1]~=p1_id or ids[2]~=p2_id then identity_errors=identity_errors+1 end
    local actors={p1,p2}
    local x={signed(program:read_u16(p1+0x90)),signed(program:read_u16(p2+0x90))}
    local tasks={program:read_u32(0x01060260),program:read_u32(0x01060e30)}
    local health={program:read_u16(0x010602f0),program:read_u16(0x01060ec0)}
    for side=1,2 do
        min_x[side]=math.min(min_x[side],x[side])
        max_x[side]=math.max(max_x[side],x[side])
        if tasks[side]>=0x01000000 and tasks[side]<0x01100000 then
            local action=program:read_u16(tasks[side]+0x1f0)
            if last_action[side] and action~=last_action[side] then
                changes[side]=changes[side]+1
            end
            last_action[side]=action
        end
        if last_health[side] and health[side]<last_health[side] and health[side]>=10 then
            health_drops[side]=health_drops[side]+1
        end
        last_health[side]=health[side]
        local set=controls[side]
        for _,field in pairs(set) do field:clear_value() end
        local opponent=3-side
        local toward=x[opponent]>=x[side] and "right" or "left"
        local away=toward=="right" and "left" or "right"
        local phase=(active+(side==2 and 117 or 0))%240
        if phase<30 then set[toward]:set_value(1)
        elseif phase<60 then set[away]:set_value(1)
        elseif phase<85 then
            set.down:set_value(1)
            if phase<65 then set.hp:set_value(1) end
        elseif phase<110 then set.block:set_value(1)
        elseif phase<140 then
            if phase<114 then set.up:set_value(1);set[toward]:set_value(1) end
            if phase>=123 and phase<127 then set.hk:set_value(1) end
        elseif phase<170 then
            set[toward]:set_value(1)
            if phase>=148 and phase<152 then set.hp:set_value(1) end
        elseif phase<200 then
            set.down:set_value(1)
            if phase>=178 and phase<182 then set.lk:set_value(1) end
        else
            if phase>=205 and phase<209 then set.lp:set_value(1) end
            if phase>=220 and phase<224 then set.hk:set_value(1) end
        end
    end
    if active%600==0 then
        print(string.format("MK2KS_INPUT_STRESS_STATE frame=%d active=%d x=%d,%d hp=%d,%d actions=%d,%d",
            frame,active,x[1],x[2],health[1],health[2],changes[1],changes[2]))
        manager.machine.video:snapshot()
    end
end)

emu.register_stop(function()
    print(string.format("MK2KS_INPUT_STRESS_RESULT first=%s active=%d ids=%d,%d identity_errors=%d xspan=%d,%d action_changes=%d,%d health_drops=%d,%d",
        tostring(first),active,p1_id,p2_id,identity_errors,
        max_x[1]-min_x[1],max_x[2]-min_x[2],
        changes[1],changes[2],health_drops[1],health_drops[2]))
end)
