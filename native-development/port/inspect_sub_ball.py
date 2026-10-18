"""Finite physical charge/release evidence; not a winning-strategy certificate."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def charge_observations(rows):
    charging=[r for r in rows if r['phase'] in ('charge','prepare')]
    # These are observed fields, not successful throw or hit counts.
    return dict(chargingFields=len(charging),
                chargingDownFields=sum(r['down']=='1' for r in charging),
                chargingBlockFields=sum(r['block']=='1' for r in charging),
                chargingEnemyBodySlamFields=sum(int(r['enemyAction'])==0x507 for r in charging),
                chargingOwnReactionFields=sum(bool(int(r['ownFlags'])&4) for r in charging))

def release_case(index,frame,recovery_context=None):
    row=index[frame]
    assert row['phase']=='released' and row['eligible']=='1' and int(row['age'])>85
    assert row['lk']==row['block']==row['down']=='0'
    assert row['ownHeight']=='0' and int(row['ownFlags'])&0x1c==0
    if int(row['enemyFlags'])&0x1c:
        assert recovery_context is not None and int(row['enemyFlags'])&0x0c==0
        assert counter_phase(recovery_context)=='native-recovery'
    assert row['projectile']=='0'
    assert 80<=int(row['distance'])<=260
    for delta in range(1,82):
        previous=index.get(frame-delta)
        assert previous is not None and previous['lk']=='1','Missing continuous held-LK input'
    for delta in range(1,5):
        previous=index[frame-delta]
        assert previous['phase']=='prepare' and previous['eligible']=='1' and previous['block']=='0'
    later=[index[frame+delta] for delta in range(1,9) if frame+delta in index]
    activated=any(r['ownAction']==str(0x20b) for r in later)
    return dict(frame=frame,chargeAge=int(row['age']),distance=int(row['distance']),
                enemyReadiness='native-recovery' if int(row['enemyFlags'])&0x1c else 'normal',
                followingObservedFields=len(later),
                ballStateObservedWithin8=activated if activated or len(later)==8 else None)

def counter_case(index,frame):
    row=index[frame]
    assert row.get('hp')=='1' and row['lk']==row['down']=='1' and row['block']=='0'
    assert row['phase']!='released' and row['ownHeight']=='0' and int(row['ownFlags'])&0x1c==0
    assert int(row['distance'])<105
    later=[index[frame+delta] for delta in range(1,9) if frame+delta in index]
    observed=any(r['ownAction']==str(0x107) for r in later)
    return dict(frame=frame,followingObservedFields=len(later),
                uppercutStateObservedWithin8=observed if observed or len(later)==8 else None)

def counter_phase(context):
    assert context['rapidPunch']=='1' and int(context['enemyFlags'])&0x10
    if context['recovering']=='1':return 'native-recovery'
    assert context['recovering']=='0' and int(context['punchesLeft'])>1 and int(context['punchAnimation'])==0x13
    return 'early-high-punch'

def verify_approach(row):
    assert row['toward']==row['lk']=='1' and row['away']==row['block']==row['down']=='0'
    assert row['phase']!='released' and int(row['age'])>=4
    assert row['ownHeight']=='0' and int(row['ownFlags'])&0x1c==0
    assert int(row['enemyFlags'])&0x1c==0 and row['enemyAction']=='771'
    assert row['projectile']=='0' and int(row['distance'])>140

def verify_post_guard(rows):
    start=None;guarded=0
    for row in rows:
        if row['phase']!='released':
            start=None
            continue
        frame=int(row['frame'])
        if start is None:start=frame
        if frame-start>=8:
            assert row['block']==row['away']=='1' and row['down']=='0'
            guarded+=1
        else:
            assert row['block']==row['away']=='0'
    return guarded

def inspect(name):
    assert name and Path(name).name==name and '/' not in name and '\\' not in name
    subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],check=True,capture_output=True)
    run=BASE/name
    receipt=json.loads((run/'execution.json').read_text())
    assert '--campaign-kano-sub-ball' in receipt['testArguments']
    rows=list(csv.DictReader((run/'sub_ball.csv').open()))
    index={int(row['frame']):row for row in rows}
    assert len(index)==len(rows)
    recovery_ball='--campaign-kano-sub-recovery-ball' in receipt['testArguments']
    context_index={}
    if '--campaign-kano-sub-recovery-counter' in receipt['testArguments']:
        contexts=list(csv.DictReader((run/'subzero_context.csv').open()))
        context_index={int(r['frame']):r for r in contexts}
        assert len(context_index)==len(contexts)
    releases=[]
    for row in rows:
        frame=int(row['frame']);previous=index.get(frame-1)
        if row['phase']=='released' and previous is not None and previous['phase']=='prepare':
            releases.append(release_case(index,frame,context_index.get(frame) if recovery_ball else None))
    report=dict(scope='Finite observed charge/release inputs and next8-field Ball-state windows',
                run=name,releaseRequests=len(releases),
                observedActivationsWithin8=sum(r['ballStateObservedWithin8'] is True for r in releases),
                incompleteActivationWindows=sum(r['ballStateObservedWithin8'] is None for r in releases),
                chargeObservations=charge_observations(rows),
                cases=releases,nativeMatchWinCertified=False,fullPortVerified=False)
    report['nativeRecoveryReleaseRequests']=sum(r['enemyReadiness']=='native-recovery' for r in releases)
    if '--campaign-kano-sub-postball-guard' in receipt['testArguments']:
        report['postBallGuardRequestedFields']=verify_post_guard(rows)
        assert report['postBallGuardRequestedFields']>0
    if '--campaign-kano-sub-approach' in receipt['testArguments']:
        approach=[r for r in rows if r['toward']=='1']
        assert approach,'The approach strategy was not exercised'
        for row in approach:verify_approach(row)
        assert all(c['distance']<=140 for c in releases)
        report['guardedApproachRequestedFields']=len(approach)
    if '--campaign-kano-sub-ball-counter' in receipt['testArguments']:
        assert all('hp' in r for r in rows)
        counters=[counter_case(index,int(r['frame'])) for r in rows if r['hp']=='1']
        report['counterRequests']=len(counters)
        report['uppercutStatesObservedWithin8']=sum(c['uppercutStateObservedWithin8'] is True for c in counters)
        report['incompleteCounterWindows']=sum(c['uppercutStateObservedWithin8'] is None for c in counters)
        report['counterCases']=counters
        if '--campaign-kano-sub-recovery-counter' in receipt['testArguments']:
            for case in counters:
                case['nativePunchPhase']=counter_phase(context_index[case['frame']])
            report['recoveryCounterRequests']=sum(c['nativePunchPhase']=='native-recovery' for c in counters)
            report['earlyHighCounterRequests']=sum(c['nativePunchPhase']=='early-high-punch' for c in counters)
            if recovery_ball:
                if '--campaign-kano-sub-recharge' in receipt['testArguments']:
                    assert all(int(index[c['frame']]['age'])<=85 for c in counters if c['nativePunchPhase']=='native-recovery')
                else:assert report['recoveryCounterRequests']==0
    paths=[run/n for n in ('execution.json','autoboot.lua','campaign.csv','CAMPAIGN_AUDIT.json','sub_ball.csv')]
    if '--campaign-kano-sub-recovery-counter' in receipt['testArguments']:
        paths.append(run/'subzero_context.csv')
        paths.extend(BASE/'mk2-rebuild-main/srcp'/n for n in ('MKDRONE.ASM','MKDRONE.LST','MK2P.MAP'))
    paths += [Path(__file__),PORT/'audit_campaign_run.py']
    paths += [BASE/'mk2-rebuild-main/srcp'/n for n in ('KANOMOV.ASM','KSCMD.ASM','MOVES.ASM')]
    report['pins']={str(p):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in paths}
    (run/'SUB_BALL_DIAGNOSTIC.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k not in ('cases','pins')}

if __name__=='__main__':print(json.dumps(inspect(sys.argv[1]),indent=2))
