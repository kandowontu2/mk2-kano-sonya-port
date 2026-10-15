"""Original earned/cache/completion gates with same-ID distinct actors."""
import copy
import inspect
import json
import re
from qualify_bounded_stock_head_finisher import gate
import verify_native_source_sync as sync


def run(side):
    sync.verify()
    out=sync.ROOT/f'audit_bounded_mirror_finishers_p{side}_checked'
    assert not out.exists()
    source=inspect.getsource(gate).replace("a['address']=='FF8CB4A0'","a['address']==expected_address").replace("a['variant']=='1'","a['variant']==expected_variant").replace("x['own'].split(':')[-1]=='3'","x['own'].split(':')[-1]==str(identity)")
    reports=[]
    for kind in ('primary','secondary'):
        for fighter in ('kano','sonya'):
            identity=17 if fighter=='kano' else 18
            address={('primary','kano'):'FFFAAE00',('primary','sonya'):'FFFAB200',('secondary','kano'):'FFD86600',('secondary','sonya'):'FFD7B000'}[kind,fighter]
            context={'expected_address':address,'expected_variant':'1' if kind=='primary' else '2','identity':identity}
            exec(compile(source,__file__,'exec'),context)
            check=context['gate']
            case=sync.ROOT/f'audit_bounded_mirror_{kind}_finisher_{fighter}_p{side}_runtime'
            terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes']<=320*1024**2
            assert not (case/'stderr.log').read_text().strip()
            assert not list((case/'snap').rglob('*.png'))
            rows=[]
            for line in (case/'run.log').read_text().splitlines():
                assert 'LUA ERROR' not in line
                if not line.startswith('MK2_STOCK_HEAD_V921_'): continue
                assert re.search(r' victim='+fighter+' side='+str(3-side)+' killer='+fighter+r' ',line)
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['writes']=='0' and r['assistance']=='none'
                rows.append((line.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),r))
            result=check(rows,fighter,identity)
            for key,value in (('damage','321'),('wins','1'),('wrap','0')):
                bad=copy.deepcopy(rows);next(r for t,r in bad if t=='RESULT')[key]=value
                try: check(bad,fighter,identity)
                except AssertionError: pass
                else: raise AssertionError('Original fault accepted: '+key)
            reports.append({'kind':kind,'fighter':fighter,'winnerSide':side,'result':result,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finiteMirrorMechanicsPassed':True,'artAudioAcceptance':False,'transitionAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print(f'PASS: four P{side} earned mirror fatalities, distinct actors, correct native actions/completion')


if __name__=='__main__': run(1)
