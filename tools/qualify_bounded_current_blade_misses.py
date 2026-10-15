"""Preserve far-grab gate's health/identity/ordinary control/idle checks."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_bounded_current_grab_misses.py')
source=prior.read_text()
for before,after in {
 "('17','FFF91400',8) if move=='choke' else ('18','FFF80800',5)":"('17','FFF8CC00',8)",
 "for move in ('choke','leg'):":"for move in ('blade',):",
 'audit_bounded_current_grab_misses_checked':'audit_bounded_current_blade_misses_checked',
 'audit_bounded_current_grab_miss_{move}_p{side}_runtime':'audit_bounded_current_blade_miss_p{side}_runtime',
 'Four current-build physical far choke/leg whiffs':'Two current-build physical far knife-uppercut whiffs',
 'checkerSHA256=sync.sha(Path(__file__)),':'checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),',
 'contexts=4':'contexts=2'
}.items():
    assert before in source;source=source.replace(before,after)
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
