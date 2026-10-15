"""Physical stock Kitana/Liu victims, same original Kung Lao split command."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_kung_lao_split_voice_preparation'
    out=sync.ROOT/'audit_bounded_stock_split_voice_preparation';assert not out.exists();out.mkdir()
    target=out/'prepared_observer.lua';target.write_text((old/'prepared_observer.lua').read_text())
    for side in (1,2):
        for fighter in ('kitana','liu_kang'):
            runner=(old/f'run_sonya_p{side}.ps1').read_text().replace(old.name,out.name)
            before="$env:MK2KS_TEST_FIGHTER='sonya'";assert runner.count(before)==1
            runner=runner.replace(before,f"$env:MK2KS_TEST_FIGHTER='{fighter}'")
            runner=runner.replace(f'audit_bounded_sonya_p{side}_kung_lao_split_voice_runtime',f'audit_bounded_stock_{fighter}_p{side}_split_voice_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,stockReferenceOnly=True,actualVictims=['kitana','liu_kang'],observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
