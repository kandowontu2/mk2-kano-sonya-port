-- Diagnostic-only MK3 DCS command injection; never loaded by the MKII port.
-- A no-command run provides a time-aligned baseline for audio subtraction.
local command_text = os.getenv("MK3_PROBE_SOUND_CMD")
local command = command_text and tonumber(command_text, 16) or nil
local same_frame = os.getenv("MK3_PROBE_SOUND_SAME_FRAME") == "1"
local byte_write = os.getenv("MK3_PROBE_SOUND_U8") == "1"
local trace_port = os.getenv("MK3_PROBE_TRACE_PORT") == "1"
local gap_us = tonumber(os.getenv("MK3_PROBE_SOUND_GAP_US") or "0")
assert(not command or command >= 0 and command <= 0xffff)
assert(gap_us >= 0 and gap_us <= 10000)
local frame, program, port_tap = 0, nil, nil
local function send(value)
    if byte_write then program:write_u8(0x01680000, value)
    else program:write_u16(0x01680000, value) end
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        program = manager.machine.devices[":maincpu"].spaces["program"]
        if trace_port then
            port_tap = program:install_write_tap(0x01680000, 0x0168001f,
                "isolated donor sound byte delivery", function(offset, data, mask)
                    if frame >= 1199 and frame <= 1202 then
                        print(string.format("MK3_PROBE_PORT frame=%d address=%08X data=%04X mask=%04X",
                            frame, offset, data & 0xffff, mask & 0xffff))
                    end
                end)
        end
    end
    if command and frame == 1200 then
        send((command >> 8) & 0xff)
        print(string.format("MK3_PROBE_SOUND_HIGH frame=%d command=%04X", frame, command))
        if gap_us > 0 then
            local thread = coroutine.create(function()
                emu.wait(gap_us / 1000000)
                send(command & 0xff)
                print(string.format("MK3_PROBE_SOUND_LOW frame=%d command=%04X gap_us=%d",
                    frame, command, gap_us))
            end)
            assert(coroutine.resume(thread))
        elseif same_frame then
            send(command & 0xff)
            print(string.format("MK3_PROBE_SOUND_LOW frame=%d command=%04X", frame, command))
        end
    elseif command and frame == 1201 and not same_frame and gap_us == 0 then
        send(command & 0xff)
        print(string.format("MK3_PROBE_SOUND_LOW frame=%d command=%04X", frame, command))
    end
end)
