-- Qualified 1800-field physical continuation, original knife/guard observers.
-- Adapt only the existing AI observer to Kano's actual source router.
local frame=0
local p=manager.machine.devices[':maincpu'].spaces.program
local function hex(raw)return(raw:gsub('.',function(c)return string.format('%02X',c:byte())end))end
local env=setmetatable({}, {__index=_G})
env.mk2_ram_snapshot=function(label)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400,'Entire native RGB callback')
 print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',frame,label,w,h,#raw,hex(raw)))
end
local counts={['mk2ks_physical_p2_cpu_continuation_v3300.lua']=6,
 ['mk2ks_physical_p2_cpu_round_trace_v1940.lua']=0,
 ['mk2ks_physical_p2_cpu_overlap_trace_v1942.lua']=1,
 ['mk2ks_physical_p2_cpu_knife_trace_v1955.lua']=0,
 ['mk2ks_physical_p2_cpu_choice_trace_v3303.lua']=1}
local function replace_once(source,before,after)
 local at=assert(source:find(before,1,true));assert(not source:find(before,at+#before,true),'Single exact observer adaptation')
 return source:sub(1,at-1)..after..source:sub(at+#before)
end
env.dofile=function(path)
 if path=='mk2ks_cpu_recovery_probe_v1438.lua'then path='mk2ks_physical_p2_cpu_continuation_v3300.lua'end
 assert(counts[path]~=nil,'Only qualified original control/observer chain')
 local f=assert(io.open(path,'rb'));local source=f:read('*a');f:close();source=source:gsub('\r\n','\n')
 if path=='mk2ks_physical_p2_cpu_choice_trace_v3303.lua'then
  source=replace_once(source,"dofile('mk2ks_physical_p2_cpu_overlap_trace_v3302.lua')","dofile('mk2ks_physical_p2_cpu_knife_trace_v1955.lua')")
  local n;source,n=source:gsub('==18','==17');assert(n==2,'Only actual Kano CPU identity filter')
  for _,pair in ipairs({{'0xfffbc200','0xfffbc000'},{'0xfffbc220','0xfffbc020'},
   {'0xfffbc250','0xfffbc050'},{'0xfffbc280','0xfffbc080'},{'0xfffbc2b0','0xfffbc0b0'},
   {'0xfffbc2c0','0xfffbc0c0'},{'0xfffbc2f0','0xfffbc0f0'},{'0xfffbc320','0xfffbc120'},
   {'0xfffbc350','0xfffbc150'}})do
   source,n=source:gsub(pair[1],pair[2]);assert(n==(pair[1]=='0xfffbc200'and 2 or 1),'Exact native Kano AI address')
  end
  for _,pair in ipairs({{"'ring'","'knife'",1},{"'square'","'ball'",2},{"'bicycle'","'blade'",1}})do
   source,n=source:gsub(pair[1],pair[2]);assert(n==pair[3],'Exact native Kano route labels')
  end
 end
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
env.dofile('mk2ks_physical_p2_cpu_choice_trace_v3303.lua')
