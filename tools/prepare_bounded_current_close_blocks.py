"""Original native physical block tests for blade and bicycle."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_projectile_blocks_preparation'
out=sync.ROOT/'audit_bounded_current_close_blocks_preparation';assert not out.exists();out.mkdir()
for move,base in [('blade','knife'),('bicycle','ring')]:
    for side in (1,2):
        runner=(old/f'run_{base}_p{side}.ps1').read_text()
        marker=f"$env:MK2KS_HUMAN_SPECIAL_MOVE='{base}'";assert runner.count(marker)==1
        runner=runner.replace(marker,f"$env:MK2KS_HUMAN_SPECIAL_MOVE='{move}'")
        runner=runner.replace(f'audit_bounded_current_projectile_block_{base}_p{side}_runtime',f'audit_bounded_current_close_block_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,observerUnchanged=True,physicalBlocks=True)))
