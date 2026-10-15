"""Reuse all original earned/native wrap/cache gates with actual added IDs."""
import copy
import inspect
import json
import re
from qualify_bounded_stock_head_finisher import gate
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_cross_primary_finishers_checked'
assert not out.exists()
gate_source=inspect.getsource(gate)
assert gate_source.count("a['address']=='FF8CB4A0'")==1
assert gate_source.count("x['own'].split(':')[-1]=='3'")==1
gate_source=gate_source.replace("a['address']=='FF8CB4A0'","a['address']==expected_address")
gate_source=gate_source.replace("x['own'].split(':')[-1]=='3'","x['own'].split(':')[-1]==str(killer_id)")
reports=[]
for fighter,killer_id,address in (('kano',17,'FFFAAE00'),('sonya',18,'FFFAB200')):
    victim='sonya' if fighter=='kano' else 'kano'
    victim_id=18 if killer_id==17 else 17
    context={'expected_address':address,'killer_id':killer_id}
    exec(compile(gate_source,__file__,'exec'),context)
    check=context['gate']
    for winner_side in (1,2):
        case=sync.ROOT/f'audit_bounded_cross_primary_finisher_{fighter}_p{winner_side}_runtime'
        terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<=320*1024**2
        assert not (case/'stderr.log').read_text().strip()
        rows=[]
        for line in (case/'run.log').read_text().splitlines():
            assert 'LUA ERROR' not in line
            if not line.startswith('MK2_STOCK_HEAD_V921_'): continue
            assert re.search(r' victim='+victim+' side='+str(3-winner_side)+' killer='+fighter+r' ',line)
            tag=line.split()[0].removeprefix('MK2_STOCK_HEAD_V921_')
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            assert r['writes']=='0' and r['assistance']=='none'
            rows.append((tag,r))
        result=check(rows,victim,victim_id)
        for key,value in (('damage','321'),('wins','1'),('wrap','0')):
            bad=copy.deepcopy(rows)
            next(r for t,r in bad if t=='RESULT')[key]=value
            try: check(bad,victim,victim_id)
            except AssertionError: pass
            else: raise AssertionError('Original fault accepted: '+key)
        assert not list((case/'snap').rglob('*.png'))
        reports.append({'performer':fighter,'winnerSide':winner_side,'victim':victim,'result':result,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
out.mkdir()
(out/'report.json').write_text(json.dumps({'finiteCrossPrimaryMechanicsPassed':True,'artAudioAcceptance':False,'allVictimsAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
print('PASS: four earned reciprocal added-victim primary fatalities, native completion, no observed cache overwrite')
