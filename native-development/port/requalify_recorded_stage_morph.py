"""Explicit current6AE0 stage/morph evidence refresh; no emulator launches."""
import sys
from refresh_stage_regression import plan as stage_plan
from refresh_morph_regression import plan as morph_plan
from refresh_morph_finisher_rejoin import plan as rejoin_plan
from stage_profiles import profile
from requalify_recorded_finishers import check,receipt

def main():
    assert len(sys.argv)==1,'Explicit existing current6AE0 fixtures only'
    stages=stage_plan('stock_wolf_6ae0_stage')
    for name,args in stages:
        receipt(name,args)
        kind,actor,_=profile(args)
        if kind in ('deadpool','negative'):check('qualify_deadpool_runtime.py',name)
        elif kind=='tomb':check('qualify_tomb_stage.py',name,str(actor))
        else:check('qualify_pit_rejoin.py',name,str(actor))
        print('REQUALIFIED',name,flush=True)
    check('qualify_stage_positive_matrix.py',*[name for name,_ in stages])
    morphs=morph_plan('stock_wolf_6ae0_morph')
    for name,args in morphs:
        receipt(name,args)
        check('qualify_morph.py',name)
        print('REQUALIFIED',name,flush=True)
    check('qualify_morph_art_trace.py',*[name for name,args in morphs if '--morph-specials' in args])
    # Only the qualified extended melee3 profile, never earlier failed attempts.
    extended=[]
    for label,flag in (('ball','ball'),('melee3','melee'),('grapples','grapples'),('square','square')):
        for side in (1,2):
            name=f'stock_wolf_6ae0_extended_{label}_p{side}'
            args=['--game','--morph','--morph-'+flag,*(['--mirror'] if side==2 else []),'--sound-candidate']
            receipt(name,args)
            check('qualify_morph.py',name)
            extended.append(name)
            print('REQUALIFIED',name,flush=True)
    rejoins=rejoin_plan('stock_wolf_6ae0_morph')
    for name,kind,side,args in rejoins:
        receipt(name,args)
        check('qualify_finisher_rejoin.py',name)
        check('qualify_'+kind+'.py',name,str(side),'17' if kind in ('kiss','bubble') else '18')
        print('REQUALIFIED',name,flush=True)
    check('qualify_morph_finisher_rejoin_matrix.py',*[name for name,_,_,_ in rejoins])
    print('36 recorded stage/morph fixtures, art and finite matrices requalified; no runtime launched.',flush=True)

if __name__=='__main__':main()
