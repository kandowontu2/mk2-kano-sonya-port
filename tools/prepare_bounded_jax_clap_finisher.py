"""Earn Jax clap finisher through existing physical selection/round driver."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_finisher_preparation'
    out=sync.ROOT/'audit_bounded_jax_clap_finisher_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace("$env:MK2KS_STOCK_KILLER='baraka'","$env:MK2KS_STOCK_KILLER='jax'")
        runner=runner.replace("$env:MK2KS_STOCK_COMMAND='bbbb_hp'","$env:MK2KS_STOCK_COMMAND='fff_lp_release'")
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_finisher_runtime',f'audit_bounded_{fighter}_jax_clap_finisher_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
