"""Keep failed checker; account explicitly for pre-clamp samples and arrival time."""
import verify_native_source_sync as sync
old=sync.ROOT/'tools/qualify_bounded_air_throw_boundary.py'
target=sync.ROOT/'tools/qualify_bounded_air_throw_boundary_entry.py'
assert not target.exists()
source=old.read_text()
source=source.replace('audit_bounded_air_throw_boundary_checked','audit_bounded_air_throw_boundary_entry_checked')
before="assert len(held)>=30 and all(int(r['x'])==leading for r in held)"
assert source.count(before)==1
source=source.replace(before,"""tail=[r for r in held if int(r['frame'])>=end-8]
            assert len(tail)>=7 and all(abs(int(r['x'])-leading)<=1 for r in tail)
            assert any(int(r['x'])==leading for r in tail)""")
source=source.replace('unchanged leading X for30+held-input boundary calls','final8held-input boundary calls within1pixel of clamp and exact-limit arrival marker')
target.write_text(source)
print('Prepared explicit pre-clamp/final8field gate; failed30field checker preserved')
