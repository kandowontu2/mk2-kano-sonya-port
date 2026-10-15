"""Opposite-slot Jax scalar FIFO census, bounded through native completion."""
import json
import verify_native_source_sync as sync
from prepare_bounded_stock_head_effect_census import TAIL

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_p2_jax_clap_audio_route_preparation'
    out=sync.ROOT/'audit_bounded_p2_jax_draw_census_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+TAIL.replace('frame-action_start>174','frame-action_start>188')
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_p2_{fighter}_jax_clap_audio_route_runtime',f'audit_bounded_p2_{fighter}_jax_draw_census_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
