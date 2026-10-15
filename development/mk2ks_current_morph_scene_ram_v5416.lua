-- Entire unchanged controller; entire original native scene observer; RAM sinks.
dofile('mk2ks_current_morph_adversity_ram_v5403.lua')
local f=assert(io.open('mk2ks_native_tomb_ram_v3624.lua','r'));local transport=f:read('*a');f:close()
transport=transport:sub(1,assert(transport:find('local handle=assert(io.open',1,true))-1)
transport=transport:gsub('function MK2KS_TOMB_RAM_SAVE','local function save_buffer')
transport=transport:gsub('function MK2KS_TOMB_RAM_PIXELS','local function save_pixels')
f=assert(io.open('mk2ks_physical_p2_cpu_square_display_v2039.lua','r'));local source=f:read('*a');f:close()
local function once(before,after)
 local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
 source=source:sub(1,at-1)..after..source:sub(at+#before)
end
once("dofile('mk2ks_physical_p2_cpu_square_trace_v2038.lua')",'-- No CPU controller loaded; original human morph controller already owns inputs.')
once('local frame,command=0,nil',[[local frame,command=0,tonumber(assert(os.getenv('MK2KS_MORPH_SCENE_FIRST')))
local final=tonumber(assert(os.getenv('MK2KS_MORPH_SCENE_LAST')))
local targets={}
for a,b in assert(os.getenv('MK2KS_MORPH_SCENE_TARGETS')):gmatch('(%d+):(%d+)')do
 for n=tonumber(a),tonumber(b)do targets[n]=true end
end]])
once('local side=2',"local side=tonumber(assert(os.getenv('MK2KS_HUMAN_SHANG_SIDE')))")
once("local move='square'","local move='morph'")
once('local spec=assert(specs[move]);local identity,action_entry=spec[1],spec[2]',
 'local identity,action_entry=6,0xff86e480')
once('local origin,event,snaps=nil,0,0','local origin,event,snaps=command,0,0')
once('local function window_end()return observed_recovery and observed_recovery+30 or command and command+480 end',
 'local function window_end()return final end')
once([[local function sampled(f)
 if not(command and f>=command+1 and f<=window_end())then return false end
 return true
end]],'local function sampled(f)return targets[f]==true end')
once(" local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",' save_buffer(file,raw)')
once(" local file=string.format('display_%d.png',frame);screen:snapshot(file)",
 " local file=string.format('display_%d.rgb',frame);save_pixels(file)")
assert(not source:find(':snapshot(',1,true)and not source:find('io.open(output',1,true))
assert(load(transport..source,'@entire_original_native_scene_three_morph_timers_RAM_v5416','t',_ENV))()
