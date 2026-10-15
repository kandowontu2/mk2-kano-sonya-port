"""Earned reciprocal-victim fatality completion to native paid new match."""
import json
import re
from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync


def run(side):
    sync.verify()
    out=sync.ROOT/f'audit_bounded_cross_finisher_rejoin_p{side}_checked'
    assert not out.exists()
    reports=[]
    prefix='MK2_STOCK_HEAD_V921_'
    for kind in ('primary','secondary'):
        for fighter in ('kano','sonya'):
            own=17 if fighter=='kano' else 18;victim=18 if own==17 else 17
            victim_name='sonya' if own==17 else 'kano'
            case=sync.ROOT/f'audit_bounded_cross_rejoin_{kind}_{fighter}_p{side}_runtime'
            baseline=sync.ROOT/f'audit_bounded_cross_{kind}_finisher_{fighter}_p{side}_runtime'
            terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes']<=320*1024**2
            assert not (case/'stderr.log').read_text().strip()
            assert not list((case/'snap').rglob('*.png'))
            text=(case/'run.log').read_text()
            assert 'LUA ERROR' not in text
            rows=[]
            for line in text.splitlines():
                if not line.startswith(prefix): continue
                assert re.search(r' victim='+victim_name+' side='+str(3-side)+' killer='+fighter+r' ',line)
                r=fields(line);assert r['writes']=='0' and r['assistance']=='none'
                rows.append((line.split()[0].removeprefix(prefix),r))
            def select(tag): return [r for t,r in rows if t==tag]
            assert not select('CACHE_OVERWRITE') and not select('REJOIN_FAILED') and not select('BOUNDED_FAILED')
            action=select('ACTION');wrap=select('WRAP');live=select('REJOIN_LIVE');done=select('REJOIN_TERMINAL');request=select('REJOIN_REQUEST')
            assert len(action)==len(wrap)==len(live)==len(done)==len(request)==1
            a,w,l,d=action[0],wrap[0],live[0],done[0]
            expected={('primary','kano'):'FFFAAE00',('primary','sonya'):'FFFAB200',('secondary','kano'):'FFD86600',('secondary','sonya'):'FFD7B000'}[kind,fighter]
            assert a['address']==expected and a['variant']==('1' if kind=='primary' else '2') and a['damage']=='322'
            assert [r['count'] for r in select('WIN')]==['1','2']
            health=[r for r in select('HEALTH') if r['pc']=='FF836700' and int(r['after'])<int(r['before'])<=161]
            assert sum(int(r['before'])-int(r['after']) for r in health)==322
            assert sum(r['after']=='0' for r in health)==2
            assert int(a['frame'])<int(w['frame'])<int(l['frame'])<int(d['frame'])
            assert request[0]['native_continue_state']=='2'
            assert int(l['own_id'])==own and int(l['victim_id'])==victim
            assert l['own_actor']==l['own_owner'] and l['victim_actor']==l['victim_owner']
            assert l['own_actor']!=a['actor'] and l['victim_actor']!=a['victim_actor']
            assert int(d['frame'])-int(l['frame'])==60 and d['next_match_survival']=='60'
            cutoff=int(w['frame'])+120
            def core(value): return [line for line in value.splitlines() if line.startswith(prefix) and not line.startswith(prefix+'REJOIN') and int(fields(line)['frame'])<cutoff]
            assert core(text)==core((baseline/'run.log').read_text())
            reports.append({'kind':kind,'fighter':fighter,'side':side,'action':a,'wrap':w,'newMatch':l,'survival':d,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finitePaidRejoinPassed':True,'transitionRasterAcceptance':False,'audioAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print(f'PASS: four P{side} earned reciprocal fatality paid rejoins and fresh true-ID/owner matches')


if __name__=='__main__': run(1)
