"""Remove incidental400emulatedsecond stop, retain all physical resource caps."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_kitana_close_guard_24000_preparation'
out=sync.ROOT/'audit_current_kano_close_guard_24000_scoped_preparation'
assert not out.exists();out.mkdir()
runner=(base/'run.ps1').read_text()
assert runner.count("'-str','400'")==1
runner=runner.replace("'-str','400'","'-str','450'")
runner=runner.replace('audit_current_kano_kitana_close_guard_24000_runtime','audit_current_kano_close_guard_24000_scoped_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared identical24000field Lua with450emulatedsecond allowance;90secwall/320MiB')
