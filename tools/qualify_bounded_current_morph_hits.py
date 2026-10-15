"""Actual formed-state native hit and restoration, no KO/scene/art acceptance."""
import copy
import json
import re
import verify_native_source_sync as sync


def gate(rows,target,side):
    identity=17 if target=='kano' else 18
    assert not rows.get('ERROR') and not rows.get('PAIR_MISSING')
    result=rows['RESULT'][0]
    assert result['forms']==result['restores']=='1' and result['errors']=='0'
    match=rows['MATCH'][0];actor,main=match['actor'],match['main']
    stores=rows['STORE']
    assert [(r['old'],r['id'],r['pc']) for r in stores]==[('6',str(identity),'FF86E670'),(str(identity),'6','FFA16700')]
    assert all(r['actor']==actor and r['main']==main for r in stores)
    fields=rows['FIELD']
    assert [int(r['age']) for r in fields]==list(range(2401))
    for r in fields:
        current=6
        for store in stores:
            if int(store['frame'])<int(r['frame']):current=int(store['id'])
        assert r['actor']==actor and r['main']==main and r['roster']=='6' and int(r['id'])==current
        assert r['mode']=='2' and r['state']=='1'
    pairs=rows['PAIR']
    for slot in (1,2):
        own=[r for r in pairs if int(r['slot'])==slot]
        assert [int(r['age']) for r in own]==list(range(2401))
        assert all(r['actor']==r['owner'] and r['state']=='1' and r['mode']=='2' for r in own)
    hits=[r for r in rows['HEALTH'] if int(r['slot'])==side and int(r['before'])>int(r['after'])]
    assert len(hits)==1 and hits[0]['before']=='161' and hits[0]['after']=='121' and hits[0]['pc']=='FF836700'
    hit=hits[0]
    assert int(stores[0]['frame'])<int(hit['frame'])<int(stores[1]['frame'])
    enemy=next(r for r in pairs if int(r['frame'])==int(hit['frame']) and int(r['slot'])==3-side)
    assert hit['a8']==enemy['actor']
    post=[r for r in fields if int(r['age'])>=1100]
    assert any(int(r['x'])!=int(post[0]['x']) for r in post)
    assert any(r['action']=='030B' and int(r['vy'],16)!=0 for r in post)
    assert any(r['action']=='0101' for r in post)
    for slot in (1,2):
        final=next(r for r in pairs if r['age']=='2400' and int(r['slot'])==slot)
        assert final['action']=='0303' and final['y']==final['floor']
        assert all(int(final[k],16)==0 for k in ('vx','vy','gravity','trail'))
        assert int(final['flags'],16)&0x1c==int(final['body'],16)&0x0c==0
    return dict(nativeHitDamage=40,forwardFrame=int(stores[0]['frame']),hitFrame=int(hit['frame']),
                returnFrame=int(stores[1]['frame']),continuousPairedFields=2401,ordinaryPostReturnControls=True)


if __name__=='__main__':
    out=sync.ROOT/'audit_bounded_current_morph_hits_checked';assert not out.exists()
    results={}
    for target in ('kano','sonya'):
        for side in (1,2):
            folder=sync.ROOT/f'audit_bounded_current_morph_hit_{target}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in ('.png','.wav','.bin') for p in folder.rglob('*'))
            rows={}
            for line in (folder/'run.log').read_text().splitlines():
                assert '[LUA ERROR]' not in line and 'hex=' not in line
                if line.startswith('MK2_HUMAN_SHANG_'):
                    rows.setdefault(line.split()[0].removeprefix('MK2_HUMAN_SHANG_'),[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
            proof=gate(rows,target,side)
            broken=copy.deepcopy(rows);broken['STORE'][1]['pc']='00000000'
            try:gate(broken,target,side)
            except AssertionError:pass
            else:raise AssertionError('Wrong restoration store accepted')
            results[target+str(side)]=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),wrongRestorePCRejected=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullPortAcceptance=False,
        scope='Four current real uppercut hits while Shang formed as Kano/Sonya: native40damage, true ID stores/roster6,2401continuous paired fields, timed return and ordinary controls/clean physics. No KO, forward/reverse attack timing, CPU morph, whole visuals/audio/port acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,fullPortAcceptance=False)))
