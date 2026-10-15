-- Same qualified physical controls and native observers; RAM-only transport.
local frame=0
local p=manager.machine.devices[':maincpu'].spaces.program
local function hex(raw)return(raw:gsub('.',function(c)return string.format('%02X',c:byte())end))end
local env=setmetatable({}, {__index=_G})
env.mk2_ram_snapshot=function(label)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400,'Entire native RGB callback')
 print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',frame,label,w,h,#raw,hex(raw)))
end
local counts={['mk2ks_cpu_recovery_probe_v1438.lua']=6,
 ['mk2ks_physical_p2_cpu_round_trace_v1940.lua']=0,
 ['mk2ks_physical_p2_cpu_overlap_trace_v1942.lua']=1,
 ['mk2ks_physical_p2_cpu_knife_trace_v1955.lua']=0}
env.dofile=function(path)
 assert(counts[path]~=nil,'Only original qualified control/observer chain')
 local f=assert(io.open(path,'rb'));local source=f:read('*a');f:close()
 source=source:gsub('\r\n','\n')
 local n;source,n=source:gsub("manager.machine.screens%[':screen'%]:snapshot",'mk2_ram_snapshot')
 assert(n==counts[path],'Only exact snapshot transport substitution')
 assert(not source:find(':snapshot',1,true) and not source:find("'wb'",1,true),'No guest/media writer')
 return assert(load(source,'@'..path,'t',env))()
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local bytes={}
  for at=0xff800000,0xfffffff0,16 do
   local word=p:read_u16(at);bytes[#bytes+1]=string.char(word&255,(word>>8)&255)
  end
  local raw=table.concat(bytes);assert(#raw==1048576,'Entire initialized current guest')
  print(string.format('MK2_KNIFE_RAM_GUEST frame=1 bytes=%d hex=%s',#raw,hex(raw)))
 end
end)
env.dofile('mk2ks_physical_p2_cpu_knife_trace_v1955.lua')
