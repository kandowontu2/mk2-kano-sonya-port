"""Normal stock Raiden LowPunch against real added victims."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_ground_throw_dispatch_preparation'
    out=root/'audit_bounded_raiden_ground_throw_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    needle="if age>=112 and age<116 then input(1,'Low Punch')end"
    assert lua.count(needle)==1
    lua=lua.replace(needle,"if age>=112 and age<116 then input(2,'Low Punch')end")
    lua=lua.replace('physical_added_ground_throw','physical_raiden_ground_throw')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_ground_throw_dispatch_runtime',
                              f'audit_bounded_{fighter}_raiden_ground_throw_runtime')
        runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_VICTIM='kitana'",
                              "$env:MK2KS_HUMAN_SPECIAL_VICTIM='raiden'")
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
