"""Earned friendly finisher to paid rejoin; no raster/audio certification."""
import json
from qualify_bounded_current_friendships import fields, validate as validate_friend
from qualify_bounded_current_babalities import validate as validate_baby
import verify_native_source_sync as sync


def validate_rejoin(text, prefix, own, side):
    rows=[(line.split()[0],fields(line)) for line in text.splitlines() if line.startswith(prefix)]
    def select(tag): return [r for t,r in rows if t==prefix+tag]
    assert not select('HOST_BOUND') and not select('REJOIN_FAILED')
    request=select('REJOIN_REQUEST');css=select('REJOIN_CSS');live=select('REJOIN_LIVE');done=select('REJOIN_TERMINAL')
    assert len(request)==len(css)==len(live)==len(done)==1
    assert request[0]['mode']=='3' and request[0]['loser_state']=='2'
    assert int(request[0]['frame'])<int(css[0]['frame'])<int(live[0]['frame'])<int(done[0]['frame'])
    assert int(done[0]['frame'])-int(live[0]['frame'])==60 and done[0]['next_match_survival']=='60'
    r=live[0]
    assert int(r['own_id'])==own and int(r['victim_id'])==(18 if own==17 else 17)
    assert r['own_actor']==r['own_owner'] and r['victim_actor']==r['victim_owner']
    for key in ('own_actor','victim_actor'): assert 0x01000000<=int(r[key],16)<0x01100000
    assert r['own_actor']!=r['victim_actor']
    selections=select('SELECT_ID')
    assert len(selections)==4 and all(r['actual']==r['target'] for r in selections)
    assert all(sum(int(r['slot'])==n for r in selections)==2 for n in (1,2))
    inputs=select('INPUT')
    request_frame=int(request[0]['frame'])
    coins=[int(r['frame'])-request_frame for r in inputs if int(r['slot'])==3-side and r['button']=='Coin' and int(r['frame'])>=request_frame]
    starts=[int(r['frame'])-request_frame for r in inputs if int(r['slot'])==3-side and r['button']=='Start' and int(r['frame'])>=request_frame]
    assert coins==list(range(20,25))+list(range(270,275)) and starts==list(range(310,315))
    return {'request':request[0],'css':css[0],'live':live[0],'terminal':done[0]}


def main():
    sync.verify()
    out=sync.ROOT/'audit_bounded_friendly_rejoin_checked'
    assert not out.exists()
    reports=[]
    for kind in ('friendship','babality'):
        prefix='MK2_FRIEND_' if kind=='friendship' else 'MK2_NATIVE_BABY_'
        validator=validate_friend if kind=='friendship' else validate_baby
        lua=sync.ROOT/f'audit_bounded_friendly_rejoin_both_selectors_preparation/{kind}.lua'
        for fighter in ('kano','sonya'):
            own=17 if fighter=='kano' else 18
            for side in (1,2):
                case=sync.ROOT/f'audit_bounded_rejoin_both_selectors_{kind}_{fighter}_p{side}_runtime'
                original=sync.ROOT/f'audit_bounded_current_{kind}_{fighter}_p{side}_runtime'
                terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
                assert terminal['exitCode']==0 and terminal['limitReason'] is None
                assert terminal['peakWorkingSetBytes']<=320*1024**2
                assert terminal['observerSha256'].lower()==sync.sha(lua).lower()
                assert not (case/'stderr.log').read_text().strip()
                assert not list((case/'snap').rglob('*.png'))
                text=(case/'run.log').read_text();baseline=(original/'run.log').read_text()
                assert 'LUA ERROR' not in text
                validator(baseline,fighter,side)
                cutoff=int(fields(next(line for line in baseline.splitlines() if line.startswith(prefix+'RESULT')))['frame'])
                def core(value):
                    return [line for line in value.splitlines() if line.startswith(prefix) and not line.startswith(prefix+'RESULT') and not line.startswith(prefix+'REJOIN') and int(fields(line)['frame'])<cutoff]
                assert core(text)==core(baseline),'Finisher observations changed before baseline stop'
                result=validate_rejoin(text,prefix,own,side)
                for before,after in (('next_match_survival=60','next_match_survival=0'),(f'own_id={own}', 'own_id=1')):
                    try: validate_rejoin(text.replace(before,after),prefix,own,side)
                    except AssertionError: pass
                    else: raise AssertionError('Fault accepted: '+before)
                reports.append({'kind':kind,'fighter':fighter,'side':side,'rejoin':result,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finitePaidRejoinPassed':True,'transitionRasterAcceptance':False,'audioAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print('PASS: eight earned friendly-finisher paid rejoins, true identities/owners, sixty new-match fields')


if __name__=='__main__': main()
