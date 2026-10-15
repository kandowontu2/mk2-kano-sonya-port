"""Ordinary player Back/LowKick for the actual added-fighter attacker."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_spaced_sweep_preparation'
    out=root/'audit_bounded_added_sweep_attack_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    for before,after in (
        ("input(2,b.x>a.x and 'Right' or 'Left')", "input(1,a.x<b.x and 'Left' or 'Right')"),
        ("if age>=112 and age<116 then input(2,'Low Kick')end",
         "if age>=112 and age<116 then input(1,'Low Kick')end"),
        ('physical_spaced_sweep_recovery','physical_added_sweep_attack')):
        assert lua.count(before)==1;lua=lua.replace(before,after)
    assert ':write_' not in lua
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_spaced_sweep_runtime',
                              f'audit_bounded_{fighter}_added_sweep_attack_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
