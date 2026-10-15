"""Natural campaign experiment, exact old prefix before physical policy switch."""
from pathlib import Path
from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_bounded_kano_campaign_reactive_p1_runtime'
baseline=sync.ROOT/'audit_bounded_compact_kano_campaign_p1_runtime'
text=(case/'run.log').read_text();old=(baseline/'run.log').read_text()
prefix='MK2_NAT_CAMPAIGN_'
cutoff=int(fields(next(line for line in old.splitlines() if line.startswith(prefix+'STAGE') and fields(line)['stage']=='3'))['frame'])
def early(value): return [line for line in value.splitlines() if line.startswith(prefix) and int(fields(line)['frame'])<cutoff]
assert early(text)==early(old),'Earlier physical/gameplay/input-digest prefix changed'
policy=[fields(line) for line in text.splitlines() if line.startswith(prefix+'POLICY')]
assert policy and policy[0]['stage']=='3' and policy[0]['physical_policy']=='reactive_jumpkick'
original=Path(__file__).with_name('qualify_bounded_campaign_progress.py')
source=original.read_text()
changes={"'audit_bounded_campaign_progress_checked'":"'audit_bounded_kano_campaign_reactive_checked'","for fighter in ('kano','sonya'):":"for fighter in ('kano',):",'for side in (1,2):':'for side in (1,):',"f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime'":"'audit_bounded_kano_campaign_reactive_p1_runtime'","result['frame']=='12000'":"result['frame']=='18000'",'contexts=4':'contexts=1'}
for before,after in changes.items():
    assert before in source
    source=source.replace(before,after)
source=source.replace('Four current cold physical campaigns bounded at12000 fields. Genuine round wins/stage advancement/paid losses/reselection. SonyaP2 did not clear first opponent. No bosses, ending, full audio/art or whole-port acceptance.','Current Kano P1 physical reactive policy from natural stage3; earlier zoning/gameplay/input digests exactly unchanged. Original earned progression/paid reselect gates retained. Bounded experiment, not full campaign/art/audio/release acceptance.')
exec(compile(source,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})
print('Exact old prefix through stage3 arrival; later controller policy only changes normal inputs')
