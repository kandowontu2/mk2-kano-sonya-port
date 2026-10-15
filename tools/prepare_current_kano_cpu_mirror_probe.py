"""Existing ordinary guard probe, genuine Kano mirror native selection."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_kano_cpu_router_probe_preparation'
out=sync.ROOT/'audit_current_kano_cpu_mirror_probe_preparation';assert not out.exists()
runner=(old/'run.ps1').read_text()
assert runner.count("MK2KS_TEST_FIGHTER='sonya'")==1
runner=runner.replace("MK2KS_TEST_FIGHTER='sonya'","MK2KS_TEST_FIGHTER='kano'")
runner=runner.replace('audit_current_kano_cpu_router_probe_runtime','audit_current_kano_cpu_mirror_probe_runtime')
out.mkdir();(out/'run.ps1').write_text(runner)
print('Prepared12000field physical Kano mirror probe; original observer and limits retained')
