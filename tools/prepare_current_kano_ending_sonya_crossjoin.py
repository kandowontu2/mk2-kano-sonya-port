"""Prepare earned Kano campaign unchanged, then physically pay/reselect native Sonya."""
import json
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_kano_postending_two_coin_join_preparation'
out=root/'audit_current_kano_ending_sonya_crossjoin_preparation'
proof=root/'audit_current_kano_ending_sonya_crossjoin_source_checked'
assert not out.exists() and not proof.exists()
original=(base/'campaign.lua').read_text()
source=original
replacements=[
 ('local function route(start)\n','local function route(start,target)\n target=target or identity\n'),
 ('if current[1]==identity then return current[2]end','if current[1]==target then return current[2]end'),
 ("log('POST_ENDING_PAID_START','coin_ages=20,50 start_age=100 target=17')","log('POST_ENDING_PAID_START','coin_ages=20,50 start_age=100 target=18 previous=17')"),
 ('css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster))','local css_target=(ending_completed and pj_attract)and18or identity\n  css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster),css_target)'),
 ('selections,p:read_u16(slots[side].roster),identity,table.concat(plan', 'selections,p:read_u16(slots[side].roster),css_target,table.concat(plan'),
]
for old,new in replacements:
 assert source.count(old)==1
 source=source.replace(old,new,1)
start=source.index(' if ending_completed then\n  if frame-ending_completed>=12000')
end=source.index('\n if stage==14 and other',start)
old_fresh=source[start:end]
new_fresh=old_fresh.replace('human.id==17 and human.roster==17','human.id==18 and human.roster==18').replace('human=17:17','human=18:18')
marker="   if not pj_live then pj_live=frame;log('POST_ENDING_FIGHT'"
assert new_fresh.count(marker)==1
observe="""   if not pj_move_tap then
    local observed_main=human.main
    pj_move_tap=p:install_write_tap(observed_main+0x1f0,observed_main+0x1ff,'passive fresh Sonya native moves',function(at,data,mask)
     if at~=observed_main+0x1f0 or mask~=0xffff then return end
     local h=sample(side);local action=data&0xffff
     if not h or h.id~=18 or h.roster~=18 or h.main~=observed_main or h.owner~=h.actor or h.hp==0 or cpu.A8.value~=h.actor or cpu.A13.value~=h.main then return end
     if action==776 or action==779 or action==257 or action==276 or action==0 or action==771 then
      log('POST_ENDING_MOVE_STORE',string.format('actor=%08X main=%08X owner=%08X a8=%08X a13=%08X id=%d roster=%d at=%08X before=%d after=%d mask=%04X pc=%08X hp=%d',h.actor,h.main,h.owner,cpu.A8.value,cpu.A13.value,h.id,h.roster,at,p:read_u16(at),action,mask,cpu.PC.value,h.hp))
     end
    end)
    taps[#taps+1]=pj_move_tap
   end
"""
new_fresh=new_fresh.replace(marker,observe+marker,1)
new_fresh=new_fresh.replace('stage=%d actor=%08X main=%08X\'',"stage=%d actor=%08X main=%08X owner=%08X id=%d roster=%d'").replace('other.id,other.roster,stage,human.actor,human.main))','other.id,other.roster,stage,human.actor,human.main,human.owner,human.id,human.roster))')
new_fresh=new_fresh.replace('main=%08X human=18:18 hp=%d','main=%08X owner=%08X id=%d roster=%d human=18:18 hp=%d').replace('pj_live,pj_recovered,human.actor,human.main,human.hp))','pj_live,pj_recovered,human.actor,human.main,human.owner,human.id,human.roster,human.hp))')
source=source[:start]+new_fresh+source[end:]
header='local pj_move_tap=nil\n';source=header+source
def gate(candidate):
 assert candidate.startswith(header) and candidate.count(new_fresh)==1
 restored=candidate[len(header):].replace(new_fresh,old_fresh,1)
 for old,new in reversed(replacements):
  assert restored.count(new)==1
  restored=restored.replace(new,old,1)
 assert restored==original
 assert ':write_' not in candidate and ':snapshot(' not in candidate
 assert 'local identity=assert(({kano=17,sonya=18})[fighter])' in candidate
gate(source);faults=[]
for name,bad in (
 ('late_route_ignores_target',source.replace('if current[1]==target then','if current[1]==identity then',1)),
 ('fresh_owner_assertion_removed',source.replace('human.id==18 and human.roster==18 and human.owner==human.actor','human.id==18 and human.roster==18',1)),
 ('global_campaign_identity_mutated',source.replace('local identity=assert(({kano=17,sonya=18})[fighter])','local identity=18',1)),
):
 assert bad!=source
 try:gate(bad)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Source conservation fault accepted')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_postending_two_coin_join_runtime','audit_current_kano_ending_sonya_crossjoin_runtime')
(out/'run.ps1').write_text(runner)
report=dict(preparedOnlyNotRun=True,exactOriginalSourceConservedOutsideExplicitLateRouteAndObserverChanges=True,
 originalCampaignIdentityAndEndingTapClosuresPreserved=True,lateTarget=18,priorEndingIdentity=17,
 ordinaryPhysicalControlSequencePreserved=True,actualAttractRequiredBeforeTwoCoinStart=True,
 sourceFaultsRejected=faults,preparedLuaSHA256=sync.sha(lua),baselineLuaSHA256=sync.sha(base/'campaign.lua'),
 runtimePrefixAccepted=False,crossJoinAccepted=False,SonyaOwnEndingAccepted=False,fullPortAccepted=False)
proof.mkdir();(proof/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
