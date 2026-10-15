"""Far physical knife-uppercut whiff, unchanged controller and renderer."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_grab_misses_preparation'
out=sync.ROOT/'audit_bounded_current_blade_misses_preparation';assert not out.exists();out.mkdir()
for side in (1,2):
    runner=(old/f'run_choke_p{side}.ps1').read_text()
    runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_MOVE='choke'","$env:MK2KS_HUMAN_SPECIAL_MOVE='blade'")
    runner=runner.replace(f'audit_bounded_current_grab_miss_choke_p{side}_runtime',f'audit_bounded_current_blade_miss_p{side}_runtime')
    (out/f'run_p{side}.ps1').write_text(runner)
