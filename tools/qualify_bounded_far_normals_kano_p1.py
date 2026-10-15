"""Original normal action/contact gates, one actual wider-range slot."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_range_gated_normals.py')
source=prior.read_text()
for before,after in [
 ('audit_bounded_range_gated_normals_checked','audit_bounded_far_normals_kano_p1_checked'),
 ('audit_bounded_range_gated_normals_{move}','audit_bounded_far_normal_contacts_{move}'),
 ("[('knife','17'),('ring','18')]","[('knife','17')]"),
 ('for side in (1,2):','for side in (1,):'),
 ("int(command['gap'])<=48","64<=int(command['gap'])<=80"),
 ('Four true-ID physical slot cases','One true-ID Kano P1 physical case'),
 ('contexts=4,normalContacts=16','contexts=1,normalContacts=4')]:
    assert before in source
    source=source.replace(before,after)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
