-- Original animation script tokens and Sonya victim list; read-only.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v265_original_victim_script.asm,FF9635F0,C00")
d:command("dasm audit_v265_original_sonya_victim_list.asm,FF9B2BF0,120")
d.execution_state="run"
