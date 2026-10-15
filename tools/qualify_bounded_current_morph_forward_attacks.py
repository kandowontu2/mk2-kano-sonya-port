"""Actual pre-store cancellation branch; never mislabel cancelled choice a morph."""
import copy
import json
import re
import verify_native_source_sync as sync


def gate(rows,target,side):
    assert not any(rows.get(tag) for tag in ('ERROR','STORE','OTHER_STORE','PAIR_MISSING'))
    result=rows['RESULT'][0]
    assert result['forms']==result['restores']=='0' and result['errors']=='0'
    choice=rows['CHOICE'];assert len(choice)==1
    assert choice[0]['id']==('17' if target=='kano' else '18') and choice[0]['pc']=='FF86E490'
    attack=rows['ATTACK'];assert len(attack)==1
    assert int(attack[0]['frame'])==int(choice[0]['frame'])+2 and int(attack[0]['slot'])==3-side
    hits=[r for r in rows['HEALTH'] if int(r['slot'])==side and int(r['before'])>int(r['after'])]
    assert len(hits)==1 and hits[0]['before']=='161' and hits[0]['after']=='121' and hits[0]['pc']=='FF836700'
    assert int(choice[0]['frame'])<int(hits[0]['frame'])
    match=rows['MATCH'][0]
    fields=rows['FIELD']
    assert [int(r['age']) for r in fields]==list(range(2401))
    for r in fields:
        assert r['actor']==match['actor'] and r['main']==match['main'] and r['roster']==r['id']=='6'
        assert r['mode']=='2' and r['state']=='1'
    pairs=rows['PAIR']
    for slot in (1,2):
        own=[r for r in pairs if int(r['slot'])==slot]
        assert [int(r['age']) for r in own]==list(range(2401))
        assert all(r['actor']==r['owner'] and r['mode']=='2' and r['state']=='1' and r['id']==r['roster']==('6' if slot==side else '17') for r in own)
        final=own[-1]
        assert final['action']=='0303' and final['y']==final['floor']
        assert all(int(final[k],16)==0 for k in ('vx','vy','gravity','trail'))
        assert int(final['flags'],16)&0x1c==int(final['body'],16)&0x0c==0
    enemy=next(r for r in pairs if int(r['slot'])==3-side and r['frame']==hits[0]['frame'])
    assert hits[0]['a8']==enemy['actor']
    post=[r for r in fields if int(r['age'])>=1100]
    assert any(r['x']!=post[0]['x'] for r in post)
    assert any(r['action']=='030B' and int(r['vy'],16)!=0 for r in post)
    assert any(r['action']=='0101' for r in post)
    return dict(nativeChoiceFrame=int(choice[0]['frame']),nativeHitFrame=int(hits[0]['frame']),
                damage=40,cancelledBeforeIdentityStore=True,continuousPairedFields=2401,ordinaryControlsAfterCancellation=True)


if __name__=='__main__':
    out=sync.ROOT/'audit_bounded_current_morph_forward_attacks_checked';assert not out.exists()
    results={}
    for target in ('kano','sonya'):
        for side in (1,2):
            folder=sync.ROOT/f'audit_bounded_current_morph_forward_attack_{target}_p{side}_runtime'
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
            broken=copy.deepcopy(rows);broken['FIELD'][200]['id']='17'
            try:gate(broken,target,side)
            except AssertionError:pass
            else:raise AssertionError('Unexpected cancelled-morph identity accepted')
            results[target+str(side)]=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),unexpectedIDRejected=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullPortAcceptance=False,
        scope='Four current40damage attacks during forward transformation: native target choice then cancellation before ID store, true Shang identity/roster/ownership continuously, ordinary controls/clean paired physics. Not a completed morph; no KO/CPU/art/audio/port acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,fullPortAcceptance=False)))
