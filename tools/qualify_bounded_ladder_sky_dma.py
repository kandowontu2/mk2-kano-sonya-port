"""Separate original native ladder animation draws from added CSS artifacts."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    result={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_UI_'):
            result.setdefault(line.split()[0][7:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return result

out=sync.ROOT/'audit_bounded_ladder_sky_dma_checked';assert not out.exists()
proof_path=sync.ROOT/'audit_bounded_ladder_scanout_observed/report.json';proof=json.loads(proof_path.read_text());assert proof['passed'];cases={}
for suffix in ('added','stock'):
    folder=sync.ROOT/f'audit_bounded_ladder_sky_dma_sonya_p2_{suffix}_runtime'
    base=sync.ROOT/f'audit_bounded_ladder_scanout_sonya_p2_{suffix}_runtime'
    assert sync.sha(base/'run.log')==proof['results']['sonyaP2']['cases'][suffix]['logSHA256']
    t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None and t['rawMedia']=='none'
    actual,old=load(folder),load(base)
    for tag in ('SELECT','INPUT','FIELD','CADENCE','TEARDOWN','SCANOUT','RESULT'):assert actual[tag]==old[tag]
    cases[suffix]=(actual,dict(terminal=t,logSHA256=sync.sha(folder/'run.log')))
keys=('command','source','palette','palhash','x','y','width','height')
background={}
for age in (86,87,99,100,199,200):
    groups=[]
    for suffix in ('added','stock'):
        selected=[r for r in cases[suffix][0]['SKYDMA'] if int(r['age'])==age]
        assert selected and all(r['pc']=='FF804640' for r in selected)
        assert not any(r['source'] in ('0F008000','0F010000') for r in selected)
        groups.append([tuple(r[k] for k in keys) for r in selected if r['source'].startswith(('05B','05C'))])
    assert groups[0] and groups[0]==groups[1]
    background[str(age)]=len(groups[0])
fragment=next(r for r in cases['added'][0]['SKYDMA'] if r['age']=='86' and r['source']=='045D267C')
assert fragment['palette']=='1400' and fragment['palhash']=='9C980ABF'
assert (fragment['x'],fragment['y'],fragment['width'],fragment['height'])==('347','49','35','25')
assert any(r['palette']=='1400' and r['palhash']==fragment['palhash'] for r in cases['stock'][0]['SKYDMA'])
assert any(r['age']=='86' and r['source']=='045CF32C' for r in cases['added'][0]['SKYDMA'])
assert any(r['age']=='86' and r['source']=='045CEF94' for r in cases['stock'][0]['SKYDMA'])
report=dict(passed=True,cases={suffix:data[1] for suffix,data in cases.items()},backgroundDrawCounts=background,originalNativeAnimationFragment=fragment,nativeAnimationSourcesDiffer=True,skyGeometrySourceAndPaletteMatch=True,cssPortraitGraphicsAbsent=True,scope='Sampled native DMA identifies original animation fragment consistent with tiny sky differences. Exact opaque-pixel attribution and whole-ladder raster acceptance remain open.',sourceSync=sync.verify(),priorProofSHA256=sync.sha(proof_path),checkerSHA256=sync.sha(Path(__file__)),fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,nativeSkyMatches=True,originalAnimationDrawDifferenceIdentified=True)))
