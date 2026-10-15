"""Retain every identical FIFO entry instead of consuming its shared key once."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_effect_mapping_preparation'
    out=sync.ROOT/'audit_bounded_stock_effect_duplicate_queue_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    needle='assert(not idle_owned[key]);idle_owned[key]={slot=slot,id=a.id,pose=a.pose}'
    assert text.count(needle)==1
    text=text.replace(needle,'local prior=idle_owned[key];if prior then prior.count=prior.count+1 else idle_owned[key]={slot=slot,id=a.id,pose=a.pose,count=1}end')
    needle='idle_owned[key]=nil';assert text.count(needle)==1
    text=text.replace(needle,'own.count=own.count-1;if own.count==0 then idle_owned[key]=nil end')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    runner=(old/'run_sonya.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace('audit_bounded_sonya_stock_effect_mapping_runtime','audit_bounded_sonya_stock_effect_duplicate_queue_runtime')
    (out/'run_sonya.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
