"""Keep original natural progression gates; a bounded run is not a clear."""
from pathlib import Path
from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_bounded_kano_campaign_18000_p1_runtime'
old=sync.ROOT/'audit_bounded_campaign_progress_core_kano_p1_runtime'
prefix='MK2_NAT_CAMPAIGN_'
def early(path):
    return [line for line in path.read_text().splitlines() if line.startswith(prefix) and int(fields(line)['frame'])<12000]
assert early(case/'run.log')==early(old/'run.log'),'Early physical campaign changed'
original=Path(__file__).with_name('qualify_bounded_campaign_progress.py')
source=original.read_text()
changes={
    "'audit_bounded_campaign_progress_checked'":"'audit_bounded_kano_campaign_18000_checked'",
    "for fighter in ('kano','sonya'):":"for fighter in ('kano',):",
    'for side in (1,2):':'for side in (1,):',
    "f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime'":"'audit_bounded_kano_campaign_18000_p1_runtime'",
    "result['frame']=='12000'":"result['frame']=='18000'",
    'Four current cold physical campaigns bounded at12000 fields. Genuine round wins/stage advancement/paid losses/reselection. SonyaP2 did not clear first opponent. No bosses, ending, full audio/art or whole-port acceptance.':'Current KanoP1 cold campaign extended to18000 fields, early prefix identical. Original natural win/stage/paid reselect gates retained. Bounded observation, not whole campaign/art/audio/release acceptance.',
    'contexts=4':'contexts=1',
}
for before,after in changes.items():
    assert before in source,before
    source=source.replace(before,after)
exec(compile(source,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})
