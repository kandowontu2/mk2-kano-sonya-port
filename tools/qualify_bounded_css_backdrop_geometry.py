"""Actual stock backdrop FIFO invariance across physical Kano/Liu navigation."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    groups={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_UI_'):
            tag=line.split()[0][7:]
            groups.setdefault(tag,[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return groups

def gate(draw):
    groups={age:[tuple(r[k] for k in ('actor','id','xy','size','source','command')) for r in draw if int(r['age'])==age and r['source'].startswith('05C')] for age in (66,90,228)}
    assert all(len(v)==15 for v in groups.values())
    assert groups[66]==groups[90]==groups[228]
    assert any(r['id']=='17' and r['source'].startswith('100') for r in draw if r['age']=='66')
    assert any(r['id']=='1' and r['source'].startswith('004B') for r in draw if r['age']=='90')
    return groups

out=sync.ROOT/'audit_bounded_css_backdrop_geometry_checked';assert not out.exists();results={}
proof_path=sync.ROOT/'audit_bounded_css_background_observed/report.json';proof=json.loads(proof_path.read_text());assert proof['passed']
for side in (1,2):
    folder=sync.ROOT/f'audit_bounded_css_draw_fetch_kano_p{side}_runtime'
    base=sync.ROOT/f'audit_bounded_css_background_kano_p{side}_runtime'
    assert sync.sha(base/'run.log')==proof['results'][f'kanoP{side}']['logSHA256']
    t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None and t['rawMedia']=='none'
    actual,old=load(folder),load(base)
    for tag in ('SELECT','INPUT','FIELD','CADENCE','BACKGROUND','RESULT'):assert actual[tag]==old[tag]
    geometry=gate(actual['DRAW']);bad=copy.deepcopy(actual['DRAW'])
    target=next(r for r in bad if r['age']=='66' and r['source'].startswith('05C'))
    target['xy']=f"{int(target['xy'],16)+1:08X}"
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('One-pixel shifted backdrop accepted')
    results[f'kanoP{side}']=dict(terminal=t,backdropDrawsPerSample=15,sampledAges=[66,90,228],exactBackdropGeometrySourceAndOrderMatch=True,onePixelShiftFaultRejected=True,stockReferenceGeometry=geometry[90],logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),priorProofSHA256=sync.sha(proof_path),checkerSHA256=sync.sha(Path(__file__)),scope='Native 05C-series backdrop FIFO commands unchanged at three selection samples in both slots. Does not accept full rendered composition, occluded pixel parity or every transition.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=2,backdropGeometryUnchanged=True)))
