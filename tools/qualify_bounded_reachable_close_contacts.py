"""Reachable close input selects elbow/throw/kick, not far-normal actions."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_range_gated_normals.py')
source=prior.read_text()
for before,after in [
 ('audit_bounded_range_gated_normals_checked','audit_bounded_reachable_close_contacts_checked'),
 ('audit_bounded_range_gated_normals_{move}','audit_bounded_reachable_normals_exit_{move}'),
 ("int(command['gap'])<=48","int(command['gap'])<=63"),
 ('[257,258,259,260]','[276,1287,271,271]'),
 ('Four true-ID physical slot cases versus Kitana, four standing normals with actual collision/damage and both-actor recovery.',
  'Four true-ID physical slot cases versus Kitana: close HP elbow276, close LP throw1287, close HK/LK kick271, actual collision/damage and both-actor recovery.'),
 ('normalContacts=16','closeContacts=16')]:
    assert before in source
    source=source.replace(before,after)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
