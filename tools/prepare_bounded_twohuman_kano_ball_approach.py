"""Opponent physically reapproaches after native initial-kick knockback."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_kano_ball_counter_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_kano_ball_approach_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    before="if age<110 then\n    input(3-side,'Down');if age>=80 and age<84 then input(3-side,'High Punch')end\n   end"
    assert source.count(before)==1
    source=source.replace(before,"if age<65 then\n    if math.abs(own.x-victim.x)>48 then input(3-side,victim.x<own.x and 'Right' or 'Left')end\n   elseif age<110 then\n    input(3-side,'Down');if age>=80 and age<84 then input(3-side,'High Punch')end\n   end")
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    for side in (1,2):
        runner=(old/f'run_p{side}.ps1').read_text()
        for before,after in {old.name:out.name,
            f'audit_bounded_twohuman_kano_ball_p{side}_counter_runtime':f'audit_bounded_twohuman_kano_ball_p{side}_approach_runtime',
            sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
            assert runner.count(before)==1;runner=runner.replace(before,after)
        (out/f'run_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
