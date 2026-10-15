"""Kano slot2 native Tomb; same ordinary rematch controller."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_preparation'
out=sync.ROOT/'audit_current_native_tomb_p2_preparation';assert not out.exists()
runner=(base/'run_kano_p1.ps1').read_text()
assert runner.count("MK2KS_STAGE_SIDE='1'")==1
runner=runner.replace("MK2KS_STAGE_SIDE='1'","MK2KS_STAGE_SIDE='2'")
runner=runner.replace('audit_current_native_tomb_kano_p1_runtime','audit_current_native_tomb_kano_p2_runtime')
out.mkdir();(out/'run_kano_p2.ps1').write_text(runner)
print('Prepared native KanoP2/SonyaP1 Tomb, unchanged Lua/no media/resource caps')
