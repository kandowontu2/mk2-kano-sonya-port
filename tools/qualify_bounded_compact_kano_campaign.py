"""Bind compact inputs to prior complete raw prefix, retaining campaign gates."""
import json
from pathlib import Path
from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_bounded_compact_kano_campaign_p1_runtime'
prior=sync.ROOT/'audit_bounded_kano_campaign_18000_p1_runtime'
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
text=(case/'run.log').read_text();baseline=(prior/'run.log').read_text()
prefix='MK2_NAT_CAMPAIGN_'
old_lines=[line for line in baseline.splitlines() if line.startswith(prefix)]
cutoff=max(int(fields(line)['frame']) for line in old_lines)
def core(value):
    return [line for line in value.splitlines() if line.startswith(prefix) and not line.startswith(prefix+'INPUT') and int(fields(line)['frame'])<cutoff]
assert core(text)==core(baseline),'Non-input gameplay prefix changed'
digests={int(fields(line)['frame']):fields(line) for line in text.splitlines() if line.startswith(prefix+'INPUT_DIGEST ')}
digest=2166136261;events=0;checked=0
inputs=[line for line in old_lines if line.startswith(prefix+'INPUT ')]
index=0
for frame in sorted(digests):
    if frame>=cutoff: break
    while index<len(inputs) and int(fields(inputs[index])['frame'])<=frame:
        line=inputs[index];index+=1
        payload=str(int(fields(line)['frame']))+':'+line.split('assistance=none ',1)[1]
        for byte in payload.encode(): digest=((digest^byte)*16777619)&0xffffffff
        events+=1
    assert int(digests[frame]['events'])==events and int(digests[frame]['fnv32'],16)==digest
    checked+=1
assert checked>=50
assert terminal['peakWorkingSetBytes']<=320*1024**2
assert terminal['exitCode']==0 and terminal['limitReason'] is None
original=Path(__file__).with_name('qualify_bounded_campaign_progress.py')
source=original.read_text()
changes={"'audit_bounded_campaign_progress_checked'":"'audit_bounded_compact_kano_campaign_checked'","for fighter in ('kano','sonya'):":"for fighter in ('kano',):",'for side in (1,2):':'for side in (1,):',"f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime'":"'audit_bounded_compact_kano_campaign_p1_runtime'","result['frame']=='12000'":"result['frame']=='18000'",'contexts=4':'contexts=1'}
for before,after in changes.items():
    assert before in source
    source=source.replace(before,after)
source=source.replace('Four current cold physical campaigns bounded at12000 fields. Genuine round wins/stage advancement/paid losses/reselection. SonyaP2 did not clear first opponent. No bosses, ending, full audio/art or whole-port acceptance.','Kano P1 completed18000-field bounded campaign; compact input digests bind prior raw prefix and non-input observations remain exact. Original natural progression gates retained; not whole campaign/release acceptance.')
exec(compile(source,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})
print('Matched '+str(checked)+' cumulative input digests and exact earlier non-input gameplay')
