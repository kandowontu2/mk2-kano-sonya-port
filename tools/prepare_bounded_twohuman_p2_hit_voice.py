"""Identical physical command/counter, genuinely swapped selected slots."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_hit_voice_state_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_p2_hit_voice_preparation';assert not out.exists()
    runner=(old/'run.ps1').read_text()
    for before,after in {
        'audit_bounded_twohuman_hit_voice_state_runtime':'audit_bounded_twohuman_p2_hit_voice_runtime',
        "MK2KS_HUMAN_SPECIAL_SIDE='1'":"MK2KS_HUMAN_SPECIAL_SIDE='2'",
    }.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    out.mkdir();(out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(old/'prepared_observer.lua'),onlySelectedPhysicalSideChanged=True,rawMedia=False)))

if __name__=='__main__':main()
