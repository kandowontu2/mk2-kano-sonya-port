-- Read-only original MKII shadow-row engine, no gameplay or guest writes.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[':maincpu']
d:command('dasm audit_v632_native_shadow_geometry/engine.asm,FF801000,800')
d.execution_state='run'
