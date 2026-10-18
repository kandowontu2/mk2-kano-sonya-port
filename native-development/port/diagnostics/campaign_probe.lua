-- Single-player exploration. Physical controls only, no guest writes or cheats.
-- This controller is NOT evidence of beating the game unless the trace does so.
local m=manager.machine
local cpu=m.devices[':maincpu']
local p=cpu.spaces.program
local fields={}
local commands={}
for _,port in pairs(m.ioport.ports) do
 for name,field in pairs(port.fields) do fields[name]=field end
end
local function set(name,value)
 if fields[name] then fields[name]:set_value(value);commands[name]=value end
end
local function u16(a) return p:read_u8(a)|(p:read_u8(a+8)<<8) end
local function s16(a)
 local value=u16(a)
 return value<0x8000 and value or value-0x10000
end
local function u32(a)
 local v=0
 for i=0,3 do v=v|(p:read_u8(a+i*8)<<(i*8)) end
 return v
end
local target=assert(tonumber(os.getenv('KS_CAMPAIGN_ACTOR')))
local continueLimit=tonumber(os.getenv('KS_CAMPAIGN_CONTINUES') or '0')
local fieldLimit=tonumber(os.getenv('KS_CAMPAIGN_FIELDS') or '30000')
local endingWindow=os.getenv('KS_CAMPAIGN_ENDING_WINDOW')=='1'
local finaleWindow=os.getenv('KS_CAMPAIGN_FINALE_WINDOW')=='1'
if os.getenv('KS_CAMPAIGN_BOSS_ENDURANCE')=='1' then assert(finaleWindow and endingWindow and fieldLimit==300000)
elseif finaleWindow then assert(endingWindow and fieldLimit==180000)
else
 assert(fieldLimit>=9000 and fieldLimit<=(endingWindow and 150000 or 120000))
 assert(not endingWindow or fieldLimit==150000)
end
local extraContinues=os.getenv('KS_CAMPAIGN_EXTRA_CONTINUES')=='1'
assert(not extraContinues or fieldLimit>=120000)
if os.getenv('KS_CAMPAIGN_BOSS_ENDURANCE')=='1' then assert(extraContinues and continueLimit>=0 and continueLimit<=64)
else assert(continueLimit>=0 and continueLimit<=(extraContinues and 32 or 20)) end
assert(continueLimit<=5 or fieldLimit>=90000)
local continuesUsed,buyinAge=0,0
local bossContinueDelay=tonumber(os.getenv('KS_CAMPAIGN_BOSS_CONTINUE_DELAY') or '0')
assert(bossContinueDelay==0 or bossContinueDelay==60)
local continuing=false
local continueLog=assert(io.open('campaign_continues.csv','w'))
continueLog:write('frame,attempt,map,phase\n')
local style=os.getenv('KS_CAMPAIGN_STYLE') or 'grapple'
local kickOverride=tonumber(os.getenv('KS_CAMPAIGN_KICK_AGE'))
local defensive=os.getenv('KS_CAMPAIGN_DEFENSE')=='1'
local jaxRing=os.getenv('KS_CAMPAIGN_JAX_RING')=='1'
local jaxSafeRing=os.getenv('KS_CAMPAIGN_JAX_SAFE_RING')=='1'
local kanoKnife=os.getenv('KS_CAMPAIGN_KANO_KNIFE')=='1'
local raidenKnife=os.getenv('KS_CAMPAIGN_RAIDEN_KNIFE')=='1'
local femaleZoning=os.getenv('KS_CAMPAIGN_FEMALE_ZONING')=='1'
local femaleCounter=os.getenv('KS_CAMPAIGN_FEMALE_COUNTER')=='1'
local kitanaKnifeGuard=os.getenv('KS_CAMPAIGN_KITANA_KNIFE_GUARD')=='1'
local kitanaKnifeInterval=tonumber(os.getenv('KS_CAMPAIGN_KITANA_KNIFE_INTERVAL') or '60')
assert(kitanaKnifeInterval and kitanaKnifeInterval%1==0 and kitanaKnifeInterval>=24 and kitanaKnifeInterval<=120)
local liuKnifeInterval=tonumber(os.getenv('KS_CAMPAIGN_LIU_KNIFE_INTERVAL') or '60')
assert(liuKnifeInterval and liuKnifeInterval%1==0 and liuKnifeInterval>=24 and liuKnifeInterval<=120)
local subzeroKnifeInterval=tonumber(os.getenv('KS_CAMPAIGN_SUBZERO_KNIFE_INTERVAL') or '60')
assert(subzeroKnifeInterval and subzeroKnifeInterval%1==0 and subzeroKnifeInterval>=24 and subzeroKnifeInterval<=120)
local kitanaRfpDuck=os.getenv('KS_CAMPAIGN_KITANA_RFP_DUCK')=='1'
local liuRfpDuck=os.getenv('KS_CAMPAIGN_LIU_RFP_DUCK')=='1'
local subzeroRfpDuck=os.getenv('KS_CAMPAIGN_SUBZERO_RFP_DUCK')=='1'
local subzeroCrouchReady=os.getenv('KS_CAMPAIGN_SUBZERO_CROUCH_READY')=='1'
local kanoSubJump=os.getenv('KS_CAMPAIGN_KANO_SUB_JUMP')=='1'
local kanoSubJumpHold=os.getenv('KS_CAMPAIGN_KANO_SUB_JUMP_HOLD')=='1'
local kanoSubRangeKick=os.getenv('KS_CAMPAIGN_KANO_SUB_RANGE_KICK')=='1'
local kanoSubBall=os.getenv('KS_CAMPAIGN_KANO_SUB_BALL')=='1'
local kanoSubStandingCharge=os.getenv('KS_CAMPAIGN_KANO_SUB_STANDING_CHARGE')=='1'
local kanoSubAdaptiveCharge=os.getenv('KS_CAMPAIGN_KANO_SUB_ADAPTIVE_CHARGE')=='1'
local kanoSubBallCounter=os.getenv('KS_CAMPAIGN_KANO_SUB_BALL_COUNTER')=='1'
local subBallRecovery={counter=os.getenv('KS_CAMPAIGN_KANO_SUB_RECOVERY_COUNTER')=='1',
 ball=os.getenv('KS_CAMPAIGN_KANO_SUB_RECOVERY_BALL')=='1',
 recharge=os.getenv('KS_CAMPAIGN_KANO_SUB_RECHARGE')=='1',
 approach=os.getenv('KS_CAMPAIGN_KANO_SUB_APPROACH')=='1',
 postGuard=os.getenv('KS_CAMPAIGN_KANO_SUB_POSTBALL_GUARD')=='1',
 normalThrow=os.getenv('KS_CAMPAIGN_KANO_SUB_NORMAL_THROW')=='1',throwAt=-1000,start=nil,
 neutralUppercut=os.getenv('KS_CAMPAIGN_KANO_SUB_NEUTRAL_UPPERCUT')=='1',uppercutAt=-1000,uppercutPrepare=nil,
 finishKnifeStart=nil,finishKnifeReady=false,finishKnifeAt=-1000,
 mileenaPrepare=os.getenv('KS_CAMPAIGN_KANO_MILEENA_PREPARE')=='1',
 humanPrepare=os.getenv('KS_CAMPAIGN_KANO_HUMAN_PREPARE')=='1',activeOpponent=0,
 kanoBoss=os.getenv('KS_CAMPAIGN_KANO_BOSS_GUARD')=='1',
 kintaroFastPulse=os.getenv('KS_CAMPAIGN_KANO_KINTARO_FAST_PULSE')=='1',
 kintaroReady=os.getenv('KS_CAMPAIGN_KANO_KINTARO_READY')=='1',
 kintaroEarlyCounter=os.getenv('KS_CAMPAIGN_KANO_KINTARO_EARLY_COUNTER')=='1',
 kintaroVaried=os.getenv('KS_CAMPAIGN_KANO_KINTARO_VARIED')=='1',
 kintaroVariedCounter=os.getenv('KS_CAMPAIGN_KANO_KINTARO_VARIED_COUNTER')=='1',
 kintaroVariedAdaptive=os.getenv('KS_CAMPAIGN_KANO_KINTARO_VARIED_ADAPTIVE')=='1',
 kintaroVariedReactive=os.getenv('KS_CAMPAIGN_KANO_KINTARO_VARIED_REACTIVE')=='1',
 kintaroVariedFinish=os.getenv('KS_CAMPAIGN_KANO_KINTARO_VARIED_FINISH')=='1',
 kintaroVariedFinishUpper=os.getenv('KS_CAMPAIGN_KANO_KINTARO_VARIED_FINISH_UPPERCUT')=='1',
 finishUpperThreshold=tonumber(os.getenv('KS_CAMPAIGN_FINISH_UPPERCUT_THRESHOLD') or '20'),
 knifeClearance=tonumber(os.getenv('KS_CAMPAIGN_KNIFE_CLEARANCE') or '175'),
 fixedAirAge=tonumber(os.getenv('KS_CAMPAIGN_MIXED_AIR_AGE') or '28'),
 punchRetreatHop=os.getenv('KS_CAMPAIGN_PUNCH_RETREAT_HOP')=='1',lastPunchRetreat=false,
 kintaroStompRefresh=os.getenv('KS_CAMPAIGN_KANO_KINTARO_STOMP_REFRESH')=='1',stompJumpRequested=false,
 kintaroStompMomentum=os.getenv('KS_CAMPAIGN_KANO_KINTARO_STOMP_MOMENTUM')=='1',
 kintaroWalkStomp=os.getenv('KS_CAMPAIGN_WALK_STOMP')=='1',
 kintaroVertical=os.getenv('KS_CAMPAIGN_KANO_KINTARO_VERTICAL_KICK')=='1',
 verticalAttackAge=tonumber(os.getenv('KS_CAMPAIGN_KANO_KINTARO_VERTICAL_AGE') or '28'),
 kintaroRecovery=os.getenv('KS_CAMPAIGN_KANO_KINTARO_RECOVERY_COUNTER')=='1',bossPunishAt=-1000,
 kintaroRecoveryApproach=os.getenv('KS_CAMPAIGN_KANO_KINTARO_RECOVERY_APPROACH')=='1',
 readyRange=tonumber(os.getenv('KS_CAMPAIGN_KANO_KINTARO_READY_RANGE') or '115'),
 kintaroPrepare=os.getenv('KS_CAMPAIGN_KANO_KINTARO_PREPARE')=='1' or os.getenv('KS_CAMPAIGN_KANO_KINTARO_WIDE')=='1',
 kintaroWide=os.getenv('KS_CAMPAIGN_KANO_KINTARO_WIDE')=='1',
 kintaroBlade=os.getenv('KS_CAMPAIGN_KANO_KINTARO_BLADE')=='1',bladeAt=-1000,
 kintaroKnife=os.getenv('KS_CAMPAIGN_KANO_KINTARO_KNIFE')=='1',bossShotAt=-1000,
 kintaroKnifeMidrange=os.getenv('KS_CAMPAIGN_KANO_KINTARO_KNIFE_MIDRANGE')=='1',
 kintaroKnifeReady=os.getenv('KS_CAMPAIGN_KANO_KINTARO_KNIFE_READY')=='1',knifeReadySince=nil,
 kintaroEvadeCounter=os.getenv('KS_CAMPAIGN_KANO_KINTARO_EVADE_COUNTER')=='1',
 kintaroShortKick=os.getenv('KS_CAMPAIGN_KANO_KINTARO_SHORT_KICK')=='1',shortKickAt=-1000,
 kintaroRetreatBall=os.getenv('KS_CAMPAIGN_KANO_KINTARO_RETREAT_BALL')=='1',bossBallStart=nil,bossBallAt=-1000,
 kintaroBallFinishKnife=os.getenv('KS_CAMPAIGN_KANO_KINTARO_RETREAT_BALL_FINISH_KNIFE')=='1',
 kintaroMixed=os.getenv('KS_CAMPAIGN_KANO_KINTARO_MIXED')=='1',
 kintaroMixedGuard=os.getenv('KS_CAMPAIGN_KANO_KINTARO_MIXED_GUARD')=='1',
 kintaroJumpkick=os.getenv('KS_CAMPAIGN_KANO_KINTARO_JUMPKICK')=='1'}
if subBallRecovery.normalThrow then
 subBallRecovery.throwLog=assert(io.open(subBallRecovery.neutralUppercut and 'sub_neutral_uppercut.csv' or 'sub_normal_throw.csv','w'))
 subBallRecovery.throwLog:write('frame,phase,ownAction,ownFlags,ownHeight,enemyAction,enemyFlags,enemyHeight,distance,projectile,toward,away,block,down,lp,hp,bodyHeight,buttonTable,duckTable,opponent,activeOpponent\n')
end
if subBallRecovery.kintaroReady or subBallRecovery.kintaroVariedCounter or subBallRecovery.kintaroVariedFinishUpper then
 assert(subBallRecovery.finishUpperThreshold==13 or subBallRecovery.finishUpperThreshold==20)
 assert(subBallRecovery.readyRange==84 or subBallRecovery.readyRange==104 or subBallRecovery.readyRange==115)
 subBallRecovery.readyLog=assert(io.open('kintaro_ready_counter.csv','w'))
 subBallRecovery.readyLog:write('frame,ownAction,ownFlags,ownHeight,bodyHeight,buttonTable,duckTable,distance,enemyAction,enemyHeight,phase,hp,ownHP,enemyHP\n')
end
if subBallRecovery.kintaroKnifeReady or subBallRecovery.kintaroBallFinishKnife then
 subBallRecovery.knifeReadyLog=assert(io.open('kintaro_knife_ready.csv','w'))
 subBallRecovery.knifeReadyLog:write('frame,phase,ownAction,ownFlags,ownHeight,bodyHeight,buttonTable,stanceTable,distance,ownHP,enemyHP\n')
end
if subBallRecovery.kintaroRetreatBall then
 subBallRecovery.bossBallLog=assert(io.open('boss_ball_charge.csv','w'))
 subBallRecovery.bossBallLog:write('frame,age,phase,action,flags,height,distance,ownHP,enemyHP,lk,up,away\n')
end
if subBallRecovery.kintaroVaried then
 subBallRecovery.variedLog=assert(io.open('kintaro_variety.csv','w'))
 subBallRecovery.variedLog:write('frame,history,kicks,punches,distance,ownAction,ownFlags,ownHeight,decision,ownHP,enemyHP,airAttackAge\n')
 if subBallRecovery.punchRetreatHop then
  subBallRecovery.hopLog=assert(io.open('kintaro_punch_hops.csv','w'))
  subBallRecovery.hopLog:write('frame,plan,distance,direction,away,toward,retreat,ownHP,enemyHP\n')
 end
end
if subBallRecovery.kintaroVertical then
 assert(subBallRecovery.verticalAttackAge==10 or subBallRecovery.verticalAttackAge==28)
 subBallRecovery.verticalLog=assert(io.open('kintaro_vertical.csv','w'))
 subBallRecovery.verticalLog:write('frame,distance,ownAction,ownFlags,ownHeight,bodyHeight,buttonTable,stanceTable,decision,ownHP,enemyHP,attackAge\n')
end
if subBallRecovery.kintaroVariedReactive then
 subBallRecovery.airTimingLog=assert(io.open('kintaro_air_timing.csv','w'))
 subBallRecovery.airTimingLog:write('frame,requestFrame,plan,age,windup,ownHeight,attackAt,hp,hk\n')
end
if subBallRecovery.kintaroRecovery then
 subBallRecovery.recoveryLog=assert(io.open('kintaro_recovery_counter.csv','w'))
 subBallRecovery.recoveryLog:write('frame,ownAction,ownFlags,ownHeight,bodyHeight,buttonTable,duckTable,distance,enemyAction,enemyHeight,phase,hp,ownHP,enemyHP,enemyRecovery,enemyWake,toward,down,block\n')
