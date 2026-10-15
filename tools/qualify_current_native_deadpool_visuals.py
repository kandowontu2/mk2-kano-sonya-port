"""Recheck both visual runs and exact scalar equivalence to qualified roles."""
import json
import qualify_current_native_deadpool_roles as acid
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_current_native_deadpool_visuals_checked'
assert not out.exists()
cases=[]
for fighter,side in [('kano',1),('sonya',2)]:
    folder=sync.ROOT/f'audit_current_native_deadpool_visual_{fighter}_p{side}_runtime'
    baseline=sync.ROOT/f'audit_current_native_deadpool_gate_hold_{fighter}_p{side}_runtime'
    records=acid.rows(folder/'run.log')
    result=acid.check(records,fighter,side)
    filtered=[r for r in records if r[0]!='VISUAL_SAVED']
    assert filtered==acid.rows(baseline/'run.log')
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    pictures=sorted((folder/'snap').glob('*.png'))
    assert len(pictures)==3 and sum(p.stat().st_size for p in pictures)<=512*1024
    assert [int(r['age']) for tag,r in records if tag=='VISUAL_SAVED']==[60,120,200]
    result.update(scalarBaselineExact=True,logSHA256=sync.sha(folder/'run.log'),
                  images=[{'name':p.name,'bytes':p.stat().st_size,'SHA256':sync.sha(p)} for p in pictures])
    cases.append(result)
out.mkdir()
(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,
    'continuousVisualAudioAcceptance':False,'fullPortAccepted':False},indent=2))
print('PASS both visual runs: earned native gates,801fields, scalar baselines exact, six bounded PNGs')
