-- Whole original input-only UI probe. Only its PNG sink becomes native pixels
-- streamed to verifier RAM; original control/record ordering stays unchanged.
local f=assert(io.open('mk2ks_native_ui_flow_v2_probe.lua','rb'))
local source=f:read('*a');f:close()
local before='screen:snapshot(name)'
local first,last=assert(source:find(before,1,true))
assert(not source:find(before,last+1,true))
source=source:sub(1,first-1)..'_ui_emit(name,frame)'..source:sub(last+1)
local helper=[[
local function _ui_emit(filename,frame)
 local raw,width,height=manager.machine.screens[':screen']:pixels()
 assert(width==400 and height==254 and #raw==400*254*4)
 print(string.format('MK2_UI_RAM_FRAME frame=%d seconds=%.12f filename=%s width=%d height=%d bytes=%d hex=%s',
  frame,emu.time(),filename,width,height,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
]]
assert(load(helper..source,'@whole_UI_probe_only_PNG_sink_replaced'))()
