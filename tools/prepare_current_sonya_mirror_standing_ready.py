"""Reject counter plans from crouch/block; physical release until standing."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_active_flag_guard_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_standing_ready_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then')
end=source.index('   elseif leg_tactic and other.roster==0 then',start)
branch=source[start:end]
old='local stance=human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793'
assert branch.count(old)==1
branch=branch.replace(old,'local stance=human.action==0 or human.action==771 or human.action==772')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_active_flag_guard_runtime','audit_current_sonya_mirror_standing_ready_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared21000fields; only standing-readiness predicate changed; no media')
