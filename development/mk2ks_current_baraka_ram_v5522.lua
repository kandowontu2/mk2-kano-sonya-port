-- Whole5509 transport/ordered native observer, whole921 physical controller,
-- whole1003 actual detached-head/body observers. No game-state modifications.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_cage_ram_v5509.lua','rb'))
local s=f:read('*a');f:close();s=s:gsub('\r\n','\n')
local function replace_once(before,after)
 local first,last=assert(s:find(before,1,true));assert(not s:find(before,last+1,true))
 s=s:sub(1,first-1)..after..s:sub(last+1)
end
replace_once('frame-start>=69 and frame-start<=141','frame-start>=58 and frame-start<=199')
replace_once("filename:match('^torso_pose_')","filename:match('^head_pose_')")
replace_once("local observer=read('mk2ks_cage_torso_display_v979.lua')","local observer=read('mk2ks_rolling_head_display_v1003.lua')")
replace_once([=[observer=replace_once(observer,'local count=0xc04c -- Exact v894 packed allocation, including alignment.',
 'local count=p:read_u32(0xff300040) -- Actual compiled current death allocation, passive header read.')]=],
 '-- Original1003 already reads its exact actual current native-death header.')
replace_once("manager.machine.screens[':screen']:snapshot('torso_pose_'..item.key..'_'..frame..'.png')",
 "manager.machine.screens[':screen']:snapshot('head_pose_'..item.key..'_'..frame..'.png')")
replace_once("mk2_cage_ram_snapshot('torso_pose_'..item.key..'_'..frame..'.png')",
 "mk2_cage_ram_snapshot('head_pose_'..item.key..'_'..frame..'.png')")
local count=0
s=s:gsub('mk2_cage_ram_',function()count=count+1;return'mk2_baraka_ram_'end)
assert(count==9,'Exactly the entire RAM emitter/snapshot namespace')
count=0
s=s:gsub('CURRENT_CAGE_',function()count=count+1;return'CURRENT_BARAKA_'end)
assert(count==3,'Exactly actual ordered scene/RAM transport tags')
assert(load(s,'@entire5509_RAM_controller_transport_original1003_Baraka_native_observers','t',_ENV))()
