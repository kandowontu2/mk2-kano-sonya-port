"""Original campaign gates; distinguish emulator timed exit from host bound."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_campaign_progress.py')
source=prior.read_text()
changes=[
 ('audit_bounded_campaign_progress_checked','audit_extended_sonya_campaign_timed_terminal_checked'),
 ("for fighter in ('kano','sonya'):","for fighter in ('sonya',):"),
 ('for side in (1,2):','for side in (1,):'),
 ("f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime'","f'audit_bounded_extended_sonya_campaign_p{side}_runtime'"),
 ("assert len(rows['HOST_BOUND'])==len(rows['RESULT'])==1","assert not rows.get('HOST_BOUND') and len(rows['RESULT'])==1"),
 ("result['frame']=='12000'","result['frame']=='16413'"),
 ('Four current cold physical campaigns bounded at12000 fields.','One cold Sonya P1 physical campaign ended at emulator 300-second limit, field16413; no host bound reached.'),
 ('SonyaP2 did not clear first opponent.','No claim about other slots.'),
 ('contexts=4','contexts=1')]
for before,after in changes:
    assert before in source
    source=source.replace(before,after)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
