"""Native two-slot close-special gates; no older executable acceptance."""
import argparse
from pathlib import Path
import verify_native_source_sync as sync
arg=argparse.ArgumentParser();arg.add_argument('move',choices=('blade','choke'));move=arg.parse_args().move
entry,damage=('FFF8CC00',26) if move=='blade' else ('FFF91400',32)
prior=Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
source=prior.read_text()
for before,after in [
    ('audit_bounded_current_knife_cycles_checked',f'audit_bounded_current_{move}_cycles_checked'),
    ('audit_bounded_current_special_cycles_knife_p',f'audit_bounded_current_special_cycles_{move}_p'),
    ('FFFFB000',entry),('FFFFB010',f'{int(entry,16)+16:08X}'),
    ('==22',f'=={damage}'),('nativeDamagePerCycle=22',f'nativeDamagePerCycle={damage}'),
    ('Kano knife',f'Kano {move}')]:
    assert before in source;source=source.replace(before,after)
marker="    fields=rows['FIELD'];own=[r for r in fields if r['slot']==str(side)]"
assert source.count(marker)==1
source=source.replace(marker,"""    assert len(events)==2
    for command,activation,recovery in zip(rows['COMMAND'],events,rows['RECOVERED']):
        assert activation['attempt']==command['attempt']==recovery['attempt']
        assert int(activation['frame'])-int(command['frame'])==8
        assert int(recovery['frame'])>int(activation['frame'])+12
"""+marker)
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorCheckerSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