end
local subBallCounterAt=-1000
local subBallStart,subBallReleaseAt,subBallReleased=nil,nil,false
local subBallLog=kanoSubBall and assert(io.open('sub_ball.csv','w')) or nil
if subBallLog then subBallLog:write('frame,age,phase,eligible,ownAction,ownFlags,ownHeight,enemyAction,enemyFlags,distance,projectile,lk,block,down,hp,toward,away\n') end
local subJumpStart=nil
local subJumpRequest=-1000
local sonyaKitanaRfpDuck=os.getenv('KS_CAMPAIGN_SONYA_KITANA_RFP_DUCK')=='1'
local sonyaRecoveryCounter=os.getenv('KS_CAMPAIGN_SONYA_KITANA_RECOVER_COUNTER')=='1'
local sonyaRecoveryKick=os.getenv('KS_CAMPAIGN_SONYA_KITANA_RECOVER_KICK')=='1'
local sonyaGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_KITANA_GUARD_LEG')=='1'
local sonyaLiuGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_LIU_GUARD_LEG')=='1'
local sonyaSubGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_SUB_GUARD_LEG')=='1'
local sonyaSubNeutralLeg=os.getenv('KS_CAMPAIGN_SONYA_SUB_NEUTRAL_LEG')=='1'
local sonyaMileenaGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_MILEENA_GUARD_LEG')=='1'
local sonyaCageGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_CAGE_GUARD_LEG')=='1'
local sonyaLaoGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_LAO_GUARD_LEG')=='1'
local sonyaScorpionGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_SCORPION_GUARD_LEG')=='1'
local sonyaKintaroGuard=os.getenv('KS_CAMPAIGN_SONYA_KINTARO_GUARD')=='1'
local sonyaKahnGuard=os.getenv('KS_CAMPAIGN_SONYA_KAHN_GUARD')=='1'
local kahnContactReady=os.getenv('KS_CAMPAIGN_SONYA_KAHN_CONTACT_READY')=='1' or subBallRecovery.kanoBoss
local kahnOpeningJump=os.getenv('KS_CAMPAIGN_SONYA_KAHN_OPENING_JUMP')=='1' or subBallRecovery.kanoBoss
local captureEnding=os.getenv('KS_CAMPAIGN_CAPTURE_ENDING')=='1'
local endingFirst=nil
local endingCaptures=0
local endingState=os.getenv('KS_CAMPAIGN_ENDING_STATE')=='1'
assert(not endingState or captureEnding)
local endingStateLog=endingState and assert(io.open('ending_state.csv','w')) or nil
if endingStateLog then endingStateLog:write('frame,age,dlists,displayon,noflip,pageaddr,autoerase,objlst,objlst2,scrntl,scrnlr,photoX,photoY,photoShape\n') end
local endingVideoLog=endingState and assert(io.open('ending_video_samples.csv','w')) or nil
if endingVideoLog then endingVideoLog:write('frame,age,videoControl,vramSampleFNV,paletteSampleFNV\n') end
local kahnCounterRetry=-1000
local kahnLog=(sonyaKahnGuard or subBallRecovery.kanoBoss) and assert(io.open('kahn_counter.csv','w')) or nil
if kahnLog then kahnLog:write('frame,chargeRoutine,velocity,distance,ownHeight,ownFlags,bodyHeight,buttonTable,duckTable,enemyWake,ownHP,enemyHP,down,block,hp,contactRecovery\n') end
local sonyaKintaroEvade=os.getenv('KS_CAMPAIGN_SONYA_KINTARO_EVADE')=='1' or subBallRecovery.kanoBoss
local earlyStompEvade=os.getenv('KS_CAMPAIGN_SONYA_KINTARO_EARLY_EVADE')=='1' or subBallRecovery.kanoBoss
local stompPhaseSeen,stompFlightActive,stompSawAir,stompJumped=false,false,false,false
local stompEscapeLast,stompEscapeDirection=-1000,nil
local stompEscapeLog=sonyaKintaroEvade and assert(io.open('stomp_escape.csv','w')) or nil
if stompEscapeLog then stompEscapeLog:write('frame,ownX,enemyX,enemyHeight,leftEdge,rightEdge,leftDistance,rightDistance,direction,ownHP,ownFlags,ownHeight,up\n') end
local bossCounterRetry=-1000
local bossCounterPrepare=nil
local bossContextLog=(sonyaKintaroGuard or subBallRecovery.kintaroEvadeCounter) and assert(io.open('boss_context.csv','w')) or nil
if bossContextLog then bossContextLog:write('frame,ownHeight,bodyHeight,ownFlags,buttonTable,duckTable,enemyHeight,enemyFlags,enemyAction,ownWake,enemyWake,prepareAge,cooldownAge,hp\n') end
local sonyaShangGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_SHANG_GUARD_LEG')=='1'
local sonyaOwnGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_OWN_GUARD_LEG')=='1'
local sonyaMileenaNoRing=os.getenv('KS_CAMPAIGN_SONYA_MILEENA_NO_RING')=='1'
local sonyaMileenaLeg85=os.getenv('KS_CAMPAIGN_SONYA_MILEENA_LEG85')=='1'
local lowGuardFields,guardLegRetry=0,-1000
local guardLegStart=nil
local guardLegLog=(sonyaGuardLeg or sonyaSubGuardLeg or sonyaKintaroGuard or sonyaShangGuardLeg or sonyaOwnGuardLeg or sonyaScorpionGuardLeg or sonyaLaoGuardLeg or sonyaCageGuardLeg or sonyaMileenaGuardLeg or sonyaLiuGuardLeg) and assert(io.open('guard_leg.csv','w')) or nil
if guardLegLog then guardLegLog:write('frame,phase,age,guardFields,height,ownFlags,distance,down,block,lp\n') end
local recoveryCounterStart=nil
local recoveryCounterLog=sonyaRecoveryCounter and assert(io.open('recovery_counter.csv','w')) or nil
if recoveryCounterLog then recoveryCounterLog:write('frame,phase,age,ownHP,enemyHP,distance,ownFlags,ownRenderedHeight,buttonTable,down,block,hp,lk\n') end
local subzeroCounterRetry=-1000
local subzeroObserve=os.getenv('KS_CAMPAIGN_SUBZERO_OBSERVE')=='1'
local rfpBegin,rfpEnd=tonumber(os.getenv('KS_RFP_BEGIN')),tonumber(os.getenv('KS_RFP_END'))
local rfpRecovery=tonumber(os.getenv('KS_RFP_RECOVER'))
if kitanaRfpDuck or liuRfpDuck or subzeroRfpDuck or sonyaKitanaRfpDuck or sonyaSubGuardLeg or sonyaKintaroGuard or sonyaShangGuardLeg or sonyaOwnGuardLeg or sonyaScorpionGuardLeg or sonyaLaoGuardLeg or sonyaCageGuardLeg or sonyaMileenaGuardLeg or sonyaLiuGuardLeg or subzeroObserve then assert(rfpBegin and rfpEnd and rfpRecovery and rfpBegin<rfpRecovery and rfpRecovery<rfpEnd) end
local rfpLog=(kitanaRfpDuck or liuRfpDuck or subzeroRfpDuck or sonyaKitanaRfpDuck or sonyaSubGuardLeg or sonyaKintaroGuard or sonyaShangGuardLeg or sonyaOwnGuardLeg or sonyaScorpionGuardLeg or sonyaLaoGuardLeg or sonyaCageGuardLeg or sonyaMileenaGuardLeg or sonyaLiuGuardLeg) and assert(io.open('rfp_control.csv','w')) or nil
if rfpLog then rfpLog:write('frame,count,enemyWake,ownHP,enemyHP,distance,down,block,recovering,hp,punchAnimation,ownRenderedHeight,ownFlags,ownButtonTable,duckButtonsReady\n') end
local subzeroObservationLog=subzeroObserve and assert(io.open('subzero_context.csv','w')) or nil
if subzeroObservationLog then subzeroObservationLog:write('frame,enemyFlags,enemyWake,rapidPunch,punchesLeft,recovering,punchAnimation,ownAction,enemyAction,ownHP,enemyHP,distance\n') end
local function cpuRapidPunch(proc)
 if proc<0x01000000 or proc+0x6f0>0x01400000 then return false,0 end
 if (u16(proc+0x210)&0x10)==0 then return false,0 end
 local function inside(pc) return pc>=rfpBegin and pc<rfpEnd end
 local count=u16(proc+0x2a0)
 local stack=u32(proc+0x40)
 if stack<proc+0x3d0 or stack>proc+0x6f0-32 then return false,0 end
 local wake=u32(proc+0xe0)
 if inside(wake) then return true,count,wake>=rfpRecovery,u32(stack) end
 -- mframew sleeps in generic code. Its live process-stack return address
 -- identifies the caller; inspect at most8 words, never outside this stack.
 for cursor=stack,math.min(stack+7*32,proc+0x6f0-32),32 do
  local pc=u32(cursor)
  if inside(pc) and cursor+64<=proc+0x6f0 then return true,count,pc>=rfpRecovery,u32(cursor+32) end
 end
 return false,0
end
local function nativeRoutineActive(proc,first,last)
 if proc<0x01000000 or proc+0x6f0>0x01400000 then return false end
 local function inside(pc) return pc>=first and pc<last end
 if inside(u32(proc+0xe0)) then return true end
 local stack=u32(proc+0x40)
 if stack<proc+0x3d0 or stack>proc+0x6f0-32 then return false end
 for cursor=stack,math.min(stack+7*32,proc+0x6f0-32),32 do
  if inside(u32(cursor)) then return true end
 end
 return false
end
local function renderedHeight(object)
 local groundAddress=tonumber(os.getenv('KS_GROUND_Y'))
 if not groundAddress or object<0x01000000 or object+0x200>=0x01400000 then return nil end
 local image=u32(object+0x1a0);local highest=65535
 -- Mirror highest_mpart/get_my_height, not animation-ground minus origin.
 for index=0,63 do
  local part=image+index*112
  if part<0x01000000 or part+112>=0x01400000 then return nil end
  if u32(part)==0 then
   if index==0 then return nil end
   return s16(groundAddress)-highest
  end
  highest=math.min(highest,s16(object+0xb0)-s16(part+96))
 end
 return nil
end
local sonyaRaidenRing=os.getenv('KS_CAMPAIGN_SONYA_RAIDEN_RING')=='1'
local sonyaKitanaRing=os.getenv('KS_CAMPAIGN_SONYA_KITANA_RING')=='1'
local sonyaKitanaLegCounter=os.getenv('KS_CAMPAIGN_SONYA_KITANA_LEG_COUNTER')=='1'
local kitanaLegStart,kitanaLegRetry=nil,-1000
local sonyaKitanaRingInterval=tonumber(os.getenv('KS_CAMPAIGN_SONYA_KITANA_RING_INTERVAL') or '60')
assert(sonyaKitanaRingInterval and sonyaKitanaRingInterval%1==0 and sonyaKitanaRingInterval>=24 and sonyaKitanaRingInterval<=120)
local subzeroGuard=os.getenv('KS_CAMPAIGN_SUBZERO_GUARD')=='1'
local kitanaReadyKnife=os.getenv('KS_CAMPAIGN_KITANA_READY_KNIFE')=='1' or sonyaRaidenRing or sonyaKitanaRing or subzeroGuard or sonyaSubGuardLeg or sonyaKintaroGuard or sonyaShangGuardLeg or sonyaOwnGuardLeg or sonyaScorpionGuardLeg or sonyaLaoGuardLeg or sonyaCageGuardLeg or sonyaMileenaGuardLeg or sonyaLiuGuardLeg
local kitanaFanGuard=os.getenv('KS_CAMPAIGN_KITANA_FAN_GUARD')=='1' or sonyaRaidenRing or sonyaKitanaRing or subzeroGuard or sonyaSubGuardLeg or sonyaKintaroGuard or sonyaShangGuardLeg or sonyaOwnGuardLeg or sonyaScorpionGuardLeg or sonyaLaoGuardLeg or sonyaCageGuardLeg or sonyaMileenaGuardLeg or sonyaLiuGuardLeg
local liuKnifeGuard=os.getenv('KS_CAMPAIGN_LIU_KNIFE_GUARD')=='1'
local liuRetreat=os.getenv('KS_CAMPAIGN_LIU_RETREAT')=='1'
local liuChoke=os.getenv('KS_CAMPAIGN_LIU_CHOKE')=='1'
local subzeroChoke=os.getenv('KS_CAMPAIGN_SUBZERO_CHOKE')=='1'
local subzeroNeutralChoke=os.getenv('KS_CAMPAIGN_SUBZERO_NEUTRAL_CHOKE')=='1'
local subzeroFastChoke=os.getenv('KS_CAMPAIGN_SUBZERO_FAST_CHOKE')=='1'
local fastChokeLog=subzeroFastChoke and assert(io.open('choke_ready.csv','w')) or nil
if fastChokeLog then fastChokeLog:write('frame,age,ownAction,ownFlags,height,bodyHeight,buttonTable,duckTable,distance,enemyAction,down,block,lp\n') end
local subzeroApproach=os.getenv('KS_CAMPAIGN_SUBZERO_APPROACH')=='1'
local subzeroWalkFields=tonumber(os.getenv('KS_CAMPAIGN_SUBZERO_APPROACH_FIELDS') or '6')
assert(subzeroWalkFields and subzeroWalkFields%1==0 and subzeroWalkFields>=6 and subzeroWalkFields<=30)
local subzeroKnife=os.getenv('KS_CAMPAIGN_SUBZERO_KNIFE')=='1'
local liuChokeStart,liuChokeRetry,liuChokeReady=nil,-1000,false
local retreatLastX,retreatLastFrame,retreatStill,retreatUntil=nil,-1,0,-1000
local liuBall=os.getenv('KS_CAMPAIGN_LIU_BALL')=='1'
local liuBallRelease,liuBallReleased=nil,false
local guardAfterHit=os.getenv('KS_CAMPAIGN_GUARD_AFTER_HIT')=='1'
local postHitGuardFields=tonumber(os.getenv('KS_CAMPAIGN_POST_HIT_FIELDS') or '24')
assert(postHitGuardFields and postHitGuardFields>=0 and postHitGuardFields<=64)
local postHitOpponent=tonumber(os.getenv('KS_CAMPAIGN_POST_HIT_OPPONENT') or '-1')
assert(postHitOpponent and postHitOpponent>=-1 and postHitOpponent<=18)
local projectileGuardUntil=-1000
local function cpuProjectileActive()
 local head=assert(tonumber(os.getenv('KS_ACTIVE_LIST')))
 local cursor=u32(head);local seen={};local count=0
 while cursor~=0 do
  assert(cursor>=0x01000000 and cursor<0x01400000 and not seen[cursor] and count<512)
  seen[cursor]=true;count=count+1
  local pid=u16(cursor+0x20)
  -- Sub-Zero replaces the generic projectile PID with pid_ice2 after spawn.
  -- Keep this extension optional so earlier established policies stay fixed.
  if pid==0x800 or ((subzeroGuard or sonyaSubGuardLeg) and pid==0x803) then return true end
  cursor=u32(cursor)
 end
 return false
