"""Physical opponent walking before the earlier counter, not position writes."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_bicycle_early_counter_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_bicycle_approach_counter_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    before="if age>=12 and age<16 then input(3-side,'High Kick')end"
    assert source.count(before)==1
    source=source.replace(before,"if age<12 then input(3-side,victim.x<own.x and 'Right' or 'Left')\n   elseif age<16 then input(3-side,'High Kick')end")
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {old.name:out.name,
        'audit_bounded_twohuman_bicycle_early_counter_runtime':'audit_bounded_twohuman_bicycle_approach_counter_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),physicalApproachFields=12,rawMedia=False)))

if __name__=='__main__':main()
