-- Diagnostic: reach a native hidden-CPU fight, then observe its movement.
-- The ladder harness wins the opening match; this wrapper overrides only P1
-- inputs in the hidden match and can restore P1 health to keep the audit live.
-- Set MK2KS_HIDDEN_MOTION_ID to the injected CPU ID (14, 15, or 16).
dofile("mk2ks_cpu_ladder_trace.lua")

local frame, program, buttons = 0, nil, nil
local hidden_id = tonumber(os.getenv("MK2KS_HIDDEN_MOTION_ID") or "14")
assert(hidden_id == 14 or hidden_id == 15 or hidden_id == 16)
local hidden_fields, airborne_fields, jump_starts, near_fields = 0, 0, 0, 0
local last_airborne, min_x, max_x = false, 0xffff, 0
local last_action, action_changes = nil, 0
local function signed(value) return value >= 0x8000 and value - 0x10000 or value end
emu.register_frame(function()
    frame = frame + 1
    if not program then
        program = manager.machine.devices[":maincpu"].spaces.program
        local ports = manager.machine.ioport.ports
        local high, low = ports[":IN0"].fields, ports[":IN2"].fields
        buttons = {high["P1 Left"], high["P1 Right"], high["P1 Up"],
            high["P1 Down"], high["P1 High Punch"], high["P1 Block"],
            low["P1 Low Punch"], high["P1 High Kick"], low["P1 Low Kick"]}
    end
    local actor = program:read_u32(0x01060df0)
    local player = program:read_u32(0x01060220)
    if actor < 0x01000000 or actor >= 0x01100000 or
        player < 0x01000000 or player >= 0x01100000 or
        program:read_u16(actor + 0x1f0) ~= hidden_id or
        program:read_u16(player + 0x1f0) ~= 17 or
        program:read_u16(0x01061b30) ~= 1 or
        program:read_u16(0x01060ec0) ~= 161 then return end
    for _, button in ipairs(buttons) do button:set_value(0) end
    local hp = program:read_u16(0x010602f0)
    if hp > 0 and hp < 161 then program:write_u16(0x010602f0, 161) end
    local process = program:read_u32(0x01060e30)
    if process < 0x01000000 or process >= 0x01100000 then return end
    local x, y = signed(program:read_u16(actor + 0x90)), signed(program:read_u16(actor + 0xb0))
    local floor_y = signed(program:read_u16(process + 0x200))
    local player_x = signed(program:read_u16(player + 0x90))
    local action = program:read_u16(process + 0x1f0)
    local airborne = y + 10 < floor_y
    hidden_fields = hidden_fields + 1
    if airborne then airborne_fields = airborne_fields + 1 end
    if airborne and not last_airborne then jump_starts = jump_starts + 1 end
    if math.abs(player_x - x) <= 75 then near_fields = near_fields + 1 end
    if x < min_x then min_x = x end
    if x > max_x then max_x = x end
    if action ~= last_action then
        if action_changes < 60 then
            print(string.format("MK2KS_HIDDEN_CPU_MOTION frame=%d action=%04X x=%d px=%d y=%d floor=%d hp=%d",
                frame, action, x, player_x, y, floor_y, hp))
        end
        action_changes = action_changes + 1
    end
    last_action, last_airborne = action, airborne
end)
emu.register_stop(function()
    print(string.format("MK2KS_HIDDEN_CPU_MOTION_RESULT id=%d fields=%d airborne=%d jumps=%d near=%d min_x=%d max_x=%d actions=%d",
        hidden_id, hidden_fields, airborne_fields, jump_starts, near_fields,
        min_x, max_x, action_changes))
end)
