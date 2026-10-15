"""Preserve failed observer; fix only extra call-closing parenthesis."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_p2_stock_effect_clip_census_preparation'
    out=sync.ROOT/'audit_bounded_p2_stock_effect_clip_census_syntax_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    before='reg(0),eligible,count-eligible)))';assert text.count(before)==1
    text=text.replace(before,'reg(0),eligible,count-eligible))')
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_p2_{fighter}_stock_effect_clip_census_runtime',f'audit_bounded_p2_{fighter}_stock_effect_clip_census_syntax_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
