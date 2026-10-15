-- Current physical/native allocation driver unchanged. RAM-only full scene.
dofile('mk2ks_current_cpu_blade_allocation_v6340.lua')
local function read(file)
 local handle=assert(io.open(file,'rb'));local source=handle:read('a'):gsub('\r\n','\n');handle:close();return source
end
local sinks=read('mk2ks_native_tomb_ram_v3624.lua')
local stop=assert(sinks:find("local handle=assert(io.open('mk2ks_native_tomb_display_v2062.lua'",1,true))
assert(load(sinks:sub(1,stop-1),'@original_RAM_only_native_render_transport','t',_G))()
local source=read('mk2ks_physical_p2_cpu_knife_display_v1966.lua')
local function replace(before,after)
 local first=assert(source:find(before,1,true),before)
 assert(not source:find(before,first+1,true),'One explicit observer adaptation')
 source=source:sub(1,first-1)..after..source:sub(first+#before)
end
replace("dofile('mk2ks_physical_p2_cpu_knife_trace_v1955.lua')",'-- Physical driver already loaded above.')
replace('local frame,command=0,nil','local frame,command=0,1869')
replace("local output=assert(os.getenv('MK2KS_FLOOR_OUT'))","local output='RAM_ONLY'")
replace('local function active()return command and frame>=command and frame<=command+480 end',
        'local function active()return frame>=1869 and frame<=2510 end')
replace([[local function sampled(f)
 if not(command and f>=command+1 and f<=command+480)then return false end
 for _,start in ipairs(shots)do if f>=start+1 and f<=start+68 then return true end end
 return f%30==0
end]],[[local function sampled(f)return f>=1870 and f<=2510 end]])
replace("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)')
replace('screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)')
replace(' if n==4 then return end\n local physical=n==3 and side or n',
        ' local physical=(n==3 or n==4)and side or n')
replace(' return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),',[[ if n==4 then
  a=p:read_u32(m+0x190)
  -- The blade is type51 on its real parent's Main, not a third fighter.
  if not valid(a)or a==parent or p:read_u16(a+0xc0)~=0x51 then return end
 end
 return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),]])
replace('parent=parent,kind=n==3 and 1 or 0,','parent=parent,kind=n==3 and 1 or n==4 and 2 or 0,')
replace('for _,address in ipairs({action_entry})do','for _,address in ipairs({0xfff8cc00,0xffffb000})do')
assert(not source:find('io.open',1,true)and not source:find('screen:snapshot',1,true))
assert(load(source,'@full_original_CPU_effect_scene_RAM_v6346','t',_G))()
