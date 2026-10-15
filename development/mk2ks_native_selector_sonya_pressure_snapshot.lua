-- Same single pressure controller; complete passive live/nonlive display data.
dofile('mk2ks_native_selector_sonya_cpu_pressure_bound.lua')
local f=assert(io.open('mk2ks_human_projectile_full_display_v1289.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("dofile('mk2ks_human_special_matrix_v3.lua')",'-- Original pressure inputs already loaded once above.')
once("local output=assert(os.getenv('MK2KS_PROJECTILE_DISPLAY_OUT'))","local output='RAM_ONLY'")
once("local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))",'local side=2')
once("local move=assert(os.getenv('MK2KS_HUMAN_SPECIAL_MOVE'))","local move='ring'")
once('frame<=origin+960','frame<=origin+1801')
local a=assert(source:find('local function sampled(f)',1,true))
local z=assert(source:find('local function next_event()',a,true))
source=source:sub(1,a-1)..[[local function sampled(f)
 return origin and f>=origin+1 and f<=origin+1801
end
]]..source:sub(z)
once([[local function save(file,raw)
 local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()
end]],[[local function save(file,raw)
 print(string.format('MK2_PROJECTILE_RAM frame=%d file=%s bytes=%d hex=%s writes=0 assistance=none',
  frame,file,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end]])
-- The current CPU controller already inventories every real projectile child
-- and retirement. Do not install the obsolete classic one-child allocator.
-- All native FIFO/DMA/scenery/effect objects below remain observed throughout.
a=assert(source:find('-- The original helper allocates A10',1,true))
z=assert(source:find("taps[#taps+1]=p:install_read_tap(0xff840b60",a,true))
source=source:sub(1,a-1)..source:sub(z)
once('screen:snapshot(file)',[[local video=manager.machine.video
 local rgb=video:snapshot_pixels();local w,h=video:snapshot_size()
 assert(w==400 and h==254 and #rgb==406400)
 print(string.format('MK2_PROJECTILE_RGB frame=%d file=%s width=%d height=%d bytes=%d hex=%s writes=0 assistance=none',
  frame,file,w,h,#rgb,rgb:gsub('.',function(c)return string.format('%02X',c:byte())end))) ]])
assert(not source:find("'wb'",1,true)and not source:find('screen:snapshot(',1,true)and
 not source:match(':write_[ui]%d+')and not source:match('%.value%s*=[^=]'))
assert(load(source,'@whole_original_native_display_every_pressure_live_nonlive_callback','t',_G))()
