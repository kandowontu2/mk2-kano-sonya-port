"""Observe requests, native activation and native round counters separately."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from bisect import bisect_right
from campaign_rounds import split_rounds, native_round_wins, completed_native_matches

PORT = Path(__file__).resolve().parent
BASE = PORT.parent / 'baseline'


def boss_evidence(cases, campaign):
    """Keep boss health windows and earned counters separate from human damage."""
    requests=[case for case in cases if case['opponent']==12]
    fight=[row for row in campaign if row['mode']=='2' and row['p1char']=='17' and row['p2char']=='12']
    wins=native_round_wins(campaign,split_rounds(fight))
    return dict(kintaroRequests=len(requests),
                kintaroNativeActivationsWithin8=sum(case['nativeUppercutWithin8'] is True for case in requests),
                kintaroActivationWithObserved20HPDropWindows=sum(case['nativeUppercutWithin8'] is True and
                    case['observedHPDropWithin55']==20 for case in requests),
                kintaroNativeRoundWins=wins,kintaroCompletedMatches=completed_native_matches(wins))


def opponent_roles(row):
    selected=int(row.get('opponent','8'))
    active=int(row.get('activeOpponent',str(selected)))
    assert selected in (0,2,5,6,8,10,12,17,18)
    assert active in (*range(12),17,18) or selected==active==12
    assert selected==6 or active==selected, 'Non-Shang identity mismatch'
    return selected,active


def request_case(index, frame, boss_range=84):
    assert boss_range in (84,105)
    row = index[frame]
    assert row['phase'] in ('uppercut', 'uppercut_counter')
    assert row['ownHeight'] == row['enemyHeight'] == '0'
    assert int(row['ownFlags']) & 0x1c == 0
    assert int(row['enemyFlags']) & 0x1c == (0x10 if row['phase']=='uppercut_counter' else 0)
    assert 0 <= int(row['bodyHeight']) <= 96
    assert int(row['buttonTable']) == int(row['duckTable']) != 0
    assert int(row['distance']) <= (boss_range if row.get('opponent')=='12' else 84) and row['projectile'] == '0'
    assert row['block'] == row['away'] == row['toward'] == row['lp'] == '0'
    assert row['down'] == row['hp'] == '1'
    later = [index[frame + delta] for delta in range(1, 9) if frame + delta in index]
    active = any(int(r['ownAction']) == 0x107 for r in later)
    opponent,active_identity=opponent_roles(row)
    return dict(frame=frame, opponent=opponent, activeOpponent=active_identity, phase=row['phase'], distance=int(row['distance']), followingFields=len(later),
                nativeUppercutWithin8=active if active or len(later) == 8 else None)


def damage_window(campaign, frame, opponent=8):
    frames = [int(r['frame']) for r in campaign]
    assert frames == sorted(set(frames))
    at = bisect_right(frames, frame) - 1
    if at < 0 or frame - frames[at] > 2:
        return dict(observedHPDropWithin55=None, victimHitTagObserved=False, sampledFields=0)
    before = campaign[at]
    context = tuple(before[k] for k in ('attempt', 'map', 'round', 'p1char', 'p2char'))
    assert context[-2:] == ('17', str(opponent))
    window = [r for r in campaign[at+1:bisect_right(frames, frame+55)]
              if tuple(r[k] for k in ('attempt', 'map', 'round', 'p1char', 'p2char')) == context]
    return dict(observedHPDropWithin55=int(before['p2hp'])-min([int(before['p2hp'])]+[int(r['p2hp']) for r in window]),
                victimHitTagObserved=any(int(r['p2action'])==0x503 for r in window),
                sampledFields=len(window), complete55FieldWindow=bool(window) and int(window[-1]['frame'])>=frame+53)


def knife_case(index, frame):
    row=index[frame]
    assert row['phase']=='knife_punch' and row['hp']=='1'
    assert row['lp']==row['down']==row['away']==row['toward']==row['block']=='0'
    spaced=index[frame-1]['phase']=='knife_gap_back'
    for delta in ((4,5,6) if spaced else (1,2,3)):
        before=index[frame-delta]
        assert before['phase']=='knife_back' and before['away']=='1'
        assert before['down']==before['hp']==before['block']=='0'
    for delta in ((10,11,12) if spaced else (4,5,6)):
        before=index[frame-delta]
        assert before['phase']=='knife_down' and before['down']=='1'
        assert before['away']==before['hp']==before['block']=='0'
    ready=index[frame-12 if spaced else frame-7]
    if spaced:
        assert ready['phase']=='knife_down' and int(ready['ownAction'])==0x303
        assert int(ready['bodyHeight'])>=96 and int(ready['buttonTable'])!=int(ready['duckTable'])
        for delta,phase in [(d,'knife_gap_back') for d in (1,2,3)]+[(d,'knife_gap_down') for d in (7,8,9)]:
            before=index[frame-delta]
            assert before['phase']==phase and all(before[k]=='0' for k in ('hp','lp','down','away','toward','block'))
    else:
        assert ready['phase']=='knife_prepare' and ready['down']=='0'
        assert int(ready['ownAction'])==0x303 or (0<=int(ready['bodyHeight'])<=96 and
                                                 int(ready['buttonTable'])==int(ready['duckTable'])!=0)
    later=[index[frame+d] for d in range(1,9) if frame+d in index]
    active=any(int(r['ownAction'])==0x211 for r in later)
    opponent,active_identity=opponent_roles(row)
    return dict(frame=frame,opponent=opponent,activeOpponent=active_identity,physicalDownBackPunchVerified=True,recipe='spaced-standing' if spaced else 'compact',
                nativeKnifeWithin8=active if active or len(later)==8 else None,
                followingFields=len(later))


def inspect(name):
    assert name and Path(name).name == name and '/' not in name and '\\' not in name
    flags = (subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform == 'win32' else 0
    result = subprocess.run([sys.executable, str(PORT / 'audit_campaign_run.py'), name],
                            capture_output=True, text=True, creationflags=flags)
    assert result.returncode == 0, result.stderr[-3000:]
    folder = BASE / name
    receipt = json.loads((folder / 'execution.json').read_text())
    assert '--campaign-kano-sub-neutral-uppercut' in receipt['testArguments']
    with (folder / 'sub_neutral_uppercut.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    assert rows, 'No Sub-Zero policy observations'
    if any(row.get('opponent')=='12' for row in rows):
        assert any(flag in receipt['testArguments'] for flag in ('--campaign-kano-kintaro-prepare','--campaign-kano-kintaro-wide-prepare'))
    index = {int(r['frame']): r for r in rows}
    assert len(index) == len(rows)
    boss_range=105 if '--campaign-kano-kintaro-wide-prepare' in receipt['testArguments'] else 84
    cases = [request_case(index, int(r['frame']),boss_range) for r in rows if r['phase'] in ('uppercut','uppercut_counter')]
    assert all(b['frame'] - a['frame'] >= 60 for a, b in zip(cases, cases[1:]))
    with (folder / 'campaign.csv').open() as stream:
        campaign = list(csv.DictReader(stream))
    for case in cases:
        case.update(damage_window(campaign, case['frame'], case['activeOpponent']))
    knives=[knife_case(index,int(r['frame'])) for r in rows if r['phase']=='knife_punch'
            and index.get(int(r['frame'])-1,{}).get('phase')!='knife_punch']
    for case in knives:
        case.update(damage_window(campaign,case['frame'],case['activeOpponent']))
    fight = [r for r in campaign if r['mode'] == '2' and r['p1char'] == '17' and r['p2char'] == '8']
    wins = native_round_wins(campaign, split_rounds(fight))
    matches = completed_native_matches(wins)
    mileena=[r for r in campaign if r['mode']=='2' and r['p1char']=='17' and r['p2char']=='5']
    mileena_wins=native_round_wins(campaign,split_rounds(mileena))
    other=[dict(r,p2char=r['p2selected']) for r in campaign if r['mode']=='2' and r['p1char']=='17'
           and r['p2selected'] in ('0','2','6','10','17','18')]
    other_wins=native_round_wins(campaign,split_rounds(other))
    paths = [Path(__file__), PORT / 'campaign_rounds.py', PORT / 'audit_campaign_run.py', PORT / 'campaign_budget.py',
             BASE / 'test_wolf_baseline.py']
    paths += [folder / item for item in ('execution.json', 'autoboot.lua', 'CAMPAIGN_AUDIT.json',
                                        'campaign.csv', 'sub_neutral_uppercut.csv')]
    report = dict(run=name, scope='Physical neutral-uppercut requests and observed native counters',
                  requestCount=len(cases), cases=cases,
                  activationsWithin8=sum(c['nativeUppercutWithin8'] is True for c in cases),
                  incompleteWindows=sum(c['nativeUppercutWithin8'] is None for c in cases),
                  activationAndHitTagWith40HPDrop=sum(c['nativeUppercutWithin8'] is True and c['victimHitTagObserved']
                                                    and c['observedHPDropWithin55']==40 for c in cases),
                  knifeRequests=knives,knifeRequestCount=len(knives),
                  nativeKnifeActivationsWithin8=sum(c['nativeKnifeWithin8'] is True for c in knives),
                  subZeroNativeRoundWins=wins, subZeroCompletedMatches=matches,
                  mileenaNativeRoundWins=mileena_wins,mileenaCompletedMatches=completed_native_matches(mileena_wins),
                  otherHumanNativeRoundWins=other_wins,otherHumanCompletedMatches=completed_native_matches(other_wins),
                  fullCampaignCertified=False, fullPortVerified=False,
                  pins={str(p): hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in paths})
    report.update(boss_evidence(cases,campaign))
    (folder / 'SUB_NEUTRAL_UPPERCUT_DIAGNOSTIC.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('cases', 'pins')}, indent=2))


if __name__ == '__main__':
    inspect(sys.argv[1])
