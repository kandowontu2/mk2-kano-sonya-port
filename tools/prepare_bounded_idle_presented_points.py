"""Use rendered presentation texture, not screen_device current draw bitmap."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_idle_vram_points_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker='local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400)'
    assert lua.count(marker)==1
    lua=lua.replace(marker,'local w,h=manager.machine.video:snapshot_size();local raw=manager.machine.video:snapshot_pixels();assert(w==400 and h==254 and #raw==406400)',1)
    out=root/'audit_bounded_idle_presented_points_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_idle_vram_points_runtime',f'audit_bounded_{fighter}_idle_presented_points_runtime')
        runner=runner.replace("'-video','none'","'-snapsize','400x254','-video','none'")
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target),retainedPixels=False)))

if __name__=='__main__':main()
