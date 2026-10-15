"""Genuinely selected stock Kitana reference, same physical arm-rip driver."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_jax_arms_voice_priority_preparation'
    out=sync.ROOT/'audit_bounded_stock_kitana_jax_arm_voice_preparation';assert not out.exists();out.mkdir()
    target=out/'prepared_observer.lua';target.write_text((old/'prepared_observer.lua').read_text())
    for side in (1,2):
        runner=(old/f'run_sonya_p{side}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace("$env:MK2KS_TEST_FIGHTER='sonya'","$env:MK2KS_TEST_FIGHTER='kitana'")
        runner=runner.replace(f'audit_bounded_sonya_p{side}_jax_arms_voice_priority_runtime',f'audit_bounded_stock_kitana_p{side}_jax_arm_voice_runtime')
        (out/f'run_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,actualVictim='kitana',stockReferenceOnly=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
