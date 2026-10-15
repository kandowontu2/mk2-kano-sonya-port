-- Read-only loaded candidate code and native stock body rows.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v264_skeleton_action_loaded.asm,FFFB8000,3000")
local p=manager.machine.devices[":maincpu"].spaces.program
for id=0,11 do
    local groups={}
    for phase=0,5 do groups[#groups+1]=string.format("%08X",p:read_u32(0xff800000+0xf7a00*8+id*256+phase*32)) end
    print(string.format("MK2_NATIVE_STOCK_BODY_ROW id=%d groups=%s primary=%08X alternate=%08X",id,table.concat(groups,","),p:read_u32(0xff90c900+id*64),p:read_u32(0xff90c920+id*64)))
end
d.execution_state="run"
