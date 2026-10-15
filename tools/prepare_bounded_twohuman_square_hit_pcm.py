"""Square hit paired mixed-output hashes, transient raw update strings only."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_square_rise_counter_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_square_hit_pcm_preparation';assert not out.exists()
    donor=(sync.ROOT/'audit_bounded_twohuman_hit_pcm_preparation/prepared_observer.lua').read_text()
    tail=donor[donor.index('local human_hit_updates=0'):]
    source=(old/'prepared_observer.lua').read_text()+(sync.ROOT/'tools/bounded_pcm_sha256.lua').read_text()+tail
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    for side in (1,2):
        for label in ('samples','nosamples'):
            runner=(old/f'run_p{side}.ps1').read_text()
            for before,after in {old.name:out.name,
                f'audit_bounded_twohuman_square_p{side}_rise_counter_runtime':f'audit_bounded_twohuman_square_p{side}_pcm_{label}_runtime',
                sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
                assert runner.count(before)==1;runner=runner.replace(before,after)
            if label=='nosamples':
                assert runner.count("'-samples'")==1;runner=runner.replace("'-samples'","'-nosamples'")
            (out/f'run_p{side}_{label}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
