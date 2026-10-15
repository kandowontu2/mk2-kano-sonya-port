"""Extend the existing physical kiss replay with passive DCS delivery taps."""
import json
import verify_native_source_sync as sync
from prepare_bounded_kung_lao_split_dcs_delivery import TAIL

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_kitana_kiss_voice_priority_preparation'
    out=sync.ROOT/'audit_bounded_kitana_kiss_dcs_delivery_preparation'
    assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()+TAIL
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):
        assert banned not in source
    out.mkdir(); target=out/'prepared_observer.lua'; target.write_text(source)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
            runner=runner.replace(old.name,out.name).replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace('kitana_kiss_voice_priority_runtime','kitana_kiss_dcs_delivery_runtime')
            assert 'kitana_kiss_dcs_delivery_runtime' in runner
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
