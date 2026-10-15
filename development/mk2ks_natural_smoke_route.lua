-- Native paid two-player arena rotation, physical Toasty/Down+Start entry.
-- No actor, roster, stage, health, position, clock, RNG or sound-state writes.
-- Original rejected controller/source is preserved in the first attempt folder.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true),'One exact native smoke-route adaptation')
 return s:sub(1,a-1)..after..s:sub(b+1)
end
local source=read('mk2ks_native_stage_performer_v806.lua')
source=change(source,"assert(target_arena==0 or target_arena==1 or target_arena==6)","assert(target_arena==7)")
source=change(source,"local rematch_at,action_arena,last_state=nil,nil,nil",[[local rematch_at,action_arena,last_state=nil,nil,nil
local toast,accepted,secretFight,walk,jump,punch,recover,walkStart,jumpStart,punchStart,walkX=nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil
local walkHP,jumpHP,rearm=nil,nil,nil
local function owned(a,identity,state)return a and a.id==identity and a.roster==identity and a.owner==a.actor and a.state==state end
local function flat(a)return a and a.y==a.floor and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 end
local function grounded(a)return a and a.y==a.floor and a.vx==0 and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 end]])
source=change(source,"hp=p:read_u16(s.hp),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210)}",
 "hp=p:read_u16(s.hp),pose=p:read_u32(a+0x1d0),flags=p:read_u16(m+0x210),state=p:read_u16(s.state),floor=p:read_i16(m+0x200),action=p:read_u16(m+0x1f0),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20)}")
source=change(source,"local f=assert(io.open(assert(os.getenv('MK2KS_STAGE_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()",
 "print('MK2_HPHASE_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))")
local snapshots
source,snapshots=source:gsub('screen:snapshot%(', '_secret_emit(');assert(snapshots==2)
source=change(source,' frame=frame+1\n for n=1,2 do'," frame=frame+1;rawset(_G,'MK2_SECRET_FRAME',frame)\n for n=1,2 do")
source=change(source,"else press(side,'Down');if frame%22<4 then press(side,'Low Kick')end end",[[else press(side,'Down');if frame%22<4 then press(side,arena==7 and 'High Punch' or 'Low Kick')end end
   if arena==7 and toast and frame-toast<=48 then press(side,'Down');if (frame-toast)%8<4 then press(side,'Start')end end]])
-- Earlier 72-field policy and both Sonya native miss attempts are archived.
-- This distinct physical cadence tests the unresolved native secret route;
-- it never changes the RNG, actor/health state, or original Toasty threshold.
source=change(source,"if frame%22<4 then press(side,arena==7 and 'High Punch' or 'Low Kick')end",
 "if arena==7 then if frame%104>=16 and frame%104<20 then press(side,'High Punch')end elseif frame%22<4 then press(side,'Low Kick')end")
-- No stage fatality. A paid challenger is still required to ENTER Portal.
source=change(source,'   if arena==target_arena then','   if false and arena==target_arena then')
source=change(source,'if not action and not command and window and frame-window>=720 and mode~=4 then',
 'if not accepted and not action and not command and window and frame-window>=720 and mode~=4 then')
-- Attract-mode stage actions are not this controller's finish commands.
source=change(source,'if at~=entry or not window then return end','if at~=entry or not command then return end')
source=change(source,"log('MATCH','arena='..arena..' ids='..h.id..','..v.id)",
 "log('MATCH','arena='..arena..' ids='..h.id..','..v.id);if arena==7 then _secret_emit('portal_match.png')end")
