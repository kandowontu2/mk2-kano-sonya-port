"""Read current native dispatch operands rather than obsolete stock table rows."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_own_finishers_preparation'
out=sync.ROOT/'audit_bounded_own_finishers_dispatch_preparation'
assert not out.exists()
out.mkdir()
source=(old/'finishers.lua').read_text()
marker='local action_addresses={p:read_u32(0xff8ba210+killer_id*32),p:read_u32(0xff8ba390+killer_id*32)}'
assert source.count(marker)==1
source=source.replace(marker,'local action_addresses={p:read_u32(p:read_u32(0xff876b50)+killer_id*32),p:read_u32(p:read_u32(0xff876b90)+killer_id*32)}')
lua=out/'finishers.lua'
lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
    runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
    runner=runner.replace(old.name+'/finishers.lua',out.name+'/finishers.lua').replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_own_finisher_{fighter}_p{side}_runtime',f'audit_bounded_own_finisher_dispatch_{fighter}_p{side}_runtime')
    (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
