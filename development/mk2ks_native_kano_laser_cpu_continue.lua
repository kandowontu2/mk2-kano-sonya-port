-- Same original first ladder attempt. After its actual loss, normally
-- continue/reselect Kano; keep the same CPU opponent rather than clearing75losses.
-- Real buttons only; no AI/RNG/state assistance.
local filename='mk2ks_native_kano_laser_cpu_campaign.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a'):gsub('\r\n','\n');file:close()
local before='emu.register_frame(function()frame=frame+1 end)'
local after=[=[emu.register_frame(function()
 frame=frame+1
 if p:read_u16(0x010601d0)==3 and p:read_u16(slots[1][4])==2 and
 p:read_u16(0x01061b00)==2 and p:read_u32(slots[1][1])==0 then
  _G._mk2_cpu_after_first_loss=true
 end
end)]=]
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..after..source:sub(b+1)
before='started=frame;_mk2_cpu_laser_started=frame'
after='started=frame;_G._mk2_cpu_laser_started=frame'
a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..after..source:sub(b+1)
local native_load=load
local function scoped_load(text,name,mode,environment)
 if text:find('local function postending_join()',1,true) and text:find('local function sample(',1,true)then
  local before=" if ending_completed and frame-ending_completed>=300 then postending_join();return end"
  local a,b=assert(text:find(before,1,true));assert(not text:find(before,b+1,true))
  text=text:sub(1,a-1)..' if _mk2_cpu_after_first_loss then _cpu_laser_followup(frame);return end\n'..text:sub(a)
 end
 return native_load(text,name,mode,environment or _G)
end
-- The existing campaign creates an environment inheriting_G, so scope load
-- through its exact local environment construction, not a global replacement.
before='local environment=setmetatable({io=scoped_io,_cpu_laser_followup=followup},{__index=_G})'
after='local environment=setmetatable({io=scoped_io,load=_cpu_laser_scoped_load,_cpu_laser_followup=followup},{__index=_G})'
a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..after..source:sub(b+1)
local environment=setmetatable({_cpu_laser_scoped_load=scoped_load},{__index=_G})
assert(native_load(source,'@'..filename..'::first_loss_ordinary_paid_Kano_continue','t',environment))()
