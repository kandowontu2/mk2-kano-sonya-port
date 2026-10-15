"""Qualify observed overlaps, retaining all nonmatching final pixels."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_idle_dma_clip_trace import full_native_bounds

def load(folder):
    rows={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line and '_FAILED ' not in line
        if line.startswith('MK2_HSPECIAL_'):
            rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return rows

out=sync.ROOT/'audit_bounded_jump_shadow_coverage_checked';assert not out.exists()
prior=sync.ROOT/'audit_bounded_jump_shadow_observed/report.json'
pins=json.loads(prior.read_text())['results'];results={}
for fighter,identity in [('kano','17'),('sonya','18')]:
    folder=sync.ROOT/f'audit_bounded_{fighter}_jump_shadow_coverage_runtime'
    base=sync.ROOT/f'audit_bounded_{fighter}_jump_shadow_points_runtime'
    assert sync.sha(base/'run.log')==pins[fighter]['logSHA256']
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
    assert not (folder/'stderr.log').read_text().strip()
    rows=load(folder);old=load(base)
    for tag in ('FIELD','INPUT','READY','IDLE_TERMINAL','IDLE_SCANPOINT'):
        assert rows[tag]==old[tag],f'Changed original {tag}'
    for r in rows['IDLE_DMA_CLIP']:full_native_bounds(r)
    covers=[r for r in rows['IDLE_SHADOW_COVER'] if r['slot']=='1']
    points=[r for r in rows['IDLE_SCANPOINT'] if r['slot']=='1' and r['kind']=='shadow']
    assert len(covers)==len(points)
    proved=[];unresolved=[]
    for r,q in zip(covers,points):
        assert r['source_frame']==q['source_frame'] and r['actual']==q['actual'] and r['id']==identity
        assert int(r['match'])==int(r['final']==r['actual'])
        if r['covered']=='1':assert r['cover_pc']=='FF804640'
        if q['match']=='0':
            if r['covered']=='1' and r['match']=='1':proved.append(r)
            else:unresolved.append(r)
    results[fighter]=dict(terminal=terminal,bodyOverlapExplainedPoints=len(proved),
        unresolvedPoints=unresolved,allClipSkipCommandsFullNativeBounds=True,
        originalPhysicalGameplayAndScanpointsUnchanged=True,logSHA256=sync.sha(folder/'run.log'))
report=dict(passedObservation=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),
    priorReportSHA256=sync.sha(prior),wholeShadowAcceptance=False,fullGoalComplete=False,
    nextEvidence='Later non-body draw commands and exact display handoff for retained points; also both-slot and other-arena coverage.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:dict(explained=v['bodyOverlapExplainedPoints'],unresolved=len(v['unresolvedPoints'])) for k,v in results.items()}))
