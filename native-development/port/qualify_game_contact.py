"""Qualify only the bounded physical-input roster/contact smoke test."""
import csv
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'baseline'
RUN=BASE/'stock_wolf_game_contact_06'
SRC=BASE/'mk2-rebuild-main/srcp'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def main():
    execution=json.loads((RUN/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    assert not execution['customDriver'] and not execution['gameMemoryWrites']
    rows=list(csv.DictReader((RUN/'probe.csv').open()))
    combat=[r for r in rows if (r['mode'],r['p1char'],r['p2char'])==('2','17','18')]
    assert len(combat)>=70
    assert all((r['p1objectchar'],r['p2objectchar'])==('17','18') for r in combat)
    assert min(int(r['p1hp']) for r in combat)<161
    assert min(int(r['p2hp']) for r in combat)==0
    assert all(int(r['missing'])==0 for r in rows)
    assert all(0xff800000<=int(r['pc'],16)<=0xffffffff for r in rows if int(r['frame'])>=3000)
    assert 'stack ' not in (RUN/'state.txt').read_text()
    pins=[RUN/'execution.json',RUN/'probe.csv',RUN/'state.txt',
          RUN/'snap/frame_03240.png',RUN/'snap/frame_04800.png',
          HERE/'diagnostics/game_probe.lua',BASE/'test_wolf_baseline.py',
          HERE/'prepare_game_candidate.py',SRC/'MK2P.OUT',SRC/'MK2P.MAP']
    pins+=sorted(SRC.glob('*.ASM'))
    result=dict(scope='physical-input selection and high-punch contact smoke test',
                trueRosterAndObjectIDs=[17,18],combatSamples=len(combat),
                firstCombatFrame=int(combat[0]['frame']),lastCombatFrame=int(combat[-1]['frame']),
                healthMinima=[min(int(r[k]) for r in combat) for k in ('p1hp','p2hp')],
                missingAnimationMarkers=0,recoveryObserved=False,
                nativeWinnerTextVisuallyReviewed='KANO WINS',
                allMovesVerified=False,fatalitiesVerified=False,fullCampaignVerified=False,
                releaseReady=False,pins={str(p):sha(p) for p in pins})
    (RUN/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='pins'},indent=2))

if __name__=='__main__':main()
