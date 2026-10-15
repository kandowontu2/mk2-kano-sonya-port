"""Held-LK cannonball command and distinct kick/ball collision damage."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
source=prior.read_text()
for before,after in [
    ('audit_bounded_current_knife_cycles_checked','audit_bounded_current_ball_cycles_checked'),
    ('audit_bounded_current_special_cycles_knife_p','audit_bounded_current_special_cycles_ball_p'),
    ('FFFFB000','FFFFDE00'),('FFFFB010','FFFFDE10'),('nativeDamagePerCycle=22','nativeDamagePerCycle=44'),
    ('Kano knife','Kano held-LK cannonball')]:
    assert before in source;source=source.replace(before,after)
marker="    assert len(damage)==2 and all(int(r['before'])-int(r['after'])==22 and r['pc']=='FF836700' for r in damage)"
assert source.count(marker)==1
source=source.replace(marker,"""    assert len(events)==2 and len(damage)==4
    for attempt in ('1','2'):
        command=next(r for r in rows['COMMAND'] if r['attempt']==attempt)
        activation=next(r for r in events if r['attempt']==attempt)
        recovery=next(r for r in rows['RECOVERED'] if r['attempt']==attempt)
        base=int(command['frame']);launch=int(activation['frame'])
        assert launch-base==86
        charge=[r for r in rows['INPUT'] if r['attempt']==attempt and r['slot']==str(side) and r['button']=='Low_Kick']
        assert [int(r['frame']) for r in charge]==list(range(base,base+84))
        hits=[r for r in damage if r['attempt']==attempt]
        assert [int(r['before'])-int(r['after']) for r in hits]==[20,24]
        assert all(r['pc']=='FF836700' for r in hits)
        assert int(hits[0]['frame'])<launch<int(hits[1]['frame'])<int(recovery['frame'])
    assert int(last['flags'],16)&0x1c==0 and int(last['body'],16)&0x0c==0
""")
# The settled-state check must follow construction of the final actor receipt.
source=source.replace("    assert int(last['flags'],16)&0x1c==0 and int(last['body'],16)&0x0c==0\n",'')
marker="    assert all(int(last[k],16)==0 for k in ('vx','vy','gravity','trail'))"
source=source.replace(marker,marker+"\n    assert int(last['flags'],16)&0x1c==0 and int(last['body'],16)&0x0c==0")
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
