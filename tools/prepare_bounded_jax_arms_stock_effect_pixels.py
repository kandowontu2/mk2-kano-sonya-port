"""Independent stock blood source union; duplicate-safe native pixel observer."""
import json,re
import verify_native_source_sync as sync
from prepare_bounded_jax_arm_prop_pixels import PALETTE

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_arm_prop_pixels_preparation'
    out=sync.ROOT/'audit_bounded_jax_arms_stock_effect_pixels_preparation';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_jax_arms_nonphysical_sources/report.json').read_text());assert proof['passed']
    sources={s for case in proof['results'].values() for actor in case['stockEffectActors'].values() for s in actor['sources']}
    assert sources and all(0x04000000<=int(s,16)<0x05000000 for s in sources)
    text=(old/'prepared_observer.lua').read_text()
    table='local clap_effect_sources={'+','.join('[0x'+s+']=true' for s in sorted(sources))+'}'
    text,count=re.subn(r'local clap_effect_sources=\{[^\n]+\}',lambda m:table,text);assert count==1
    assert text.count(PALETTE)==1;text=text.replace(PALETTE,'')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace(f'audit_bounded_{fighter}_p{side}_jax_arm_prop_pixels_runtime',f'audit_bounded_{fighter}_p{side}_jax_arms_stock_effect_pixels_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,sources=sorted(sources),observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
