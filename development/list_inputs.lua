local done = false

emu.register_frame(function()
    if done then return end
    done = true
    for tag, port in pairs(manager.machine.ioport.ports) do
        print("PORT " .. tag)
        for name, field in pairs(port.fields) do
            print(string.format("  %s mask=%04X", name, field.mask))
        end
    end
end)
