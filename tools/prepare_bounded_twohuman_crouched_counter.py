"""No walking: physical Down buildup followed by High Punch."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_counter_action_writes_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_crouched_counter_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    before="if age<8 then input(3-side,victim.x<own.x and 'Right' or 'Left')\n   elseif age<20 then\n    input(3-side,'Down');if age>=14 and age<18 then input(3-side,'High Punch')end\n   end"
    assert source.count(before)==1
    source=source.replace(before,"if age<30 then\n    input(3-side,'Down');if age>=14 and age<18 then input(3-side,'High Punch')end\n   end")
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {old.name:out.name,
        'audit_bounded_twohuman_counter_action_writes_runtime':'audit_bounded_twohuman_crouched_counter_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
