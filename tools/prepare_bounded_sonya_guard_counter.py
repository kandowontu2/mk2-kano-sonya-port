"""Initial real Block input, then existing natural counter policy."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_sonya_natural_counter_preparation'
    out=sync.ROOT/'audit_bounded_sonya_guard_counter_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    before='    if ordinary then\n'
    assert source.count(before)==1
    source=source.replace(before,"    if age<180 then\n        high['P1 Block']:set_value(1);press='block'\n    elseif ordinary then\n")
    # Observe channels throughout gameplay, but limit PCM to the old short window.
    before='    if selection_frame<2500 or selection_frame>2700 then return end'
    assert source.count(before)==1
    source=source.replace(before,'    if not first_live then return end')
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {old.name:out.name,
        'audit_bounded_sonya_natural_counter_runtime':'audit_bounded_sonya_guard_counter_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),physicalInitialGuardFields=180,forcedOpponent=False,rawMedia=False)))

if __name__=='__main__':main()
