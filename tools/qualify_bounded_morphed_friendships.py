"""Finite genuine Kano friendship and Sonya native punch-eligibility rejection."""
import inspect,json,re
import qualify_bounded_current_friendships as prior
import verify_native_source_sync as sync

source=inspect.getsource(prior.validate)
source=source.replace("['actual'] == str(own)","['actual'] == '6'")
source=source.replace("r['roster'] == str(own)","r['roster'] == '6'")
namespace=dict(fields=prior.fields)
exec(compile(source,__file__+'::original_friendship_gate','exec'),namespace)
positive=namespace['validate']

def validate(text,fighter,side):
    rows=[(line.split()[0].removeprefix('MK2_FRIEND_'),prior.fields(line)) for line in text.splitlines() if line.startswith('MK2_FRIEND_')]
    def tagged(tag): return [r for t,r in rows if t==tag]
    assert rows and all(r['writes']=='0' and r['assistance']=='none' and r['winner']==fighter and int(r['side'])==side and r['case']=='positive' for _,r in rows)
    assert not tagged('HOST_BOUND')
    identity=17 if fighter=='kano' else 18
    choices=tagged('SELECT_ID')
    assert len(choices)==2 and all(r['actual']==r['target'] for r in choices)
    assert next(r for r in choices if int(r['slot'])==side)['actual']=='6'
    forms=[r for r in tagged('MORPH_STORE') if r['old']=='6' and r['id']==str(identity)]
    assert len(forms)==1
    form=forms[0]
    assert (form['roster'],form['pc'],form['a9'])==('6','FF86E670',f'{identity:08X}')
    for r in tagged('MORPH_STORE'):
        assert r==form or(r['old']==str(identity) and r['id']=='6' and r['pc']=='FFA16700' and r['a0']=='00000006' and r['roster']=='6')
    damage=tagged('DAMAGE')
    assert all(r['pc']=='FF836700' and int(r['before'])>int(r['after'])>=0 for r in damage)
    assert sum(int(r['before'])-int(r['after']) for r in damage)==322
    zeros=[r for r in damage if r['after']=='0']
    assert len(zeros)==2 and int(zeros[0]['frame'])<int(form['frame'])<int(zeros[1]['frame'])
    plan=tagged('MORPH_PLAN'); assert len(plan)==1
    due=int(plan[0]['due'])
    presses={(int(r['frame']),r['button']) for r in tagged('INPUT') if int(r['slot'])==side and due<=int(r['frame'])<due+40}
    if fighter=='kano':
        back='Left' if side==1 else 'Right'
        expected={(due+i,back) for i in(0,1,8,9)}|{(due+i,'Down') for i in(4,5)}|{(due+i,'Low_Kick') for i in(8,9)}
    else: expected={(due+i,k) for i in range(8) for k in('Down','Low_Punch','Block')}
    assert presses==expected
    window=tagged('WINDOW');result=tagged('RESULT')
    assert len(window)==len(result)==1
    w,r=window[0],result[0]
    assert w['kos']==r['kos']=='2' and w['damage']==r['damage']=='322'
    assert w['hp_counters']=='0,0'
    if fighter=='kano':
        positive(text,fighter,side)
        assert all((p['actor'],p['main'])==(form['actor'],form['main']) for p in tagged('POSE'))
        return dict(outcome='native_friendship_completed_and_retired',result=r)
    counters=[int(v) for v in w['lp_counters'].split(',')]
    assert counters[side-1]>0 and counters[2-side]==0
    assert r['action']=='-1' and r['cleanup']=='false'
    assert not tagged('POSE') and not any(e['entry']=='FFFCE000' for e in tagged('ENTRY'))
    assert any(e['entry']=='FF880770' and e['id']=='18' and e['a8']==form['actor'] for e in tagged('ENTRY'))
    samples=tagged('FIELD')
    assert samples and int(samples[-1]['age'])>=720 and samples[-1]['finish']!='3'
    return dict(outcome='native_low_punch_eligibility_rejection',lowPunchCounter=counters[side-1],result=r)

if __name__=='__main__':
    source_sync=sync.verify()
    out=sync.ROOT/'audit_bounded_morphed_friendships_checked'; assert not out.exists()
    lua=sync.ROOT/'audit_bounded_morphed_friendship_followthrough_preparation/friendships.lua'
    results={}
    for fighter in('kano','sonya'):
        for side in(1,2):
            folder=sync.ROOT/f'audit_bounded_morphed_friendship_followthrough_{fighter}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in('.png','.bin','.wav') for p in folder.rglob('*'))
            text=(folder/'run.log').read_text(); assert 'LUA ERROR' not in text
            proof=validate(text,fighter,side)
            bad=text.replace('pc=FF86E670','pc=DEADBEEF')
            assert bad!=text
            try: validate(bad,fighter,side)
            except AssertionError: pass
            else: raise AssertionError('Foreign morph writer accepted')
            results[f'{fighter}{side}']=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),foreignMorphWriterRejected=True)
    report=dict(passed=True,results=results,sourceSync=source_sync,fullPortAcceptance=False,
        scope='Both-slot genuine Kano-form friendships with cleanup/retirement and both-slot Sonya-form native LP eligibility rejection. Counters untouched. No successful Sonya-form friendship claim, no babality/morphed victim/complete art/audio/CPU/campaign acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,successfulFriendships=2,nativeEligibilityRejections=2,fullPortAcceptance=False)))
