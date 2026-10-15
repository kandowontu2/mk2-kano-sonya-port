"""Ordinary stock sweep against added fighters; scalar-only observation."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT
    sync.verify()
    old=root/'audit_bounded_crouch_kick_pain_preparation'
    out=root/'audit_bounded_sweep_reaction_preparation'
    assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    needle="if age>=96 and age<124 then input(2,'Down')end"
    assert lua.count(needle)==1
    lua=lua.replace(needle,"if age>=112 and age<116 then input(2,b.x>a.x and 'Right' or 'Left')end")
    lua=lua.replace('physical_crouch_lowkick_reaction','physical_sweep_recovery')
    assert ':write_' not in lua and 'snapshot_pixels' not in lua
    out.mkdir()
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_crouch_kick_pain_runtime',
                              f'audit_bounded_{fighter}_sweep_reaction_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,
                                                observerSha=sync.sha(target))))

if __name__=='__main__':main()
