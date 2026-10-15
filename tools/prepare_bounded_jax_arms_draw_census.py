"""All native FIFO actors through147-field arm-rip, both physical slots."""
import json
import verify_native_source_sync as sync
from prepare_bounded_stock_head_effect_census import TAIL

def main():
    sync.verify();out=sync.ROOT/'audit_bounded_jax_arms_draw_census_preparation';assert not out.exists();out.mkdir()
    old=sync.ROOT/'audit_bounded_jax_arms_finisher_preparation'
    text=(old/'prepared_observer.lua').read_text()+TAIL.replace('frame-action_start>174','frame-action_start>147')
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace("$env:MK2KS_CAMPAIGN_SIDE='1'",f"$env:MK2KS_CAMPAIGN_SIDE='{side}'")
            runner=runner.replace(f'audit_bounded_{fighter}_jax_arms_finisher_runtime',f'audit_bounded_{fighter}_p{side}_jax_arms_draw_census_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
