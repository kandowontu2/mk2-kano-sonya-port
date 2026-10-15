local count=0
emu.register_frame(function()
    count=count+1
    if count~=30 then return end
    local api=emu.plugin and emu.plugin.cheat
    print("MK3_CHEAT_API available="..tostring(api~=nil))
    if api then
        for index,name in pairs(api.list()) do
            if name:find("Fatality") then
                print(string.format("MK3_CHEAT_ENTRY %d %s",index,name))
                local entry=api.get(index)
                if entry and entry.parameter then
                    for slot,item in pairs(entry.parameter.item or {}) do
                        print(string.format("MK3_CHEAT_PARAM entry=%d slot=%d value=%s text=%s",
                            index,slot,tostring(item.value),item.text))
                    end
                end
            end
        end
    end
end)
