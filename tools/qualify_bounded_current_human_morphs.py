"""Finite native forward/store/form projectile/return/control chronology."""
import copy
import json
import re
import verify_native_source_sync as sync


def gate(rows,target,side):
    identity=17 if target=='kano' else 18
    result=rows['RESULT']
    assert len(result)==1 and result[0]['forms']==result[0]['restores']=='1' and result[0]['errors']=='0'
    match=rows['MATCH'][0]
    actor,main=match['actor'],match['main']
    stores=rows['STORE']
    assert len(stores)==2
    assert [(r['old'],r['id'],r['pc']) for r in stores]==[('6',str(identity),'FF86E670'),(str(identity),'6','FFA16700')]
    assert int(stores[0]['a9'],16)==identity and int(stores[1]['a0'],16)==6
    assert all(r['actor']==actor and r['main']==main for r in stores)
    fields=rows['FIELD']
    assert [int(r['age']) for r in fields]==list(range(1001))
    for r in fields:
        assert r['actor']==actor and r['main']==main and r['mode']=='2' and r['state']=='1' and r['roster']=='6'
        current=6
        for store in stores:
            if int(store['frame'])<int(r['frame']):current=int(store['id'])
        assert int(r['id'])==current
        assert int(r['hp1'])>0 and int(r['hp2'])>0
    action=rows['PROJECTILE_ACTION'];create=rows['PROJECTILE_CREATE']
    assert len(action)==len(create)==1
    expected=('FFFFB000','FFFC5800') if target=='kano' else ('FFFFB400','FFFC5C00')
    assert action[0]['entry']==expected[0] and create[0]['entry']==expected[1]
    for r in action+create:
        assert r['actor']==actor and r['main']==main and int(r['id'])==identity
        assert int(stores[0]['frame'])<int(r['frame'])<int(stores[1]['frame'])
    post=[r for r in fields if int(r['age'])>=820]
    assert any(int(r['x'])!=int(post[0]['x']) for r in post)
    assert any(r['action']=='030B' and int(r['vy'],16)!=0 for r in post)
    assert any(r['action']=='0101' for r in post)
    final=fields[-1]
    assert final['id']=='6' and final['action']=='0303' and final['y']==final['floor']
    assert all(int(final[key],16)==0 for key in ('vx','vy','trail'))
    return dict(forwardFrame=int(stores[0]['frame']),returnFrame=int(stores[1]['frame']),
                continuousFields=1001,nativeRosterRemainsShang=True,postReturnWalkJumpPunch=True)


if __name__=='__main__':
    out=sync.ROOT/'audit_bounded_current_human_morphs_checked'
    assert not out.exists()
    results={}
    for target in ('kano','sonya'):
        for side in (1,2):
            folder=sync.ROOT/f'audit_bounded_current_human_morph_{target}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
            rows={}
            for line in (folder/'run.log').read_text().splitlines():
                assert '[LUA ERROR]' not in line and 'hex=' not in line
                if line.startswith('MK2_HUMAN_SHANG_'):
                    rows.setdefault(line.split()[0].removeprefix('MK2_HUMAN_SHANG_'),[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
            proof=gate(rows,target,side)
            broken=copy.deepcopy(rows);broken['STORE'][0]['pc']='00000000'
            try:gate(broken,target,side)
            except AssertionError:pass
            else:raise AssertionError('Wrong native morph-store PC accepted')
            results[target+str(side)]=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),wrongStorePCRejected=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullPortAcceptance=False,
        scope='Four actual current cold human Shang morphs: native true ID store, owned knife/ring, original timed restoration, continuous roster6 fields, ordinary walk/jump/punch after return. No full visuals/audio, CPU morph/adversity/KO/finisher or whole-port acceptance.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,fullPortAcceptance=False)))