source=change(source,"local h,v=sample(side),sample(3-side)\n if mode==2 and pending",[[local h,v=sample(side),sample(3-side)
 if accepted and not secretFight and mode==2 and owned(h,id,1)and owned(v,14,0)and h.hp==161 and v.hp==161 then
  secretFight=frame;log('SECRET_FIGHT',string.format('accepted=%d arena=%d actor=%08X main=%08X id=%d cpu_actor=%08X cpu_main=%08X cpu_id=%d states=%d,%d',
   accepted,arena,h.actor,h.main,h.id,v.actor,v.main,v.id,h.state,v.state));_secret_emit('secret_fight.png')
 end
 if secretFight and mode~=2 and not rearm then
  rearm=frame;walk,jump,punch,recover,walkStart,jumpStart,punchStart,walkX,walkHP,jumpHP=nil,nil,nil,nil,nil,nil,nil,nil,nil,nil
  log('SECRET_REARM','mode='..mode)
 end
 if secretFight and mode==2 and owned(h,id,1)and owned(v,14,0)and h.hp>0 and v.hp>0 then
  if rearm then log('SECRET_ROUND_READY','rearm='..rearm);rearm=nil end
  if not walk then
   if walkStart and(h.hp~=walkHP or h.action==1283 or not flat(h))then walkStart=nil end
   if not walkStart and flat(h)and(h.action==0 or h.action==771)then walkStart=frame;walkX=h.x;walkHP=h.hp end
   if walkStart and flat(h)and h.action==0 and h.hp==walkHP and math.abs(h.x-walkX)>=4 then
    walk=frame;log('SECRET_WALK','start='..walkStart..' fromX='..walkX..' toX='..h.x)
   elseif walkStart then press(side,h.x<v.x and'Right'or'Left')else press(side,'Block')end
  elseif not jump then
   if jumpStart and h.hp~=jumpHP then jumpStart=nil end
   if grounded(h)and(h.action==0 or h.action==771)and not jumpStart then jumpStart=frame;jumpHP=h.hp end
   if jumpStart and h.hp==jumpHP and h.y<h.floor and h.action~=1283 then jump=frame;log('SECRET_JUMP','start='..jumpStart..' action='..h.action..' y='..h.y..' floor='..h.floor)
   elseif jumpStart then press(side,'Up')end
  elseif not punch then
   -- Use the already proven paid-continue control policy: a finite pulse
   -- after actual idle, release, then retry. Held HP through get-up is not
   -- proof that the native parser received a new standing-punch edge.
   if grounded(h)and(h.action==0 or h.action==771)and not punchStart then punchStart=frame end
   if punchStart and h.action==257 then punch=frame;log('SECRET_PUNCH','start='..punchStart)
   elseif punchStart then
    if frame-punchStart<8 then press(side,'High Punch')
    elseif frame-punchStart>30 then punchStart=nil end
   end
  elseif not recover then
   if grounded(h)and(h.action==0 or h.action==771)then recover=frame;log('SECRET_RECOVER','hp='..h.hp);_secret_emit('secret_recovered.png')end
  else
   if frame-recover>=180 then
    log('SECRET_RESULT',string.format('accepted=%d secretFight=%d walk=%d jump=%d punch=%d recover=%d arena=%d',accepted,secretFight,walk,jump,punch,recover,arena))
    _secret_emit('secret_terminal.png');rawset(_G,'MK2_SECRET_COMPLETE',frame);manager.machine:exit()
   else press(side,'Block')end
  end
 end
 if mode==2 and pending]])
source=change(source,"emu.register_frame(function()",[[-- Native event/store observers run before the unchanged physical driver.
taps[#taps+1]=p:install_write_tap(0x01061cc0,0x01061ccf,'native Toasty clock',function(at,data,mask)
 if mask~=0xffff then return end
 if p:read_u16(0x01061ac0)==7 then log('TOASTY_CLOCK',string.format('tick=%d master=%d pc=%08X',data&0xffff,p:read_u16(0x0105d090),cpu.PC.value))end
 if cpu.PC.value~=0xffa0baf0 then return end
 log('TOASTY',string.format('arena=%d tick=%d master=%d pc=%08X',p:read_u16(0x01061ac0),data&0xffff,p:read_u16(0x0105d090),cpu.PC.value))
 if p:read_u16(0x01061ac0)==7 then toast=frame end
end)
-- Observe the real uppercut-created popup task and RNG branch, never alter it.
for _,entry in ipairs({0xff8debf0,0xff8def20,0xff8df070,0xff8df0f0,0xff8df120,0xffa0ba10})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'native Toasty task/decision',function(at)
  if at==entry and p:read_u16(0x01061ac0)==7 then
   log('TOASTY_DECISION',string.format('entry=%08X pc=%08X a0=%08X a1=%08X actor=%08X task=%08X states=%d,%d',
    entry,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,p:read_u16(slots[1].state),p:read_u16(slots[2].state)))
  end
 end)
end
taps[#taps+1]=p:install_write_tap(0x010601d0,0x010601df,'native secret mode',function(at,data,mask)
 if mask==0xffff and data&0xffff==15 then
  accepted=frame
  log('SECRET_ACCEPT',string.format('arena=%d pc=%08X task=%08X secretID=%d taskSide=%d in0=%08X tick=%d toastTick=%d states=%d,%d rosters=%d,%d',
   p:read_u16(0x01061ac0),cpu.PC.value,cpu.A13.value,p:read_u16(cpu.A13.value+0x120),p:read_u16(cpu.A13.value+0x100),p:read_u32(0x01600000),
   p:read_u16(0x0105d090),p:read_u16(0x01061cc0),p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].roster),p:read_u16(slots[2].roster)))
  _secret_emit('secret_accepted.png')
 end
end)
for _,entry in ipairs({0xffa19fd0,0xffa1a180,0xffa1a240,0xffa1a310,0xffa1a380,0xffa1a610,0xffa1bfc0,0xffa1c100,0xffa1c2c0})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'native secret trigger chain',function(at)
  if at==entry and p:read_u16(0x01061ac0)==7 then
   log('SECRET_ENTRY',string.format('entry=%08X pc=%08X a0=%08X a1=%08X a13=%08X a14=%08X mode=%d',entry,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A13.value,cpu.A14.value,p:read_u16(0x010601d0)))
  end
 end)
