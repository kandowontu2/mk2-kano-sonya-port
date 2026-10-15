"""Reuse identical scalar observer with physically reversed selected roles."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_pcm_boundary_frames_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_p2_hit_pcm_preparation';assert not out.exists()
    out.mkdir()
    for label in ('samples','nosamples'):
        runner=(old/f'run_{label}.ps1').read_text()
        for before,after in {
            f'audit_bounded_twohuman_pcm_boundary_frames_{label}_runtime':f'audit_bounded_twohuman_p2_hit_pcm_{label}_runtime',
            "MK2KS_HUMAN_SPECIAL_SIDE='1'":"MK2KS_HUMAN_SPECIAL_SIDE='2'",
        }.items():
            assert runner.count(before)==1;runner=runner.replace(before,after)
        (out/f'run_{label}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(old/'prepared_observer.lua'),rawMedia=False)))

if __name__=='__main__':main()
