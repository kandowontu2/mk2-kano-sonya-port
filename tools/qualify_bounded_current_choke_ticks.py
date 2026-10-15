"""Choke has four native eight-point ticks per physical activation."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
failed=Path(__file__).with_name('qualify_bounded_current_kano_close_cycles.py')
source=prior.read_text()
for before,after in [
    ('audit_bounded_current_knife_cycles_checked','audit_bounded_current_choke_ticks_checked'),
    ('audit_bounded_current_special_cycles_knife_p','audit_bounded_current_special_cycles_choke_p'),
    ('FFFFB000','FFF91400'),('FFFFB010','FFF91410'),('nativeDamagePerCycle=22','nativeDamagePerCycle=32'),
    ('Kano knife','Kano choke')]:
    assert before in source;source=source.replace(before,after)
marker="    assert len(damage)==2 and all(int(r['before'])-int(r['after'])==22 and r['pc']=='FF836700' for r in damage)"
assert source.count(marker)==1
source=source.replace(marker,"""    assert len(damage)==8
    assert len(events)==2
    for attempt in ('1','2'):
        ticks=[r for r in damage if r['attempt']==attempt]
        assert len(ticks)==4
        assert all(int(r['before'])-int(r['after'])==8 and r['pc']=='FF836700' for r in ticks)
        assert all(a['after']==b['before'] and int(b['frame'])-int(a['frame'])==12 for a,b in zip(ticks,ticks[1:]))
        activation=next(r for r in events if r['attempt']==attempt)
        command=next(r for r in rows['COMMAND'] if r['attempt']==attempt)
        recovery=next(r for r in rows['RECOVERED'] if r['attempt']==attempt)
        assert int(activation['frame'])-int(command['frame'])==8
        assert int(activation['frame'])<int(ticks[0]['frame'])<int(ticks[-1]['frame'])<int(recovery['frame'])
""")
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),failedSingleWriteCheckerSHA256=sync.sha(failed),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior,failed=failed))
