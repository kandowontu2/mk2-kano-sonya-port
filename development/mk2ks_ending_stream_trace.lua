dofile("mk2ks_cpu_ladder_trace.lua")
local frame, tap, setup_tap, seen = 0, nil, nil, {}
emu.register_frame(function()
    frame = frame + 1
    if tap then return end
    local cpu = manager.machine.devices[":maincpu"]
    local program = cpu.spaces.program
    setup_tap = program:install_read_tap(0xff904440, 0xff9044ff,
        "native ending codebooks", function(offset, data, mask)
            local pc = cpu.state.PC.value
            if (pc == 0xff904440 or pc == 0xff9044d0) and frame > 3000 and not seen[pc] then
                seen[pc] = true
                print(string.format("MK2KS_END_CODEBOOK frame=%d pc=%08X A8=%08X A7=%08X B2=%08X A4=%08X A6=%08X",
                    frame, pc, cpu.state.A8.value, cpu.state.A7.value,
                    cpu.state.B2.value, cpu.state.A4.value, cpu.state.A6.value))
            end
        end)
    tap = program:install_read_tap(0xff904a30, 0xff904a7f,
        "native ending stream entry", function(offset, data, mask)
            local pc = cpu.state.PC.value
            if pc == 0xff904a60 and frame > 3000 then
                local a8 = cpu.state.A8.value
                local origin = cpu.state.B2.value
                if not seen[origin] then
                    seen[origin] = true
                    print(string.format("MK2KS_END_STREAM frame=%d source=%08X first_pixel=%08X skip_bytes=%d A9=%08X B3=%08X B9=%d A11=%d",
                        frame, origin, a8, (a8-origin)//8, cpu.state.A9.value,
                        cpu.state.B3.value, cpu.state.B9.value, cpu.state.A11.value))
                end
            end
        end)
end)
