"""Bind each observed VRAM transition to the preceding native DMA receipt."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    rows={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line and '_FAILED ' not in line
        if line.startswith('MK2_HSPECIAL_'):
            rows.setdefault(line.split()[0][13:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return rows

out=sync.ROOT/'audit_bounded_shadow_writer_trace_checked';assert not out.exists()
prior=sync.ROOT/'audit_bounded_jump_presented_points_checked/report.json'
pins=json.loads(prior.read_text())['results'];results={}
for fighter in ('kano','sonya'):
    folder=sync.ROOT/f'audit_bounded_{fighter}_shadow_writer_trace_identity_runtime'
    base=sync.ROOT/f'audit_bounded_{fighter}_jump_presented_points_runtime'
    assert sync.sha(base/'run.log')==pins[fighter]['logSHA256']
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
    rows=load(folder);old=load(base)
    for tag,values in old.items():assert rows[tag]==values,tag
    targets={}
    for r in rows['SHADOW_WRITER']:
        targets.setdefault((r['frame'],r['x'],r['y']),[]).append(r)
    cases=[]
    for point in pins[fighter]['unresolvedVRAMPoints']:
        key=(point['source_frame'],point['dma_x'],point['dma_y'])
        trace=targets[key];assert len(trace)>1
        transitions=[]
        for before,after in zip(trace,trace[1:]):
            if before['before']!=after['before']:
                transitions.append(dict(commandReceipt=before,newIndex=after['before']))
        assert transitions
        assert trace[-1]['before']==point['source_vram'], 'Last trace must agree with source-frame VRAM'
        cases.append(dict(sourceFrame=key[0],x=key[1],y=key[2],transitions=transitions,
            finalIndex=point['source_vram'],presentationRGB=point['actual'],
            predictorIndex=point['predicted'],lastChangingCommand=transitions[-1]['commandReceipt']))
    assert len(cases)==(6 if fighter=='kano' else 3)
    results[fighter]=dict(terminal=terminal,cases=cases,logSHA256=sync.sha(folder/'run.log'),
        originalPhysicalGameplayAndPresentationUnchanged=True)
report=dict(observedNativeWriterTransitionsVerified=True,results=results,sourceSync=sync.verify(),
    priorReportSHA256=sync.sha(prior),checkerSHA256=sync.sha(Path(__file__)),
    scope='Nine targeted point transitions observed between native DMA calls; preceding receipt attribution assumes synchronous blitter implementation confirmed in source. Does not decode every source pixel or prove whole shadow geometry.',
    fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:[dict(frame=c['sourceFrame'],x=c['x'],y=c['y'],source=c['lastChangingCommand']['source'],pc=c['lastChangingCommand']['pc'],command=c['lastChangingCommand']['command'],final=c['finalIndex']) for c in v['cases']] for k,v in results.items()}))
