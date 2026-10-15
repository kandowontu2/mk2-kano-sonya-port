"""Correct observer-only identity routing; preserve first untraced runs."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_shadow_writer_trace_preparation'
out=sync.ROOT/'audit_bounded_shadow_writer_trace_identity_preparation';assert not out.exists();out.mkdir()
lua=(old/'prepared_observer.lua').read_text()
marker="local trace_fighter=os.getenv('MK2KS_TEST_FIGHTER')"
assert lua.count(marker)==1
lua=lua.replace(marker,"local trace_fighter=spec[1]==17 and 'kano' or 'sonya'")
target=out/'prepared_observer.lua';target.write_text(lua)
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace(f'audit_bounded_{fighter}_shadow_writer_trace_runtime',f'audit_bounded_{fighter}_shadow_writer_trace_identity_runtime')
    (out/f'run_{fighter}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,observerIdentityFromActualTestSpec=True,observerSHA256=sync.sha(target))))
