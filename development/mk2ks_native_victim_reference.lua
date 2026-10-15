-- Read-only discovery. No gameplay writes, inputs, or actor substitutions.
local cpu=assert(manager.machine.devices[":maincpu"])
local p=cpu.spaces.program
local d=assert(manager.machine.debugger)
d.visible_cpu=cpu
d:command("dasm audit_v262_native_fatality_core.asm,FF8C0000,10000")
d:command("dasm audit_v262_native_up_dispatch.asm,FF866000,2000")
d:command("dasm audit_v262_native_palette_helpers.asm,FFA11F00,2000")
d:command("dasm audit_v262_native_victim_effects.asm,FF8EA3F0,600")
d:command("dasm audit_v262_native_group_renderer.asm,FF838650,1600")
d:command("dasm audit_v262_native_frame_palette.asm,FF83AA00,1600")
d:command("dasm audit_v262_native_palette_queue.asm,FF80C600,900")
d:command("dasm audit_v262_native_palette_ownership.asm,FF80CF60,900")
d:command("dasm audit_v262_native_actor_palette_switch.asm,FF90C800,600")
d:command("dasm audit_v262_native_corpse_retirement.asm,FF8CDC40,400")
d:command("dasm audit_v262_native_palette_switch_core.asm,FF840450,1100")
d:command("dasm audit_v262_native_palette_switch_apply.asm,FF841090,400")
for index=0,11 do
    local ptr=p:read_u32(0xff800000+(0xff180+index*0x50)*8+2*32)
    print(string.format("MK2_NATIVE_CAGE_DISPATCH index=%d ptr=%08X",index,ptr))
    if ptr>=0xff800000 and ptr<0xffff0000 then
        d:command(string.format("dasm audit_v262_native_cage_dispatch_%02d.asm,%08X,2000",index,ptr))
    end
end
for _,kind in ipairs({{"main",0xfffe4000},{"special",0xfffe4400}}) do
    for _,id in ipairs({2,11}) do
        local root=p:read_u32(kind[2]+id*32)
        print(string.format("MK2_NATIVE_ROOT kind=%s id=%d root=%08X",kind[1],id,root))
        for index=0,63 do
            local ptr=p:read_u32(root+index*32)
            local values={}
            if ptr>=0xff800000 and ptr<0xffff0000 then
                for n=0,11 do values[#values+1]=string.format("%08X",p:read_u32(ptr+n*32)) end
            end
            print(string.format("MK2_NATIVE_ANIM kind=%s id=%d index=%d ptr=%08X words=%s",
                kind[1],id,index,ptr,table.concat(values,",")))
        end
    end
end
d.execution_state="run"
