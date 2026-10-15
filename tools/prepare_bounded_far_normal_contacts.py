"""Physical range80 separates standing normals from close elbow/throw."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_reachable_normals_exit_preparation'
out=sync.ROOT/'audit_bounded_far_normal_contacts_preparation'
assert not out.exists()
out.mkdir()
source=(old/'normals.lua').read_text()
assert source.count('math.abs(own.x-victim.x)>63')==1
lua=out/'normals.lua'
lua.write_text(source.replace('math.abs(own.x-victim.x)>63','math.abs(own.x-victim.x)>80'))
for move in ('knife','ring'):
 for side in (1,2):
    runner=(old/f'run_{move}_p{side}.ps1').read_text()
    runner=runner.replace(old.name+'/normals.lua',out.name+'/normals.lua').replace(sync.sha(old/'normals.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_reachable_normals_exit_{move}_p{side}_runtime',f'audit_bounded_far_normal_contacts_{move}_p{side}_runtime')
    (out/f'run_{move}_p{side}.ps1').write_text(runner)
