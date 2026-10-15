"""Finite babality input and native no-punch rejection checks."""
import json
from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync


def validate(text,fighter,case,side):
    rows=[(line.split()[0],fields(line)) for line in text.splitlines() if line.startswith('MK2_NATIVE_BABY_')]
    assert rows
    for _,r in rows:
        assert r['writes']=='0' and r['assistance']=='none' and int(r['winner_slot'])==side
    def select(tag): return [r for t,r in rows if t=='MK2_NATIVE_BABY_'+tag]
    boot=select('BOOT')
    own=17 if fighter=='kano' else 18
    assert len(boot)==1 and int(boot[0]['own_id'])==own and boot[0]['case']==case
    window=select('FINISH_WINDOW')
    assert len(window)==1 and window[0]['native_kos']=='2' and window[0]['damage']=='322'
    counters=[int(n) for n in window[0]['hp_counters'].split(',')]
    assert (counters[side-1]>0) if case=='punch_used' else (counters==[0,0])
    assert window[0]['lp_counters']=='0,0'
    result=select('RESULT')
    assert len(result)==1 and result[0]['action']=='-1'
    assert result[0]['wins']=='2' and result[0]['damage']=='322'
    assert result[0]['winner']==fighter and result[0]['case']==case
    assert int(result[0]['window'])>0
    assert not select('CONSTRUCT') and not select('BABY') and not select('BABY_REUSED')
    assert not any(r['entry']=='FF87E520' for r in select('ENTRY'))
    assert not select('HOST_BOUND')
    states=select('STATE')
    assert states and states[-1]['mode']=='3' and states[-1]['winner']==str(side)
    selections=select('SELECT_ID')
    assert len(selections)==2 and all(r['actual']==r['target'] for r in selections)
    return result[0]


def run(side):
    sync.verify()
    out=sync.ROOT/f'audit_bounded_babality_rejections_p{side}_checked'
    assert not out.exists()
    reports=[]
    lua=sync.ROOT/'audit_bounded_current_babalities_preparation/babalities.lua'
    for fighter in ('kano','sonya'):
        for case_name in ('wrong_direction','punch_used'):
            case=sync.ROOT/f'audit_bounded_babality_{case_name}_{fighter}_p{side}_runtime'
            terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes']<=320*1024**2
            assert terminal['observerSha256'].lower()==sync.sha(lua).lower()
            assert not (case/'stderr.log').read_text().strip()
            assert not list((case/'snap').rglob('*.png'))
            text=(case/'run.log').read_text()
            assert 'LUA ERROR' not in text
            result=validate(text,fighter,case_name,side)
            for before,after in (('damage=322','damage=321'),('action=-1','action=4000')):
                try: validate(text.replace(before,after),fighter,case_name,side)
                except AssertionError: pass
                else: raise AssertionError('Fault accepted: '+before)
            reports.append({'fighter':fighter,'side':side,'case':case_name,'result':result,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finiteRejectionPassed':True,'exhaustiveInputs':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print(f'PASS: four earned P{side} babality rejection cases')


if __name__=='__main__': run(1)
