"""Earned original split, scalar native voice/priority/port bytes."""
import json
import verify_native_source_sync as sync
from prepare_bounded_stock_head_audio_route import TAIL as AUDIO
from prepare_bounded_p2_voice_selector import TAIL as SELECTOR
from prepare_bounded_p2_jax_voice_priority import QUEUE

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_kung_lao_split_finisher_preparation'
    out=sync.ROOT/'audit_bounded_kung_lao_split_voice_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+AUDIO+SELECTOR+QUEUE
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace('kung_lao_split_finisher_runtime','kung_lao_split_voice_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
