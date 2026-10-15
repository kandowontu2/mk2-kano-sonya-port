-- Read-only original native body-copy coordinate arithmetic.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[':maincpu']
d:command('dasm audit_v649_native_sprite_coordinate_code/body.asm,FF804200,600')
d.execution_state='run'
