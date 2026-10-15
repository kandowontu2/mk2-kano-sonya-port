"""Add passive later-body overlap and native clip receipts to jump tests."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_idle_dma_clip_preparation'
physical=sync.ROOT/'audit_bounded_jump_shadow_points_preparation'
out=sync.ROOT/'audit_bounded_jump_shadow_coverage_preparation'
assert not out.exists();out.mkdir()
lua=(old/'prepared_observer.lua').read_text()
marker="  if frame-ready>=120 then log('IDLE_TERMINAL','fields=120');manager.machine:exit();return end"
assert lua.count(marker)==1
jump=(physical/'prepared_observer.lua').read_text()
replacement=jump.split('  local age=frame-ready',1)[1].split('\n end',1)[0]
lua=lua.replace(marker,'  local age=frame-ready'+replacement)
assert ':write_' not in lua
target=out/'prepared_observer.lua';target.write_text(lua)
for fighter in ('kano','sonya'):
    runner=(physical/f'run_{fighter}.ps1').read_text().replace(physical.name,out.name)
    runner=runner.replace(sync.sha(physical/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace(f'audit_bounded_{fighter}_jump_shadow_points_runtime',f'audit_bounded_{fighter}_jump_shadow_coverage_runtime')
    (out/f'run_{fighter}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,physicalInputsUnchanged=True,rawMedia=False,observerSHA256=sync.sha(target))))
