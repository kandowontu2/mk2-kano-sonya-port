"""Physical walk/crouch/kick extension of the corrected presentation probe."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_idle_presented_points_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker="  if frame-ready>=120 then log('IDLE_TERMINAL','fields=120');manager.machine:exit();return end"
    assert lua.count(marker)==1
    lua=lua.replace(marker,r'''
  local age=frame-ready
  if age>=180 then log('IDLE_TERMINAL','fields=180 policy=physical_ground_motion');manager.machine:exit();return end
  if age>=8 and age<24 then input(1,'Right')end
  if age>=32 and age<48 then input(1,'Left')end
  if age>=64 and age<80 then input(1,'Down')end
  if age>=96 and age<100 then input(1,'High Kick')end
''',1)
    assert ':write_' not in lua
    out=root/'audit_bounded_ground_motion_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_idle_presented_points_runtime',f'audit_bounded_{fighter}_ground_motion_points_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target),maximumReadyFields=180)))

if __name__=='__main__':main()
