"""Normal spacing outside knee range, early Back plus LowKick."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_held_back_sweep_preparation'
    out=root/'audit_bounded_spaced_sweep_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    assert lua.count('math.abs(a.x-b.x)>45')==1
    lua=lua.replace('math.abs(a.x-b.x)>45','math.abs(a.x-b.x)>85')
    lua=lua.replace('if age>=96 and age<116 then input(2,', 'if age>=108 and age<116 then input(2,')
    lua=lua.replace('physical_held_back_sweep_recovery','physical_spaced_sweep_recovery')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_held_back_sweep_runtime',
                              f'audit_bounded_{fighter}_spaced_sweep_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
