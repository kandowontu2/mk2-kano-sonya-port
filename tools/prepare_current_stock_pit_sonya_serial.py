"""Serial retry, preserve capped parallel evidence and identical controller."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_stock_pit_other_sides_preparation'
out=sync.ROOT/'audit_current_stock_pit_sonya_serial_preparation'
assert not out.exists();out.mkdir()
runner=(base/'sonya_p1_kitana.ps1').read_text()
old='audit_current_stock_pit_sonya_p1_kitana_runtime'
assert runner.count(old)==1
runner=runner.replace(old,'audit_current_stock_pit_sonya_serial_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared serial retry, identical pinned Lua,90sec/320MiB/no media')
