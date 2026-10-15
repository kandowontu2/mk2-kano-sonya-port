-- Add only the missing passive true Sonya AI-choice observer. The original
-- accepted physical driver, current cold/HP/state/audio observers remain once.
local file=assert(io.open('mk2ks_physical_p2_cpu_choice_trace_v3303.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("dofile('mk2ks_physical_p2_cpu_overlap_trace_v3302.lua')",'-- Controller supplied once by the original outer driver below.')
once("  if kind=='square'then manager.machine.screens[':screen']:snapshot('native_square_choice_'..frame..'.png')end",'  -- Passive source-only observer: no persistent raw snapshots.')
once('MK2_CPU_CHOICE_%s','MK2_SONYA_STARTUP_CHOICE_%s')
assert(load(source,'@whole_original_passive_Sonya_AI_choices_new_namespace','t',_G))()
dofile('mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua')
