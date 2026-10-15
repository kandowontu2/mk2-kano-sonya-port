"""Qualify exposed marble observations without treating occlusion as alignment."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
def rows(folder):
    result={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_UI_'):
            tag=line.split()[0][7:]
            result.setdefault(tag,[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return result

out=sync.ROOT/'audit_bounded_css_background_observed';assert not out.exists()
proof_path=sync.ROOT/'audit_bounded_css_cadence_checked/report.json'
proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
for fighter in ('kano','sonya'):
    for side in (1,2):
        key=f'{fighter}P{side}'
        folder=sync.ROOT/f'audit_bounded_css_background_{fighter}_p{side}_runtime'
        base=sync.ROOT/f'audit_bounded_css_cadence_{fighter}_p{side}_runtime'
        assert sync.sha(base/'run.log')==proof['results'][key]['logSHA256']
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None and t['rawMedia']=='none'
        actual,old=rows(folder),rows(base)
        for tag in ('SELECT','INPUT','FIELD','CADENCE','RESULT'):assert actual[tag]==old[tag]
        bg=actual['BACKGROUND']
        stock=[r for r in bg if 78<=int(r['age'])<=94];assert len(stock)==17
        baseline={r['hash'] for r in stock};assert len(baseline)==1
        own=[r for r in bg if 54<=int(r['age'])<=70 or 224<=int(r['age'])<=260];assert len(own)==54
        matches=sum(r['hash'] in baseline for r in own)
        if fighter=='sonya':assert matches==54
        else:assert 0<matches<54
        results[key]=dict(terminal=t,stockEdgeHash=next(iter(baseline)),selectedEdgeFields=len(own),matchingFields=matches,exposedStripAlignmentProven=fighter=='sonya',kanoVaryingSignatureCauseUnproven=fighter=='kano',logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),priorProofSHA256=sync.sha(proof_path),checkerSHA256=sync.sha(Path(__file__)),scope='Eight-pixel exposed edge only. Sonya matches stock; Kano occlusion versus backdrop variation unresolved. Full occluded background and alignment not accepted.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,sonyaEdgeContexts=2,kanoAlignmentUnresolved=True)))

