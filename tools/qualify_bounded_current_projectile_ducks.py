"""Require physical crouch throughout projectile passage and zero damage."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_bounded_current_grab_misses.py')
source=prior.read_text()
for before,after in {
 "('17','FFF91400',8) if move=='choke' else ('18','FFF80800',5)":"('17','FFFFB000',8) if move=='knife' else ('18','FFFFB400',8)",
 "for move in ('choke','leg'):":"for move in ('knife','ring'):",
 'audit_bounded_current_grab_misses_checked':'audit_bounded_current_projectile_ducks_checked',
 'audit_bounded_current_grab_miss_{move}_p{side}_runtime':'audit_bounded_current_projectile_duck_{move}_p{side}_runtime',
 'physical far choke/leg whiffs':'physical crouch knife/ring misses',
 'checkerSHA256=sync.sha(Path(__file__)),':'checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),'
}.items():
    assert before in source;source=source.replace(before,after)
marker="    assert not rows.get('HEALTH',[])"
source=source.replace(marker,marker+"""
    down=[r for r in rows['INPUT'] if r['slot']==str(3-side) and r['button']=='Down' and base<=int(r['frame'])<base+220]
    assert [int(r['frame']) for r in down]==list(range(base,base+220))
    assert any(r['slot']==str(3-side) and r['action']=='1793' and base<=int(r['frame'])<base+220 for r in rows['FIELD'])
""")
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
