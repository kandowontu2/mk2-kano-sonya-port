"""Reuse current-build P1 native Kung Lao guarded leg inputs for P2."""
import json
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_contact_trace_preparation'
proved=sync.ROOT/'audit_current_sonya_kunglao_guard_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_verified_leg_preparation'
assert not out.exists()
proof=json.loads((sync.ROOT/'audit_current_sonya_kunglao_guard_checked/report.json').read_text())
assert proof['passedObservationChecks'] and proof['earnedStages']==[0,1,2,3,4,5]
assert proof['logSHA256']==sync.sha(sync.ROOT/'audit_current_sonya_kunglao_guard_runtime/run.log')
prior=(proved/'campaign.lua').read_text()
start=prior.index('   elseif leg_tactic and other.roster==0 then\n')
end=prior.index('   elseif (leg_tactic or strategy==',start)
branch=prior[start:end]
source=(base/'campaign.lua').read_text()
marker="   elseif fighter=='sonya' and side==2 and (other.roster==8 or other.roster==2 or other.roster==0) then"
assert source.count(marker)==1
source=source.replace(marker,branch+marker)
source='local kg_last,kg_leg,kg_retry,kg_upper,kg_guard=nil,nil,-1000,-1000,-1000\n'+source
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_contact_trace_runtime','audit_current_sonya_p2_kunglao_verified_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Exact current P1 KungLao leg policy via side-bound physical controls;60k/90sec/320MiB/10MiB/no media')
