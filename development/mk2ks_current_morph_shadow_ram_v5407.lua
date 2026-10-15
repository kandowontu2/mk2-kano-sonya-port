-- Exact original physical morph controller, isolated passive native observer.
local f=assert(io.open('mk2ks_special_shadow_v5131.lua','r'));local original=f:read('*a');f:close()
local function slice(first,last)
 local a=assert(original:find(first,1,true));assert(not original:find(first,a+1,true))
 local b=assert(original:find(last,a+#first,true));return original:sub(a,b-1)
end
local prefix=slice('local p=manager.machine.devices','local high,low,system=')..[[
local move='morph';local side=tonumber(assert(os.getenv('MK2KS_HUMAN_SHANG_SIDE')))
local attempt,air=1,false;local victim_name='kano'
local frame,ready,command,recovered=0,nil,nil,nil;local marks,taps={},{}
local windows={};local previews={}
for a,b in assert(os.getenv('MK2KS_MORPH_SHADOW_WINDOWS')):gmatch('(%d+):(%d+)')do windows[#windows+1]={tonumber(a),tonumber(b)}end
for a in assert(os.getenv('MK2KS_MORPH_SHADOW_PREVIEWS')):gmatch('%d+')do previews[tonumber(a)]=true end
local function active()
 for _,w in ipairs(windows)do if frame>=w[1]and frame<=w[2]then return true end end
 return false
end
]]..slice('local function valid(a)','local function pair_live(a,b)')..[[
local function phase_sample(tag)
 for slot=1,2 do
  local a=sample(slot);assert(a,'Actual repeated-morph actor publication')
  local text={'slot='..slot,'mode='..p:read_u16(0x010601d0)}
  for _,k in ipairs({'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank'})do text[#text+1]=string.format('%s=%08X',k,a[k])end
  for _,k in ipairs({'id','roster','state','hp','x','y','floor','action'})do text[#text+1]=k..'='..a[k]end
  print('MK2_MORPH_SHADOW_'..tag..' frame='..frame..' '..table.concat(text,' ')..' writes=0 assistance=none')
 end
end
emu.register_frame(function()
 frame=frame+1;ready=active()and frame or nil
 if ready then phase_sample('PRE')end
end)
-- Preserve every physical controller callback, route and native lifecycle tap.
dofile('mk2ks_current_morph_adversity_ram_v5403.lua')
]]
local observer=slice('-- BEGIN v1763 read-only consecutive move-phase observer','local function snapshot_ram(label)')
local callback=[[
emu.register_frame_done(function()
 if ready then phase_sample('POST')end
 if previews[frame]then
  local raw=manager.machine.video:snapshot_pixels();assert(#raw==406400)
  print('MK2_MORPH_SHADOW_RGB frame='..frame..' bytes='..#raw..' hex='..raw:gsub('.',function(c)return string.format('%02x',c:byte())end))
 end
end)
emu.register_stop(function()
 phase_tap:remove();phase_clip_tap:remove()
 for _,tap in ipairs(taps)do tap:remove()end
 print('MK2_MORPH_SHADOW_STOP frame='..frame..' writes=0 assistance=none')
end)
]]
assert(load(prefix..observer..callback,'@actual_native_morph_body_shadow_v5407','t',_G))()
