"""Real Sonya selection and ordinary reactive kicks; never choose CPU state."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_voice_hit_pcm_window_preparation'
    out=sync.ROOT/'audit_bounded_sonya_natural_counter_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    before="assert(human=='kano','This distinct policy is the physical Kano uppercut probe')"
    assert source.count(before)==1
    source=source.replace(before,"assert(human=='sonya','Physical Sonya counter probe')")
    before='a.id==17 and a.hp>0';assert source.count(before)==1
    source=source.replace(before,'a.id==18 and a.hp>0')
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {
        old.name:out.name,
        'audit_bounded_voice_hit_pcm_window_runtime':'audit_bounded_sonya_natural_counter_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer),
        "$env:MK2KS_TEST_FIGHTER='kano'":"$env:MK2KS_TEST_FIGHTER='sonya'",
    }.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),forcedOpponent=False,rawMedia=False,acceptance=False)))

if __name__=='__main__':main()
