"""Remaining body draw window up to observed native common completion."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_body_middle_preparation'
    out=sync.ROOT/'audit_bounded_stock_head_body_completion_preparation';assert not out.exists()
    prior=json.loads((sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked/report.json').read_text())
    ends={r['nativeWrapFrame']-r['nativeActionFrame'] for r in prior['results'].values()}
    assert prior['passed'] and ends=={174}
    text=(old/'prepared_observer.lua').read_text()
    needle='frame-ready>=31 and frame-ready<=60';assert text.count(needle)==2
    text=text.replace(needle,'frame-ready>=61 and frame-ready<=174')
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_body_middle_runtime',
                              f'audit_bounded_{fighter}_stock_head_body_completion_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,actionAges=[61,174],
        observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
