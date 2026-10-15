"""Earn original Kung Lao FFF LK at gap112 against real added victims."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_kitana_kiss_finisher_preparation'
    out=sync.ROOT/'audit_bounded_kung_lao_split_finisher_preparation';assert not out.exists();out.mkdir()
    target=out/'prepared_observer.lua';target.write_text((old/'prepared_observer.lua').read_text())
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
            for before,after in [("$env:MK2KS_STOCK_KILLER='kitana'","$env:MK2KS_STOCK_KILLER='kung_lao'"),("$env:MK2KS_STOCK_COMMAND='ffdf_lk_release'","$env:MK2KS_STOCK_COMMAND='fff_lk'"),("$env:MK2KS_STOCK_GAP='64'","$env:MK2KS_STOCK_GAP='112'"),("$env:MK2KS_CAMPAIGN_SIDE='1'",f"$env:MK2KS_CAMPAIGN_SIDE='{side}'")]:
                assert runner.count(before)==1;runner=runner.replace(before,after)
            runner=runner.replace(f'audit_bounded_{fighter}_kitana_kiss_finisher_runtime',f'audit_bounded_{fighter}_p{side}_kung_lao_split_finisher_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
