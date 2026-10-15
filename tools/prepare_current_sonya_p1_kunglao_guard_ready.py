"""Prepared only: stage4 native guard recovery readiness; physical chord/range unchanged."""
import json
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_sonya_p1_default_kick_deferred_preparation'
out=root/'audit_current_sonya_p1_kunglao_guard_ready_preparation'
proof=root/'audit_current_sonya_p1_kunglao_guard_ready_source_checked'
assert not out.exists() and not proof.exists()
original=(base/'campaign.lua').read_text()
start=original.index("   elseif leg_tactic and (other.roster==0 or (side==1 and other.roster==1)) then")
end=original.index("   elseif fighter=='sonya' and side==1 and other.roster==8 and stage==11 then",start)
branch=original[start:end]
old='and human.flags&0x1c==0 and (blocking or human.body&0x0c==0)'
new='and (human.flags&0x1c==0 or(stage==4 and other.roster==0 and blocking and human.flags&0x18==0)) and (blocking or human.body&0x0c==0)'
assert branch.count(old)==1
source=original[:start]+branch.replace(old,new,1)+original[end:]
def gate(candidate):
 assert candidate.count(new)==1
 assert candidate.replace(new,old,1)==original
 assert ':write_' not in candidate and ':snapshot(' not in candidate
gate(source);faults=[]
for name,bad in (
 ('unguarded_flags_exception',source.replace('and blocking and human.flags&0x18==0','and human.flags&0x18==0',1)),
 ('wrong_stage_scope',source.replace('stage==4 and other.roster==0 and blocking','stage==11 and other.roster==0 and blocking',1)),
 ('changed_boss_jump_direction',source.replace('boss_jump_direction=forward;boss_walk_last_x=nil','boss_jump_direction=back;boss_walk_last_x=nil',1)),
):
 assert bad!=source
 try:gate(bad)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Conservation fault accepted')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_default_kick_deferred_runtime','audit_current_sonya_p1_kunglao_guard_ready_runtime')
(out/'run.ps1').write_text(runner)
report=dict(preparedOnlyNotRun=True,onlyStage4KungNativeGuardReadinessChanged=True,
 exactOtherSourceConservation=True,allPhysicalCommandTimingRangeAndBossControlsPreserved=True,
 sourceFaultsRejected=faults,preparedLuaSHA256=sync.sha(lua),baselineLuaSHA256=sync.sha(base/'campaign.lua'),
 futureRuntimeGate='Preserveprestage4prefix12471 excludingonlyearlySPECIAL, actualtrue18 nativechronology and samepaidmatchoutcomes; do not assertoldpost-changeRNG/roundhistory',
 shorterCampaignAccepted=False,winningRouteAccepted=False,fullPortAccepted=False)
proof.mkdir();(proof/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
