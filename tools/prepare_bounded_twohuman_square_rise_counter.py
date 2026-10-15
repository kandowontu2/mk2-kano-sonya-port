"""Earlier physical HP against the actual twelve-pixel-per-field rise."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_square_counter_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_square_rise_counter_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    assert source.count('age>=10 and age<14')==1
    source=source.replace('age>=10 and age<14','age>=6 and age<10')
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    for side in (1,2):
        runner=(old/f'run_p{side}.ps1').read_text()
        for before,after in {old.name:out.name,
            f'audit_bounded_twohuman_square_p{side}_counter_runtime':f'audit_bounded_twohuman_square_p{side}_rise_counter_runtime',
            sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
            assert runner.count(before)==1;runner=runner.replace(before,after)
        (out/f'run_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
