"""Bounded sparse presented-point observation of real cross-added throws."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_sweep_presentation_preparation'
    scalar=root/'audit_bounded_cross_added_ground_throw_preparation'
    out=root/'audit_bounded_cross_throw_presentation_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    for before,after in (
        ('math.abs(a.x-b.x)>85','math.abs(a.x-b.x)>35'),
        ("if age>=108 and age<116 then input(2,b.x>a.x and 'Right' or 'Left')end",''),
        ("if age>=112 and age<116 then input(2,'Low Kick')end",
         "if age>=112 and age<116 then input(1,'Low Punch')end"),
        ('physical_sweep_presentation','physical_cross_throw_presentation')):
        assert lua.count(before)==1;lua=lua.replace(before,after)
    extra=(scalar/'prepared_observer.lua').read_text()
    marker='local throw_dispatch_taps={}'
    assert extra.count(marker)==1;lua+=extra[extra.index(marker):]
    assert ':write_' not in lua
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter,victim in (('sonya','kano'),('kano','sonya')):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_sweep_presentation_runtime',
                              f'audit_bounded_{fighter}_cross_throw_presentation_runtime')
        runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_VICTIM='kitana'",
                              f"$env:MK2KS_HUMAN_SPECIAL_VICTIM='{victim}'")
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
