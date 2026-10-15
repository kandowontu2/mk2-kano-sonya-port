-- Same unassisted CPU losses/payment/selection; observe actual controls,
-- rather than scheduling Up/HP during a CPU hit reaction and calling it a jump.
local f=assert(io.open('mk2ks_single_continue_v6567.lua','rb'))
local source=f:read('*a');f:close()
local function replace(before,after)
 local first,last=assert(source:find(before,1,true))
 assert(not source:find(before,last+1,true),'One exact controller adaptation')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace("{'Left','Right','Up','Down','High Punch'}","{'Left','Right','Up','Down','High Punch','Block'}")
replace('local phase,lastMode,lastRoster=1,nil,nil',[[local phase,lastMode,lastRoster=1,nil,nil
local walk,jump,punch,recover,walkStart,jumpStart,punchStart,walkX=nil,nil,nil,nil,nil,nil,nil,nil]])
replace("local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Start',age,80,5)",
 "local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Coin',age,270,5);pulse('Start',age,310,5)")
replace('if mode==4 and state==3 then reselect=frame;',
 'if mode==4 and state==3 and p:read_u16(slots[side].roster)<=18 then reselect=frame;')
local before=[[ if reReady then
  local age=frame-reReady
  local away=own and enemy and own.x<enemy.x and 'Left' or 'Right'
  pulse(away,age,12,24);pulse('Up',age,64,3);pulse('High Punch',age,128,3)
  if age==38 or age==80 or age==145 or age==180 then snap('continued_control')end
  if age>=180 then manager.machine:exit()end
 end]]
local after=[[ if reReady and mode==2 and owned(own,ids[target])and own.hp>0 then
  local away=own.x<enemy.x and 'Left' or 'Right'
  local idle=(own.action==0 or own.action==771)and grounded(own)
  if not walk then
   if not walkStart and idle then walkStart=frame;walkX=own.x end
   if walkStart then
    pulse(away,frame-walkStart,0,180)
    if own.action==0 and own.y==own.floor and own.vy==0 and own.gravity==0 and own.flags&0x1c==0 and math.abs(own.x-walkX)>=4 then walk=frame;log('WALK','start='..walkStart..' fromX='..walkX..' toX='..own.x);snap('actual_walk')
    elseif frame-walkStart>180 then walkStart=nil end
   end
  elseif not jump then
   if not jumpStart and idle then jumpStart=frame end
   if jumpStart then
    pulse('Up',frame-jumpStart,0,8)
    if own.y<own.floor and own.action~=1283 then jump=frame;log('JUMP','start='..jumpStart..' action='..own.action..' y='..own.y..' floor='..own.floor);snap('actual_jump')
    elseif frame-jumpStart>30 then jumpStart=nil end
   end
  elseif not punch then
   if not punchStart and idle then punchStart=frame end
   if punchStart then
    pulse('High Punch',frame-punchStart,0,8)
    if own.action==257 then punch=frame;log('PUNCH','start='..punchStart..' action='..own.action);snap('actual_punch')
    elseif frame-punchStart>30 then punchStart=nil end
   end
  elseif not recover then
   if idle then recover=frame;log('RECOVER','hp='..own.hp);snap('control_recovered')end
  else
   pulse('Block',frame-recover,0,180)
   if frame-recover==60 or frame-recover==120 or frame-recover==180 then snap('continued_control')end
   if frame-recover>=180 then manager.machine:exit()end
  end
 end]]
replace(before,after)
replace('cpuID=%d scope=unassisted_CPU_loss_paid_single_player_continue_not_full_port',
 'cpuID=%d walk=%d jump=%d punch=%d recover=%d scope=unassisted_CPU_loss_paid_single_player_continue_actual_controls_not_full_port')
replace('reLive or -1,reReady or -1,cpuID or -1))',
 'reLive or -1,reReady or -1,cpuID or -1,walk or -1,jump or -1,punch or -1,recover or -1))')
assert(load(source,'@mk2ks_single_continue_v6567.lua::physical_actual_control_observer'))()
