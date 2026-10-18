"""Recheck explicit existing current-ROM traces; never launch or alter gameplay."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
from refresh_fatality_regression import plan as fatality_plan
from refresh_nonlethal_regression import plan as nonlethal_plan
from qualify_own_fatality_matrix import profile as fatality_profile,qualify as fatality_matrix
from nonlethal_profiles import profile as nonlethal_profile

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
FLAGS=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0

def check(script,*arguments):
    result=subprocess.run([sys.executable,str(PORT/script),*arguments],cwd=PORT,
        capture_output=True,text=True,creationflags=FLAGS)
    assert result.returncode==0,(script,arguments,result.stderr[-4000:])

def receipt(name,args):
    proof=json.loads((BASE/name/'execution.json').read_text())
    assert proof['exitCode']==0 and not proof['timedOut']
    assert proof['testArguments']==args,'Recorded fixture profile changed'

def main():
    assert len(sys.argv)==1,'Explicit current6AE0 fixtures only; no arbitrary output paths'
    fatalities=fatality_plan('stock_wolf_6ae0_fatality')
    nonlethals=nonlethal_plan('stock_wolf_6ae0_nonlethal')
    for name,args in fatalities:
        receipt(name,args)
        check('qualify_finisher_rejoin.py',name)
        kind,side,victim=fatality_profile(args)
        importlib.import_module('qualify_'+kind).qualify(name,side,victim)
        print('REQUALIFIED',name,flush=True)
    fatality_matrix([name for name,_ in fatalities])
    for name,args,negative in nonlethals:
        receipt(name,args)
        kind,actor,_,_=nonlethal_profile(args,negative)
        if not negative:check('qualify_finisher_rejoin.py',name)
        if kind=='baby':check('qualify_baby.py',name,str(actor))
        else:check('qualify_kano_friend.py' if actor==17 else 'qualify_sonya_friend.py',name)
        if kind=='friend' and actor==18 and not negative:check('qualify_friend_lifecycle.py',name)
        print('REQUALIFIED',name,flush=True)
    for negative,script in ((False,'qualify_nonlethal_matrix.py'),(True,'qualify_negative_nonlethal_matrix.py')):
        check(script,*[name for name,_,mode in nonlethals if mode==negative])
    print('24 existing finisher fixtures and three finite matrices requalified; no runtime launched.',flush=True)

if __name__=='__main__':main()
