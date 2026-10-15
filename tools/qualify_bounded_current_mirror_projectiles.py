"""Keep original projectile gates and add both-actor mirror identity gates."""
from pathlib import Path
import verify_native_source_sync as sync
prior = Path(__file__).with_name('qualify_bounded_current_knife_cycles.py')
original = prior.read_text()
for move, fighter_id, entry in [('knife', '17', 'FFFFB000'), ('ring', '18', 'FFFFB400')]:
    source = original.replace('audit_bounded_current_knife_cycles_checked', f'audit_bounded_current_mirror_{move}_cycles_checked')
    source = source.replace('audit_bounded_current_special_cycles_knife_p', f'audit_bounded_current_mirror_projectile_{move}_p')
    source = source.replace("=='17'", f"=='{fighter_id}'").replace('FFFFB000', entry).replace('FFFFB010', f'{int(entry,16)+16:08X}')
    marker = "    fields=rows['FIELD'];own=[r for r in fields if r['slot']==str(side)]"
    assert source.count(marker) == 1
    source = source.replace(marker, marker + f'''
    assert len(events)==2
    assert all(r['id']==r['roster']=='{fighter_id}' and r['actor']==r['owner'] for r in fields)
    for command,activation,recovery in zip(rows['COMMAND'],events,rows['RECOVERED']):
        assert command['attempt']==activation['attempt']==recovery['attempt']
        assert int(activation['frame'])-int(command['frame'])==8
        assert int(recovery['frame'])>int(activation['frame'])
    for slot in (1,2):
        final=[r for r in fields if r['slot']==str(slot)][-1]
        assert final['y']==final['floor'] and final['action']=='771'
        assert all(int(final[k],16)==0 for k in ('vx','vy','gravity','trail'))
''')
    source = source.replace('Kano knife', f'{move} mirror').replace('versus Kitana', f'versus true mirror ID {fighter_id}')
    source = source.replace('checkerSHA256=sync.sha(Path(__file__)),', 'checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),')
    exec(compile(source, __file__, 'exec'), dict(__file__=__file__, prior=prior))
