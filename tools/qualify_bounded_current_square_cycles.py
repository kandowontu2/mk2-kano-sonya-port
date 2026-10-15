"""Ground-target square activation/recovery; explicitly not contact proof."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
source=prior.read_text()
for before,after in [
    ('audit_bounded_current_knife_cycles_checked','audit_bounded_current_square_cycles_observed'),
    ('audit_bounded_current_special_cycles_knife_p','audit_bounded_current_special_cycles_square_p'),
    ("=='17'","=='18'"),('FFFFB000','FFFFCA00'),('FFFFB010','FFFFCA10'),
    ('nativeDamagePerCycle=22','nativeDamagePerCycle=0,contactVerified=False'),('Kano knife','Sonya ground-target square')]:
    assert before in source;source=source.replace(before,after)
marker="    assert len(damage)==2 and all(int(r['before'])-int(r['after'])==22 and r['pc']=='FF836700' for r in damage)"
assert source.count(marker)==1
source=source.replace(marker,"    assert not damage and len(events)==2\n    for command,activation in zip(rows['COMMAND'],events):\n        assert int(activation['frame'])-int(command['frame'])==8")
source=source.replace('collision damage and ordinary follow-up/idle','activation and ordinary follow-up/idle; contact/damage not proven')
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