end
emu.register_frame(function()]])
source=change(source," -- A normal paid challenger after an expired finish window.",[[ if match>0 then
  for n=1,2 do
   local a=sample(n)
   log('SECRET_FIELD',string.format('slot=%d mode=%d arena=%d state=%d roster=%d actor=%08X main=%08X owner=%08X id=%d hp=%d x=%d y=%d floor=%d action=%d flags=%04X vx=%08X vy=%08X gravity=%08X',
    n,mode,arena,p:read_u16(slots[n].state),p:read_u16(slots[n].roster),a and a.actor or 0,a and a.main or 0,a and a.owner or 0,a and a.id or-1,p:read_u16(slots[n].hp),
    a and a.x or-1,a and a.y or-1,a and a.floor or-1,a and a.action or-1,a and a.flags or 0,a and a.vx or 0,a and a.vy or 0,a and a.gravity or 0))
  end
 end
 -- A normal paid challenger after an expired finish window.]])
local prefix=[[
local function _secret_emit(name)
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_HPHASE_RGB frame=%d move=ball side=%s attempt=1 stage=%s width=%d height=%d bytes=%d hex=%s',
  rawget(_G,'MK2_SECRET_FRAME')or 0,os.getenv('MK2KS_STAGE_SIDE'),name,w,h,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
]]
assert(load(prefix..source,'@whole_native_arena_rotation_and_natural_Smoke_route','t',_G))()
emu.register_frame_done(function()
 if emu.time()>tonumber(os.getenv('MK2KS_SECRET_LIMIT')or'900') and not rawget(_G,'MK2_SECRET_COMPLETE')then
  print('MK2_SECRET_DEADLINE writes=0 assistance=none scope=unaccepted_attempt');manager.machine:exit()
 end
end)
-- Both complete native HP ledgers, not just the original winning damage count.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local taps={}
for side,address in ipairs({0x010602f0,0x01060ec0})do
 taps[#taps+1]=p:install_write_tap(address,address+15,'whole secret-route native HP ledger',function(at,data,mask)
  if mask~=0xffff then return end
  local pc=cpu.PC.value
  print(string.format('MK2_SECRET_HEALTH frame=%d slot=%d writes=0 assistance=none at=%08X before=%d after=%d mask=%04X pc=%08X op0=%04X op1=%04X op2=%04X',
   rawget(_G,'MK2_SECRET_FRAME')or 0,side,at,p:read_u16(at),data&0xffff,mask,pc,p:read_u16(pc-48),p:read_u16(pc-32),p:read_u16(pc-16)))
 end)
end
emu.register_frame(function()
 if rawget(_G,'MK2_SECRET_FRAME')==1 then
  local g=assert(manager.machine.memory.regions[':gfxrom']);local bytes={}
  for i=0,11943 do bytes[#bytes+1]=string.char(g:read_u8(0x1fa0000+i))end
  for i=0,7031 do bytes[#bytes+1]=string.char(g:read_u8(0x1fa4000+i))end
  local raw=table.concat(bytes)
  print('MK2_HPHASE_GFX frame=1 bytes=18976 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
 end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
-- Passive reset provenance. The preceding failed run had a later attract
-- reset; do not hide that observation or classify it as a secret softlock.
local last_watchdog,last_watchdog_pc=emu.time(),0
taps[#taps+1]=p:install_write_tap(0x01d81060,0x01d8107f,'native watchdog service',function(at,data,mask)
 last_watchdog,last_watchdog_pc=emu.time(),cpu.PC.value
end)
emu.register_frame_done(function()
 local f=rawget(_G,'MK2_SECRET_FRAME')or 0
 local elapsed=emu.time()-last_watchdog
 if f%60==0 or elapsed>2.5 then
  print(string.format('MK2_SECRET_RESET_TRACE frame=%d seconds=%.12f writes=0 assistance=none pc=%08X mode=%d arena=%d watchdogSeconds=%.12f watchdogPC=%08X',
   f,emu.time(),cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061ac0),elapsed,last_watchdog_pc))
 end
end)
emu.register_prestart(function()
 print(string.format('MK2_SECRET_NATIVE_RESET frame=%d seconds=%.12f writes=0 assistance=none pc=%08X mode=%d watchdogSeconds=%.12f watchdogPC=%08X',
  rawget(_G,'MK2_SECRET_FRAME')or 0,emu.time(),cpu.PC.value,p:read_u16(0x010601d0),emu.time()-last_watchdog,last_watchdog_pc))
end)
