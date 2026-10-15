"""Preserve complete presented-signature comparisons, including real differences."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    groups={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_UI_'):
            groups.setdefault(line.split()[0][7:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return groups

out=sync.ROOT/'audit_bounded_ladder_scanout_observed';assert not out.exists();results={}
proof_path=sync.ROOT/'audit_bounded_css_teardown_owner_checked/report.json';proof=json.loads(proof_path.read_text());assert proof['passed']
for fighter in ('kano','sonya'):
    for side in (1,2):
        key=f'{fighter}P{side}';cases={}
        for suffix in ('added','stock'):
            folder=sync.ROOT/f'audit_bounded_ladder_scanout_{fighter}_p{side}_{suffix}_runtime'
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None and t['rawMedia']=='none'
            cases[suffix]=(load(folder),dict(terminal=t,logSHA256=sync.sha(folder/'run.log')))
        actual=cases['added'][0];control=cases['stock'][0]
        base=sync.ROOT/f'audit_bounded_css_teardown_owner_{fighter}_p{side}_runtime'
        assert sync.sha(base/'run.log')==proof['results'][key]['logSHA256']
        prior=load(base)
        for tag in ('SELECT','INPUT','FIELD','CADENCE','TEARDOWN','RESULT'):assert actual[tag]==prior[tag]
        a,b=actual['SCANOUT'],control['SCANOUT']
        assert len(a)==len(b)==529
        assert [int(r['age']) for r in a]==[int(r['age']) for r in b]==list(range(529))
        assert all(r['stock']=='0' for r in a) and all(r['stock']=='1' for r in b)
        differences={region:[int(x['age']) for x,y in zip(a,b) if x[region]!=y[region]] for region in ('left','right')}
        first=min(age for values in differences.values() for age in values)
        assert first>0
        assert cases['added'][0]['FIELD'][0]['roster'] in ('17','18')
        results[key]=dict(cases={suffix:data[1] for suffix,data in cases.items()},pairedPresentedFields=529,initialBothRegionsMatchingFields=first,allDifferingAges=differences,laterDifferencesClassified=False,wholeLadderRasterAcceptance=False)
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),priorProofSHA256=sync.sha(proof_path),scope='Complete scalar presented-region observations, not acceptance of all later pixels. Character-dependent ladder portrait and match construction require classification. 64-bit FNV signatures, not stored rasters or bytewise equality.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,observedPairs=4,laterDifferencesUnresolved=True)))
