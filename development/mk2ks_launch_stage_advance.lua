-- Genuine existing Kano zoning campaign through an earned first ladder advance.
-- Then the complete established actual-response controls/recovery/survival policy.
-- All media, guest, GFX and sound inventories are passive RAM transports.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true),'One exact stage observer adaptation')
 return s:sub(1,a-1)..after..s:sub(b+1)
end
assert(os.getenv('MK2KS_TEST_FIGHTER')=='kano' and os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')
local source=read('mk2ks_natural_campaign_shao_knife_retreat_v3510.lua')
source=change(source,"local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()",
 "print('MK2_HPHASE_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))")
local count
source,count=source:gsub('screen:snapshot%(', '_campaign_emit(');assert(count==6)
source=change(source,'local ending_completed=nil',[[local ending_completed=nil
local advance,walk,jump,punch,recover,walkStart,jumpStart,punchStart,walkX=nil,nil,nil,nil,nil,nil,nil,nil,nil
local function grounded(a)return a and a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 end
local function owned(a,id)return a and a.id==id and a.roster==id and a.owner==a.actor and a.state==1 end
local function pulse(button,age,start,hold)if age>=start and age<start+(hold or 4)then press(button)end end]])
-- pulse needs the already declared original press function, not a forward global.
source=change(source,'local function pulse(button,age,start,hold)if age>=start and age<start+(hold or 4)then press(button)end end','local pulse')
source=change(source,'-- Observe actual own special entries independently of intended button plans.',
 'pulse=function(button,age,start,hold)if age>=start and age<start+(hold or 4)then press(button)end end\n-- Observe actual own special entries independently of intended button plans.')
source=change(source,'body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140),action=p:read_u16(m+0x1f0)}',
 'body=p:read_u16(a+0x160),bank=p:read_u16(a+0x140),action=p:read_u16(m+0x1f0),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20)}')
source=change(source,' frame=frame+1\n for _,field in pairs(buttons)do field:clear_value()end',
 " frame=frame+1;rawset(_G,'MK2_STAGE_FRAME',frame)\n for _,field in pairs(buttons)do field:clear_value()end")
source=change(source,' local human,other=sample(side),sample(opponent)',[[ local human,other=sample(side),sample(opponent)
 if not rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')and mode==7 and human and other and human.hp==161 and other.hp==161 and
  owned(human,identity)and other.state==0 and other.owner==other.actor and other.id==other.roster then
  rawset(_G,'MK2PORT_NATIVE_AUDIO_READY',frame);log('AUDIO_READY','stage='..stage)
 end
 if first_live and not advance and stage==1 and mode==2 and human and other and owned(human,identity)and
  other.state==0 and other.owner==other.actor and other.id==other.roster and human.hp==161 and other.hp==161 then
  advance=frame;rawset(_G,'MK2_STAGE_ADVANCE',frame)
  log('ADVANCE',string.format('stage=1 actor=%08X main=%08X id=%d cpu=%d schedule=%08X',human.actor,human.main,human.id,other.id,schedule))
 end]])
source=change(source,'if winner==0 and human.hp>0 and other.hp>0 then','if winner==0 and human.hp>0 and other.hp>0 and not advance then')
local controls=read('mk2ks_single_continue_controls_v6579.lua')
local a=assert(controls:find('local after=[[',1,true))+#'local after=[['
local b=assert(controls:find(']]\nreplace(before,after)',a,true))
local after=controls:sub(a,b-1)
after=change(after,'if frame-recover>=180 then manager.machine:exit()end',[[if frame-recover>=180 then
    rawset(_G,'MK2PORT_NATIVE_AUDIO_FINAL',frame)
    log('STAGE_RESULT',string.format('advance=%d walk=%d jump=%d punch=%d recover=%d stage=%d',advance,walk,jump,punch,recover,stage))
    manager.machine:exit()
   end]])
local tail=[[ local reReady=advance;local own,enemy=human,other;local ids={kano=17,sonya=18};local target=fighter
 local function snap(label)_campaign_emit(label..'.png')end
]]..after
source=change(source,' if first_live and stage==16 and mode==11 and winner==side',tail..'\n if first_live and stage==16 and mode==11 and winner==side')
source=change(source,"dofile('mk2ks_campaign_shao_knife_observer_v3508.lua')",[[-- Bosses are outside this earned stage-zero to stage-one observation.
emu.register_frame_done(function()
 if emu.time()>300 and not rawget(_G,'MK2PORT_NATIVE_AUDIO_FINAL')then
  print('MK2_STAGE_DEADLINE writes=0 assistance=none scope=unaccepted_attempt');manager.machine:exit()
 end
end)]])
local prefix=[[
local function _campaign_emit(name)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_HPHASE_RGB frame=%d move=ball side=2 attempt=1 stage=%s width=%d height=%d bytes=%d hex=%s',
  rawget(_G,'MK2_STAGE_FRAME'),name,w,h,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
]]
assert(load(prefix..source,'@whole_original_Kano_zoning_then_actual_stage_controls','t',_G))()

-- Full original launch/channel/health/DAC/PCM/ROM observer, without opponent input.
local passive=read('mk2ks_launch_interrupt_v6680.lua')
local start=assert(passive:find("local cpu=manager.machine.devices[':maincpu'];local p,regs=cpu.spaces.program,cpu.state",1,true))
passive=passive:sub(start)
passive=change(passive,' if entry then\n  local age=frame-entry',' if false and entry then\n  local age=frame-entry')
passive=change(passive,[[   local actor=p:read_u32(side==1 and 0x01060220 or 0x01060df0)
   local main=p:read_u32(side==1 and 0x01060260 or 0x01060e30)
   assert(regs.A8.value==actor and regs.A13.value==main and p:read_u16(actor+0x1f0)==identity and p:read_u32(main+0xc0)==actor)
   entry=frame;serial=serial+1
   log('ENTRY',string.format('serial=%d slot=%d command=%04X pc=%08X actor=%08X main=%08X id=%d',serial,side,data,regs.PC.value,actor,main,identity))]],[[   local matched=false
   for slot=1,2 do
    local actor=p:read_u32(slot==1 and 0x01060220 or 0x01060df0)
    local main=p:read_u32(slot==1 and 0x01060260 or 0x01060e30)
    if regs.A8.value==actor and regs.A13.value==main then
     local id=p:read_u16(actor+0x1f0)
     assert(id==(data==0x6b03 and 17 or 18)and p:read_u32(main+0xc0)==actor)
     entry=frame;serial=serial+1;matched=true
     log('ENTRY',string.format('serial=%d slot=%d command=%04X pc=%08X actor=%08X main=%08X id=%d',serial,slot,data,regs.PC.value,actor,main,id))
    end
   end
   assert(matched,'Actual native CPU/human startup owner')]])
passive=change(passive,[[  assert(frame==rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')and p:read_u16(0x010601d0)==2)
  local side=assert(tonumber(os.getenv('MK2PORT_ACCEPT_SIDE')))
  local id=assert(({ball=17,square=18,bicycle=18})[os.getenv('MK2PORT_ACCEPT_MOVE')])
  local a,m=p:read_u32(side==1 and 0x01060220 or 0x01060df0),p:read_u32(side==1 and 0x01060260 or 0x01060e30)
  assert(valid(a)and valid(m)and p:read_u16(a+0x1f0)==id and p:read_u32(m+0xc0)==a)
  origin=frame;log('BEGIN',string.format('origin=%d a8=%08X a13=%08X id=%d slot=%d',origin,a,m,id,side))]],[[  assert(frame==rawget(_G,'MK2PORT_NATIVE_AUDIO_READY')and p:read_u16(0x010601d0)==7)
  origin=frame;log('BEGIN','origin='..origin..' scope=native_full_health_precombat_before_CPU_launch')]])
local helper=read('mk2ks_launch_interrupt_v6680.lua')
local hstart=assert(helper:find('local function read(name)',1,true))
local hend=assert(helper:find('local getenv=os.getenv',hstart,true))
helper=helper:sub(hstart,hend-1)..'\nlocal side=2;local move="ball";local identity=17;local delay=1\n'
assert(load(helper..passive,'@whole_original_passive_audio_through_earned_stage_advance','t',_G))()
local physical=read('mk2ks_launch_ko_round.lua')
local at=assert(physical:find("local p=manager.machine.devices[':maincpu'].spaces.program",1,true))
assert(load(physical:sub(at),'@whole_original_continuous_both_slot_physical_inventory','t',_G))()
emu.register_frame(function()
 if rawget(_G,'MK2_STAGE_FRAME')==1 then
  local g=assert(manager.machine.memory.regions[':gfxrom']);local bytes={}
  for i=0,11943 do bytes[#bytes+1]=string.char(g:read_u8(0x1fa0000+i))end
  for i=0,7031 do bytes[#bytes+1]=string.char(g:read_u8(0x1fa4000+i))end
  local raw=table.concat(bytes);assert(#raw==18976)
  print('MK2_HPHASE_GFX frame=1 bytes=18976 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
 end
end)
