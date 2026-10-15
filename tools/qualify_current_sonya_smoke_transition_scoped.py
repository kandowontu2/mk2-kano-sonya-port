"""Allow only real post-secret CSS inputs; retain capped evidence as partial."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_smoke_transition.py').read_text()
source=source.replace("out=sync.ROOT/'audit_current_sonya_smoke_transition_checked'",
                      "out=sync.ROOT/'audit_current_sonya_smoke_transition_scoped_checked'")
old="assert not [r for r in rows.get('INPUT',[]) if int(r['frame'])>end]"
assert source.count(old)==1
source=source.replace(old,'''post_inputs=[r for r in rows.get('INPUT',[]) if int(r['frame'])>end]
for r in post_inputs:
    mode=next(m for m in reversed(rows['MODE']) if int(m['frame'])<=int(r['frame']))
    assert mode['mode']=='4' and mode['arena']=='8'
    assert r['button'] in ('Left','Right','Down','High_Punch')
    assert r['slot'] in ('1','2')
post_selected=[r for r in rows.get('SELECT_ID',[]) if int(r['frame'])>end]
assert all(r['actual']==r['target'] and r['actual']==('18' if r['slot']=='1' else '4') for r in post_selected)''')
start=source.index('if returns and tails:')
finish=source.index('bad=copy.deepcopy(prefix)',start)
source=source[:start]+'''return_fields=[]
if returns:
    assert len(returns)==1
    arrival=returns[0]
    assert arrival['mode']=='2' and arrival['arena']=='8'
    assert arrival['ids']==arrival['rosters']=='18,4' and arrival['states']=='1,1'
    assert arrival['actors']==arrival['owners'] and arrival['hp']=='161,161'
    assert len([r for r in lethals if r['slot']=='1' and int(r['frame'])<int(arrival['frame'])])==2
    assert len(post_selected)==2
    return_fields=[r for r in rows['SECRET_FIELD'] if int(r['frame'])>=int(arrival['frame'])]
    assert return_fields and [int(r['frame']) for r in return_fields]==list(range(int(arrival['frame']),int(return_fields[-1]['frame'])+1))
    assert all(r['mode']=='2' and r['arena']=='8' and r['ids']==r['rosters']=='18,4' and r['states']=='1,1' and r['actors']==r['owners'] for r in return_fields)
    if tails:
        assert len(tails)==1 and int(tails[0]['frame'])-int(arrival['frame'])>=180
        assert return_fields[-1]['frame']==tails[0]['frame']
        normal_return=completed and not rows.get('SECRET_NATIVE_RESET')
elif tails:
    raise AssertionError('Return tail without actual arrival')
''' +source[finish:]
source=source.replace('observedReturn=returns,observedReturnTail=tails,normalTwoHumanReturnAccepted=normal_return,',
    'observedReturn=returns,observedReturnTail=tails,observedReturnFields=len(return_fields),normalTwoHumanReturnAccepted=normal_return,')
exec(compile(source,__file__+'::original_gate_with_native_css_scope','exec'))
