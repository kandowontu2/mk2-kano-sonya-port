"""Finite P1 command/eligibility rejection, not exhaustive input coverage."""
import json
from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync


def validate(text, fighter, case, side=1):
    rows = [(line.split()[0],fields(line)) for line in text.splitlines() if line.startswith('MK2_FRIEND_')]
    assert rows
    for _,r in rows:
        assert r['writes']=='0' and r['assistance']=='none'
        assert r['case']==case and r['winner']==fighter and int(r['side'])==side
    def select(tag): return [r for t,r in rows if t=='MK2_FRIEND_'+tag]
    window=select('WINDOW')
    assert len(window)==1 and window[0]['kos']=='2' and window[0]['damage']=='322'
    counters=[int(n) for n in window[0]['hp_counters'].split(',')]
    assert (counters[side-1]>0) if case=='punch_used' else (counters==[0,0])
    assert window[0]['lp_counters']=='0,0'
    result=select('RESULT')
    assert len(result)==1 and result[0]['action']=='-1' and result[0]['kos']=='2' and result[0]['damage']=='322'
    assert int(result[0]['window'])>0
    entry='FFFCD000' if fighter=='kano' else 'FFFCE000'
    assert not any(r['entry']==entry for r in select('ENTRY'))
    assert not select('POSE') and not select('HOST_BOUND')
    samples=select('FIELD')
    assert samples and int(samples[-1]['age'])>=720 and samples[-1]['finish']!='3'
    selections=select('SELECT_ID')
    assert len(selections)==2 and all(r['actual']==r['target'] for r in selections)
    return result[0]


def main():
    sync.verify()
    out=sync.ROOT/'audit_bounded_friendship_rejections_p1_checked'
    assert not out.exists()
    reports=[]
    for fighter in ('kano','sonya'):
        for case_name in ('wrong_command','punch_used'):
            case=sync.ROOT/f'audit_bounded_friendship_{case_name}_{fighter}_p1_runtime'
            terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert not (case/'stderr.log').read_text().strip()
            text=(case/'run.log').read_text()
            assert 'LUA ERROR' not in text
            result=validate(text,fighter,case_name)
            for before,after in (('damage=322','damage=321'),('action=-1','action=4000')):
                try: validate(text.replace(before,after),fighter,case_name)
                except AssertionError: pass
                else: raise AssertionError('Fault accepted: '+before)
            reports.append({'fighter':fighter,'case':case_name,'result':result,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finiteRejectionPassed':True,'exhaustiveInputs':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print('PASS: four earned P1 friendship rejection cases')


if __name__=='__main__': main()
