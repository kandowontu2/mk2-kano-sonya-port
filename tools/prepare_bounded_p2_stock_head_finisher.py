"""Opposite physical player slot, unchanged native earned-round inputs."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_audio_route_preparation'
    out=sync.ROOT/'audit_bounded_p2_stock_head_finisher_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        needle="$env:MK2KS_CAMPAIGN_SIDE='1'";assert runner.count(needle)==1
        runner=runner.replace(needle,"$env:MK2KS_CAMPAIGN_SIDE='2'")
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_audio_route_runtime',
                              f'audit_bounded_p2_{fighter}_stock_head_finisher_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
