-- Current physical CPU run unchanged; two bounded read-only body/shadow windows.
-- Original qualified shadow kernels/taps, no actor/AI/RNG/HP fixture.
dofile('mk2ks_current_kano_cpu_extended_ram_v6290.lua')
local file=assert(io.open('mk2ks_special_shadow_v5131.lua','rb'))
local original=file:read('*a'):gsub('\r\n','\n');file:close()
local function slice(first,last)
 local a=assert(original:find(first,1,true));assert(not original:find(first,a+1,true))
 local b=assert(original:find(last,a+#first,true));return original:sub(a,b-1)
end
local prefix=slice('local p=manager.machine.devices','local high,low,system=')
prefix=prefix..[[
local move,side,attempt,air='blade',2,1,false
local victim_name='kano'
local frame,ready,command,recovered=0,nil,nil,nil
local marks,taps={},{}
]]
prefix=prefix..slice('local function valid(a)','local function pair_live(a,b)')
prefix=prefix..[[
local function window(f)return(f>=1870 and f<=1912)or(f>=2441 and f<=2509)end
local checkpoints={
 [1870]='blade_before',[1871]='blade_entry',[1874]='blade_pose2',
 [1878]='blade_pose4',[1881]='blade_contact',[1886]='blade_pose6',
 [1890]='blade_hold',[1906]='blade_last_pose',[1910]='blade_recovered',
 [2442]='knife_entry',[2446]='knife_intro',[2454]='knife_intro4',
 [2465]='knife_flight',[2471]='knife_contact',[2472]='knife_impact',
 [2480]='knife_impact3',[2491]='knife_own_ready',[2495]='knife_retire',
 [2496]='knife_after_retirement',[2509]='knife_tail'}
emu.register_frame(function()
 frame=frame+1
 move=frame<2200 and'blade'or'knife';attempt=frame<2200 and 1 or 2
 ready=window(frame)and frame or nil
 marks[frame]=ready and checkpoints[frame]or nil
end)
]]
local observer=slice('-- BEGIN v1763 read-only consecutive move-phase observer','local function snapshot_ram(label)')
local callbacks=[[
emu.register_frame_done(function()
 if not ready then return end
 local a,b=sample(1),sample(2)
 assert(a and b and a.owner==a.actor and b.owner==b.actor and
  a.id==17 and b.id==17 and a.roster==17 and b.roster==17 and
  a.state==1 and b.state==0,'Actual native Kano/human identities within bounded drawing windows')
 for n,actor in ipairs({a,b})do
  local text={'slot='..n,'mode='..p:read_u16(0x010601d0)}
  for _,key in ipairs({'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank'})do
   text[#text+1]=string.format('%s=%08X',key,actor[key])
  end
  for _,key in ipairs({'id','roster','state','hp','x','y','floor','action'})do text[#text+1]=key..'='..actor[key]end
  phase_log('POST_FIELD',table.concat(text,' '))
 end
 if not marks[frame]then return end
 local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',
  frame,marks[frame],w,h,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 phase_log('SNAP','stage='..marks[frame])
end)
emu.register_stop(function()
 phase_log('RESULT','scope=two_current_CPU_body_shadow_windows_not_effect_raster_audio_or_full_port')
 phase_tap:remove();phase_clip_tap:remove()
 for _,tap in ipairs(taps)do tap:remove()end
end)
]]
assert(load(prefix..observer..callbacks,'@current_CPU_body_shadow_windows_v6312','t',_G))()
