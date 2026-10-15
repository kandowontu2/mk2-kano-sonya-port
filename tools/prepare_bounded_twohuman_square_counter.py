"""Real Square command and physical crouched counter, no forced state."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_hit_voice_state_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_square_counter_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    before="pulse(side,backward,age,0,3);pulse(side,backward,age,6,3);pulse(side,'Down',age,12,3);pulse(side,'High Kick',age,13,3)"
    assert source.count(before)==1
    source=source.replace(before,"pulse(side,forward,age,0,3);pulse(side,backward,age,5,3);pulse(side,'High Punch',age,6,3)")
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    for side in (1,2):
        runner=(old/'run.ps1').read_text()
        for before,after in {old.name:out.name,
            'audit_bounded_twohuman_hit_voice_state_runtime':f'audit_bounded_twohuman_square_p{side}_counter_runtime',
            sync.sha(old/'prepared_observer.lua'):sync.sha(observer),
            "MK2KS_HUMAN_SPECIAL_MOVE='bicycle'":"MK2KS_HUMAN_SPECIAL_MOVE='square'"}.items():
            assert runner.count(before)==1;runner=runner.replace(before,after)
        if side==2:runner=runner.replace("MK2KS_HUMAN_SPECIAL_SIDE='1'","MK2KS_HUMAN_SPECIAL_SIDE='2'")
        (out/f'run_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
