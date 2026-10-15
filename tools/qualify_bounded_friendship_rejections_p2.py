"""Opposite-slot finite friendship rejection checks."""
import json
from qualify_bounded_friendship_rejections_p1 import validate
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_friendship_rejections_p2_checked'
assert not out.exists()
reports=[]
lua=sync.ROOT/'audit_bounded_current_friendships_preparation/friendships.lua'
for fighter in ('kano','sonya'):
    for case_name in ('wrong_command','punch_used'):
        case=sync.ROOT/f'audit_bounded_friendship_{case_name}_{fighter}_p2_runtime'
        terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes'] <= 320*1024**2
        assert terminal['observerSha256'].lower()==sync.sha(lua).lower()
        assert not (case/'stderr.log').read_text().strip()
        assert not list((case/'snap').rglob('*.png'))
        text=(case/'run.log').read_text()
        assert 'LUA ERROR' not in text
        result=validate(text,fighter,case_name,2)
        for before,after in (('damage=322','damage=321'),('action=-1','action=4000')):
            try: validate(text.replace(before,after),fighter,case_name,2)
            except AssertionError: pass
            else: raise AssertionError('Fault accepted: '+before)
        reports.append({'fighter':fighter,'side':2,'case':case_name,'result':result,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
out.mkdir()
(out/'report.json').write_text(json.dumps({'finiteRejectionPassed':True,'exhaustiveInputs':False,'releaseAcceptance':False,'cases':reports},indent=2))
print('PASS: four earned P2 friendship rejection cases')
