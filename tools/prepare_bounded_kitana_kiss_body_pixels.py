"""Full276-field kiss body pixel observer, original physical held-LK command."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_arms_body_pixels_preparation'
    out=sync.ROOT/'audit_bounded_kitana_kiss_body_pixels_preparation';assert not out.exists();out.mkdir()
    text=(old/'prepared_observer.lua').read_text();needle='frame-ready>=1 and frame-ready<=147';assert text.count(needle)==2
    text=text.replace(needle,'frame-ready>=1 and frame-ready<=276')
    target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace("$env:MK2KS_STOCK_KILLER='jax'","$env:MK2KS_STOCK_KILLER='kitana'")
            runner=runner.replace("$env:MK2KS_STOCK_COMMAND='bbbb_lp'","$env:MK2KS_STOCK_COMMAND='ffdf_lk_release'")
            runner=runner.replace("$env:MK2KS_STOCK_GAP='96'","$env:MK2KS_STOCK_GAP='64'")
            runner=runner.replace(f'audit_bounded_{fighter}_p{side}_jax_arms_body_pixels_runtime',f'audit_bounded_{fighter}_p{side}_kitana_kiss_body_pixels_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
