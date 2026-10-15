"""Observe the following completed display field, not current draw buffer."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_idle_scanout_points_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker=' if #idle_points==0 then return end'
    assert lua.count(marker)==1
    lua=lua.replace(marker,marker+'\n if idle_points[1].frame>=frame then return end',1)
    lua=lua.replace('row=%d column=%d effective=%04X','row=%d column=%d effective=%04X',1)
    out=root/'audit_bounded_idle_scanout_delayed_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_idle_scanout_points_runtime',f'audit_bounded_{fighter}_idle_scanout_delayed_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,sourceFieldDelay=1,observerSha=sync.sha(target))))

if __name__=='__main__':main()
