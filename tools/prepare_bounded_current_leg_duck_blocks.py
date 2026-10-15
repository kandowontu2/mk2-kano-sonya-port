"""Physical crouching Block versus original leg-grab command."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_projectile_blocks_preparation'
out=sync.ROOT/'audit_bounded_current_leg_duck_blocks_preparation';assert not out.exists();out.mkdir()
for side in (1,2):
    runner=(old/f'run_ring_p{side}.ps1').read_text()
    runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_MOVE='ring'","$env:MK2KS_HUMAN_SPECIAL_MOVE='leg'")
    runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_SCENARIO='block'","$env:MK2KS_HUMAN_SPECIAL_SCENARIO='duck_block'")
    runner=runner.replace(f'audit_bounded_current_projectile_block_ring_p{side}_runtime',f'audit_bounded_current_leg_duck_block_p{side}_runtime')
    (out/f'run_p{side}.ps1').write_text(runner)
