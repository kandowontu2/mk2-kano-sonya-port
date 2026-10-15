-- Original physical Square/entry/lock observers and complete native audio tap.
-- Only raw transport/window and redundant drawing observer are adapted.
local allowed={
 ['mk2ks_physical_p2_cpu_continuation_v1997.lua']=6,
 ['mk2ks_physical_p2_cpu_round_trace_v1998.lua']=0,
 ['mk2ks_physical_p2_cpu_overlap_trace_v1999.lua']=1,
 ['mk2ks_physical_p2_cpu_choice_trace_v2035.lua']=1,
 ['mk2ks_physical_p2_cpu_square_trace_v2038.lua']=0,
 ['mk2ks_native_cpu_square_boundary_v2993.lua']=0,
 ['mk2ks_native_cpu_square_locks_v3000.lua']=0,
 ['mk2ks_cpu_bicycle_hit_audio_v3396.lua']=0}
local environment=setmetatable({}, {__index=_G})
local loaded={}
environment.audio_snapshot_mark=function(label)print('MK2_SQAUDIO_SNAPSHOT_MARK label='..label..' writes=0 assistance=none')end
environment.audio_ram_guest=function(raw)
 assert(#raw==1048576)
 print(string.format('MK2_SQAUDIO_GUEST frame=1 bytes=%d hex=%s',#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
environment.dofile=function(name)
 local snapshots=assert(allowed[name],'Only original physical/native audio chain')
 assert(not loaded[name]);loaded[name]=true
 local file=assert(io.open(name,'rb'));local source=file:read('*a'):gsub('\r\n','\n');file:close()
 local function once(before,after)
  local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
  source=source:sub(1,at-1)..after..source:sub(at+#before)
 end
 if name=='mk2ks_native_cpu_square_boundary_v2993.lua'then
  once("dofile('mk2ks_physical_p2_cpu_square_display_v2039.lua')","dofile('mk2ks_physical_p2_cpu_square_trace_v2038.lua')")
 elseif name=='mk2ks_cpu_bicycle_hit_audio_v3396.lua'then
  once("dofile('mk2ks_native_cpu_audio_mobility_v3395.lua')","dofile('mk2ks_native_cpu_square_locks_v3000.lua')")
  once("  local file=assert(io.open(assert(os.getenv('MK2KS_FLOOR_OUT'))..'/guest_maincpu.bin','wb'))\n  file:write(table.concat(rom));file:close()",'  audio_ram_guest(table.concat(rom))')
  local count;source,count=source:gsub('frame>=2600 and frame<=2930','frame>=2200 and frame<=2600');assert(count==2)
 end
 local count;source,count=source:gsub("manager.machine.screens%[':screen'%]:snapshot",'audio_snapshot_mark')
 assert(count==snapshots)
 assert(not source:find(':snapshot',1,true)and not source:find("'wb'",1,true),'No media/ROM file writer')
 return assert(load(source,'@'..name,'t',environment))()
end
environment.dofile('mk2ks_cpu_bicycle_hit_audio_v3396.lua')
for name in pairs(allowed)do assert(loaded[name],'Whole original physical/entry/lock/audio observer chain')end
