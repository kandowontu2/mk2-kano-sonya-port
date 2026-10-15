-- Original cold selection/physical controller and whole passive observers.
-- Add Sonya's actual router alongside the preserved Kano-only observer.
dofile('mk2ks_native_selector_cpu_first_round_projectile.lua')
local file=assert(io.open('mk2ks_physical_p2_cpu_choice_trace_v3303.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local function replace(before,after)
 local first,last=assert(source:find(before,1,true))
 assert(not source:find(before,last+1,true),'One exact passive boundary')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
-- Do not install a second controller. All original Sonya ownership filters,
-- RNG-return/status taps and original router/RNG code windows remain intact.
replace("dofile('mk2ks_physical_p2_cpu_overlap_trace_v3302.lua')",'')
replace('MK2_CPU_CHOICE_%s','MK2_SONYA_CHOICE_%s')
replace("if kind=='square'then manager.machine.screens[':screen']:snapshot('native_square_choice_'..frame..'.png')end", [[
  if kind=='ring' or kind=='square' or kind=='bicycle' then
   local raw,w,h=manager.machine.screens[':screen']:pixels()
   assert(w==400 and h==254 and #raw==406400)
   local hex=raw:gsub('.',function(c)return string.format('%02X',c:byte())end)
   print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=sonya_choice_%s_%d width=%d height=%d bytes=%d hex=%s',frame,kind,serial,w,h,#raw,hex))
  end]])
assert(not source:find(':snapshot',1,true),'No new media files')
assert(load(source,'@whole_original_sonya_native_choices_passive','t',_G))()
