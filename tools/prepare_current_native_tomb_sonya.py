"""Reciprocal current Tomb, unchanged controller/scalar observer."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_preparation'
out=sync.ROOT/'audit_current_native_tomb_sonya_preparation';assert not out.exists()
runner=(base/'run_kano_p1.ps1').read_text()
assert runner.count("MK2KS_STAGE_WINNER='kano'")==1
runner=runner.replace("MK2KS_STAGE_WINNER='kano'","MK2KS_STAGE_WINNER='sonya'")
runner=runner.replace('audit_current_native_tomb_kano_p1_runtime','audit_current_native_tomb_sonya_p1_runtime')
out.mkdir();(out/'run_sonya_p1.ps1').write_text(runner)
print('Prepared reciprocal real SonyaP1/KanoP2 Tomb, same Lua/no media/caps')
