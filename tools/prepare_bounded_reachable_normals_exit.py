"""Schedule existing scalar final marker so observer exits promptly."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_reachable_range_normals_preparation'
out=sync.ROOT/'audit_bounded_reachable_normals_exit_preparation'
assert not out.exists()
out.mkdir()
source=(old/'normals.lua').read_text()
marker="completed=2;log('FINAL');rawset(_G,'MK2_SPECIAL_EXIT_PENDING',true)"
assert source.count(marker)==1
lua=out/'normals.lua'
lua.write_text(source.replace(marker,"completed=2;log('FINAL');snapshot_ram('special_final.png');rawset(_G,'MK2_SPECIAL_EXIT_PENDING',true)"))
assert ':snapshot(' not in lua.read_text()
for move in ('knife','ring'):
 for side in (1,2):
    runner=(old/f'run_{move}_p{side}.ps1').read_text()
    runner=runner.replace(old.name+'/normals.lua',out.name+'/normals.lua').replace(sync.sha(old/'normals.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_reachable_range_normals_{move}_p{side}_runtime',f'audit_bounded_reachable_normals_exit_{move}_p{side}_runtime')
    (out/f'run_{move}_p{side}.ps1').write_text(runner)
