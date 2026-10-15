"""Physical standing Block against Kano choke, unchanged bounded observer."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_projectile_blocks_preparation'
out=sync.ROOT/'audit_bounded_current_choke_blocks_preparation';assert not out.exists();out.mkdir()
for side in (1,2):
    runner=(old/f'run_knife_p{side}.ps1').read_text()
    runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_MOVE='knife'","$env:MK2KS_HUMAN_SPECIAL_MOVE='choke'")
    runner=runner.replace(f'audit_bounded_current_projectile_block_knife_p{side}_runtime',f'audit_bounded_current_choke_block_p{side}_runtime')
    (out/f'run_p{side}.ps1').write_text(runner)
