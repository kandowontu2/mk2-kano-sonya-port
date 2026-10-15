"""Successor retains all edge gates and adds actual native limit evidence."""
import verify_native_source_sync as sync
old=sync.ROOT/'tools/qualify_bounded_air_throw_edges.py'
target=sync.ROOT/'tools/qualify_bounded_air_throw_boundary.py'
assert not target.exists()
source=old.read_text()
source=source.replace('audit_bounded_air_throw_edges_checked','audit_bounded_air_throw_boundary_checked')
source=source.replace('audit_bounded_air_throw_edge_','audit_bounded_air_throw_boundary_')
source=source.replace("marker[0]['fields']=='100'","marker[0]['fields']=='240'")
source=source.replace('end-100','end-240')
marker="            results[f'{direction}P{side}']=dict"
assert source.count(marker)==1
source=source.replace(marker,"""            boundary=rows['BOUNDARY']
            prior=[r for r in boundary if end-40<=int(r['frame'])<end]
            assert prior and all(r['actor']==r['owner'] for r in boundary)
            lower={int(r['lower']) for r in prior};upper={int(r['upper']) for r in prior}
            assert lower=={60} and upper=={1098}
            leading=min(int(marker[0]['aX']),int(marker[0]['bX'])) if direction=='left' else max(int(marker[0]['aX']),int(marker[0]['bX']))
            assert leading==(60 if direction=='left' else 1098)
            edge_slot=next(int(r['slot']) for r in prior if int(r['x'])==leading)
            held=[r for r in prior if int(r['slot'])==edge_slot]
            assert len(held)>=30 and all(int(r['x'])==leading for r in held)
"""+marker)
source=source.replace('Four100field real paired left/right walks then eight Kano/Sonya catches, true ownership/damage/native recovery and ordinary followups. Displaced positions only; exact arena clamp/camera raster coverage still unproven.',
 'Four240field physical paired walks reached native60/1098 arena limits, unchanged leading X for30+held-input boundary calls, then eight actual Kano/Sonya catches and followups. Exact camera raster/body clipping still unproven.')
target.write_text(source)
print('Prepared successor preserves native earned gates; adds reached-limit/stationary-held-input checks')
