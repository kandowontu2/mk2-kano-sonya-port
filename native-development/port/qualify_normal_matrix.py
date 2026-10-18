"""Aggregate136 actual normal/proximity contact cells; never all-port acceptance."""
import json
from refresh_special_videos import BASE,PORT
from refresh_normal_contact import plan as basic_plan
from refresh_ground_matrix import plan as ground_plan
from qualify_normal_contact import qualify,contact_spec

def plan():
    fixtures=basic_plan('stock_wolf_2219_normal_contact')
    fixtures+=basic_plan('stock_wolf_2219_basic_inrange',True)
    fixtures+=ground_plan('stock_wolf_2219_ground_matrix')
    fixtures+=ground_plan('stock_wolf_2219_jump_matrix',True)
    assert len(fixtures)==len({name for name,_,_ in fixtures})==136
    return fixtures

def main():
    fixtures=plan()
    assert all((BASE/name/'execution.json').is_file() for name,_,_ in fixtures),'Remaining runtime cells missing'
    results=[dict(run=name,**qualify(name)) for name,_,_ in fixtures]
    keys={(r['actor'],r['side'],r['actualAction'],r['blocking']) for r in results}
    assert len(keys)==136
    actions={r['actualAction'] for r in results}
    assert len(actions)==17
    assert all((actor,side,action,blocking) in keys for actor in (17,18)
               for side in (1,2) for action in actions for blocking in (False,True))
    (PORT/'NORMAL_CONTACT_ACCEPTANCE_2219.json').write_text(json.dumps(dict(cases=results,
        all136FiniteContactCellsPassed=True,actualActionTypes=sorted(actions),
        arbitraryRangesVictimsAndAnimationFramesVerified=False,fullPortVerified=False,releaseReady=False),indent=2)+'\n')
    print('136 finite native normal/proximity contact cells requalified,17 action types; not whole-port acceptance.')

if __name__=='__main__':main()
