"""Physical mirror controller: reject hit-reaction readiness/active special grabs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_kunglao_guard_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_stance_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then\n')
end=source.index('   elseif leg_tactic and other.roster==0 then',start)
branch=source[start:end]
assert branch.count('human.flags&0x18')==1
branch=branch.replace('human.flags&0x18','human.flags&0x1c')
old='or (other.action>=1536 and other.action<=1551)'
assert branch.count(old)==1
branch=branch.replace(old,'or other.action==1792 or other.action==1793')
branch=branch.replace('    if other.action==4','    safe=safe and other.flags&0x0c==0\n    if other.action==4')
source=source[:start]+branch+source[end:]
source=source.replace('frame>=18000','frame>=30000').replace('maximum_fields=18000','maximum_fields=30000')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_kunglao_guard_runtime','audit_current_sonya_mirror_stance_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared actual mirror stance guard after productive route,30000fields/90sec/320MiB,no media')
