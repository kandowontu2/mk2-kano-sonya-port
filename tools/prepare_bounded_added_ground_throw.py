"""Close approach and ordinary LowPunch throw attempt, no forced state."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_added_sweep_attack_preparation'
    out=root/'audit_bounded_added_ground_throw_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    replacements={
        'math.abs(a.x-b.x)>85':'math.abs(a.x-b.x)>35',
        "if age>=108 and age<116 then input(1,a.x<b.x and 'Left' or 'Right')end":'',
        "if age>=112 and age<116 then input(1,'Low Kick')end":
            "if age>=112 and age<116 then input(1,'Low Punch')end",
        'physical_added_sweep_attack':'physical_added_ground_throw'}
    for before,after in replacements.items():
        assert lua.count(before)==1;lua=lua.replace(before,after)
    assert ':write_' not in lua
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_added_sweep_attack_runtime',
                              f'audit_bounded_{fighter}_added_ground_throw_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
