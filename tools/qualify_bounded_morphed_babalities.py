"""Native transformed Kano baby flow and Sonya punch-eligibility rejection."""
import inspect,json
import verify_native_source_sync as sync
import qualify_bounded_current_babalities as prior
from qualify_bounded_current_friendships import fields

source=inspect.getsource(prior.validate)
before="int(r['id']) == own and int(r['roster']) == own"
assert source.count(before)==1
source=source.replace(before,"int(r['id']) in (6,own) and int(r['roster']) == 6")
namespace=dict(fields=fields)
exec(compile(source,__file__+'::retained_baby_handoff_gate','exec'),namespace)
positive=namespace['validate']

def validate(text,fighter,side):
    rows=[(line.split()[0].removeprefix('MK2_NATIVE_BABY_'),fields(line)) for line in text.splitlines() if line.startswith('MK2_NATIVE_BABY_')]
    def tagged(tag):return [r for t,r in rows if t==tag]
    assert rows and all(r['writes']=='0' and r['assistance']=='none' and int(r['winner_slot'])==side for _,r in rows)
    assert not tagged('HOST_BOUND')
    ident=17 if fighter=='kano' else 18
    choices=tagged('SELECT_ID');assert len(choices)==2 and all(r['actual']==r['target'] for r in choices)
    assert next(r for r in choices if int(r['slot'])==side)['actual']=='6'
    stores=tagged('MORPH_STORE');assert len(stores)==2
    form,restore=stores
    assert (form['old'],form['id'],form['roster'],form['pc'],form['a9'])==('6',str(ident),'6','FF86E670',f'{ident:08X}')
    assert (restore['old'],restore['id'],restore['roster'],restore['pc'],restore['a0'])==(str(ident),'6','6','FFA16700','00000006')
    assert (form['actor'],form['main'])==(restore['actor'],restore['main'])
    damage=tagged('DAMAGE');assert all(r['pc']=='FF836700' and int(r['before'])>int(r['after'])>=0 for r in damage)
    assert sum(int(r['before'])-int(r['after']) for r in damage)==322
    zeros=[r for r in damage if r['after']=='0']
    assert len(zeros)==2 and int(zeros[0]['frame'])<int(form['frame'])<int(zeros[1]['frame'])
    plan=tagged('MORPH_PLAN');assert len(plan)==1
    due=int(plan[0]['due'])
    actual={(int(r['frame']),r['button']) for r in tagged('INPUT') if int(r['slot'])==side and due<=int(r['frame'])<due+40}
    if fighter=='kano':
        back='Left' if side==1 else 'Right'
        expected={(due+i,back) for i in(0,1,8,9)}|{(due+i,'Down') for i in(4,5)}|{(due+i,'Low_Kick') for i in(8,9)}
    else:expected={(due+i,key) for i in range(8) for key in('Down','Low_Punch','Block')}
    assert actual==expected
    window=tagged('FINISH_WINDOW');result=tagged('RESULT')
    assert len(window)==len(result)==1
    w,r=window[0],result[0]
    assert w['native_kos']=='2' and w['damage']==r['damage']=='322' and r['wins']=='2'
    assert r['winner']==fighter and r['case']=='positive' and w['hp_counters']=='0,0'
    if fighter=='kano':
        positive(text,fighter,side)
        assert int(form['frame'])<int(r['action'])<int(restore['frame'])
        assert any(e['entry']=='FF87E520' and e['a8']==form['actor'] and e['a13']==form['main'] for e in tagged('ENTRY'))
        for p in tagged('FIELD'):
            if int(p['slot'])!=side:continue
            expected_id=ident if int(p['frame'])<int(restore['frame']) else 6
            assert int(p['id'])==expected_id and p['roster']=='6'
        return dict(outcome='native_babality_handoff_retirement_reuse',result=r)
    lp=[int(v) for v in w['lp_counters'].split(',')]
    assert lp[side-1]>0 and lp[2-side]==0 and r['action']=='-1'
    assert not tagged('CONSTRUCT') and not tagged('BABY')
    assert not any(e['entry']=='FF87E520' for e in tagged('ENTRY'))
    assert any(e['entry']=='FF87E120' and e['a8']==form['actor'] for e in tagged('ENTRY'))
    return dict(outcome='native_low_punch_eligibility_rejection',lowPunchCounter=lp[side-1],result=r)

if __name__=='__main__':
    source_sync=sync.verify()
    out=sync.ROOT/'audit_bounded_morphed_babalities_checked';assert not out.exists()
    lua=sync.ROOT/'audit_bounded_morphed_babalities_preparation/babalities.lua'
    cases={}
    for fighter in('kano','sonya'):
        for side in(1,2):
            folder=sync.ROOT/f'audit_bounded_morphed_babality_{fighter}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in('.png','.bin','.wav') for p in folder.rglob('*'))
            text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
            proof=validate(text,fighter,side)
            corrupt=text.replace('pc=FF86E670','pc=DEADBEEF');assert corrupt!=text
            try:validate(corrupt,fighter,side)
            except AssertionError:pass
            else:raise AssertionError('Foreign morph writer accepted')
            cases[f'{fighter}{side}']=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),foreignMorphWriterRejected=True)
    report=dict(passed=True,cases=cases,sourceSync=source_sync,fullPortAcceptance=False,
        scope='Both-slot actual Kano-form babality, native baby victim handoff/retirement/reuse and Shang restoration. Both-slot actual Sonya morph with nonzero native LP counter and rejected baby command. No successful Sonya-form baby, full art/audio, morphed victim, CPU, campaign or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,successfulBabalities=2,nativeEligibilityRejections=2,fullPortAcceptance=False)))
