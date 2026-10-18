"""Finite loaded-state boss results, never continuous campaign acceptance."""
import csv
import json
import sys
import zipfile
from inspect_normal_runtime import BASE, sha
from verify_finisher_roms import verify
from campaign_rounds import split_rounds,native_round_wins,completed_native_matches,require_clean_runtime_log


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run=BASE/name;receipt=json.loads((run/'execution.json').read_text())
    assert receipt['planningStateLoadUsed'] and receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha(run/'autoboot.lua')==receipt['controllerSHA256']
    require_clean_runtime_log((run/'mame.log').read_text())
    with zipfile.ZipFile(run/'roms/mk3.zip') as archive:verify(archive,receipt)
    with (run/'campaign.csv').open() as stream:rows=list(csv.DictReader(stream))
    fights=[r for r in rows if r['mode']=='2']
    assert fights and all(r['p1selected']==r['p1char']=='17' for r in fights)
    assert all(int(r['missing'])==0 for r in rows)
    rounds=split_rounds(fights);wins=native_round_wins(rows,rounds);matches=completed_native_matches(wins)
    report=dict(scope='Explicit loaded-state planning ONLY, not continuous campaign/video evidence',
        rounds=rounds,nativeWinningRounds=wins,completedNativeMatches=matches,
        campaignAcceptance=False,fullPortVerified=False,pins={str(p):sha(p) for p in
            (run/'autoboot.lua',run/'execution.json',run/'campaign.csv')})
    (run/'PLANNING_BOSS_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PLANNING ONLY:',len(rounds),'rounds;',len(wins),'native round wins;',len(matches),'native match wins;',
        'best Kintaro HP',min(r['minimumCPUHP'] for r in rounds if r['opponent']==12))


if __name__=='__main__':
    assert len(sys.argv)==2
    main(sys.argv[1])
