"""Finite reviewed edge samples and original scalar catch gates."""
import inspect
import json
import re
import qualify_bounded_air_throw_retirement as prior
import verify_native_source_sync as sync

if __name__=='__main__':
    out=sync.ROOT/'audit_bounded_air_throw_boundary_visuals_checked'
    assert not out.exists()
    source=inspect.getsource(prior.gate).replace('3-side: 11','3-side: 18')
    source=source.replace("attacker = side if fighter == 'kano' and cycle == 1 else 3-side",'attacker = side')
    scope={}
    exec(compile(source,__file__+'::real_sonya_victim','exec'),scope)
    results={}
    total=0
    for thrower in ('kano','jax'):
        for direction in ('left','right'):
            folder=sync.ROOT/f'audit_bounded_air_throw_boundary_visual_{thrower}_{direction}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            lines=[line for line in (folder/'run.log').read_text().splitlines() if line.startswith('MK2_BASIC_')]
            rows={}
            for line in lines:
                rows.setdefault(line.split()[0][10:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
            if thrower=='kano':
                scope['gate'](rows,'kano',1)
                baseline=sync.ROOT/f'audit_bounded_air_throw_boundary_{direction}_p1_runtime/run.log'
                original=[line for line in baseline.read_text().splitlines() if line.startswith('MK2_BASIC_')]
                assert [line for line in lines if not line.startswith('MK2_BASIC_VISUAL_SAVED ')]==original
            else:
                prior.gate(rows,'sonya',1)
            marker=rows['EDGE_WALK_DONE'][0]
            assert marker['fields']=='240' and marker['direction']==direction.title()
            limit=60 if direction=='left' else 1098
            assert limit in (int(marker['aX']),int(marker['bX']))
            images=sorted((folder/'snap').rglob('*.png'))
            assert len(images)==2 and {p.stem for p in images}=={'air_1_phase56','air_1_recovered'}
            size=sum(p.stat().st_size for p in images)
            total+=size
            results[thrower+direction]=dict(imageSHA256={str(p):sync.sha(p) for p in images},imageBytes=size,
                actualArenaLimit=limit,reviewedOwnSonyaVictimBody=True,reviewedNormalRecovery=True)
    report=dict(passed=True,results=results,pngCount=8,pngBytes=total,
        fullVisualAcceptance=False,fullCameraBoundaryAcceptance=False,fullPortAcceptance=False,
        observations='Reviewed finite Kano release versus native Jax holding poses at actual left/right arena limits: own Sonya bodies, normal shadows/HUD/recovery, no proxy/selector residue. Different throw styles are not pixel-equal; whole transient camera path remains unverified.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,pngCount=8,pngBytes=total,fullPortAcceptance=False)))
