"""Preserve failed all-damage assumption; distinguish native follow-up HP."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_bicycle_cycles.py')
scope={'__file__':str(prior)}
exec(compile(prior.read_text().split('exec(compile(source',1)[0],str(prior),'exec'),scope))
source=scope['source']
marker="    assert len(damage)==2 and all(int(r['before'])-int(r['after'])==22 and r['pc']=='FF836700' for r in damage)"
assert source.count(marker)==1
source=source.replace(marker,"""    special=[];followups=[]
    for hit in damage:
        activation=next(r for r in events if r['attempt']==hit['attempt'])
        recovery=next(r for r in rows['RECOVERED'] if r['attempt']==hit['attempt'])
        if int(activation['frame'])<=int(hit['frame'])<=int(recovery['frame']):special.append(hit)
        else:followups.append(hit)
    assert len(special)==2 and all(int(r['before'])-int(r['after'])==22 and r['pc']=='FF836700' for r in special)
    assert len(followups)==(0 if side==1 else 1)
    for hit in followups:
        assert hit['pc']=='FF836700' and int(hit['before'])-int(hit['after'])==11
        at=int(hit['frame']);followup=int(rows['RESULT'][0]['followup'])
        assert at>=followup+112 and any(r['button']=='High_Punch' and int(r['frame'])==followup+112 for r in rows['INPUT'])
        assert any(r['slot']==str(side) and r['action']=='257' and at-8<=int(r['frame'])<=at for r in rows['FIELD'])
""")
source=source.replace('audit_bounded_current_bicycle_cycles_checked','audit_bounded_current_bicycle_followup_damage_checked')
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),failedBicycleCheckerSHA256=sync.sha(failed),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=scope['prior'],failed=prior))
