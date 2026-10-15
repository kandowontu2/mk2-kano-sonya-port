"""Require physical opponent jumps, actual airborne contact and native damage."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
source=prior.read_text()
for before,after in [
    ('audit_bounded_current_knife_cycles_checked','audit_bounded_current_square_air_contact_checked'),
    ('audit_bounded_current_special_cycles_knife_p{side}_runtime','audit_bounded_current_square_air_cycles_p{side}_runtime'),
    ("=='17'","=='18'"),('FFFFB000','FFFFCA00'),('FFFFB010','FFFFCA10'),
    ('==22','==27'),('nativeDamagePerCycle=22','nativeDamagePerCycle=27'),('Kano knife','Sonya square airborne contact')]:
    assert before in source;source=source.replace(before,after)
marker="    last=own[-1];assert last['y']==last['floor'] and last['action']=='771'"
assert source.count(marker)==1
source=source.replace(marker,"""    assert len(events)==2
    for command,activation,recovery,hit in zip(rows['COMMAND'],events,rows['RECOVERED'],damage):
        base=int(command['frame']);at=int(hit['frame'])
        assert int(activation['frame'])-base==8
        assert int(activation['frame'])<=at<int(recovery['frame'])
        jumps=[r for r in rows['INPUT'] if r['slot']==str(3-side) and r['attempt']==command['attempt'] and r['button']=='Up']
        assert [int(r['frame']) for r in jumps]==list(range(base,base+3))
        assert any(r['slot']==str(3-side) and r['y']!=r['floor'] and at-2<=int(r['frame'])<=at for r in fields)
        assert any(r['slot']==str(side) and r['y']!=r['floor'] and at-2<=int(r['frame'])<=at for r in fields)
"""+marker)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
