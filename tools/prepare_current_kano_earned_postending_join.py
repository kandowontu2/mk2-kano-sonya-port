"""Earned ending, paid physical P2 restart, independently observed controls."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_backjump_charge_counter_preparation'
out=sync.ROOT/'audit_current_kano_earned_postending_join_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local pj_reset,pj_live,pj_walk_x,pj_walk,pj_jump,pj_pulse,pj_punch,pj_recovered=false,nil,nil,nil,nil,nil,nil,nil\n'+source
marker=' if not css and frame>700 and mode==4'
assert source.count(marker)==1
source=source.replace(marker,""" if ending_completed then
  local age=frame-ending_completed
  if age>=60 and not pj_reset then
   pj_reset=true;css=nil;css_exit=nil;loss_at=nil
   log('POST_ENDING_PAID_START','coin_age=60 start_age=80 target=17')
  end
  if age>=60 and age<64 then press('Coin')end
  if age>=80 and age<84 then press('Start')end
 end
"""+marker)
marker=' local human,other=sample(side),sample(opponent)'
assert source.count(marker)==1
source=source.replace(marker,marker+'''
 if ending_completed then
  if frame-ending_completed>=6000 then log('POST_ENDING_BOUND','maximum_fields=6000');manager.machine:exit();return end
  if mode==2 and state==1 and human and other and other.state==0 and human.hp>0 and other.hp>0 then
   assert(human.id==17 and human.roster==17 and human.owner==human.actor and other.owner==other.actor)
   if not pj_live then pj_live=frame;log('POST_ENDING_FIGHT',string.format('human=17:17 cpu=%d:%d stage=%d actor=%08X main=%08X',other.id,other.roster,stage,human.actor,human.main))end
   local ready=human.y==human.floor and human.flags&0x1c==0 and human.body&0x0c==0 and(human.action==0 or human.action==771 or human.action==770 or human.action==772)
   if not pj_walk then
    if ready then
     pj_walk_x=pj_walk_x or human.x
     if math.abs(human.x-pj_walk_x)>=4 then pj_walk=frame;log('POST_ENDING_WALK','from='..pj_walk_x..' x='..human.x)
     else press(human.x<other.x and'Right'or'Left')end
    else press('Block')end
   elseif not pj_jump then
    if human.y<human.floor and(human.action==776 or human.action==779)then pj_jump=frame;log('POST_ENDING_JUMP','action='..human.action..' y='..human.y..' floor='..human.floor)
    elseif ready then press('Up')end
   elseif not pj_punch then
    if pj_pulse and(human.action==257 or human.action==276)then pj_punch=frame;log('POST_ENDING_PUNCH','action='..human.action)
    elseif ready and not pj_pulse then pj_pulse=frame;press('High Punch')
    elseif pj_pulse and frame-pj_pulse<4 then press('High Punch')
    elseif pj_pulse and frame-pj_pulse>40 then pj_pulse=nil end
   elseif not pj_recovered then
    if ready then pj_recovered=frame;log('POST_ENDING_RECOVERED','hp='..human.hp)end
   elseif frame-pj_recovered>=180 then
    log('POST_ENDING_COMPLETE',string.format('start=%d recovered=%d actor=%08X main=%08X human=17:17 hp=%d',pj_live,pj_recovered,human.actor,human.main,human.hp));manager.machine:exit()
   else press('Block')end
  end
  return
 end
''')
old=' if ending_completed and frame-ending_completed>=300 then manager.machine:exit()end'
assert source.count(old)==1;source=source.replace(old,' -- Fresh paid post-ending join owns the subsequent stop condition.')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_backjump_charge_counter_runtime','audit_current_kano_earned_postending_join_runtime')
(out/'run.ps1').write_text(runner)
print('Earnedending/paidP2reselect/walkjumpHP/recovery;180sec/320MiB/10MiB/no media')