end
local raidenCounter=os.getenv('KS_CAMPAIGN_RAIDEN_COUNTER')=='1'
local raidenBike=os.getenv('KS_CAMPAIGN_RAIDEN_BIKE_PUNISH')=='1'
local raidenFastBike=os.getenv('KS_CAMPAIGN_RAIDEN_FAST_BIKE')=='1'
local raidenReadyBike=os.getenv('KS_CAMPAIGN_RAIDEN_READY_BIKE')=='1'
local raidenBackLeg=os.getenv('KS_CAMPAIGN_RAIDEN_BACK_LEG')=='1'
local raidenSweep=os.getenv('KS_CAMPAIGN_RAIDEN_SWEEP')=='1'
local raidenJump=os.getenv('KS_CAMPAIGN_RAIDEN_JUMP')=='1'
local kitanaJump=os.getenv('KS_CAMPAIGN_KITANA_JUMP')=='1'
local guardWake=tonumber(os.getenv('KS_CAMPAIGN_GUARD_PC'))
local raidenPlan,raidenStart,raidenRetry=nil,-1000,-1000
local knifeGuardStart,knifeGuardRetry=nil,-1000
local knifeGuardWait=false
local counterJump,counterSweep=-1000,-1000
local counterTakeoff=os.getenv('KS_CAMPAIGN_COUNTER_TAKEOFF')=='1'
local counterForward=os.getenv('KS_CAMPAIGN_COUNTER_FORWARD')=='1'
local counterPrepare,counterAir,counterPreviousAction=nil,nil,-1
local counterLog=(femaleCounter or kitanaKnifeGuard or raidenCounter or liuBall or liuRetreat or liuChoke or subzeroGuard or sonyaKitanaLegCounter or sonyaRecoveryCounter or sonyaGuardLeg or sonyaSubGuardLeg or sonyaKintaroGuard or sonyaShangGuardLeg or sonyaOwnGuardLeg or sonyaScorpionGuardLeg or sonyaLaoGuardLeg or sonyaCageGuardLeg or sonyaMileenaGuardLeg or sonyaLiuGuardLeg) and assert(io.open('campaign_counter.csv','w')) or nil
if counterLog then counterLog:write('frame,attempt,opponent,distance,ownHeight,enemyHeight,ownAction,enemyAction,jumpAge,up,down,hp,hk,lk,block,left,right,ownY,ownGround,enemyY,enemyGround,retreatStill,retreatUntil,retreatRequested,ownFlags,ownX,enemyX,lp\n') end
local mixedZoning=os.getenv('KS_CAMPAIGN_MIXED_ZONING')=='1'
local projectileMixCount=0
local rosterGuard=os.getenv('KS_CAMPAIGN_ROSTER_GUARD')=='1'
local backGuard=os.getenv('KS_CAMPAIGN_BACK_GUARD')=='1'
local guardPlan,guardStart,guardRetry,guardUntil,guardLast=nil,-1000,-1000,-1000,-1000
local knifeGuard=os.getenv('KS_CAMPAIGN_KNIFE_GUARD')=='1'
local jaxSweep=os.getenv('KS_CAMPAIGN_JAX_SWEEP')=='1'
local jaxThrow=os.getenv('KS_CAMPAIGN_JAX_THROW')=='1'
local jaxAir=os.getenv('KS_CAMPAIGN_JAX_AIR')=='1'
local jaxReactive=os.getenv('KS_CAMPAIGN_JAX_REACTIVE')=='1'
local jaxPoundUntil,jaxJump,jaxLeg=-1000,-1000,-1000
local defenseUntil=0
if kickOverride then assert(kickOverride>=6 and kickOverride<=28) end
local navigation={}
for _,direction in ipairs({'Up','Down','Left','Right'}) do
 local values={};local i=0
 for value in (os.getenv('KS_SELECT_'..direction:upper()) or ''):gmatch('[^,]+') do values[i]=assert(tonumber(value));i=i+1 end
 navigation[direction]=values
