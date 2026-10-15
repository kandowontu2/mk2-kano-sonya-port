"""Retain basic-control gates and require the three native crouching normals."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_basic_controls.py')
source=prior.read_text()
source=source.replace('audit_bounded_current_basic_controls_checked','audit_bounded_current_crouching_attacks_checked')
source=source.replace('audit_bounded_current_basic_controls_{move}', 'audit_bounded_current_crouching_attacks_{move}')
source=source.replace('(424,1793)]:','(424,1793),(452,281),(516,282),(580,263)]:')
source=source.replace('start+500','start+660')
source=source.replace('nativeNormalActions=[257,258,259,260,1792,770,1793]', 'nativeNormalActions=[257,258,259,260,1792,770,1793,281,282,263]')
source=source.replace('crouch-block/jump and final idle.', 'crouch-block/jump, settled crouch LP/LK/uppercut and final idle.')
source=source.replace('throws, crouching attacks, full raster', 'throws, full raster')
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),', 'checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
