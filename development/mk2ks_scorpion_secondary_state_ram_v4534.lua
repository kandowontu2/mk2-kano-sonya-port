-- Existing real coin/select/two-round/held-HP release controls, RAM sinks only.
local handle=assert(io.open('mk2ks_stock_scorpion_secondary_inputs_v1210.lua','r'))
local source=handle:read('a');handle:close()
local changed,count=source:gsub('screen:snapshot%(', '_scorpion_emit(')
assert(count==2,'Only two original image sinks change; every input stays intact')
local prefix=[[
local function _scorpion_emit(name)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_SSECOND_RGB file=%s width=%d height=%d bytes=%d hex=%s',name,w,h,#raw,
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
]]
assert(load(prefix..changed,'@entire1210_physical_controls_two_RAM_sinks_only_4534','t',_ENV))()
-- Everything below observes native instruction execution or physical state.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local side=assert(tonumber(os.getenv('MK2KS_CAMPAIGN_SIDE')))
assert(side==1 or side==2)
local winner=3-side
local identity=assert(({kano=17,sonya=18,kitana=4,liu_kang=1})[os.getenv('MK2KS_TEST_FIGHTER')])
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,hp=0x01060ec0}}
local frame,origin,completed,retired=0,nil,nil,nil
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,s)
 print(string.format('MK2_SSECOND_%s frame=%d victim=%d victim_slot=%d winner_slot=%d writes=0 assistance=none %s',tag,frame,identity,side,winner,s))
end
local function actor(n)
 local s=slots[n];local a,m=p:read_u32(s.actor),p:read_u32(s.main)
 if not valid(a)or not valid(m)then return end
 return a,m,p:read_u16(a+0x1f0),p:read_u16(s.roster),p:read_u32(m+0xc0)
end
for _,entry in ipairs({0xff8bbfe0,0xff8bc810,0xff8bca00,0xff876650,0xff8bc710,0xff8cdc40})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'actual original secondary cooperative instruction fetch',function(at,data,mask)
  if at~=entry or cpu.PC.value~=entry+16 then return end
  if entry==0xff8bbfe0 and not origin then
   local a,m,id,roster,owner=actor(winner)
   local va,vm,vid,vroster,vowner=actor(side)
   if not a or not va or cpu.A8.value~=a or cpu.A13.value~=m or id~=10 or roster~=10 or owner~=a or
    vid~=identity or vroster~=identity or vowner~=va or p:read_u16(slots[side].hp)~=0 or
    p:read_u16(slots[winner].hp)<=0 or p:read_u16(0x01061b00)~=3 then return end
   origin=frame
   log('BEGIN',string.format('entry=%08X pc=%08X op=%04X mask=%04X actor=%08X main=%08X victim_actor=%08X victim_main=%08X winner_id=%d victim_id=%d mode=%d',
    entry,cpu.PC.value,data,mask,a,m,va,vm,id,vid,p:read_u16(0x010601d0)))
  end
  if not origin or frame-origin>960 then return end
  local a,m=cpu.A8.value,cpu.A13.value
  log('CALL',string.format('age=%d entry=%08X pc=%08X op=%04X mask=%04X actor=%08X main=%08X id=%d owner=%08X',
   frame-origin,entry,cpu.PC.value,data,mask,a,m,valid(a)and p:read_u16(a+0x1f0)or-1,valid(m)and p:read_u32(m+0xc0)or 0))
  if entry==0xff8cdc40 and not completed then
   completed=frame;log('COMPLETE',string.format('age=%d entry=%08X pc=%08X actor=%08X main=%08X',frame-origin,entry,cpu.PC.value,a,m))
  end
 end)
end
local win_entry=0xfffef800+10*32
taps[#taps+1]=p:install_read_tap(win_entry,win_entry+15,'actual original secondary round-winner read',function(at,data,mask)
 if at~=win_entry or cpu.PC.value~=0xff8296b0 or frame<600 then return end
 local a,m,id,roster,owner=actor(winner)
 local va,vm,vid,vroster,vowner=actor(side)
 if a and va and id==10 and roster==10 and vid==identity and vroster==identity and owner==a and vowner==va and
  p:read_u16(slots[side].hp)==0 and p:read_u16(slots[winner].hp)>0 then
  log('WIN',string.format('entry=%08X pc=%08X value=%04X mask=%04X actor=%08X main=%08X victim_actor=%08X victim_main=%08X',win_entry,cpu.PC.value,data,mask,a,m,va,vm))
 end
end)
emu.register_frame(function()
 frame=frame+1;assert(#taps==7)
 if frame==1 then
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  print(string.format('MK2_SSECOND_GUEST frame=1 bytes=%d hex=%s',#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
 end
 if origin and frame-origin<=960 then
  local a1,a2=p:read_u32(slots[1].actor),p:read_u32(slots[2].actor)
  local m1,m2=p:read_u32(slots[1].main),p:read_u32(slots[2].main)
  log('FIELD',string.format('origin=%d age=%d mode=%d actor1=%08X actor2=%08X main1=%08X main2=%08X roster1=%d roster2=%d health1=%d health2=%d winner=%d',
   origin,frame-origin,p:read_u16(0x010601d0),a1,a2,m1,m2,p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),
   p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),p:read_u16(0x01061b00)))
  if a1==0 and a2==0 and not retired then retired=frame;log('RETIRED','age='..(frame-origin))end
 end
end)
emu.register_frame_done(function()
 if manager.machine.time:as_double()>=94 then
  log('HOST_DEADLINE','seconds='..manager.machine.time:as_double()..' limit=94')
  manager.machine:exit()
 end
end)
emu.register_stop(function()
 log('RESULT',string.format('origin=%d completed=%d retired=%d raw_media_files=0',origin or-1,completed or-1,retired or-1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
