-- Normal-input Liu trial. The whole successful Sub-Zero branch stays intact.
local path='mk2ks_native_paired_stumble_subzero_guard_pressure.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before="replacement=ranged..'\\n'..replacement"
local after=[=========================[
local liu_range=ranged
liu_range=ring_once(liu_range,'other.roster==8','other.roster==1')
liu_range=ring_once(liu_range,'target.roster~=8','target.roster~=1')
liu_range=ring_once(liu_range,'target.id~=8','target.id~=1')
-- Task addresses can be reused across opponents. Separate passive tap keys
-- so the old CPU8 callback cannot suppress the CPU1-owned observer.
liu_range=ring_once(liu_range,"tostring(n)..':'..tostring(observed_main)",
 "tostring(n)..':'..tostring(observed_main)..':liu1'")
local history='subzero_guard_pressure_inputs'
local a,b=assert(liu_range:find(history,1,true))
liu_range=liu_range:sub(1,a-1)..'liu_early_leg_inputs'..liu_range:sub(b+1)
a,b=assert(liu_range:find(history,1,true))
liu_range=liu_range:sub(1,a-1)..'liu_early_leg_inputs'..liu_range:sub(b+1)
assert(not liu_range:find(history,1,true))
-- No inference that a Liu action ordinal is Sub-Zero's freeze startup.
liu_range=ring_once(liu_range,
 "    if other.action==0x604 and feedback.last_cpu~=0x604 then\n     feedback.guard_until=frame+45\n    end\n",'')
liu_range=ring_once(liu_range,
 "    elseif frame<feedback.guard_until then\n     reason='guard_pressure_visible_freeze_guard';press('Down');press('Block')\n",'')
liu_range=ring_once(liu_range,'cpu_height<=8 and other.action~=0x604 and',
 'cpu_height<=8 and')
replacement=ranged..'\n'..liu_range..'\n'..replacement
print('MK2_CURRENT_LIU_EARLY_LEG_POLICY player=sonya slot=1 true_cpu=1 leg_gap=115 earlier_twelve_inputs=unchanged native_contact=required writes=0 assistance=none')
]=========================]
local a,b=source:find(before,1,true)
assert(a and not source:find(before,b+1,true),'One late CPU1-only clone boundary')
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@'..path..'::only_Liu_earlier_physical_leg_inputs','t',_ENV))()
