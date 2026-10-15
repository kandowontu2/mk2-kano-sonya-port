"""P2 selected stock effects, full source VRAM and duplicate-safe queue."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_effect_duplicate_queue_preparation'
    out=sync.ROOT/'audit_bounded_p2_stock_effect_pixels_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    needle='local a=sample(slot)';assert text.count(needle)==1
    text=text.replace(needle,'local a=sample(3-slot)')
    needle='if dx<400 and dx>=actual_dma[16]';assert text.count(needle)==1
    text=text.replace(needle,'if dx<512 and dx>=actual_dma[16]')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/'run_sonya.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace("$env:MK2KS_CAMPAIGN_SIDE='1'","$env:MK2KS_CAMPAIGN_SIDE='2'")
        runner=runner.replace("$env:MK2KS_TEST_FIGHTER='sonya'",f"$env:MK2KS_TEST_FIGHTER='{fighter}'")
        runner=runner.replace('audit_bounded_sonya_stock_effect_duplicate_queue_runtime',f'audit_bounded_p2_{fighter}_stock_effect_pixels_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,physicalVictimSlot=2,observerBucket=1,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
