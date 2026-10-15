-- Observe A5's original ADDXY display-buffer origin as well as world/camera.
local file=assert(io.open('mk2ks_current_babality_ram_v5452.lua','rb'))
local source=file:read('*a');file:close()
local changes={
 {'body=cpu.A7.value,command=cpu.A12.value','display=cpu.A5.value,body=cpu.A7.value,command=cpu.A12.value'},
 {'world=%08X camera=%08X body=%08X','world=%08X camera=%08X display=%08X body=%08X'},
 {'q.world,q.camera,q.body,q.command','q.world,q.camera,q.display,q.body,q.command'}
}
for _,change in ipairs(changes)do
 local first,last=assert(source:find(change[1],1,true));assert(not source:find(change[1],last+1,true))
 source=source:sub(1,first-1)..change[2]..source:sub(last+1)
end
assert(load(source,'@native_A5_display_origin_only_added_to_passive_baby_FIFO_record','t',_ENV))()
