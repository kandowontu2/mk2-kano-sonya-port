"""Opposite-slot body source footprints, full observed action window."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_body_completion_preparation'
    out=sync.ROOT/'audit_bounded_p2_stock_head_body_pixels_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_p2_stock_head_control_checked/report.json').read_text())
    assert proof['passed'] and {r['nativeWrapFrame']-r['nativeActionFrame'] for r in proof['results'].values()}=={174}
    text=(old/'prepared_observer.lua').read_text()
    needle='frame-ready>=61 and frame-ready<=174';assert text.count(needle)==2
    text=text.replace(needle,'frame-ready>=1 and frame-ready<=174')
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace("$env:MK2KS_CAMPAIGN_SIDE='1'","$env:MK2KS_CAMPAIGN_SIDE='2'")
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_body_completion_runtime',
                              f'audit_bounded_p2_{fighter}_stock_head_body_pixels_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,actionAges=[1,174],observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
