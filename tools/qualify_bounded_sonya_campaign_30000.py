"""Original native identity, earned-win and paid-continue gates at 30000."""
from pathlib import Path
import verify_native_source_sync as sync
predecessor=Path(__file__).with_name('qualify_bounded_campaign_progress.py')
source=predecessor.read_text()
for before,after in [
 ('audit_bounded_campaign_progress_checked','audit_bounded_sonya_campaign_30000_checked'),
 ("for fighter in ('kano','sonya'):","for fighter in ('sonya',):"),
 ('for side in (1,2):','for side in (1,):'),
 ("f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime'","f'audit_bounded_sonya_campaign_30000_p{side}_runtime'"),
 ('12000','30000'),
 ('Four current cold physical campaigns','One current cold Sonya P1 physical campaign'),
 ('SonyaP2 did not clear first opponent.','No claims about other slots or characters.'),
 ('contexts=4','contexts=1')]:
    assert before in source
    source=source.replace(before,after)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(predecessor),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,predecessor=predecessor))
