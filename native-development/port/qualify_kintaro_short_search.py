"""Check the bounded search route; success is planning-only until no-load replay."""
import csv
import json
import zipfile
from inspect_normal_runtime import BASE,PORT,sha
from verify_finisher_roms import verify


def score(row):
    value=int(row['p1wins'])*10000-int(row['p2wins'])*10000+2*int(row['p1hp'])-int(row['p2hp'])
    return value+min(int(row['distance']),260)/1000+(100000 if int(row['map'])>15 else 0)


def main():
    run=BASE/'stock_wolf_2219_kano_short_search'
    earned=BASE/'stock_wolf_2219_kano_earned_kintaro_checkpoint_v3'
    execution=json.loads((run/'execution.json').read_text())
    prior=json.loads((earned/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut'] and execution['planningStateLoadUsed']
    assert execution['observerSHA256']==sha(run/'autoboot.lua')
    assert execution['checkpointSHA256']==sha(earned/'earned_kintaro_intro.sta')
    assert execution['emulatorSHA256']==prior['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    with zipfile.ZipFile(earned/'roms/mk3.zip') as archive:verify(archive,prior)
    with (run/'search.csv').open() as stream:candidates=list(csv.DictReader(stream))
    with (run/'chosen.csv').open() as stream:chosen=list(csv.DictReader(stream))
    actions=('kick','punch','counter','knife','guard','away','backkick')
    assert len(chosen)==37 and len(candidates)==37*7
    for depth,row in enumerate(chosen,1):
        group=[r for r in candidates if int(r['depth'])==depth]
        assert len(group)==7 and [r['action'] for r in group]==list(actions)
        assert all(abs(float(r['score'])-score(r))<.00001 for r in group)
        assert row==max(group,key=score),'Chosen branch is not the recorded best branch'
    final=chosen[-1]
    assert final['p1wins']=='2' and final['p2wins']=='0' and final['p2hp']=='0' and int(final['p1hp'])>0
    assert (run/'search_end.txt').read_text().strip()=='planning_candidate_match_win'
    target=PORT/'KINTARO_SHORT_ROUTE.json'
    assert not target.exists(),'Never overwrite a route awaiting replay'
    report=dict(scope='Planning candidate only; continuous startup replay REQUIRED',
        actions=[r['action'] for r in chosen],fieldsPerAction=120,expectedStartField=130294,
        chosenDepths=37,candidatesCompared=259,finalNativeCounters=dict(player=2,cpu=0),
        finalHP=dict(player=int(final['p1hp']),cpu=0),continuousReplayVerified=False,
        campaignAcceptance=False,fullPortVerified=False,pins={str(p):sha(p) for p in
            (run/'autoboot.lua',run/'execution.json',run/'search.csv',run/'chosen.csv',
             earned/'earned_kintaro_intro.sta')})
    target.write_text(json.dumps(report,indent=2)+'\n')
    print('Verified259 comparisons and37 input chunks; candidate native2-0, NOT continuous campaign acceptance')


if __name__=='__main__':main()
