"""Opposite physical slot using the same four-shot visual observer."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_cross_grab_visuals_preparation'
out=sync.ROOT/'audit_bounded_p2_cross_grab_visuals_preparation';assert not out.exists();out.mkdir()
for move in ('choke','leg'):
    runner=(old/f'run_{move}.ps1').read_text()
    runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_SIDE='1'","$env:MK2KS_HUMAN_SPECIAL_SIDE='2'")
    runner=runner.replace(f'audit_bounded_cross_grab_visual_{move}_p1_runtime',f'audit_bounded_cross_grab_visual_{move}_p2_runtime')
    (out/f'run_{move}.ps1').write_text(runner)
