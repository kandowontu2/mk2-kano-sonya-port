-- Exact existing physical route/observer binding, plus the missing native
-- horizontal write operand registers. No new driver or game/register writes.
local f=assert(io.open('mk2ks_native_selector_sonya_choice_shadow_bound.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once('local original_dofile=function(path)','local function original_dofile(path)')
once('a8=%08X a13=%08X writes=0 assistance=none',
     'a8=%08X a13=%08X a6=%08X a7=%08X a9=%08X a10=%08X a11=%08X a12=%08X a14=%08X status=%08X writes=0 assistance=none')
once('regs.A4.value,regs.A5.value,regs.A8.value,regs.A13.value))',
     'regs.A4.value,regs.A5.value,regs.A8.value,regs.A13.value,regs.A6.value,regs.A7.value,regs.A9.value,regs.A10.value,regs.A11.value,regs.A12.value,regs.A14.value,regs.ST.value))')
assert(not source:match(':write_[ui]%d+')and not source:match('%.value%s*=[^=]'))
assert(load(source,'@whole_original_bound_Sonya_with_complete_horizontal_operands','t',_G))()
