"""Require launched standing normals and actual physical walk-in collisions."""
from pathlib import Path
import verify_native_source_sync as sync
parent=Path(__file__).with_name('qualify_bounded_far_normals_range_band_kano.py')
wrapper=parent.read_text()
marker="exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))"
assert wrapper.count(marker)==1
context=dict(__file__=str(parent))
exec(compile(wrapper.split(marker)[0],str(parent),'exec'),context)
source=context['source'].replace('audit_bounded_far_normals_range_band_kano_checked','audit_bounded_standing_punch_walkin_kano_checked')
source=source.replace('audit_bounded_far_normals_range_band_{move}','audit_bounded_standing_punch_walkin_{move}')
source=source.replace('four standing normals with actual collision/damage','four standing normals against physical punch walk-ins with actual collision/damage')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=context['prior']))
