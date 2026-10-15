"""Established crouch with earlier physical punch, no guest state changes."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_crouched_counter_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_crouched_early_punch_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    assert source.count('age>=14 and age<18')==1
    source=source.replace('age>=14 and age<18','age>=10 and age<14')
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {old.name:out.name,
        'audit_bounded_twohuman_crouched_counter_runtime':'audit_bounded_twohuman_crouched_early_punch_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
