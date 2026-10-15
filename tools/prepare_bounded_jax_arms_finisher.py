"""Physical Jax BBBB LP at original gap96; no assistance or media."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_clap_finisher_preparation'
    out=sync.ROOT/'audit_bounded_jax_arms_finisher_preparation';assert not out.exists();out.mkdir()
    target=out/'prepared_observer.lua';target.write_text((old/'prepared_observer.lua').read_text())
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace("$env:MK2KS_STOCK_COMMAND='fff_lp_release'","$env:MK2KS_STOCK_COMMAND='bbbb_lp'")
        runner=runner.replace("$env:MK2KS_STOCK_GAP='64'","$env:MK2KS_STOCK_GAP='96'")
        runner=runner.replace(f'audit_bounded_{fighter}_jax_clap_finisher_runtime',f'audit_bounded_{fighter}_jax_arms_finisher_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
