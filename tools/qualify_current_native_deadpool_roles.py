"""Finite acid eligibility/identity/followthrough qualification, not full-port acceptance."""
import json
import re
import verify_native_source_sync as sync


def rows(path):
    result=[]
    for line in path.read_text().splitlines():
        if line.startswith('MK2_STAGE_'):
            parts=line.split()
            result.append((parts[0][10:],dict(p.split('=',1) for p in parts[1:] if '=' in p)))
    return result


def check(records,fighter,side):
    own=17 if fighter=='kano' else 18
    victim=18 if own==17 else 17
    assert all(r['writes']=='0' and r['assistance']=='none' for _,r in records)
    gates=[r for tag,r in records if tag=='ACID_GATE']
    accepted=[r for r in gates if r['entry']=='FF8712A0']
    assert len(accepted)==1
    g=accepted[0]
    assert int(g['id'])==own and int(g['side'])==side
    assert g['arena']=='0' and g['finish']=='3' and g['a3']=='00000003'
    mask=3 if side==1 else 0x30
    assert int(g['in2'],16)&mask==0
    assert not any(r['entry']=='FF8714D0' for r in gates)
    damage=[r for tag,r in records if tag=='DAMAGE']
    assert damage and int(damage[-1]['total'])==322 and damage[-1]['kos']=='2'
    assert all(r['pc']=='FF836700' for r in damage)
    fields=[r for tag,r in records if tag=='FIELD' and int(r['age'])<=800]
    assert [int(r['age']) for r in fields]==list(range(801))
    live=[r for r in fields if r['own']!='00000000']
    assert live and all(int(r['id'])==own and int(r['victim_id'])==victim for r in live)
    retired=[r for r in fields if r['own']=='00000000']
    assert retired and all(r['victim']=='00000000' and r['mode']=='3' and r['arena']=='1' for r in retired)
    result=[r for tag,r in records if tag=='RESULT']
    assert len(result)==1 and result[0]['damage']=='322' and result[0]['kos']=='2'
    assert int(result[0]['frame'])-int(result[0]['action'])==1101
    assert not any(tag=='HOST_BOUND' for tag,_ in records)
    return {'fighter':fighter,'side':side,'nativeAcidBranch':True,'ownAndVictimIDs':True,
            'consecutiveSceneFields':801,'normalActorRetirement':True}


if __name__=='__main__':
    sync.verify()
    cases=[]
    for fighter,side in [('kano',1),('sonya',1),('kano',2),('sonya',2)]:
        folder=sync.ROOT/f'audit_current_native_deadpool_gate_hold_{fighter}_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        log=folder/'run.log'
        records=rows(log)
        case=check(records,fighter,side)
        bad=[(tag,dict(r)) for tag,r in records]
        for tag,r in bad:
            if tag=='ACID_GATE' and r['entry']=='FF8712A0': r['id']='1'
        try: check(bad,fighter,side)
        except AssertionError: pass
        else: raise AssertionError('Proxy fault accepted')
        case.update(logSHA256=sync.sha(log),terminalSHA256=sync.sha(folder/'terminal.json'))
        cases.append(case)
    out=sync.ROOT/'audit_current_native_deadpool_roles_checked'
    assert not out.exists();out.mkdir()
    report={'passed':True,'cases':cases,'proxyFaultRejected':True,
            'allVisualAudioContextsAccepted':False,'fullPortAccepted':False}
    (out/'report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))
