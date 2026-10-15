-- Read-only complete entry/context for original native sprite coordinates.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[':maincpu']
d:command('dasm audit_v649_native_sprite_coordinate_code/body-context.asm,FF804000,480')
d:command('save audit_v649_native_sprite_coordinate_code/compiled-roll.bin,FFFFEC00,100')
d.execution_state='run'
