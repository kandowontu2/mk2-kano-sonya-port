"""Same corrected observer and caps, Kano physical earned-round case."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_effect_duplicate_queue_preparation'
    out=sync.ROOT/'audit_bounded_kano_stock_effect_duplicate_queue_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    proof=json.loads((sync.ROOT/'audit_bounded_stock_effect_duplicate_queue_checked/report.json').read_text())
    assert proof['passed'] and sync.sha(old/'prepared_observer.lua')==proof['terminal']['observerSha256']
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    runner=(old/'run_sonya.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace('audit_bounded_sonya_stock_effect_duplicate_queue_runtime','audit_bounded_kano_stock_effect_duplicate_queue_runtime')
    runner=runner.replace("$env:MK2KS_TEST_FIGHTER='sonya'","$env:MK2KS_TEST_FIGHTER='kano'")
    (out/'run_kano.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
