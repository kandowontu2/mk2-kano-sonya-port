"""Same two-slot knife gate with explicit Sonya ring native identity/entry."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
source=prior.read_text()
for before,after in [
    ('audit_bounded_current_knife_cycles_checked','audit_bounded_current_ring_cycles_checked'),
    ('audit_bounded_current_special_cycles_knife_p','audit_bounded_current_special_cycles_ring_p'),
    ("=='17'","=='18'"),('FFFFB000','FFFFB400'),('FFFFB010','FFFFB410'),
    ('Kano knife','Sonya ring')]:
    assert before in source;source=source.replace(before,after)
marker="    fields=rows['FIELD'];own=[r for r in fields if r['slot']==str(side)]"
assert source.count(marker)==1
source=source.replace(marker,"""    commands=rows['COMMAND']
    for command,activation,recovery in zip(commands,events,rows['RECOVERED']):
        assert activation['attempt']==command['attempt']==recovery['attempt']
        assert int(activation['frame'])-int(command['frame'])==8
        assert int(recovery['frame'])>int(activation['frame'])+12
    assert len(events)==2
"""+marker)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
