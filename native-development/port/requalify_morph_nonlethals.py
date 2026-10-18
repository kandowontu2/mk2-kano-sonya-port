"""Refresh eight explicit transformed nonlethal recordings; no runtime launch."""
import json
from pathlib import Path
import sys
from recovery_evidence import sha
from requalify_recorded_finishers import BASE,PORT,check,receipt

def main():
    assert len(sys.argv)==1
    cases=[]
    for side in (1,2):
        mirror=['--mirror'] if side==2 else []
        fixtures=[
            (f'stock_wolf_6ae0_morph_kano_friend_p{side}',17,'friend',False,
             ['--game','--friend','--kano','--finisher-morph','--sound-candidate',*mirror]),
            (f'stock_wolf_6ae0_morph_friend_negative_p{side}',18,'friend',True,
             ['--game','--friend','--finisher-morph','--sound-candidate',*mirror]),
            *[(f'stock_wolf_6ae0_morph_baby2_{actor}_p{side}',actor,'baby',actor==18,
               ['--game','--baby','--own-victim','--finisher-morph','--sound-candidate',*(['--sonya'] if actor==18 else []),*mirror]) for actor in (17,18)]]
        for name,actor,kind,negative,args in fixtures:
            receipt(name,args)
            if kind=='baby':check('qualify_baby.py',name,str(actor))
            else:check('qualify_kano_friend.py' if actor==17 else 'qualify_sonya_friend.py',name)
            path=BASE/name/'qualification.json'
            proof=json.loads(path.read_text())
            assert proof['currentFull26ROMBytesVerified']
            for filename,value in proof['pins'].items():assert sha(Path(filename))==value
            cases.append(dict(run=name,actor=actor,side=side,kind=kind,expectedPunchRuleRejection=negative,
                              qualificationSHA256=sha(path)))
            print('REQUALIFIED',name,flush=True)
    report=dict(scope='Eight explicit transformed native nonlethal eligibility cases',cases=cases,
        allEightFiniteCasesRequalified=True,fullPortVerified=False,releaseReady=False,
        verifierSHA256=sha(Path(__file__)))
    (PORT/'MORPH_NONLETHAL_REFRESH.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
