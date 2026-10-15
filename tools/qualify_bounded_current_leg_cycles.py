"""Physical D+LP+Block leg grab, correct entry, damage and settled controls."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
source=prior.read_text()
for before,after in [
    ('audit_bounded_current_knife_cycles_checked','audit_bounded_current_leg_cycles_checked'),
    ('audit_bounded_current_special_cycles_knife_p','audit_bounded_current_special_cycles_leg_p'),
    ("=='17'","=='18'"),('FFFFB000','FFF80800'),('FFFFB010','FFF80810'),
    ('==22','==35'),('nativeDamagePerCycle=22','nativeDamagePerCycle=35'),('Kano knife','Sonya leg grab')]:
    assert before in source;source=source.replace(before,after)
marker="    fields=rows['FIELD'];own=[r for r in fields if r['slot']==str(side)]"
assert source.count(marker)==1
source=source.replace(marker,"""    assert len(events)==2
    for command,activation,recovery in zip(rows['COMMAND'],events,rows['RECOVERED']):
        base=int(command['frame']);launch=int(activation['frame'])
        assert launch-base==5 and int(recovery['frame'])>launch+12
        expected=[]
        for start,hold,button in [(0,7,'Down'),(3,4,'Low_Punch'),(3,4,'Block')]:
            expected.extend((base+age,button) for age in range(start,start+hold))
        actual=[(int(r['frame']),r['button']) for r in rows['INPUT'] if r['slot']==str(side) and base<=int(r['frame'])<base+7]
        assert sorted(actual)==sorted(expected)
"""+marker)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
