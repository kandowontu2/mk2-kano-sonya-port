"""Reciprocal acid visuals using the same pinned physical controller."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_visual_preparation'
out=sync.ROOT/'audit_current_native_deadpool_sonya_visual_preparation'
assert not out.exists();out.mkdir()
runner=(base/'run.ps1').read_text()
runner=runner.replace('audit_current_native_deadpool_visual_kano_p1_runtime','audit_current_native_deadpool_visual_sonya_p2_runtime')
runner=runner.replace("$env:MK2KS_STAGE_WINNER='kano'","$env:MK2KS_STAGE_WINNER='sonya'")
runner=runner.replace("$env:MK2KS_STAGE_SIDE='1'","$env:MK2KS_STAGE_SIDE='2'")
(out/'run.ps1').write_text(runner)
print('Prepared Sonya P2 reciprocal acid visuals, same Lua and512KiB cap')
