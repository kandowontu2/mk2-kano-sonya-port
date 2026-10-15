-- Read-only original MK3 portrait/ending lookup provenance.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v275_mk3_bio_picture.asm,FF96F280,1000")
d:command("dasm audit_v275_mk3_bio_scene.asm,FF96E580,1600")
d:command("dasm audit_v275_mk3_ending_scene.asm,FF92E900,1400")
d:command("dasm audit_v275_mk3_picture_lookup.asm,FFAA6D00,1000")
d:command("dasm audit_v275_mk3_scene_lookup.asm,FF928340,800")
d.execution_state="run"
