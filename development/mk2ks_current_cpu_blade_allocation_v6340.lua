-- Same genuine physical trajectory. Keep retired blade and later knife distinct.
-- Every later Main-field write is still logged, never silently discarded.
dofile('mk2ks_current_kano_cpu_extended_ram_v6290.lua')
local file=assert(io.open('mk2ks_blade_allocation_v2892.lua','rb'))
local original=file:read('*a'):gsub('\r\n','\n');file:close()
local function replace(before,after)
 local first=assert(original:find(before,1,true))
 assert(not original:find(before,first+1,true),'One explicit observer-lifetime repair')
 original=original:sub(1,first-1)..after..original:sub(first+#before)
end
replace("log('TRAIL_STORE',string.format(",
        "log(ctx.detached and 'LATER_PARENT_STORE' or 'TRAIL_STORE',string.format(")
replace('if ctx.object and merged==0 and state.PC.value==0xff83f050 then ctx.detached=frame end',
        'if ctx.object and not ctx.detached and merged==0 and state.PC.value==0xff83f050 and state.A10.value==ctx.object then ctx.detached=frame end')
local marker="local p=manager.machine.devices[':maincpu'].spaces.program"
local first=assert(original:find(marker,1,true))
assert(not original:find(marker,first+1,true),'Whole original observer after driver preamble')
assert(load(original:sub(first),'@current_CPU_blade_lifetime_v6340','t',_G))()
