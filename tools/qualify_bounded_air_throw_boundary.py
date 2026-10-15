"""Qualify physical displaced catches without claiming exhaustive camera coverage."""
import inspect
import json
import re
import qualify_bounded_air_throw_retirement as prior
import verify_native_source_sync as sync

if __name__=='__main__':
    out=sync.ROOT/'audit_bounded_air_throw_boundary_checked'
    assert not out.exists()
    source=inspect.getsource(prior.gate)
    assert source.count('3-side: 11')==1
    source=source.replace('3-side: 11','3-side: 18')
    before="attacker = side if fighter == 'kano' and cycle == 1 else 3-side"
    assert source.count(before)==1
    source=source.replace(before,'attacker = side')
    scope={}
    exec(compile(source,__file__+'::same_gate_real_sonya_victim','exec'),scope)
    results={}
    for side in (1,2):
        for direction in ('left','right'):
            folder=sync.ROOT/f'audit_bounded_air_throw_boundary_{direction}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in ('.png','.wav','.bin') for p in folder.rglob('*'))
            rows={}
            for line in (folder/'run.log').read_text().splitlines():
                assert '[LUA ERROR]' not in line and 'hex=' not in line
                if line.startswith('MK2_BASIC_'):
                    rows.setdefault(line.split()[0][10:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
            damage=scope['gate'](rows,'kano',side)
            marker=rows['EDGE_WALK_DONE']
            assert len(marker)==1 and marker[0]['direction']==direction.title() and marker[0]['fields']=='240'
            end=int(marker[0]['frame'])
            for slot in (1,2):
                inputs=[int(r['frame']) for r in rows['INPUT'] if int(r['slot'])==slot
                        and r['button']==direction.title() and end-240<=int(r['frame'])<end]
                assert inputs==list(range(end-240,end))
            boundary=rows['BOUNDARY']
            prior=[r for r in boundary if end-40<=int(r['frame'])<end]
            assert prior and all(r['actor']==r['owner'] for r in boundary)
            lower={int(r['lower']) for r in prior};upper={int(r['upper']) for r in prior}
            assert lower=={60} and upper=={1098}
            leading=min(int(marker[0]['aX']),int(marker[0]['bX'])) if direction=='left' else max(int(marker[0]['aX']),int(marker[0]['bX']))
            assert leading==(60 if direction=='left' else 1098)
            edge_slot=next(int(r['slot']) for r in prior if int(r['x'])==leading)
            held=[r for r in prior if int(r['slot'])==edge_slot]
            assert len(held)>=30 and all(int(r['x'])==leading for r in held)
            results[f'{direction}P{side}']=dict(damage=damage,physicalWalk=marker[0],
                terminal=terminal,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),
        fullCameraBoundaryAcceptance=False,fullVisualAcceptance=False,fullPortAcceptance=False,
        scope='Four240field physical paired walks reached native60/1098 arena limits, unchanged leading X for30+held-input boundary calls, then eight actual Kano/Sonya catches and followups. Exact camera raster/body clipping still unproven.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,catches=8,fullCameraBoundaryAcceptance=False)))
