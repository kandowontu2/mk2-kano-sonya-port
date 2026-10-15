"""Observe physical FIFO through native completion plus120, no media."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_kitana_kiss_draw_census_preparation'
    out=sync.ROOT/'audit_bounded_kitana_kiss_cleanup_census_preparation'
    assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    before='frame-action_start>276';assert text.count(before)==1
    text=text.replace(before,'frame-action_start>396')
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace('kitana_kiss_draw_census_runtime','kitana_kiss_cleanup_census_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
