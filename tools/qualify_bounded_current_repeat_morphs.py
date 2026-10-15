"""Three actual native cycles per form/slot, complete finite paired chronology."""
import copy
import json
import re
import verify_native_source_sync as sync


def gate(rows,target,side):
    identity=17 if target=='kano' else 18
    assert not rows.get('ERROR') and not rows.get('PAIR_MISSING') and not rows.get('OTHER_STORE')
    result=rows['RESULT'][0]
    assert result['forms']==result['restores']=='3' and result['errors']=='0'
    stores=rows['STORE']
    expected=[('6',str(identity),'FF86E670'),(str(identity),'6','FFA16700')]*3
    assert [(r['old'],r['id'],r['pc']) for r in stores]==expected
    match=rows['MATCH'][0]
    assert all(r['actor']==match['actor'] and r['main']==match['main'] for r in stores)
    fields=rows['FIELD']
    assert [int(r['age']) for r in fields]==list(range(2401))
    for r in fields:
        current=6
        for store in stores:
            if int(store['frame'])<int(r['frame']):current=int(store['id'])
        assert r['actor']==match['actor'] and r['main']==match['main'] and r['roster']=='6' and int(r['id'])==current
        assert r['mode']=='2' and r['state']=='1' and r['hp1']==r['hp2']=='161'
    pairs=rows['PAIR']
    for slot in (1,2):
        own=[r for r in pairs if int(r['slot'])==slot]
        assert [int(r['age']) for r in own]==list(range(2401))
        assert all(r['actor']==r['owner'] and r['mode']=='2' and r['state']=='1' for r in own)
    for store in stores:
        later=next(r for r in pairs if int(r['slot'])==side and int(r['frame'])==int(store['frame'])+40)
        assert later['id']==store['id'] and later['roster']=='6' and later['action']=='0303'
        assert later['y']==later['floor']
        assert all(int(later[k],16)==0 for k in ('vx','vy','gravity','trail'))
        assert int(later['flags'],16)&0x1c==int(later['body'],16)&0x0c==0
    final=fields[-1]
    assert final['id']=='6' and final['action']=='0303' and final['y']==final['floor']
    return dict(nativeStores=[dict(frame=int(r['frame']),id=int(r['id']),pc=r['pc']) for r in stores],
                cycles=3,continuousPairedFields=2401,eachFormAndReturnClean=True)


if __name__=='__main__':
    out=sync.ROOT/'audit_bounded_current_repeat_morphs_checked';assert not out.exists()
    results={}
    for target in ('kano','sonya'):
        for side in (1,2):
            folder=sync.ROOT/f'audit_bounded_current_repeat_morph_{target}_p{side}_runtime'
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
            broken=copy.deepcopy(rows);broken['STORE']=broken['STORE'][:-1]
            try:gate(broken,target,side)
            except AssertionError:pass
            else:raise AssertionError('Missing final native restoration accepted')
            results[target+str(side)]=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),missingFinalReturnRejected=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullPortAcceptance=False,
        scope='Twelve current physical added-form morph/return cycles across bothslots; all actual native ID stores, roster6, complete paired fields, clean form/return physics and unchanged health. No CPU/KO/finisher/full art/audio or whole-port acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,cycles=12,fullPortAcceptance=False)))
