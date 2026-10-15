"""Reuse bounded presented-point observer with verified physical sweep policy."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_settled_uppercut_recovery_preparation'
    out=root/'audit_bounded_sweep_presentation_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    replacements={
        'math.abs(a.x-b.x)>45':'math.abs(a.x-b.x)>85',
        "if age>=96 and age<124 then input(2,'Down')end":
            "if age>=108 and age<116 then input(2,b.x>a.x and 'Right' or 'Left')end",
        "if age>=112 and age<116 then input(2,'High Punch')end":
            "if age>=112 and age<116 then input(2,'Low Kick')end",
        'policy=physical_settled_uppercut_recovery':'policy=physical_sweep_presentation'}
    for before,after in replacements.items():
        assert lua.count(before)==1;lua=lua.replace(before,after)
    assert ':write_' not in lua
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_settled_uppercut_recovery_runtime',
                              f'audit_bounded_{fighter}_sweep_presentation_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,
                                                observerSha=sync.sha(target))))

if __name__=='__main__':main()
