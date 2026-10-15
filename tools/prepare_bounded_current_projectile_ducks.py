"""Original physical Down policy versus knife/ring, no health/position writes."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_projectile_blocks_preparation'
out=sync.ROOT/'audit_bounded_current_projectile_ducks_preparation';assert not out.exists();out.mkdir()
for move in ('knife','ring'):
    for side in (1,2):
        runner=(old/f'run_{move}_p{side}.ps1').read_text()
        runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_SCENARIO='block'","$env:MK2KS_HUMAN_SPECIAL_SCENARIO='miss'")
        runner=runner.replace(f'audit_bounded_current_projectile_block_{move}_p{side}_runtime',f'audit_bounded_current_projectile_duck_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
