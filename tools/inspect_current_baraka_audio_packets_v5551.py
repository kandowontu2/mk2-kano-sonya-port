"""Read-only diagnostic of sealed native audio records; no gameplay claims."""
import json
import current_baraka_audio_matrix_v5546 as matrix

ROOT=matrix.ROOT
guest=matrix.capture.original.model.current.expected()
for fighter,side in(('kano',2),('sonya',1)):
    folder=matrix.BASE/f'{fighter}_p{side}_samples';log=(folder/'run.log').read_text()
    packets=matrix.capture.rows(log,'PACKET');writes=matrix.capture.rows(log,'SOUND');failures=[]
    if len(writes)!=2*len(packets):failures.append(dict(label='packet/write count',packets=len(packets),writes=len(writes)))
    for i,p in enumerate(packets):
        pair=writes[i*2:i*2+2]
        if len(pair)!=2:continue
        bad=[k for k in('a8','a13','frame')if any(w[k]!=p[k]for w in pair)]
        word=int(p['a3'],16)
        if bad or tuple(int(w['word'],16)&255 for w in pair)!=(word>>8,word&255):
            failures.append(dict(label='actual packet owner/field/bytes',packet=p,writes=pair,differentKeys=bad))
    try:
        result=matrix.source_model.gate(log,guest,fighter,side)
        routes=dict(passed=True,selectedSourceCommands=len(result['sourceBoundActuallySelectedCommands']))
    except Exception as error:routes=dict(passed=False,error=repr(error))
    baseline=matrix.BASE/f'{fighter}_p{side}_nosamples';old=(baseline/'run.log').read_text()
    a=json.loads((folder/'result.json').read_text());b=json.loads((baseline/'result.json').read_text())
    selected=lambda s:[r for r in s.splitlines()if r.startswith(('MK2_STOCK_HEAD_V921_','MK2_ROLLING_HEAD_V1003_','MK2_CURRENT_BARAKA_SCENE_'))]
    try:matrix.phase.coverage(log,a);matrix.phase.coverage(old,b);timer=dict(passed=True)
    except Exception as error:timer=dict(passed=False,error=repr(error))
    differences=[dict(left=x,right=y)for x,y in zip(a['actualDisplayHeaders'],b['actualDisplayHeaders'])if x!=y]
    originals=[dict(left=x,right=y)for x,y in zip(selected(log),selected(old))if x!=y]
    print(json.dumps(dict(fighter=fighter,side=side,packets=len(packets),writes=len(writes),
        sourceRoutes=routes,packetBindingFailures=failures[:8],actualTimerCoverage=timer,
        differingDisplayHeaders=differences[:2],differingOriginalRows=originals[:2]),indent=2),flush=True)
