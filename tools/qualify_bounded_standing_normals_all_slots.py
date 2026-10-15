"""Original action/contact/identity/recovery gates for all four actual slots."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_range_gated_normals.py')
source=prior.read_text()
for before,after in [
 ('audit_bounded_range_gated_normals_checked','audit_bounded_standing_normals_all_slots_checked'),
 ('audit_bounded_range_gated_normals_{move}','audit_bounded_standing_punch_walkin_{move}'),
 ("int(command['gap'])<=48","80<=int(command['gap'])<=112"),
 ('four standing normals with actual collision/damage','four standing normals, physical opponent walk-in for punches, actual collision/damage')]:
    assert before in source
    source=source.replace(before,after)
marker="        damage[str(index)]=sum(int(r['before'])-int(r['after']) for r in hits)"
assert source.count(marker)==1
source=source.replace(marker,marker+'''
        assert damage[str(index)]==[11,8,32,26][index-1]
        if index<=2:
            requests=[r for r in rows['INPUT'] if r['slot']==str(3-side) and begin<=int(r['frame'])<begin+8]
            assert len(requests)==8 and all(r['button'] in ('Left','Right') for r in requests)
''')
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