end
local function nextDirection(start,destination)
 local queue={{start,nil}};local seen={[start]=true};local head=1
 while head<=#queue do
  local item=queue[head];head=head+1
  if item[1]==destination then return item[2] end
  for _,direction in ipairs({'Up','Down','Left','Right'}) do
   local neighbor=navigation[direction][item[1]]
   if neighbor and not seen[neighbor] then seen[neighbor]=true;queue[#queue+1]={neighbor,item[2] or direction} end
  end
 end
 return nil
end
local missing=assert(tonumber(os.getenv('KS_MISSING_COUNT')))
local recovery=assert(tonumber(os.getenv('KS_RECOVERY_PC')))
local log=assert(io.open('campaign.csv','w'))
log:write('frame,combat,mode,map,winner,p1selected,p2selected,p1char,p2char,p1hp,p2hp,p1x,p2x,p1action,p2action,p1shape,p2shape,missing,pc,round,p1match,p2match,attempt\n')
local n,selection,combat=0,0,0
local locked=false
local enteredCombat=false
local previousMode=-1
local closeCycle=false
local lastHealth=0
local plan=nil
local planAge=0
local planToward=nil
local controls={'Coin 1','1 Player Start','P1 High Punch','P1 Low Punch','P1 High Kick','P1 Low Kick','P1 Block','P1 Left','P1 Right','P1 Down','P1 Up'}
emu.register_frame_done(function()
 n=n+1
 for _,name in ipairs(controls) do set(name,0) end
 local mode=u16(0x010601d0)
 local c1,c2=u16(0x01060280),u16(0x01060e50)
 if mode==3 and enteredCombat then
  if previousMode~=3 and continuesUsed<continueLimit then
   continuesUsed=continuesUsed+1;continuing=true;buyinAge=0
   continueLog:write(string.format('%d,%d,%d,buyin\n',n,continuesUsed,u16(0x01061b30)));continueLog:flush()
  end
  if continuing then
   buyinAge=buyinAge+1
   local inputAge=buyinAge-((target==17 and u16(0x01061b30)>=15) and bossContinueDelay or 0)
   if inputAge>0 then
    set('Coin 1',inputAge%120<4 and 1 or 0)
    set('1 Player Start',inputAge%120>=20 and inputAge%120<24 and 1 or 0)
   end
  end
 end
 if mode==4 and previousMode~=4 and continuing then
  locked=false;selection=0
  continueLog:write(string.format('%d,%d,%d,selection\n',n,continuesUsed,u16(0x01061b30)));continueLog:flush()
 end
 if n>3000 and selection==0 and mode~=4 and not enteredCombat then
  set('Coin 1',n%600<6 and 1 or 0)
  set('1 Player Start',n%600>=60 and n%600<66 and 1 or 0)
  set('P1 High Punch',n%40<4 and 1 or 0)
 end
 if mode==4 and not locked then
  selection=selection+1
  if selection>50 and selection%20<3 and c1~=target then
   local direction=nextDirection(c1,target)
   if direction then set('P1 '..direction,1) end
  end
  if selection>160 and c1==target then set('P1 High Punch',1);locked=true end
 end
 local a,b=u32(0x01060220),u32(0x01060df0)
 local proc1,proc2=u32(0x01060260),u32(0x01060e30)
 local x1,x2=a~=0 and s16(a+0x90) or 0,b~=0 and s16(b+0x90) or 0
 if mode==2 and locked then
  if continuing then
   continueLog:write(string.format('%d,%d,%d,combat\n',n,continuesUsed,u16(0x01061b30)));continueLog:flush()
   continuing=false
  end
  enteredCombat=true
  if previousMode~=2 or u16(0x010602f0)>lastHealth+80 then
   combat=0;plan=nil;projectileMixCount=0
   kahnCounterRetry=-1000
   subJumpStart=nil;subJumpRequest=-1000
   subBallStart=nil;subBallReleaseAt=nil;subBallReleased=false;subBallRecovery.start=nil
   subBallRecovery.uppercutPrepare=nil;subBallRecovery.finishKnifeStart=nil;subBallRecovery.finishKnifeReady=false
   stompPhaseSeen=false;stompFlightActive=false;stompSawAir=false;stompJumped=false
   retreatLastX=nil;retreatLastFrame=-1;retreatStill=0;retreatUntil=-1000
   liuChokeStart=nil;liuChokeRetry=-1000;liuChokeReady=false
   subzeroCounterRetry=-1000
   recoveryCounterStart=nil
   lowGuardFields=0;guardLegRetry=-1000;guardLegStart=nil
   bossCounterPrepare=nil;bossCounterRetry=-1000
   subBallRecovery.bossBallStart=nil;subBallRecovery.bossBallAt=-1000
  end
  combat=combat+1
  local toward=x1<x2 and 'P1 Right' or 'P1 Left'
  local away=x1<x2 and 'P1 Left' or 'P1 Right'
  local distance=math.abs(x2-x1)
  -- Read-only state guides physical inputs; health/stage/AI are never modified.
  if combat<=60 and ((sonyaKahnGuard and target==18) or (subBallRecovery.kanoBoss and target==17)) and c2==13 and
     u16(0x010602f0)>0 and u16(0x01060ec0)>0 then
   if kahnOpeningJump then
    -- One physical backward jump, then retreat; no forced position or flight.
    set(away,1)
    if combat<=4 then set('P1 Up',1) end
   else set('P1 Down',1);set('P1 Block',1) end
  end
  if combat<=60 and liuKnifeGuard and target==17 and c2==1 and
     u16(0x010602f0)>0 and u16(0x01060ec0)>0 then
   set('P1 Block',1);set(away,1)
  end
  if combat<=60 and sonyaRaidenRing and target==18 and c2==7 and
     u16(0x010602f0)>0 and u16(0x01060ec0)>0 then
   set('P1 Block',1);set(away,1)
  end
  if combat<=60 and kitanaRfpDuck and target==17 and c2==4 and
     u16(0x010602f0)>0 and u16(0x01060ec0)>0 then
   set('P1 Block',1);set(away,1)
  end
  if combat<=60 and sonyaKitanaRing and target==18 and c2==4 and
     u16(0x010602f0)>0 and u16(0x01060ec0)>0 then
   set('P1 Block',1);set(away,1)
  end
  if (combat>60 or ((subBallRecovery.kintaroEarlyCounter or subBallRecovery.kintaroVaried or subBallRecovery.kintaroVertical or subBallRecovery.kintaroRecovery) and target==17 and c2==12)) and u16(0x010602f0)>0 and u16(0x01060ec0)>0 then
   local enemyY=b~=0 and s16(b+0xb0) or 0
   local enemyGround=proc2~=0 and s16(proc2+0x200) or 0
   if defensive and u16(0x010602f0)<lastHealth then
    plan=nil;defenseUntil=combat+24
   end
   if earlyStompEvade and (target==18 or (subBallRecovery.kanoBoss and target==17)) and c2==12 and u16(proc2+0x1f0)==0x407 then
    if not stompPhaseSeen or (not stompFlightActive and enemyGround-enemyY>0) then
     stompFlightActive=true;stompSawAir=false;stompJumped=false;stompEscapeLast=-1000;subBallRecovery.stompJumpRequested=false
    end
    stompPhaseSeen=true
    if enemyGround-enemyY>0 then stompSawAir=true
    elseif stompSawAir then stompFlightActive=false end
   else stompPhaseSeen=false;stompFlightActive=false;stompSawAir=false;stompJumped=false end
   if ((sonyaKahnGuard and target==18) or (subBallRecovery.kanoBoss and target==17)) and c2==13 then
    plan=nil
    local charge=nativeRoutineActive(proc2,assert(tonumber(os.getenv('KS_KAHN_CHARGE_BEGIN'))),
       assert(tonumber(os.getenv('KS_KAHN_CHARGE_END'))))
    local velocity=u32(b+0x40)
    if velocity>=0x80000000 then velocity=velocity-0x100000000 end
    local ownHeight=s16(proc1+0x200)-s16(a+0xb0)
    local ownFlags=u16(proc1+0x210)
    local bodyHeight=renderedHeight(a) or -1
    local buttonTable=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
    local duckTable=assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
    local contactRecovery=charge and u32(proc2+0xe0)==assert(tonumber(os.getenv('KS_KAHN_CONTACT_WAKE')))
    set('P1 Down',1)
    if kahnContactReady then
     -- Prepare the released guard during native block-stun; never bypass it.
     if contactRecovery then
      if distance<=105 and ownHeight==0 and (ownFlags&0x1c)==0 and
         bodyHeight>=0 and bodyHeight<=96 and buttonTable==duckTable and n-kahnCounterRetry>=36 then
       set('P1 High Punch',1);kahnCounterRetry=n
      end
     else set('P1 Block',1) end
    elseif charge and velocity==0 and distance<=140 and ownHeight==0 and (ownFlags&0x1c)==0 then
     -- Native charge contact holds32 fields; release guard, never force input readiness.
     if bodyHeight>=0 and bodyHeight<=96 and buttonTable==duckTable and n-kahnCounterRetry>=36 then
      set('P1 High Punch',1);kahnCounterRetry=n
     end
    else set('P1 Block',1) end
    kahnLog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%08x,%d,%d,%d,%d,%d,%d\n',
     n,charge and 1 or 0,velocity,distance,ownHeight,ownFlags,bodyHeight,buttonTable,duckTable,
     u32(proc2+0xe0),u16(0x010602f0),u16(0x01060ec0),commands['P1 Down'] or 0,
     commands['P1 Block'] or 0,commands['P1 High Punch'] or 0,contactRecovery and 1 or 0))
    if n%16==0 then kahnLog:flush() end
   elseif sonyaKintaroEvade and (target==18 or (subBallRecovery.kanoBoss and target==17)) and c2==12 and u16(proc2+0x1f0)==0x407 and
      (u16(proc1+0x210)&0x1c)==0 and ((earlyStompEvade and stompFlightActive) or
       (not earlyStompEvade and enemyGround-enemyY>80 and s16(proc1+0x200)==s16(a+0xb0))) then
    -- Match native get_my_dfe: right_edge is a scroll origin, not the boundary.
    plan=nil
    local leftEdge=s16(assert(tonumber(os.getenv('KS_KINTARO_LEFT_EDGE'))))
    local rightEdge=s16(assert(tonumber(os.getenv('KS_KINTARO_RIGHT_EDGE'))))+
       assert(tonumber(os.getenv('KS_KINTARO_SCREEN_RIGHT')))
    local leftDistance,rightDistance=math.abs(x1-leftEdge),math.abs(rightEdge-x1)
    if n-stompEscapeLast>1 then
     stompEscapeDirection=leftDistance>=rightDistance and 'P1 Left' or 'P1 Right'
     if subBallRecovery.kintaroStompMomentum and target==17 then
      subBallRecovery.stompVelocity=u32(a+0x40)
      if subBallRecovery.stompVelocity>=0x80000000 then subBallRecovery.stompVelocity=subBallRecovery.stompVelocity-0x100000000 end
      if subBallRecovery.stompVelocity>0 and rightDistance>=128 then stompEscapeDirection='P1 Right'
      elseif subBallRecovery.stompVelocity<0 and leftDistance>=128 then stompEscapeDirection='P1 Left' end
     end
    end
    stompEscapeLast=n
    set(stompEscapeDirection,1)
    local ownHeight=s16(proc1+0x200)-s16(a+0xb0)
    if earlyStompEvade and not (subBallRecovery.kintaroWalkStomp and target==17) then
     if subBallRecovery.kintaroStompRefresh and target==17 then
      -- An older offensive jump is not an escape jump requested this phase.
      if ownHeight>0 and subBallRecovery.stompJumpRequested then stompJumped=true end
      if ownHeight==0 and not stompJumped then
       set('P1 Up',1);subBallRecovery.stompJumpRequested=true
      end
     else
      if ownHeight>0 then stompJumped=true end
      if ownHeight==0 and not stompJumped then set('P1 Up',1) end
     end
    end
    stompEscapeLog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,%d,%d\n',
     n,x1,x2,enemyGround-enemyY,leftEdge,rightEdge,leftDistance,rightDistance,
     stompEscapeDirection,u16(0x010602f0),u16(proc1+0x210),ownHeight,commands['P1 Up'] or 0))
    if n%16==0 then stompEscapeLog:flush() end
   elseif raidenCounter and target==18 and c2==7 then
    plan=nil
    local ownAction=u16(proc1+0x1f0)
    local enemyAction=u16(proc2+0x1f0)
    local grounded=s16(proc1+0x200)==s16(a+0xb0)
    local nativeGuard=raidenSweep and guardWake and u32(proc1+0xe0)==guardWake
    local ready=grounded and (nativeGuard or ownAction==0x303 or ownAction==0x302 or ownAction==0x700 or ownAction==0x701)
    if enemyAction==0x209 then
     raidenPlan=nil;set('P1 Block',1);set(away,1)
    elseif raidenPlan then
     local age=n-raidenStart
     if raidenPlan=='bike_ready' then
      -- Rising from duck discards early direction closes. Do not start the
      -- combo clock until the actual stance accepts a fresh first Back.
      if grounded and ownAction==0x303 then
       raidenPlan='bike';raidenStart=n;age=0;set(away,1)
      end
     elseif raidenPlan=='sweep_ready' or raidenPlan=='ring_ready' then
      -- Do not spend the attack window on native unblock frames. Physical
      -- release alone lets the engine reach stance; no state is forced.
      if grounded and ownAction==0x303 then
       raidenPlan=raidenPlan=='sweep_ready' and 'sweep' or 'ring'
       raidenStart=n;age=0
      end
     elseif raidenPlan=='bike' then
      local second=raidenFastBike and 6 or 10
      local down=raidenFastBike and 9 or 20
      local kick=raidenFastBike and 12 or 26
      if age<3 or (age>=second and age<second+3) then set(away,1) end
      if age>=down and age<down+3 then set('P1 Down',1) end
      if age>=kick and age<kick+4 then set('P1 High Kick',1) end
     elseif raidenPlan=='sweep' then
      if age>=3 and age<7 then set(away,1);set('P1 Low Kick',1) end
     elseif raidenPlan=='leg' then
      if age<7 then set('P1 Down',1) end
      if age>=3 and age<7 then set('P1 Low Punch',1);set('P1 Block',1) end
     else
      if age<3 then set('P1 Down',1)
      elseif age<6 then set(toward,1)
      elseif age<9 then set('P1 Low Punch',1) end
     end
     local waiting=raidenPlan=='bike_ready' or raidenPlan=='sweep_ready' or raidenPlan=='ring_ready'
     local limit=waiting and 45 or (raidenPlan=='bike' and (raidenFastBike and 17 or 31) or 10)
     if age>=limit then raidenPlan=nil;set('P1 Down',1);set('P1 Block',1) end
    elseif ready and enemyAction==0x602 and distance<(raidenBike and 220 or 125) and n-raidenRetry>=32 then
     raidenPlan=raidenBike and (raidenReadyBike and 'bike_ready' or 'bike') or 'leg';raidenStart=n;raidenRetry=n
     if not raidenBike then set('P1 Down',1) end
    elseif ready and enemyAction==0x602 and distance>=(raidenBike and 220 or 125) then set(toward,1)
    elseif ready and distance>130 and enemyAction~=0x0f and n-raidenRetry>=60 then
     raidenPlan=raidenSweep and 'ring_ready' or 'ring';raidenStart=n;raidenRetry=n
     if not raidenSweep then set('P1 Down',1) end
    elseif ready and distance<90 and enemyGround-enemyY==0 and
       (enemyAction==0x303 or enemyAction==0x302 or enemyAction==0x700 or enemyAction==0x701) and n-raidenRetry>=40 then
     raidenPlan=raidenSweep and 'sweep_ready' or 'leg';raidenStart=n;raidenRetry=n
     if not raidenSweep then set('P1 Down',1) end
    else set('P1 Down',1);set('P1 Block',1);set(away,1) end
    if raidenBackLeg and (raidenPlan=='leg' or raidenPlan==nil) then set(away,1) end
    -- MKDRONE.drone_body_slam bypasses Away protection for a short target.
    -- Keep the measured full-height guard between attacks; Down is still
    -- required during the actual Leg Grab command above.
    if raidenBackLeg and raidenPlan==nil then set('P1 Down',0);set('P1 Block',1) end
    -- A blocked interruption can return to joy_block_loop with the old
    -- special action tag. Periodically release held guard so native stance
    -- refreshes it; never write the action or infer a stuck animation.
    if raidenBackLeg and raidenPlan==nil and ownAction==0x219 and
       n-raidenRetry>100 and n%96<12 then set('P1 Block',0) end
   elseif ((sonyaKintaroGuard and target==18) or (subBallRecovery.kintaroEvadeCounter and target==17)) and c2==12 then
    -- Physical boss strategy only. KSLEG explicitly excludes both bosses.
    plan=nil
    local height=s16(proc1+0x200)-s16(a+0xb0)
    local enemyHeight=s16(proc2+0x200)-s16(b+0xb0)
    local ownFlags=u16(proc1+0x210)
    local enemyAction=u16(proc2+0x1f0)
    local grounded=height==0 and (ownFlags&0x1c)==0
    local duckButtons=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))==
       assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
    if enemyAction==0x407 and enemyHeight>80 and grounded then
     -- Native psycho stomp saves our X before takeoff; walk out of that X.
     bossCounterPrepare=nil;set(away,1)
    elseif grounded and distance<=100 and enemyHeight<=60 and n-bossCounterRetry>=36 then
     bossCounterPrepare=bossCounterPrepare or n
     set('P1 Down',1)
     local bodyHeight=renderedHeight(a) or -1
     if bodyHeight>=0 and bodyHeight<=96 and duckButtons then
      set('P1 High Punch',1);bossCounterRetry=n;bossCounterPrepare=nil
     elseif n-bossCounterPrepare>=24 then
      bossCounterPrepare=nil;bossCounterRetry=n
      set('P1 Block',1);set(away,1)
     end
    else
     bossCounterPrepare=nil;set('P1 Down',1);set('P1 Block',1);set(away,1)
    end
    -- Passive bounded-context diagnostics; never used to alter an input.
    bossContextLog:write(string.format('%d,%d,%d,%d,%08x,%08x,%d,%d,%d,%08x,%08x,%d,%d,%d\n',
     n,height,renderedHeight(a) or -1,ownFlags,
     u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS')))),
     assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS'))),enemyHeight,
     u16(proc2+0x210),enemyAction,u32(proc1+0xe0),u32(proc2+0xe0),
     bossCounterPrepare and n-bossCounterPrepare or -1,n-bossCounterRetry,
     commands['P1 High Punch'] or 0))
    if n%16==0 then bossContextLog:flush() end
   elseif subBallRecovery.normalThrow and target==17 and (c2==8 or (subBallRecovery.mileenaPrepare and c2==5) or
       (subBallRecovery.humanPrepare and (c2==2 or c2==0 or c2==6 or c2==10 or c2==17 or c2==18)) or
       (subBallRecovery.kintaroPrepare and c2==12)) then
    plan=nil
    local ownAction=u16(proc1+0x1f0)
    local ownFlags=u16(proc1+0x210)
    local height=s16(proc1+0x200)-s16(a+0xb0)
    local enemyAction=u16(proc2+0x1f0)
    local enemyFlags=u16(proc2+0x210)
    local enemyHeight=enemyGround-enemyY
    local projectile=cpuProjectileActive()
    local phase='guard'
    subBallRecovery.activeOpponent=u16(b+0x1f0)
    set('P1 Block',1);set(away,1)
    if projectile or (subBallRecovery.activeOpponent==8 and (enemyAction==0x10 or enemyAction==0x20c)) or
       (subBallRecovery.activeOpponent==5 and (enemyAction==0x20e or enemyAction==0x208)) or
       (subBallRecovery.activeOpponent==2 and (enemyAction==0x205 or enemyAction==0x206)) or
       (subBallRecovery.activeOpponent==0 and (enemyAction==0x108 or enemyAction==0x202)) or
       (subBallRecovery.activeOpponent==10 and enemyAction==0x20a) or
       (subBallRecovery.activeOpponent==17 and enemyAction==0x20b) or
       (subBallRecovery.activeOpponent==18 and (enemyAction==0x204 or enemyAction==0x207)) or
       (subBallRecovery.kintaroPrepare and subBallRecovery.activeOpponent==12 and
        (enemyAction==0x407 or enemyAction==0x507)) then
     set('P1 Down',1)
     if enemyHeight>0 or (subBallRecovery.activeOpponent==5 and enemyAction==0x208) or
        (subBallRecovery.activeOpponent==0 and enemyAction==0x202) or
        (subBallRecovery.activeOpponent==10 and enemyAction==0x20a) then set('P1 Down',0) end
     subBallRecovery.uppercutPrepare=nil
     subBallRecovery.finishKnifeStart=nil;subBallRecovery.finishKnifeReady=false
    elseif subBallRecovery.neutralUppercut then
     -- Physical controller only: avoid the CPU throw-entry race by taking
     -- close grounded standing windows from actual native duck readiness.
     if n-subBallRecovery.uppercutAt<3 and height==0 and (ownFlags&4)==0 then
      phase='uppercut_follow';set('P1 Block',0);set(away,0);set('P1 Down',1);set('P1 High Punch',1)
     elseif subBallRecovery.finishKnifeStart or
        (u16(0x01060ec0)<=5 and distance>=120 and height==0 and (ownFlags&0x1c)==0 and enemyHeight==0) then
      -- At native lethal-chip health, use the proven D,B,HP command from
      -- the post-uppercut gap instead of walking into another CPU throw.
      subBallRecovery.uppercutPrepare=nil
      if not subBallRecovery.finishKnifeStart and n-subBallRecovery.finishKnifeAt>=80 then
       subBallRecovery.finishKnifeStart=n;subBallRecovery.finishKnifeReady=false
      end
      if subBallRecovery.finishKnifeStart then
       phase='knife_prepare';set('P1 Block',0);set(away,0);set('P1 Down',0)
       if (ownFlags&4)~=0 or height~=0 then
        subBallRecovery.finishKnifeStart=nil;subBallRecovery.finishKnifeReady=false
       elseif not subBallRecovery.finishKnifeReady then
        if (ownFlags&0x1c)==0 and ownAction==0x303 and (renderedHeight(a) or -1)>=96 and
           u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))~=assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS'))) then
         subBallRecovery.finishKnifeReady=true;subBallRecovery.finishKnifeStart=n
         phase='knife_down';set('P1 Down',1)
        elseif n-subBallRecovery.finishKnifeStart>=45 then subBallRecovery.finishKnifeStart=nil end
       elseif n-subBallRecovery.finishKnifeStart<3 then
        phase='knife_down';set('P1 Down',1)
       elseif n-subBallRecovery.finishKnifeStart<6 then
        phase='knife_gap_down'
       elseif n-subBallRecovery.finishKnifeStart<9 then
        phase='knife_back';set('P1 Down',0);set(away,1)
       elseif n-subBallRecovery.finishKnifeStart<12 then
        phase='knife_gap_back'
       elseif n-subBallRecovery.finishKnifeStart<15 then
        phase='knife_punch';set('P1 Down',0);set('P1 High Punch',1)
        subBallRecovery.finishKnifeAt=n
       else subBallRecovery.finishKnifeStart=nil;subBallRecovery.finishKnifeReady=false end
      else phase='knife_wait';set('P1 Down',1) end
     elseif height==0 and (ownFlags&0x1c)==0 and enemyHeight==0 and distance<=140 and
        (((enemyFlags&0x1c)==0 and (renderedHeight(b) or -1)>96) or
         (subBallRecovery.uppercutPrepare and n-subBallRecovery.uppercutPrepare<24 and (enemyFlags&0x0c)==0)) then
      -- Prepare before close pressure; actual HP still requires <=84.
      -- Keep a bounded physical preparation through an enemy attack instead
      -- of resetting the Down/input-table transition at every RFP entry.
      phase='uppercut_prepare';set('P1 Block',0);set(away,0);set('P1 Down',1)
      if not subBallRecovery.uppercutPrepare then subBallRecovery.uppercutPrepare=n end
      if (distance<=84 or (subBallRecovery.kintaroWide and c2==12 and distance<=105)) and n-subBallRecovery.uppercutPrepare>=4 and n-subBallRecovery.uppercutAt>=60 and
         (renderedHeight(a) or 999)<=96 and
         u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))==assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS'))) then
       phase=(enemyFlags&0x10)~=0 and 'uppercut_counter' or 'uppercut'
       set('P1 High Punch',1);subBallRecovery.uppercutAt=n;subBallRecovery.uppercutPrepare=nil
      end
     elseif height==0 and (ownFlags&0x1c)==0 and enemyHeight==0 and
        (enemyFlags&0x1c)==0 and distance>160 then
      phase='approach';set('P1 Block',0);set(away,0);set(toward,1);subBallRecovery.uppercutPrepare=nil
     else
      set('P1 Down',1);subBallRecovery.uppercutPrepare=nil
     end
    elseif height==0 and (ownFlags&0x1c)==0 and
       enemyHeight==0 and (enemyFlags&0x1c)==0 then
     if distance>60 then
      phase='approach';set('P1 Block',0);set(away,0);set(toward,1)
     else
      phase='prepare';set('P1 Block',0);set(away,0)
      if ownAction==0x303 and n-subBallRecovery.throwAt>=12 then
       phase='throw';set(toward,1);set('P1 Low Punch',1)
       subBallRecovery.throwAt=n
      end
     end
    end
    subBallRecovery.throwLog:write(string.format('%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',
     n,phase,ownAction,ownFlags,height,enemyAction,enemyFlags,enemyHeight,distance,projectile and 1 or 0,
     commands[toward] or 0,commands[away] or 0,commands['P1 Block'] or 0,commands['P1 Down'] or 0,commands['P1 Low Punch'] or 0,commands['P1 High Punch'] or 0,
     renderedHeight(a) or -1,u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS')))),assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS'))),c2,subBallRecovery.activeOpponent))
    if n%16==0 then subBallRecovery.throwLog:flush() end
   elseif kanoSubBall and target==17 and c2==8 then
    plan=nil
    local ownAction=u16(proc1+0x1f0)
    local ownFlags=u16(proc1+0x210)
    local height=s16(proc1+0x200)-s16(a+0xb0)
    local enemyAction=u16(proc2+0x1f0)
    local enemyFlags=u16(proc2+0x210)
    local projectile=cpuProjectileActive()
    local rapid,left,recovering,root=false,0,false,0
    if kanoSubAdaptiveCharge then rapid,left,recovering,root=cpuRapidPunch(proc2) end
    if subzeroObservationLog and kanoSubAdaptiveCharge then
     subzeroObservationLog:write(string.format('%d,%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',n,enemyFlags,u32(proc2+0xe0),rapid and 1 or 0,left or 0,recovering and 1 or 0,root or 0,ownAction,enemyAction,u16(0x010602f0),u16(0x01060ec0),distance))
     if n%16==0 then subzeroObservationLog:flush() end
    end
    local enemyReady=(enemyFlags&0x1c)==0 or (subBallRecovery.ball and rapid and recovering and (enemyFlags&0x0c)==0)
    local eligible=height==0 and (ownFlags&0x1c)==0 and
       enemyGround==enemyY and enemyReady and distance>=80 and distance<=260 and not projectile and (not subBallRecovery.approach or distance<=140)
    if not subBallStart then subBallStart=n end
    local age=n-subBallStart
    local recoveryBallReady=subBallRecovery.ball and (not subBallRecovery.recharge or age>85)
    if age>85 and not subBallReleased then
     if not eligible then subBallReleaseAt=nil
     elseif not subBallReleaseAt then subBallReleaseAt=n+4
     elseif n>=subBallReleaseAt then subBallReleased=true end
    end
    if not subBallReleased then
     set('P1 Low Kick',1);set(away,1)
     if not kanoSubStandingCharge then set('P1 Down',1) end
     if not subBallReleaseAt then set('P1 Block',1) end
     if kanoSubAdaptiveCharge then
      local highRfp=rapid and not recovering and left>1 and root==0x13
      if highRfp or (subBallRecovery.counter and rapid and recovering) then
       set('P1 Down',1);set('P1 Block',0)
       if kanoSubBallCounter and not (recoveryBallReady and recovering) then
        local bodyHeight=renderedHeight(a) or -1
        local buttons=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
        local duckButtons=assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
        if height==0 and (ownFlags&0x1c)==0 and distance<105 and
           bodyHeight>=0 and bodyHeight<=96 and buttons==duckButtons and n-subBallCounterAt>=12 then
         set(away,0);set('P1 High Punch',1);subBallCounterAt=n
        end
       end
      elseif projectile or enemyAction==0x10 or enemyAction==0x20c or distance>140 then
       set('P1 Down',1)
      end
     end
    end
    if subBallRecovery.approach and not subBallReleased and age>=4 and
       height==0 and (ownFlags&0x1c)==0 and enemyGround==enemyY and
       (enemyFlags&0x1c)==0 and enemyAction==0x303 and not projectile and distance>140 then
     set('P1 Down',0);set('P1 Block',0);set(away,0);set(toward,1)
    end
    if subBallRecovery.recharge and subBallReleased and n-subBallReleaseAt>=4 then
     set('P1 Low Kick',1)
     if not subBallRecovery.start then subBallRecovery.start=n end
    end
    -- Preserve the unguarded eight-field release observation window. Afterwards
    -- request standing guard/retreat through Ball recovery and enemy reactions.
    if subBallRecovery.postGuard and subBallReleased and n-subBallReleaseAt>=8 then
     set('P1 Block',1);set(away,1)
    end
    local phase=subBallReleased and 'released' or (subBallReleaseAt and 'prepare' or 'charge')
    subBallLog:write(string.format('%d,%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',
     n,age,phase,eligible and 1 or 0,ownAction,ownFlags,height,enemyAction,enemyFlags,distance,
     projectile and 1 or 0,commands['P1 Low Kick'] or 0,commands['P1 Block'] or 0,commands['P1 Down'] or 0,commands['P1 High Punch'] or 0,commands[toward] or 0,commands[away] or 0))
    if n%16==0 then subBallLog:flush() end
    if subBallReleased and ownAction==0x303 and n-subBallReleaseAt>=16 then
     subBallStart=subBallRecovery.start;subBallReleaseAt=nil;subBallReleased=false;subBallRecovery.start=nil
    end
   elseif kanoSubJump and target==17 and c2==8 then
    plan=nil
    local ownAction=u16(proc1+0x1f0)
    local height=s16(proc1+0x200)-s16(a+0xb0)
    local enemyHeight=enemyGround-enemyY
    local jumping=ownAction==0x308 or ownAction==0x30b
    if jumping and not subJumpStart then subJumpStart=n end
    if height==0 and not jumping then subJumpStart=nil end
    if height>0 then
     local kickWindow=subJumpStart and ((kanoSubRangeKick and distance<=110 and height>=16 and
        n-subJumpStart>=4 and n-subJumpStart<40) or
        (not kanoSubRangeKick and n-subJumpStart>=18 and n-subJumpStart<24))
     if jumping and kickWindow then
      set('P1 High Kick',1)
     end
    elseif enemyHeight>16 and distance<110 and (u16(proc1+0x210)&0x1c)==0 then
     set('P1 Down',1)
     local buttons=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
     local duck=assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
     local body=renderedHeight(a) or -1
     if buttons==duck and body>=0 and body<=96 then set('P1 High Punch',1) end
    elseif kanoSubJumpHold and n-subJumpRequest<8 and height==0 and not jumping and (u16(proc1+0x210)&0x1c)==0 then
     -- Hold physical diagonal across normal input-poll latency; never force takeoff.
     set(toward,1);set('P1 Up',1)
    elseif height==0 and ownAction==0x303 and (u16(proc1+0x210)&0x1c)==0 and n-subJumpRequest>=12 then
     set(toward,1);set('P1 Up',1);subJumpRequest=n
    end
   elseif (target==17 and ((kitanaKnifeGuard and c2==4) or (liuKnifeGuard and c2==1 and not liuBall) or (subzeroGuard and c2==8))) or
      (sonyaRaidenRing and target==18 and c2==7) or
      (sonyaKitanaRing and target==18 and c2==4) or (sonyaLiuGuardLeg and target==18 and c2==1) or (sonyaMileenaGuardLeg and target==18 and c2==5) or (sonyaCageGuardLeg and target==18 and c2==2) or (sonyaLaoGuardLeg and target==18 and c2==0) or (sonyaScorpionGuardLeg and target==18 and c2==10) or ((sonyaOwnGuardLeg and target==18 and (c2==17 or c2==18)) or (sonyaShangGuardLeg and target==18 and c2==6)) or (sonyaSubGuardLeg and target==18 and c2==8) then
    plan=nil
    local ownAction=u16(proc1+0x1f0)
    local height=s16(proc1+0x200)-s16(a+0xb0)
    local enemyAction=u16(proc2+0x1f0)
    if liuRetreat and target==17 and c2==1 and height==0 and (u16(proc1+0x210)&0x1c)==0 and
       retreatLastFrame==n-1 and retreatLastX==x1 then
     retreatStill=retreatStill+1
     if retreatStill>=12 then retreatUntil=n+60;retreatStill=0 end
    else retreatStill=0 end
    local fanThreat=kitanaFanGuard and ((sonyaShangGuardLeg and c2==6 and (enemyAction==0x0c or enemyAction==0x0d or enemyAction==0x0e)) or (c2==4 and (enemyAction==8 or enemyAction==9)) or
     (c2==1 and (enemyAction==2 or enemyAction==3 or enemyAction==4 or enemyAction==0x203 or enemyAction==0x204)) or
     (c2==7 and (enemyAction==0x0f or enemyAction==0x209)) or
     (sonyaOwnGuardLeg and c2==17 and (enemyAction==0x20b or enemyAction==0x211 or enemyAction==0x117 or enemyAction==0x216)) or
     (sonyaOwnGuardLeg and c2==18 and (enemyAction==0x207 or enemyAction==0x212 or enemyAction==0x204 or enemyAction==0x214 or enemyAction==0x219 or enemyAction==0x21a)) or
     (sonyaScorpionGuardLeg and c2==10 and (enemyAction==0x11 or enemyAction==0x20a)) or
     (sonyaLaoGuardLeg and c2==0 and (enemyAction==1 or enemyAction==0x108 or enemyAction==0x202)) or
     (sonyaCageGuardLeg and c2==2 and (enemyAction==5 or enemyAction==6 or enemyAction==0x205 or enemyAction==0x206)) or
     (sonyaMileenaGuardLeg and c2==5 and (enemyAction==0x0a or enemyAction==0x0b or enemyAction==0x208 or enemyAction==0x20e)) or
     ((subzeroGuard or sonyaSubGuardLeg) and c2==8 and (enemyAction==0x10 or enemyAction==0x20c)) or
     cpuProjectileActive())
    local usePressureGuard=guardAfterHit and (postHitOpponent<0 or c2==postHitOpponent)
    if usePressureGuard and u16(0x010602f0)<lastHealth then projectileGuardUntil=n+postHitGuardFields end
    local pressureGuard=usePressureGuard and n<projectileGuardUntil
    if sonyaMileenaNoRing and target==18 and c2==5 then
     knifeGuardStart=nil;knifeGuardWait=false
    end
    local rapidPunch,punchesLeft,rfpRecovering,punchAnimation=false,0,false,0
    local counterBodyHeight=-1
    local counterButtonTable,counterButtonsReady=0,false
    local knifeInterval=(target==17 and c2==1) and liuKnifeInterval or ((target==17 and c2==4) and kitanaKnifeInterval or 60)
    if target==18 and c2==4 then knifeInterval=sonyaKitanaRingInterval end
    if target==17 and c2==8 then knifeInterval=subzeroKnifeInterval end
    local nativeDuckCounter=(subzeroRfpDuck and c2==8) or (sonyaKitanaRfpDuck and target==18 and c2==4) or (sonyaLiuGuardLeg and target==18 and c2==1) or (sonyaMileenaGuardLeg and target==18 and c2==5) or (sonyaCageGuardLeg and target==18 and c2==2) or (sonyaLaoGuardLeg and target==18 and c2==0) or (sonyaScorpionGuardLeg and target==18 and c2==10) or ((sonyaOwnGuardLeg and target==18 and (c2==17 or c2==18)) or (sonyaShangGuardLeg and target==18 and c2==6)) or (sonyaSubGuardLeg and target==18 and c2==8)
    local guardLegMatch=target==18 and ((sonyaGuardLeg and c2==4) or (sonyaLiuGuardLeg and c2==1) or (sonyaMileenaGuardLeg and c2==5) or (sonyaCageGuardLeg and c2==2) or (sonyaLaoGuardLeg and c2==0) or (sonyaScorpionGuardLeg and c2==10) or ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6)) or (sonyaSubGuardLeg and c2==8))
    local useRfp=(kitanaRfpDuck and c2==4) or (liuRfpDuck and c2==1) or nativeDuckCounter
    if useRfp then rapidPunch,punchesLeft,rfpRecovering,punchAnimation=cpuRapidPunch(proc2) end
    local neutralLegDistance=((sonyaMileenaLeg85 and target==18 and c2==5) or (sonyaCageGuardLeg and target==18 and c2==2) or (sonyaLaoGuardLeg and target==18 and c2==0) or (sonyaScorpionGuardLeg and target==18 and c2==10) or ((sonyaOwnGuardLeg and target==18 and (c2==17 or c2==18)) or (sonyaShangGuardLeg and target==18 and c2==6))) and 85 or 80
    local neutralLegWindow=target==18 and ((sonyaSubNeutralLeg and c2==8) or (sonyaMileenaGuardLeg and c2==5) or (sonyaCageGuardLeg and c2==2) or (sonyaLaoGuardLeg and c2==0) or (sonyaScorpionGuardLeg and c2==10) or ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6))) and not rapidPunch
      and distance<=neutralLegDistance and s16(proc2+0x200)-s16(b+0xb0)==0
      and (u16(proc2+0x210)&0x1c)==0 and (renderedHeight(b) or -1)>96
    if subzeroObservationLog and target==17 and c2==8 then
     -- Passive classification only: these locals never enter input decisions.
     local observedRapid,observedCount,observedRecovery,observedRoot=cpuRapidPunch(proc2)
     subzeroObservationLog:write(string.format('%d,%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',
      n,u16(proc2+0x210),u32(proc2+0xe0),observedRapid and 1 or 0,observedCount,
      observedRecovery and 1 or 0,observedRoot or 0,ownAction,enemyAction,
      u16(0x010602f0),u16(0x01060ec0),distance))
     if n%16==0 then subzeroObservationLog:flush() end
    end
    local usingKitanaLeg=false
    local usingRecoveryCounter=false
    local usingGuardLeg=false
    local usingLiuChoke=false
    local approachingSubzero=false
    local retreating=false
    local closeChokeMatch=target==17 and ((liuChoke and c2==1) or (subzeroChoke and c2==8))
    local closeChokeDistance=(subzeroApproach and c2==8) and 60 or 85
    if closeChokeMatch and
       (liuChokeStart or ((c2~=8 or not fanThreat) and not knifeGuardStart and height==0 and distance<=closeChokeDistance and
        (not subzeroNeutralChoke or c2~=8 or (not rapidPunch and distance<=80 and
         (u16(proc2+0x210)&0x1c)==0 and (renderedHeight(b) or -1)>96)) and
        n-liuChokeRetry>=100 and (u16(proc1+0x210)&0x1c)==0 and
        s16(proc2+0x200)-s16(b+0xb0)==0)) then
     usingLiuChoke=true;knifeGuardStart=nil;knifeGuardWait=false
     if not liuChokeStart then liuChokeStart=n;liuChokeRetry=n;liuChokeReady=false end
     local age=n-liuChokeStart
     local fastChoke=subzeroFastChoke and target==17 and c2==8
     local chokeBodyHeight,chokeButtonTable,chokeDuckTable=-1,0,0
     if fastChoke then
      chokeBodyHeight=renderedHeight(a) or -1
      chokeButtonTable=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
      chokeDuckTable=assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
     end
     -- Release guard until actual native stance, then use the independently
     -- verified D,F,LP timing. Cancel on reaction; never force an action.
     set('P1 Block',0);set(away,0)
     if (u16(proc1+0x210)&4)~=0 then liuChokeStart=nil
     elseif fastChoke and not liuChokeReady then
      -- Release Block while staying down until native duck input is restored.
      set('P1 Down',1)
      local duckReady=chokeBodyHeight>=0 and chokeBodyHeight<=96 and chokeButtonTable==chokeDuckTable
      if height==0 and (u16(proc1+0x210)&0x1c)==0 and (ownAction==0x303 or duckReady) then
       liuChokeReady=true;liuChokeStart=n;set('P1 Down',0)
      elseif age>=45 then liuChokeStart=nil end
     elseif not liuChokeReady then
      if height==0 and ownAction==0x303 then liuChokeReady=true;liuChokeStart=n;set('P1 Down',1)
      elseif age>=45 then liuChokeStart=nil end
     elseif fastChoke then
      -- One release field refreshes Down history, then verified 3/3/4 inputs.
      if age>=1 and age<4 then set('P1 Down',1)
      elseif age>=4 and age<7 then set(toward,1)
      elseif age>=7 and age<11 then set('P1 Low Punch',1)
      elseif age>=11 then liuChokeStart=nil end
     elseif age<3 then set('P1 Down',1)
     elseif age>=6 and age<9 then set(toward,1)
     elseif age>=12 and age<16 then set('P1 Low Punch',1)
     elseif age>=16 then liuChokeStart=nil end
     if fastChoke then
      fastChokeLog:write(string.format('%d,%d,%d,%d,%d,%d,%08x,%08x,%d,%d,%d,%d,%d\n',
       n,liuChokeStart and n-liuChokeStart or -1,ownAction,u16(proc1+0x210),height,
       chokeBodyHeight,chokeButtonTable,chokeDuckTable,distance,enemyAction,
       commands['P1 Down'] or 0,commands['P1 Block'] or 0,commands['P1 Low Punch'] or 0))
      if n%16==0 then fastChokeLog:flush() end
     end
    elseif sonyaKitanaLegCounter and target==18 and c2==4 and
       (kitanaLegStart or (height==0 and distance<=72 and n-kitanaLegRetry>=90 and
        s16(proc2+0x200)-s16(b+0xb0)==0 and (u16(proc1+0x210)&0x1c)==0 and
        (u16(proc2+0x210)&0x1c)==0 and not fanThreat and not pressureGuard and
        (ownAction==0x303 or ownAction==0x302 or ownAction==0x700 or ownAction==0x701))) then
     usingKitanaLeg=true;knifeGuardStart=nil;knifeGuardWait=false
     if not kitanaLegStart then kitanaLegStart=n;kitanaLegRetry=n end
     local age=n-kitanaLegStart
     if (u16(proc1+0x210)&4)~=0 then
      kitanaLegStart=nil;set('P1 Block',1);set(away,1)
     elseif age<4 then
      -- Neutral release before the tested block-first physical chord.
     elseif age<12 then
      set('P1 Down',1);set('P1 Block',1)
      if age>=8 then set('P1 Low Punch',1) end
     else kitanaLegStart=nil;set('P1 Block',1);set(away,1) end
    elseif guardLegMatch and
       (guardLegStart or ((rapidPunch and rfpRecovering or neutralLegWindow) and lowGuardFields>=4 and
        distance<=85 and height==0 and (u16(proc1+0x210)&0x1c)==0 and
        n-guardLegRetry>=90 and not fanThreat and not pressureGuard)) then
     usingGuardLeg=true;knifeGuardStart=nil;knifeGuardWait=false
     local bodyHeight=renderedHeight(a) or -1
     local phase='not-short'
     if not guardLegStart and bodyHeight>=0 and bodyHeight<=96 then guardLegStart=n;guardLegRetry=n end
     local age=guardLegStart and n-guardLegStart or 0
     set('P1 Down',1);set('P1 Block',1);set(away,1)
     if (u16(proc1+0x210)&4)~=0 then phase='cancelled';guardLegStart=nil
     elseif guardLegStart and age<4 then phase='chord';set('P1 Low Punch',1)
     elseif guardLegStart then phase='done';guardLegStart=nil end
     guardLegLog:write(string.format('%d,%s,%d,%d,%d,%d,%d,%d,%d,%d\n',
      n,phase,age,lowGuardFields,bodyHeight,u16(proc1+0x210),distance,
      commands['P1 Down'] or 0,commands['P1 Block'] or 0,commands['P1 Low Punch'] or 0))
     if n%16==0 then guardLegLog:flush() end
    elseif sonyaRecoveryCounter and target==18 and c2==4 and
       (recoveryCounterStart or (rapidPunch and rfpRecovering and distance<105 and
        height==0 and (u16(proc1+0x210)&0x1c)==0 and not fanThreat and not pressureGuard and
        n-subzeroCounterRetry>=12)) then
     usingRecoveryCounter=true;knifeGuardStart=nil;knifeGuardWait=false
     if not recoveryCounterStart then recoveryCounterStart=n end
     local age=n-recoveryCounterStart
     local phase='waiting'
     if age>=18 or height~=0 or distance>=110 or fanThreat or pressureGuard or
        (u16(proc1+0x210)&0x1c)~=0 then
      phase='cancelled';recoveryCounterStart=nil
      set('P1 Down',1);set('P1 Block',1);set(away,1)
     else
      -- Release block naturally, wait for installed attack dispatch, then HP.
      set('P1 Down',1);set('P1 Block',0);set(away,0)
      counterBodyHeight=renderedHeight(a) or -1
      counterButtonTable=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
      counterButtonsReady=counterButtonTable==assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
      if counterBodyHeight>=0 and counterBodyHeight<=96 and counterButtonsReady and
         (u16(proc1+0x210)&0x1c)==0 and n-subzeroCounterRetry>=12 then
       phase='fired'
       if sonyaRecoveryKick then set('P1 Low Kick',1) else set('P1 High Punch',1) end
       subzeroCounterRetry=n;recoveryCounterStart=nil
      end
     end
     recoveryCounterLog:write(string.format('%d,%s,%d,%d,%d,%d,%d,%d,%08x,%d,%d,%d,%d\n',
      n,phase,age,u16(0x010602f0),u16(0x01060ec0),distance,u16(proc1+0x210),
      counterBodyHeight,counterButtonTable,commands['P1 Down'] or 0,commands['P1 Block'] or 0,commands['P1 High Punch'] or 0,commands['P1 Low Kick'] or 0))
     if n%16==0 then recoveryCounterLog:flush() end
    elseif rapidPunch then
     knifeGuardStart=nil;knifeGuardWait=false;set(away,1)
     -- Native high and low RFP use roots13h and14h respectively. Do not
     -- treat the low-punch sequence as a high attack to duck underneath.
     if not rfpRecovering and punchesLeft>1 and punchAnimation==0x13 then
      set('P1 Down',1)
      local counterReady=ownAction==0x302
      local counterPulse=n%12<3
      if nativeDuckCounter then
       set(away,0)
       counterBodyHeight=renderedHeight(a) or -1
       counterButtonTable=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
       counterButtonsReady=counterButtonTable==assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
       counterReady=counterBodyHeight>=0 and counterBodyHeight<=96 and counterButtonsReady
       counterPulse=n-subzeroCounterRetry>=12
      end
      if counterReady and height==0 and distance<105 and
         (u16(proc1+0x210)&0x1c)==0 and counterPulse then
       set('P1 High Punch',1)
       if nativeDuckCounter then subzeroCounterRetry=n end
      end
     else
      set('P1 Block',1)
      if nativeDuckCounter then set('P1 Down',1) end
     end
    elseif fanThreat or pressureGuard then
     knifeGuardStart=nil;knifeGuardWait=false
     set('P1 Block',1);set(away,1)
     if distance>=120 or ((subzeroGuard or sonyaSubGuardLeg) and c2==8) or (sonyaMileenaGuardLeg and c2==5) or (sonyaCageGuardLeg and c2==2) or (sonyaLaoGuardLeg and c2==0) or (sonyaScorpionGuardLeg and c2==10) or ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6)) then set('P1 Down',1) end
    elseif subzeroApproach and target==17 and c2==8 and not knifeGuardStart and
       height==0 and distance>60 and distance<=100 and
       (u16(proc1+0x210)&0x1c)==0 and s16(proc2+0x200)-s16(b+0xb0)==0 then
     approachingSubzero=true
     -- Short physical walks between guarded intervals; never move an object.
     if n%(subzeroWalkFields+12)<subzeroWalkFields then set('P1 Down',0);set('P1 Block',0);set(away,0);set(toward,1)
     else set('P1 Down',1);set('P1 Block',1);set(away,1) end
    elseif knifeGuardStart then
     local age=n-knifeGuardStart
     if knifeGuardWait then
      if height==0 and ownAction==0x303 then
       knifeGuardWait=false;knifeGuardStart=n;set('P1 Down',1)
      elseif age>=45 then knifeGuardStart=nil;knifeGuardWait=false end
     elseif age<3 then set('P1 Down',1)
     elseif age<6 then set(target==18 and toward or away,1)
     elseif age<9 then set(target==18 and 'P1 Low Punch' or 'P1 High Punch',1)
     else knifeGuardStart=nil;set('P1 Down',1);set('P1 Block',1) end
    elseif liuRetreat and target==17 and c2==1 and height==0 and distance<220 and
       (u16(proc1+0x210)&0x1c)==0 and n>=retreatUntil then
     -- Physical backup only when not processing a command or native threat.
     retreating=true
     retreatLastX=x1;retreatLastFrame=n
     set(away,1)
    elseif height==0 and n-knifeGuardRetry>=knifeInterval and
       not (sonyaMileenaNoRing and target==18 and c2==5) and
       (not sonyaKitanaLegCounter or target~=18 or c2~=4 or distance>=120) and
       (not useRfp or distance>=120) and
       not (subzeroCrouchReady and target==17 and c2==8 and distance<=180) and
       (ownAction==0x303 or ownAction==0x302 or ownAction==0x700 or ownAction==0x701 or
        (kitanaReadyKnife and guardWake and u32(proc1+0xe0)==guardWake)) then
     knifeGuardStart=n;knifeGuardRetry=n;knifeGuardWait=kitanaReadyKnife
     if not knifeGuardWait then set('P1 Down',1) end
    else set('P1 Down',1);set('P1 Block',1) end
    if kitanaReadyKnife and not knifeGuardStart and not usingKitanaLeg and not usingLiuChoke and not fanThreat and not pressureGuard and not rapidPunch and not retreating and not approachingSubzero and not usingRecoveryCounter and not usingGuardLeg then
     if distance<120 and not ((subzeroGuard or sonyaSubGuardLeg) and c2==8) and not (sonyaMileenaGuardLeg and c2==5) and not (sonyaCageGuardLeg and c2==2) and not (sonyaLaoGuardLeg and c2==0) and not (sonyaScorpionGuardLeg and c2==10) and not ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6)) then set('P1 Down',0) end
     set(away,1);set('P1 Block',1)
    end
    if subzeroCrouchReady and target==17 and c2==8 and distance<=180 and
       height==0 and (u16(proc1+0x210)&0x1c)==0 and not rapidPunch and
       not fanThreat and not pressureGuard and not knifeGuardStart and not usingLiuChoke then
     -- Establish native duck buttons before the high-RFP counter window.
     -- Detected ice/slide/projectile and low-RFP guards retain precedence.
     set('P1 Down',1);set('P1 Block',0);set(away,0)
    end
    if rfpLog and rapidPunch then
     rfpLog:write(string.format('%d,%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%d\n',n,punchesLeft,
      u32(proc2+0xe0),u16(0x010602f0),u16(0x01060ec0),distance,
      commands['P1 Down'] or 0,commands['P1 Block'] or 0,rfpRecovering and 1 or 0,
      commands['P1 High Punch'] or 0,punchAnimation or 0,counterBodyHeight,u16(proc1+0x210),counterButtonTable,counterButtonsReady and 1 or 0))
     if n%16==0 then rfpLog:flush() end
    end
   elseif femaleCounter and ((target==17 and c2==4) or (target==18 and (c2==4 or c2==5))) then
    plan=nil
    local height=s16(proc1+0x200)-s16(a+0xb0)
    local enemyHeight=enemyGround-enemyY
    local profile=continuesUsed%3
    if counterForward then profile=0 end
    local ownAction=u16(proc1+0x1f0)
    if counterTakeoff and (ownAction==0x308 or ownAction==0x30b) and
       counterPreviousAction~=0x308 and counterPreviousAction~=0x30b then
     counterAir=n;counterPrepare=nil
    end
    counterPreviousAction=ownAction
    -- Each paid continue explicitly changes the physical control strategy.
    -- No AI, difficulty, position, action or health writes are involved.
    if counterTakeoff and (counterPrepare or height~=0 or counterAir) then
     -- Release duck/block before asking to jump. Kick timing starts only
     -- after an observed native jump action, never on a mere Up request.
     if counterPrepare then
      local age=n-counterPrepare
      if age>=9 and age<15 then set('P1 Up',1);set(profile==1 and distance<200 and away or toward,1) end
      if age>=35 then counterPrepare=nil;counterJump=n end
     elseif counterAir then
      local age=n-counterAir
      if height==0 and ownAction~=0x308 and ownAction~=0x30b then counterAir=nil;counterJump=n
      else
       set(profile==1 and away or toward,1)
       if age>=16 and age<=21 and (ownAction==0x308 or ownAction==0x30b) then set('P1 High Kick',1) end
      end
     end
    elseif height>8 then
     if n-counterJump>=18 and n-counterJump<=23 then set('P1 High Kick',1) end
     if profile==1 then set(away,1) else set(toward,1) end
    elseif enemyHeight>18 and distance<110 then
     set('P1 Down',1)
     if combat%20<4 then set('P1 High Punch',1) else set('P1 Block',1) end
    elseif profile==2 then
     set('P1 Down',1)
     if distance<85 and combat%28<4 then set('P1 High Punch',1)
     else set('P1 Block',1) end
    elseif distance<100 and profile==0 then
     if n-counterSweep>=24 then counterSweep=n end
     if n-counterSweep<5 then set(away,1);set('P1 Low Kick',1)
     else set('P1 Down',1);set('P1 Block',1) end
    elseif counterTakeoff and n-counterJump>=48 and height==0 and
       (ownAction==0x303 or ownAction==0x302 or ownAction==0x700 or ownAction==0x701) then
     counterPrepare=n
    elseif not counterTakeoff and n-counterJump>=48 then
     counterJump=n
     set('P1 Up',1)
     set(profile==1 and distance<200 and away or toward,1)
    elseif not counterTakeoff and n-counterJump<3 then
     set('P1 Up',1);set(profile==1 and distance<200 and away or toward,1)
    else set('P1 Down',1);set('P1 Block',1) end
   elseif rosterGuard and ((target==17 and c2==4) or (target==18 and (c2==4 or c2==5))) then
    plan=nil
    if n-guardLast>1 then guardPlan=nil;guardRetry=-1000;guardUntil=-1000 end
    guardLast=n
    local ownAction=u16(proc1+0x1f0)
    local enemyAction=u16(proc2+0x1f0)
    local height=s16(proc1+0x200)-s16(a+0xb0)
    local cpuHeight=enemyGround-enemyY
    local ready=height<=8 and (ownAction==0 or ownAction==0x303 or ownAction==0x302 or ownAction==0x304 or ownAction==0x700 or ownAction==0x701)
    local safe=enemyAction==0 or enemyAction==0x303 or enemyAction==0x302 or enemyAction==0x304 or enemyAction==0x700 or enemyAction==0x701 or (enemyAction>=0x600 and enemyAction<=0x61b)
    if enemyAction==4 or enemyAction==8 or enemyAction==10 or enemyAction==16 then guardUntil=n+32 end
    if guardPlan and n-guardStart<12 then
     local age=n-guardStart
     if guardPlan=='leg' then
      if age<7 then set('P1 Down',1) end
      if age>=3 and age<7 then set('P1 Low Punch',1);set('P1 Block',1) end
     else
      if age<3 then set('P1 Down',1)
      elseif age<6 then set(toward,1)
      elseif age<9 then set('P1 High Punch',1) end
     end
    elseif height>8 then set('P1 Block',1);if backGuard then set(away,1) end
    elseif cpuHeight>15 and distance<100 then
     set('P1 Down',1)
     if ready and combat%26<3 then set('P1 High Punch',1) else set('P1 Block',1);if backGuard then set(away,1) end end
    elseif n<guardUntil or (not safe and distance<125) then set('P1 Down',1);set('P1 Block',1);if backGuard then set(away,1) end
    elseif ready and safe and cpuHeight<=8 and distance<95 and n-guardRetry>=40 then
     guardPlan=target==18 and 'leg' or 'blade';guardStart=n;guardRetry=n;set('P1 Down',1)
    elseif ready and safe and distance>85 and cpuHeight<=8 then set(toward,1)
    else set('P1 Down',1);set('P1 Block',1);if backGuard then set(away,1) end end
   elseif jaxReactive and c2==11 and target==18 then
    plan=nil
    local ownY=s16(a+0xb0);local ownGround=s16(proc1+0x200)
    local ownAction=u16(proc1+0x1f0)
    local enemyAction=u16(proc2+0x1f0)
    if enemyAction==0x137 then jaxPoundUntil=n+40 end
    local height=ownGround-ownY
    local ready=height<=8 and (ownAction==0 or ownAction==0x303 or ownAction==0x302 or ownAction==0x304 or ownAction==0x700 or ownAction==0x701)
    if n<jaxPoundUntil and height<=8 then
     if n-jaxJump>=4 then jaxJump=n end
     if n-jaxJump<3 then set('P1 Up',1);set(away,1) end
    elseif height>8 then set(away,1)
    elseif n-jaxLeg<12 then
     local age=n-jaxLeg
     if age<7 then set('P1 Down',1) end
     if age>=3 and age<7 then set('P1 Low Punch',1);set('P1 Block',1) end
    elseif ready and enemyGround-enemyY<=8 and distance<95 and n-jaxLeg>=48 then
     jaxLeg=n;set('P1 Down',1)
    elseif ready and distance>85 and enemyGround-enemyY<=8 then set(toward,1)
    else set('P1 Block',1) end
   elseif defensive and combat<defenseUntil then
    set('P1 Down',1);set('P1 Block',1)
   elseif subBallRecovery.kintaroRecovery and target==17 and c2==12 then
    plan=nil;set('P1 Down',1);set('P1 Block',1)
    subBallRecovery.bossRecovering=nativeRoutineActive(proc2,assert(tonumber(os.getenv('KS_KINTARO_RECOVERY_BEGIN'))),
     assert(tonumber(os.getenv('KS_KINTARO_RECOVERY_END'))))
    subBallRecovery.readyBody=renderedHeight(a) or 999
    subBallRecovery.readyButton=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
    subBallRecovery.readyDuck=assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
    subBallRecovery.readyPhase='guard'
    if s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 then
     if n-subBallRecovery.bossPunishAt<3 then
      set('P1 Block',0);set('P1 High Punch',1);subBallRecovery.readyPhase='pulse'
     elseif subBallRecovery.kintaroRecoveryApproach and subBallRecovery.bossRecovering and
        distance>104 and distance<=180 and s16(proc2+0x200)==s16(b+0xb0) and not cpuProjectileActive() then
      set('P1 Down',0);set('P1 Block',0);set(toward,1);subBallRecovery.readyPhase='approach'
     elseif subBallRecovery.bossRecovering and distance<=104 and s16(proc2+0x200)==s16(b+0xb0) and not cpuProjectileActive() then
      set('P1 Block',0);subBallRecovery.readyPhase='prepare'
      if subBallRecovery.readyBody<=96 and subBallRecovery.readyButton==subBallRecovery.readyDuck and n-subBallRecovery.bossPunishAt>=6 then
       set('P1 High Punch',1);subBallRecovery.bossPunishAt=n;subBallRecovery.readyPhase='fire'
      end
     end
    end
    subBallRecovery.recoveryLog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,%d,%d,%08x,%d,%d,%d\n',
     n,u16(proc1+0x1f0),u16(proc1+0x210),s16(proc1+0x200)-s16(a+0xb0),subBallRecovery.readyBody,
     subBallRecovery.readyButton,subBallRecovery.readyDuck,distance,u16(proc2+0x1f0),s16(proc2+0x200)-s16(b+0xb0),
     subBallRecovery.readyPhase,commands['P1 High Punch'] or 0,u16(0x010602f0),u16(0x01060ec0),
     subBallRecovery.bossRecovering and 1 or 0,u32(proc2+0xe0),commands[toward] or 0,
     commands['P1 Down'] or 0,commands['P1 Block'] or 0));subBallRecovery.recoveryLog:flush()
   elseif subBallRecovery.kintaroVertical and target==17 and c2==12 and not plan then
    subBallRecovery.verticalDecision='wait'
    subBallRecovery.verticalBody=renderedHeight(a) or -1
    subBallRecovery.verticalButtons=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
    subBallRecovery.verticalStance=assert(tonumber(os.getenv('KS_CAMPAIGN_STANCE_BUTTONS')))
    if s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 then
     if cpuProjectileActive() then set('P1 Down',1);set('P1 Block',1);subBallRecovery.verticalDecision='guard'
     elseif distance>115 then set(toward,1);subBallRecovery.verticalDecision='approach'
     elseif u16(proc1+0x1f0)==0x303 and subBallRecovery.verticalBody>=120 and
        subBallRecovery.verticalButtons==subBallRecovery.verticalStance then
      plan='upkick';planAge=0;planToward=toward;subBallRecovery.verticalDecision='upkick'
     end
    else set('P1 Block',1) end
    subBallRecovery.verticalLog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,%d\n',n,distance,
     u16(proc1+0x1f0),u16(proc1+0x210),s16(proc1+0x200)-s16(a+0xb0),subBallRecovery.verticalBody,
     subBallRecovery.verticalButtons,subBallRecovery.verticalStance,subBallRecovery.verticalDecision,
     u16(0x010602f0),u16(0x01060ec0),subBallRecovery.verticalAttackAge));subBallRecovery.verticalLog:flush()
   elseif subBallRecovery.kintaroVaried and target==17 and c2==12 and not plan then
    if combat<3 then subBallRecovery.variedRetreatSince=nil;subBallRecovery.variedRetreating=false;subBallRecovery.lastPunchRetreat=false end
    subBallRecovery.variedHistory={};subBallRecovery.variedKicks=0;subBallRecovery.variedPunches=0
    for index=0,5 do
     subBallRecovery.variedHistory[index+1]=u16(assert(tonumber(os.getenv('KS_CAMPAIGN_BOSS_HITQ')))+index*16)
     if subBallRecovery.variedHistory[index+1]==0x200 then subBallRecovery.variedKicks=subBallRecovery.variedKicks+1 end
     if subBallRecovery.variedHistory[index+1]==0x201 then subBallRecovery.variedPunches=subBallRecovery.variedPunches+1 end
    end
    subBallRecovery.variedWanted=subBallRecovery.variedKicks<2 and 'mixkick' or
     (subBallRecovery.variedPunches<2 and 'mixpunch' or 'readyknife')
    if subBallRecovery.kintaroVariedFinish and not subBallRecovery.kintaroVariedFinishUpper and u16(0x01060ec0)<=13 then subBallRecovery.variedWanted='mixkick' end
    subBallRecovery.variedDecision='wait'
    if s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 then
     if cpuProjectileActive() then set('P1 Down',1);set('P1 Block',1);subBallRecovery.variedDecision='guard'
     elseif (subBallRecovery.kintaroVariedCounter and (distance<=104 or n-subBallRecovery.uppercutAt<3)) or
        (subBallRecovery.kintaroVariedFinishUpper and u16(0x01060ec0)<=subBallRecovery.finishUpperThreshold) then
      set('P1 Down',1);subBallRecovery.variedDecision='close_duck'
      subBallRecovery.readyBody=renderedHeight(a) or 999
      subBallRecovery.readyButton=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
      subBallRecovery.readyDuck=assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
      subBallRecovery.readyPhase='duck'
      if n-subBallRecovery.uppercutAt<3 then
       set('P1 High Punch',1);subBallRecovery.readyPhase='pulse'
      elseif distance<=104 and s16(proc2+0x200)==s16(b+0xb0) and
         n-subBallRecovery.uppercutAt>=6 and subBallRecovery.readyBody<=96 and
         subBallRecovery.readyButton==subBallRecovery.readyDuck then
       set('P1 High Punch',1);subBallRecovery.uppercutAt=n;subBallRecovery.readyPhase='fire'
      end
      subBallRecovery.readyLog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,%d\n',
       n,u16(proc1+0x1f0),u16(proc1+0x210),s16(proc1+0x200)-s16(a+0xb0),subBallRecovery.readyBody,
       subBallRecovery.readyButton,subBallRecovery.readyDuck,distance,u16(proc2+0x1f0),s16(proc2+0x200)-s16(b+0xb0),
       subBallRecovery.readyPhase,commands['P1 High Punch'] or 0,u16(0x010602f0),u16(0x01060ec0)));subBallRecovery.readyLog:flush()
     elseif subBallRecovery.kintaroVariedFinish and subBallRecovery.variedWanted=='readyknife' and
        distance<subBallRecovery.knifeClearance and (subBallRecovery.knifeClearance==175 or
        not subBallRecovery.variedRetreatSince or n-subBallRecovery.variedRetreatSince<48) then
      subBallRecovery.variedRetreatSince=subBallRecovery.variedRetreatSince or n
      set(away,1);subBallRecovery.variedDecision='retreat'
     elseif not subBallRecovery.kintaroVariedFinish and (distance<175 or (subBallRecovery.variedRetreating and distance<220)) and
        (not subBallRecovery.variedRetreatSince or n-subBallRecovery.variedRetreatSince<48) then
      subBallRecovery.variedRetreatSince=subBallRecovery.variedRetreatSince or n
      subBallRecovery.variedRetreating=true;set(away,1);subBallRecovery.variedDecision='retreat'
     elseif subBallRecovery.variedWanted~='readyknife' and distance>260 then set(toward,1);subBallRecovery.variedDecision='approach'
     elseif subBallRecovery.variedWanted=='readyknife' and n-subBallRecovery.bossShotAt<48 then set('P1 Block',1);subBallRecovery.variedDecision='cooldown'
     elseif u16(proc1+0x1f0)==0x303 and (renderedHeight(a) or -1)>=120 and
        u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))==assert(tonumber(os.getenv('KS_CAMPAIGN_STANCE_BUTTONS'))) then
      subBallRecovery.variedRetreating=false
      subBallRecovery.variedRetreatSince=nil
      plan=subBallRecovery.variedWanted;planAge=0;planToward=plan=='readyknife' and away or toward
      if subBallRecovery.punchRetreatHop then
       local retreat=plan=='mixpunch' and distance<175 and not subBallRecovery.lastPunchRetreat
       if retreat then planToward=away end
       if plan~='readyknife' then subBallRecovery.lastPunchRetreat=retreat end
       subBallRecovery.hopLog:write(string.format('%d,%s,%d,%s,%s,%s,%d,%d,%d\n',
        n,plan,distance,planToward,away,toward,retreat and 1 or 0,u16(0x010602f0),u16(0x01060ec0)))
       subBallRecovery.hopLog:flush()
      end
      subBallRecovery.variedRequestAt=n;subBallRecovery.reactiveAirAt=nil
      subBallRecovery.variedAirAttackAge=subBallRecovery.kintaroVariedAdaptive and
       math.max(10,math.min(28,math.floor((distance-80)/4))) or subBallRecovery.fixedAirAge
      subBallRecovery.variedDecision=plan
      if plan=='readyknife' then subBallRecovery.bossShotAt=n end
     end
    else set('P1 Block',1) end
    subBallRecovery.variedLog:write(string.format('%d,%04x:%04x:%04x:%04x:%04x:%04x,%d,%d,%d,%d,%d,%d,%s,%d,%d,%d\n',
     n,subBallRecovery.variedHistory[1],subBallRecovery.variedHistory[2],subBallRecovery.variedHistory[3],
     subBallRecovery.variedHistory[4],subBallRecovery.variedHistory[5],subBallRecovery.variedHistory[6],
     subBallRecovery.variedKicks,subBallRecovery.variedPunches,distance,u16(proc1+0x1f0),u16(proc1+0x210),
     s16(proc1+0x200)-s16(a+0xb0),subBallRecovery.variedDecision,u16(0x010602f0),u16(0x01060ec0),subBallRecovery.variedAirAttackAge or 28))
    subBallRecovery.variedLog:flush()
   elseif subBallRecovery.kintaroRetreatBall and target==17 and c2==12 and not plan and
      not (subBallRecovery.kintaroBallFinishKnife and u16(0x01060ec0)<=50) then
    plan=nil
    subBallRecovery.bossBallPhase='wait'
    subBallRecovery.bossBallAge=subBallRecovery.bossBallStart and n-subBallRecovery.bossBallStart or -1
    if (u16(proc1+0x210)&0x1c)~=0 or n-subBallRecovery.bossBallAt<24 then
     subBallRecovery.bossBallStart=nil;set('P1 Block',1)
    else
     if not subBallRecovery.bossBallStart then subBallRecovery.bossBallStart=n end
     subBallRecovery.bossBallAge=n-subBallRecovery.bossBallStart
     set('P1 Low Kick',1)
     if subBallRecovery.bossBallAge<88 then
      subBallRecovery.bossBallPhase='charge';set(away,1)
      if distance<160 and s16(proc1+0x200)==s16(a+0xb0) then set('P1 Up',1) end
     elseif s16(proc1+0x200)==s16(a+0xb0) then
      -- Release direction/Block first; never manufacture native stance.
      subBallRecovery.bossBallPhase='stand_wait'
      if u16(proc1+0x1f0)==0x303 and (renderedHeight(a) or -1)>=120 and
         u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))==
         assert(tonumber(os.getenv('KS_CAMPAIGN_STANCE_BUTTONS'))) then
       set('P1 Low Kick',0);subBallRecovery.bossBallAt=n;subBallRecovery.bossBallStart=nil
       subBallRecovery.bossBallPhase='release'
      end
     else subBallRecovery.bossBallPhase='land_wait' end
    end
    subBallRecovery.bossBallLog:write(string.format('%d,%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',
     n,subBallRecovery.bossBallAge,subBallRecovery.bossBallPhase,u16(proc1+0x1f0),u16(proc1+0x210),
     s16(proc1+0x200)-s16(a+0xb0),distance,u16(0x010602f0),u16(0x01060ec0),
     commands['P1 Low Kick'] or 0,commands['P1 Up'] or 0,commands[away] or 0))
    subBallRecovery.bossBallLog:flush()
   elseif subBallRecovery.kintaroShortKick and target==17 and c2==12 then
    -- Physical standing HK only: no altered strike data or recovery cancellation.
    plan=nil
    if s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 then
     if cpuProjectileActive() then set('P1 Block',1)
     elseif distance<85 then set(away,1)
     elseif distance>135 then set('P1 Block',1)
     elseif n-subBallRecovery.shortKickAt<3 then set('P1 High Kick',1)
     elseif distance<=120 and n-subBallRecovery.shortKickAt>=12 and
        u16(proc1+0x1f0)==0x303 and (renderedHeight(a) or -1)>=120 and
        u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))==
        assert(tonumber(os.getenv('KS_CAMPAIGN_STANCE_BUTTONS'))) then
      set('P1 High Kick',1);subBallRecovery.shortKickAt=n
     end
    else set('P1 Block',1) end
   elseif subBallRecovery.kintaroReady and target==17 and c2==12 and not plan then
    set('P1 Down',1)
    subBallRecovery.readyBody=renderedHeight(a) or 999
    subBallRecovery.readyButton=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
    subBallRecovery.readyDuck=assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS')))
    subBallRecovery.readyPhase='duck'
    if cpuProjectileActive() then set('P1 Block',1);subBallRecovery.readyPhase='guard'
    elseif n-subBallRecovery.uppercutAt<3 and s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&4)==0 then
     set('P1 High Punch',1);subBallRecovery.readyPhase='pulse'
    elseif distance<=subBallRecovery.readyRange and s16(proc2+0x200)==s16(b+0xb0) and
       s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 and
       n-subBallRecovery.uppercutAt>=6 and subBallRecovery.readyBody<=96 and
       subBallRecovery.readyButton==subBallRecovery.readyDuck then
     set('P1 High Punch',1);subBallRecovery.uppercutAt=n;subBallRecovery.readyPhase='fire'
    end
    subBallRecovery.readyLog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,%d\n',
     n,u16(proc1+0x1f0),u16(proc1+0x210),s16(proc1+0x200)-s16(a+0xb0),subBallRecovery.readyBody,
     subBallRecovery.readyButton,subBallRecovery.readyDuck,distance,u16(proc2+0x1f0),s16(proc2+0x200)-s16(b+0xb0),
     subBallRecovery.readyPhase,commands['P1 High Punch'] or 0,u16(0x010602f0),u16(0x01060ec0)));subBallRecovery.readyLog:flush()
   elseif (subBallRecovery.kintaroKnifeReady or
      (subBallRecovery.kintaroBallFinishKnife and u16(0x01060ec0)<=50)) and target==17 and c2==12 and not plan then
    if subBallRecovery.kintaroBallFinishKnife then subBallRecovery.bossBallStart=nil end
    subBallRecovery.knifeBody=renderedHeight(a) or -1
    subBallRecovery.knifeButtons=u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))
    subBallRecovery.knifeStance=assert(tonumber(os.getenv('KS_CAMPAIGN_STANCE_BUTTONS')))
    subBallRecovery.knifePhase='stand_wait'
    if s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 then
     if distance<175 then
      set(away,1);subBallRecovery.knifeReadySince=nil;subBallRecovery.knifePhase='retreat'
     elseif cpuProjectileActive() or n-subBallRecovery.bossShotAt<48 then
      set('P1 Down',1);set('P1 Block',1);subBallRecovery.knifeReadySince=nil;subBallRecovery.knifePhase='guard'
     elseif u16(proc1+0x1f0)==0x303 and subBallRecovery.knifeBody>=120 and
        subBallRecovery.knifeButtons==subBallRecovery.knifeStance then
      if not subBallRecovery.knifeReadySince then subBallRecovery.knifeReadySince=n end
      if n-subBallRecovery.knifeReadySince>=4 then
       plan='readyknife';planAge=0;planToward=away;subBallRecovery.bossShotAt=n
       subBallRecovery.knifeReadySince=nil;subBallRecovery.knifePhase='fire'
      end
     else subBallRecovery.knifeReadySince=nil end
    else
     set('P1 Block',1);subBallRecovery.knifeReadySince=nil;subBallRecovery.knifePhase='unavailable'
    end
    subBallRecovery.knifeReadyLog:write(string.format('%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',n,
     subBallRecovery.knifePhase,u16(proc1+0x1f0),u16(proc1+0x210),s16(proc1+0x200)-s16(a+0xb0),
     subBallRecovery.knifeBody,subBallRecovery.knifeButtons,subBallRecovery.knifeStance,distance,
     u16(0x010602f0),u16(0x01060ec0)));subBallRecovery.knifeReadyLog:flush()
   elseif (subBallRecovery.kintaroKnife or subBallRecovery.kintaroMixed) and target==17 and c2==12 and not plan then
    -- Stay outside native close counters and issue the existing D,B,HP plan.
    if subBallRecovery.kintaroMixed and n-subBallRecovery.uppercutAt<3 and
       s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&4)==0 then
     set('P1 Down',1);set('P1 High Punch',1)
    elseif cpuProjectileActive() then set('P1 Down',1);set('P1 Block',1)
    elseif s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 then
     if subBallRecovery.kintaroMixed and distance<175 then
      set('P1 Down',1)
      if subBallRecovery.kintaroMixedGuard and distance>115 then set('P1 Block',1) end
      if distance<=115 and s16(proc2+0x200)==s16(b+0xb0) and n-subBallRecovery.uppercutAt>=24 and
         (renderedHeight(a) or 999)<=96 and
         u32(assert(tonumber(os.getenv('KS_CAMPAIGN_P1_BUTTONS'))))==assert(tonumber(os.getenv('KS_CAMPAIGN_DUCK_BUTTONS'))) then
       set('P1 High Punch',1);subBallRecovery.uppercutAt=n
      end
     elseif subBallRecovery.kintaroKnifeMidrange and distance<175 then set(away,1);set('P1 Block',0)
     elseif not subBallRecovery.kintaroKnifeMidrange and not subBallRecovery.kintaroMixed and distance<260 then set(away,1);set('P1 Block',0)
     elseif n-subBallRecovery.bossShotAt<(subBallRecovery.kintaroKnifeMidrange and 48 or 80) then set('P1 Down',1);set('P1 Block',1)
     elseif u16(proc1+0x1f0)==0x303 and (renderedHeight(a) or -1)>=96 then
      plan='knife';planAge=0;planToward=away;subBallRecovery.bossShotAt=n
     end
    else set('P1 Block',1) end
   elseif subBallRecovery.kintaroBlade and target==17 and c2==12 and not plan then
    -- Existing native Blade command; never change its range or boss AI.
    if s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 then
     if distance<175 then set(away,1);set('P1 Block',0)
     elseif distance>240 then set('P1 Block',1)
     elseif u16(proc1+0x1f0)==0x303 and (renderedHeight(a) or -1)>=96 and n-subBallRecovery.bladeAt>=80 then
      plan='blade';planAge=0;planToward=toward;subBallRecovery.bladeAt=n
     end
    else set('P1 Block',1) end
   elseif subBallRecovery.kintaroJumpkick and target==17 and c2==12 and not plan then
    -- Physical plan only. Early native stomp evasion above retains priority.
    if s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0 then
     if distance>260 then set(toward,1)
     else plan='jumpkick';planAge=0;planToward=toward end
    else set('P1 Block',1) end
   elseif plan then
    planAge=planAge+1
    if plan=='leg' then
     if planAge<=5 then set('P1 Down',1);set('P1 Block',1) end
     if planAge>=3 and planAge<=5 then set('P1 Low Punch',1) end
    elseif plan=='choke' or plan=='ring' then
     if planAge<=3 then set('P1 Down',1)
     elseif planAge<=6 then set(planToward,1)
     elseif planAge<=9 then set('P1 Low Punch',1) end
    elseif plan=='readyknife' then
     if planAge<=3 then set('P1 Down',1)
     elseif planAge>=7 and planAge<=9 then set(planToward,1)
     elseif planAge>=13 and planAge<=15 then set('P1 High Punch',1) end
    elseif plan=='knife' or plan=='blade' then
     if planAge<=3 then set('P1 Down',1)
     elseif planAge<=6 then set(planToward,1)
     elseif planAge<=9 then set('P1 High Punch',1) end
     if knifeGuard and c2==11 and plan=='knife' and planAge>9 then
      set('P1 Down',1);set('P1 Block',1)
     end
    elseif plan=='upkick' then
     if planAge<=3 then set('P1 Up',1) end
     if planAge>=subBallRecovery.verticalAttackAge and planAge<=subBallRecovery.verticalAttackAge+3 then set('P1 High Kick',1) end
    elseif plan=='mixkick' or plan=='mixpunch' then
     if planAge<=3 then set('P1 Up',1);set(planToward,1) end
     if subBallRecovery.kintaroVariedReactive then
      subBallRecovery.reactiveWindup=nativeRoutineActive(proc2,assert(tonumber(os.getenv('KS_KINTARO_UPPERCUT_BEGIN'))),
       assert(tonumber(os.getenv('KS_KINTARO_UPPERCUT_END'))))
      if not subBallRecovery.reactiveAirAt and ((planAge>=6 and subBallRecovery.reactiveWindup) or planAge>=28) then
       subBallRecovery.reactiveAirAt=planAge
      end
      if subBallRecovery.reactiveAirAt and planAge>=subBallRecovery.reactiveAirAt and planAge<=subBallRecovery.reactiveAirAt+3 then
       set(plan=='mixkick' and 'P1 High Kick' or 'P1 High Punch',1)
      end
      subBallRecovery.airTimingLog:write(string.format('%d,%d,%s,%d,%d,%d,%d,%d,%d\n',n,subBallRecovery.variedRequestAt,
       plan,planAge,subBallRecovery.reactiveWindup and 1 or 0,s16(proc1+0x200)-s16(a+0xb0),
       subBallRecovery.reactiveAirAt or -1,commands['P1 High Punch'] or 0,commands['P1 High Kick'] or 0));subBallRecovery.airTimingLog:flush()
     elseif planAge>=(subBallRecovery.variedAirAttackAge or 28) and planAge<=(subBallRecovery.variedAirAttackAge or 28)+3 then
      set(plan=='mixkick' and 'P1 High Kick' or 'P1 High Punch',1)
     end
    elseif plan=='jumpkick' then
     if planAge<=3 then set('P1 Up',1);set(planToward,1) end
     local kickAt=kickOverride or ((style=='latekick' or style=='sweepjump') and 22 or 10)
     if planAge>=kickAt and planAge<=kickAt+4 then set('P1 High Kick',1) end
     if defensive and planAge>kickAt+4 then set('P1 Block',1) end
    elseif plan=='square' then
     if planAge<=3 then set(planToward,1)
     elseif planAge<=6 then set(planToward=='P1 Right' and 'P1 Left' or 'P1 Right',1)
     elseif planAge<=9 then set('P1 High Punch',1) end
    elseif plan=='throw' then
     if planAge>=4 and planAge<=7 then set('P1 Low Punch',1) end
    elseif plan=='sweep' then
     -- Release crouch/block before Back+LK; do not cancel the command into
     -- duck block on the next global phase tick.
     if planAge>=4 and planAge<=7 then
      set(planToward,1);set('P1 Low Kick',1)
     end
    elseif plan=='ball' then
     -- Ordinary held-LK command, with a physical block during charging.
     -- Release block first, then LK after the native >50h-tick threshold.
     if liuBall and c2==1 then
      -- restricted_xfer rejects reacting/sitduck/special flags even when
      -- the action tag still says block. Hold charge until eligible, and
      -- recheck after lowering guard before emitting the release edge.
      local eligible=s16(proc1+0x200)==s16(a+0xb0) and (u16(proc1+0x210)&0x1c)==0
      if planAge>85 and not liuBallReleased then
       if not liuBallRelease and eligible then liuBallRelease=planAge+4
       elseif liuBallRelease and planAge>=liuBallRelease then
        if eligible then liuBallReleased=true else liuBallRelease=nil end
       end
      end
      if not liuBallReleased then
       set('P1 Low Kick',1);set(away,1)
       if not liuBallRelease then set('P1 Block',1) end
      end
     else
      if planAge<=81 then set('P1 Block',1) end
      if planAge<=85 then set('P1 Low Kick',1) end
     end
    end
    local ownAction=proc1~=0 and u16(proc1+0x1f0) or 0
    local limit=plan=='jumpkick' and 48 or (plan=='sweep' and 32 or (plan=='ball' and (liuBall and c2==1 and 300 or 150) or 85))
    if knifeGuard and c2==11 and plan=='knife' then limit=60 end
    local released=plan~='ball' or (liuBall and c2==1 and liuBallReleased) or (not (liuBall and c2==1) and planAge>90)
    if planAge>=limit or (released and planAge>=16 and ownAction==0x303) then plan=nil end
    if jaxSafeRing and c2==11 and target==18 and planAge>9 then
     set('P1 Down',1);set('P1 Block',1)
    end
   elseif distance<110 and enemyY+20<enemyGround then
    set('P1 Down',1);set('P1 High Punch',combat%12<3 and 1 or 0)
   elseif (style=='uppercut' or ((style=='jumpkick' or style=='ball' or style=='retreatkick' or style=='latekick' or style=='sweepjump' or style=='reptilegrapple' or style=='jumpgrapple') and c2~=9 and (style~='jumpgrapple' or c2~=11))) and not (liuBall and c2==1 and target==17) and not (raidenJump and c2==7) and not (kitanaJump and c2==4) and not (raidenKnife and c2==7 and target==17) and not (subzeroKnife and c2==8 and target==17) and not (femaleZoning and (c2==4 or c2==5)) then
    -- Stay under high projectiles and let the CPU enter uppercut range.
    set('P1 Down',1)
    if distance<115 then
     local interval=(subBallRecovery.kintaroFastPulse and target==17 and c2==12) and 12 or 24
     set('P1 High Punch',combat%interval<3 and 1 or 0)
    end
   elseif style=='jumpkick' and distance>110 then
    plan='jumpkick';planAge=0;planToward=toward
   elseif style=='ball' and target==17 and distance>130 then
    plan='ball';planAge=0;planToward=toward
   elseif style=='retreatkick' then
    if distance<180 then
     plan='jumpkick';planAge=0;planToward=away
    else
     set('P1 Down',1);set('P1 Block',1)
    end
   elseif style=='latekick' then
    plan='jumpkick';planAge=0;planToward=distance>95 and toward or away
   elseif style=='sweepjump' then
    -- Approach above projectiles; at close range use ordinary native sweeps.
    -- Inputs only: no opponent difficulty, action, health or position writes.
    if distance>95 then
     plan='jumpkick';planAge=0;planToward=toward
    else
     set(away,1)
     set('P1 Low Kick',combat%16<3 and 1 or 0)
    end
   elseif jaxAir and c2==11 then
    plan='jumpkick';planAge=0;planToward=distance>180 and toward or away
   elseif jaxThrow and c2==11 then
    if distance>65 then set(toward,1)
    else plan='throw';planAge=0;planToward=toward end
   elseif jaxSweep and c2==11 then
    -- Separate physical strategy: approach behind crouch-block, sweep close.
    -- Keep the earlier ladder strategy unchanged for controlled comparison.
    if distance>75 then
     if combat%24<10 then set(toward,1)
     else set('P1 Down',1);set('P1 Block',1) end
    else
     plan='sweep';planAge=0;planToward=away
    end
   elseif liuBall and target==17 and c2==1 then
    plan='ball';planAge=0;planToward=toward;liuBallRelease=nil;liuBallReleased=false
   elseif (kanoKnife and (c2==9 or c2==11) or raidenKnife and c2==7 or subzeroKnife and c2==8 or femaleZoning and (c2==4 or c2==5)) and target==17 then
    plan=distance>100 and 'knife' or 'blade';planAge=0
    planToward=distance>100 and away or toward
    if mixedZoning and (c2==4 or c2==5) and distance>100 then
     projectileMixCount=projectileMixCount+1
     if projectileMixCount%3==0 then plan='ball' end
    end
   elseif jaxSafeRing and c2==11 and target==18 then
    if distance>240 then plan='ring';planAge=0;planToward=toward
    elseif distance<100 then plan='leg';planAge=0;planToward=toward
    else set('P1 Down',1);set('P1 Block',1);set(away,1) end
   elseif (jaxRing and c2==11 or femaleZoning and (c2==4 or c2==5)) and target==18 then
    plan=distance>100 and 'ring' or 'leg';planAge=0;planToward=toward
    if mixedZoning and (c2==4 or c2==5) and distance>100 and enemyGround-enemyY>40 then plan='square' end
   elseif style=='jumpgrapple' then
    if distance>95 then
     plan='jumpkick';planAge=0;planToward=toward
    else
     plan=target==18 and 'leg' or 'choke';planAge=0;planToward=toward
    end
   elseif style=='reptilegrapple' then
    -- Native collision spacing can be62: do not wait for an unreachable60.
    if distance>75 then
     if combat%12<8 then set(toward,1) else set('P1 Block',1) end
    else
     plan=target==18 and 'leg' or 'choke';planAge=0;planToward=toward
    end
   elseif distance>70 then
    set(toward,1)
    if distance<115 then set('P1 High Punch',combat%16<2 and 1 or 0) end
   else
    plan=target==18 and 'leg' or 'choke';planAge=0;planToward=toward
   end
  elseif u16(0x01060ec0)==0 and u16(0x010602f0)>0 then
   -- Finish a defeated CPU with an ordinary attack; do not force a result.
   if distance>50 then set(toward,1) end
   set('P1 High Punch',combat%16<2 and 1 or 0)
  end
 end
 lastHealth=u16(0x010602f0)
 if mode==2 and locked and target==18 and ((sonyaGuardLeg and c2==4) or (sonyaLiuGuardLeg and c2==1) or (sonyaMileenaGuardLeg and c2==5) or (sonyaCageGuardLeg and c2==2) or (sonyaLaoGuardLeg and c2==0) or (sonyaScorpionGuardLeg and c2==10) or ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6)) or (sonyaSubGuardLeg and c2==8)) and
    u16(0x010602f0)>0 and u16(0x01060ec0)>0 and commands['P1 Down']==1 and
    commands['P1 Block']==1 and (u16(proc1+0x210)&0x1c)==0 then lowGuardFields=lowGuardFields+1
 else lowGuardFields=0 end
 if counterLog and mode==2 and locked and u16(0x010602f0)>0 and u16(0x01060ec0)>0 and
    ((target==17 and (c2==4 or ((liuBall or liuRetreat or liuChoke) and c2==1) or (subzeroGuard and c2==8))) or (target==18 and (c2==4 or c2==5 or (sonyaKintaroGuard and c2==12) or ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6)) or (sonyaScorpionGuardLeg and c2==10) or (sonyaLaoGuardLeg and c2==0) or (sonyaCageGuardLeg and c2==2) or (sonyaLiuGuardLeg and c2==1) or (sonyaSubGuardLeg and c2==8) or (raidenCounter and c2==7)))) then
  local ownY,ownGround=s16(a+0xb0),s16(proc1+0x200)
  local enemyY,enemyGround=s16(b+0xb0),s16(proc2+0x200)
  counterLog:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',
   n,continuesUsed,c2,math.abs(x2-x1),ownGround-ownY,enemyGround-enemyY,u16(proc1+0x1f0),u16(proc2+0x1f0),n-counterJump,
   commands['P1 Up'] or 0,commands['P1 Down'] or 0,commands['P1 High Punch'] or 0,commands['P1 High Kick'] or 0,
   commands['P1 Low Kick'] or 0,commands['P1 Block'] or 0,commands['P1 Left'] or 0,commands['P1 Right'] or 0,
   ownY,ownGround,enemyY,enemyGround,retreatStill,retreatUntil,retreatLastFrame==n and 1 or 0,
   u16(proc1+0x210),x1,x2,commands['P1 Low Punch'] or 0))
  if n%16==0 then counterLog:flush() end
 end
 local count=u32(missing)
 local reason=nil
 if count>0 then reason='missing-animation'
 elseif cpu.state['PC'].value==recovery then reason='illegal-opcode-recovery'
 elseif n>=fieldLimit then reason='field-budget'
 elseif enteredCombat and (mode==1 or (mode==4 and not continuing)) then reason='left-campaign' end
 if n%2==0 or count>0 or reason then
  log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%08x,%08x,%d,%08x,%d,%d,%d,%d\n',
   n,combat,mode,u16(0x01061b30),u16(0x01061b00),c1,c2,a~=0 and u16(a+0x1f0) or -1,b~=0 and u16(b+0x1f0) or -1,
   u16(0x010602f0),u16(0x01060ec0),x1,x2,proc1~=0 and u16(proc1+0x1f0) or 0,proc2~=0 and u16(proc2+0x1f0) or 0,
   a~=0 and u32(a+0x1d0) or 0,b~=0 and u32(b+0x1d0) or 0,count,cpu.state['PC'].value,
   u16(0x01061af0),u16(0x01060310),u16(0x01060ee0),continuesUsed))
 end
 if captureEnding and mode==11 then
  if not endingFirst then endingFirst=n end
  local age=n-endingFirst
  if endingStateLog and age<9600 then
   local function addr(name) return assert(tonumber(os.getenv('KS_ENDING_'..name))) end
   local photo=u32(addr('OBJLST2'))
   local valid=photo>=0x01000000 and photo+0x200<0x01400000
   endingStateLog:write(string.format('%d,%d,%08x,%d,%d,%08x,%d,%08x,%08x,%08x,%08x,%d,%d,%08x\n',
    n,age,u32(addr('DLISTS')),u16(addr('DISPLAYON')),u16(addr('NOFLIP')),u32(addr('PAGEADDR')),
    u16(addr('F_AUTO_ERASE')),u32(addr('OBJLST')),photo,u32(addr('SCRNTL')),u32(addr('SCRNLR')),
    valid and s16(photo+0x90) or -1,valid and s16(photo+0xb0) or -1,valid and u32(photo+0x1d0) or 0))
   if age%120==0 then endingStateLog:flush() end
   -- Two12-field windows distinguish a stable defect from capture/page phase.
   if (age>=1734 and age<1746) or (age>=2454 and age<2466) then
    m.screens[':screen']:snapshot(string.format('ending_state_%06d_age%04d.png',n,age))
   end
   if age>=2574 and age<2586 then
    m.screens[':screen']:snapshot(string.format('ending_late_%06d_age%04d.png',n,age))
   end
   if age>=2520 and age<2640 then
    -- Sparse read-only samples, not a full framebuffer/palette certificate.
    local vh,ph=2166136261,2166136261
    for y=32,224,16 do
     for x=32,352,32 do vh=((vh~u16((y*512+x)*8))*16777619)&0xffffffff end
    end
    for index=1,4095,17 do ph=((ph~u16(0x01880000+index*16))*16777619)&0xffffffff end
    endingVideoLog:write(string.format('%d,%d,%04x,%08x,%08x\n',n,age,u16(0x01b00000),vh,ph))
   end
  end
  -- At most80 small native-resolution PNGs; never capture whole-match video.
  if (n-endingFirst)%120==60 and endingCaptures<80 then
   m.screens[':screen']:snapshot(string.format('ending_%06d_age%04d.png',n,n-endingFirst))
   endingCaptures=endingCaptures+1
  end
 end
 if mode~=previousMode then log:flush();m.screens[':screen']:snapshot(string.format('campaign_%05d_mode%d.png',n,mode)) end
 previousMode=mode
 -- Bounded first campaign attempt: stop on loss/continue selection, recovery,
 -- an uncovered animation, or the field budget. Never silently retry a loss.
 if reason then
  local outcome=assert(io.open('campaign_end.txt','w'))
  outcome:write(string.format('reason=%s\nframe=%d\nmode=%d\nmap=%d\nwinner=%d\n',reason,n,mode,u16(0x01061b30),u16(0x01061b00)))
  outcome:close()
  if counterLog then counterLog:close() end
  if endingStateLog then endingStateLog:close() end
  if endingVideoLog then endingVideoLog:close() end
  if subBallLog then subBallLog:close() end
  if subBallRecovery.throwLog then subBallRecovery.throwLog:close() end
  if bossContextLog then bossContextLog:close() end
  if kahnLog then kahnLog:close() end
  if stompEscapeLog then stompEscapeLog:close() end
  if subBallRecovery.readyLog then subBallRecovery.readyLog:close() end
  if subBallRecovery.knifeReadyLog then subBallRecovery.knifeReadyLog:close() end
  if subBallRecovery.bossBallLog then subBallRecovery.bossBallLog:close() end
  if subBallRecovery.variedLog then subBallRecovery.variedLog:close() end
  if subBallRecovery.verticalLog then subBallRecovery.verticalLog:close() end
  if subBallRecovery.recoveryLog then subBallRecovery.recoveryLog:close() end
  if subBallRecovery.airTimingLog then subBallRecovery.airTimingLog:close() end
  if fastChokeLog then fastChokeLog:close() end
  if rfpLog then rfpLog:close() end
  if recoveryCounterLog then recoveryCounterLog:close() end
  if guardLegLog then guardLegLog:close() end
  if subzeroObservationLog then subzeroObservationLog:close() end
  if ks_stream_capture_close then ks_stream_capture_close(n) end
  continueLog:close();log:close();m:exit()
 end
end)
