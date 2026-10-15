"""Two real Sonya bicycle commands, owned entries and native damage."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
source=prior.read_text()
for before,after in [
    ('audit_bounded_current_knife_cycles_checked','audit_bounded_current_bicycle_cycles_checked'),
    ('audit_bounded_current_special_cycles_knife_p','audit_bounded_current_special_cycles_bicycle_p'),
    ("=='17'","=='18'"),('FFFFB000','FFF9A400'),('FFFFB010','FFF9A410'),('Kano knife','Sonya bicycle')]:
    assert before in source;source=source.replace(before,after)
marker="    fields=rows['FIELD'];own=[r for r in fields if r['slot']==str(side)]"
assert source.count(marker)==1
source=source.replace(marker,"""    assert len(events)==2
    for command,activation,recovery in zip(rows['COMMAND'],events,rows['RECOVERED']):
        assert activation['attempt']==command['attempt']==recovery['attempt']
        base=int(command['frame']);launch=int(activation['frame'])
        assert launch-base==15 and int(recovery['frame'])>launch+12
        backward='Left' if command['forward']=='Right' else 'Right'
        expected=[]
        for start,button in [(0,backward),(6,backward),(12,'Down'),(13,'High_Kick')]:
            expected.extend((base+age,button) for age in range(start,start+3))
        actual=[(int(r['frame']),r['button']) for r in rows['INPUT'] if r['slot']==str(side) and base<=int(r['frame'])<base+16]
        assert sorted(actual)==sorted(expected)
"""+marker)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
