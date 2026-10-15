local done = false

emu.register_frame(function()
    if done then return end
    done = true
    local cpu = manager.machine.devices[":maincpu"]
    for name, entry in pairs(cpu.state) do
        print(string.format("MK3STATE name=%s value=%08X", name, entry.value))
    end
end)
