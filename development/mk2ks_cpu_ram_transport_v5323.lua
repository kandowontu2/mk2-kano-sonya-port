-- Observation transport only. All original normal-input CPU callbacks retained.
local frame=0
emu.register_frame(function()frame=frame+1 end)
local function hex(raw)return(raw:gsub('.',function(c)return string.format('%02X',c:byte())end))end
local environment=setmetatable({}, {__index=_G})
environment.mk2_ram_snapshot=function(label)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400,'Entire original native RGB field')
 print(string.format('MK2_CPU_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',frame,label,w,h,#raw,hex(raw)))
end
local counts={
 ['mk2ks_physical_p2_cpu_continuation_v3300.lua']=6,
 ['mk2ks_physical_p2_cpu_round_trace_v3301.lua']=0,
 ['mk2ks_physical_p2_cpu_overlap_trace_v3302.lua']=1,
 ['mk2ks_physical_p2_cpu_choice_trace_v3303.lua']=1,
 ['mk2ks_physical_p2_cpu_square_trace_v3304.lua']=0,
 ['mk2ks_native_cpu_audio_mobility_v3395.lua']=0,
 ['mk2ks_cpu_bicycle_hit_audio_v3396.lua']=0}
environment.mk2_ram_guest=function(raw)
 assert(#raw==1048576,'Entire initialized guest')
 print(string.format('MK2_CPU_RAM_GUEST frame=%d bytes=%d hex=%s',frame,#raw,hex(raw)))
end
environment.dofile=function(path)
 assert(counts[path]~=nil,'Only qualified original observer chain')
 local file=assert(io.open(path,'rb'));local source=file:read('*a');file:close()
 source=source:gsub('\r\n','\n')
 local n
 source,n=source:gsub("manager.machine.screens%[':screen'%]:snapshot",'mk2_ram_snapshot')
 assert(n==counts[path],'Exact snapshot transport substitutions')
 if path=='mk2ks_cpu_bicycle_hit_audio_v3396.lua'then
  local before="  local file=assert(io.open(assert(os.getenv('MK2KS_FLOOR_OUT'))..'/guest_maincpu.bin','wb'))\n  file:write(table.concat(rom));file:close()"
  local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
  source=source:sub(1,at-1)..'  mk2_ram_guest(table.concat(rom))'..source:sub(at+#before)
 end
 assert(not source:find(':snapshot',1,true)and not source:find("'wb'",1,true),'No media/ROM file writer')
 return assert(load(source,'@'..path,'t',environment))()
end
environment.dofile('mk2ks_cpu_bicycle_hit_audio_v3396.lua')
