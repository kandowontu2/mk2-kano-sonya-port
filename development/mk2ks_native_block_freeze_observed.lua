-- Ordinary physical Freeze and Block; corrected passive native launch taps.
local path='mk2ks_normal_subzero_freeze_v5031.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local function replace(before,after)
 local a,b=source:find(before,1,true)
 assert(a and not source:find(before,b+1,true),'One original observer/input anchor')
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
replace("0xff86bb80,'ICE_REQUEST'","0xff86f9d0,'ICE_REQUEST'")
replace("0xff86bab0,'PROJECTILE_SETUP'","0xff8a5900,'PROJECTILE_SETUP'")
local policy=assert(os.getenv('MK2KS_BLOCK_POLICY'))
assert(policy=='none' or policy=='held' or policy=='reactive')
_G.mk2ks_observed_freeze_frame=nil
replace("   if age>=90 and age<93 then press(winner_side,'Down')end",
 "   if age<300 and ((os.getenv('MK2KS_BLOCK_POLICY')=='held' and age>=70) or (os.getenv('MK2KS_BLOCK_POLICY')=='reactive' and _G.mk2ks_observed_freeze_frame and frame>_G.mk2ks_observed_freeze_frame)) then press(side,'Block')end\n   if age>=90 and age<93 then press(winner_side,'Down')end")
replace("  if id~=identity and id~=8 then return end",
 "  if id~=identity and id~=8 then return end\n  if tag=='PROJECTILE_SETUP' and id==8 then _G.mk2ks_observed_freeze_frame=frame end")
assert(load(source,'@'..path..'::physical_Block_corrected_readonly_launch_taps','t',_ENV))()
