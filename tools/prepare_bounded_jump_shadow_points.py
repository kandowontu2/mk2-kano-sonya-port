"""Physical jump extends native shadow point observer, without new builds."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_idle_shadow_points_preparation'
out=sync.ROOT/'audit_bounded_jump_shadow_points_preparation'
assert not out.exists();out.mkdir()
lua=(old/'prepared_observer.lua').read_text()
marker="  if frame-ready>=120 then log('IDLE_TERMINAL','fields=120');manager.machine:exit();return end"
assert lua.count(marker)==1
lua=lua.replace(marker,"""  local age=frame-ready
  if age>=240 then log('IDLE_TERMINAL','fields=240 policy=physical_jump');manager.machine:exit();return end
  if age>=16 and age<20 then input(1,'Up')end
  if age>=96 and age<100 then input(1,'Up');input(1,'Right')end
  if age>=176 and age<180 then input(1,'Up');input(1,'Left')end""")
assert ':write_' not in lua
target=out/'prepared_observer.lua';target.write_text(lua)
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace(f'audit_bounded_{fighter}_idle_shadow_points_runtime',f'audit_bounded_{fighter}_jump_shadow_points_runtime')
    (out/f'run_{fighter}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,physicalJumps=True,rawMedia=False,observerSHA256=sync.sha(target))))
