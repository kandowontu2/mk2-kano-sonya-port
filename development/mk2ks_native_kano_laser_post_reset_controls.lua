-- Original native KO/round observers plus original adaptive human controls.
-- Prior human policy remains exact before reset. After reset, the last physical
-- input callback clears and owns only P1's ordinary buttons; CPU is untouched.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('*a'):gsub('\r\n','\n');f:close();return s
end
local function once(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true))
 return s:sub(1,a-1)..after..s:sub(b+1)
end
local loader=load
_G.load=function(s,name,mode,environment)
 if name=='@mk2ks_cpu_recovery_probe_v1438.lua'then
  s=once(s,'if complete_count>=2 and frame>=last_complete+30 then manager.machine:exit()end',
   '-- The actual post-reset adaptive control/recovery deadline owns observation exit.')
 end
 return loader(s,name,mode,environment)
end
local root=read('mk2ks_native_kano_laser_cpu_post_ko.lua')
root=once(root,"resumed=frame;log('RESUMED','actual_native_full_health_round')",
 "resumed=frame;MK2_POST_CTRL_READY=frame;log('RESUMED','actual_native_full_health_round')")
root=once(root,"if resumed and frame>=resumed+60 then terminal=true;log('END','sixty_actual_post_reset_fields');manager.machine:exit()end",
 "if MK2_POST_CTRL_RECOVERED and frame>=MK2_POST_CTRL_RECOVERED+180 then terminal=true;MK2_POST_CTRL_EXIT_PENDING=true;log('END','actual_control_recovery_plus_180_fields');manager.machine:exit()end")
assert(load(root,'@whole_original_post_KO_root_adaptive_deadline','t',_G))()
_G.load=loader

local original=read('mk2ks_single_continue_v6567.lua')
local function slice(first,last)
 local a=assert(original:find(first,1,true));assert(not original:find(first,a+1,true))
 local b=assert(original:find(last,a+#first,true));return original:sub(a,b-1)
end
local prefix=slice('local p=manager.machine.devices',"local buttons={}")
prefix=prefix..[[
local fighter,target,side='sonya','sonya',1
local ids={kano=17,sonya=18}
local frame,reReady,walk,jump,punch,recover,walkStart,jumpStart,punchStart,walkX=0
local pixels,width,height=nil,nil,nil
local buttons={};for _,name in ipairs({'Left','Right','Up','Down','High Punch','Block'})do buttons[name]=high['P1 '..name]end
local function log(tag,value)
 print(string.format('MK2_POST_CTRL_%s frame=%d target=sonya side=1 writes=0 assistance=none %s',tag,frame,value or''))
end
]]
prefix=prefix..slice('local function valid(a)','local adjacency=')
prefix=prefix..slice('local function sample(n)','local function snap(label)')
prefix=prefix..[[
local function snap(label)
 assert(width==400 and height==254 and #pixels==406400)
 print(string.format('MK2_POST_CTRL_RGB frame=%d native_frame=%d move=leg side=2 attempt=1 stage=%s width=%d height=%d bytes=%d hex=%s',
  frame,frame-1,label,width,height,#pixels,pixels:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
emu.register_frame(function()
 frame=frame+1
 if MK2_POST_CTRL_EXIT_PENDING then return end
 reReady=MK2_POST_CTRL_READY
 if not reReady then return end
 -- Deliberate human-policy handoff, after both original input callbacks.
 -- Never mutate the CPU inputs or any emulated memory/register/state.
 for _,field in pairs(buttons)do field:clear_value()end
 pixels,width,height=screen:pixels()
 local mode=p:read_u16(0x010601d0)
 local own,enemy=sample(1),sample(2)
]]
local adaptive=read('mk2ks_single_continue_controls_v6579.lua')
local a,b=assert(adaptive:find('local after=[[',1,true));local stop=assert(adaptive:find(']]',b+1,true))
local whole_original_controls=adaptive:sub(b+1,stop-1)
-- Keep the complete original response/retry/survival logic; the root observer
-- supplies its exact same recovery+180 exit without a duplicate callback exit.
whole_original_controls=once(whole_original_controls,'if frame-recover>=180 then manager.machine:exit()end',
 '-- Original recovery+180 exit is handled by the shared native post-KO observer.')
prefix=prefix..whole_original_controls..[[
 if recover and not MK2_POST_CTRL_RECOVERED then MK2_POST_CTRL_RECOVERED=recover end
 if own and own.hp==0 then log('FAILED','reason=actual_post_reset_human_KO_before_control_terminal');manager.machine:exit()end
end)
emu.register_stop(function()
 log('RESULT',string.format('ready=%d walk=%d jump=%d punch=%d recover=%d',reReady or -1,walk or -1,jump or -1,punch or -1,recover or -1))
end)
]]
assert(load(prefix,'@whole_original_adaptive_post_reset_human_controls','t',_G))()
