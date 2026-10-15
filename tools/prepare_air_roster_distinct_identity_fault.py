"""Ensure identity fault differs from actual Liu ID; preserve failed checker."""
import verify_native_source_sync as sync
old=sync.ROOT/'audit_bounded_air_throw_remaining_roster_preparation/qualify.py'
target=old.with_name('qualify_distinct_identity_fault.py')
assert not target.exists()
source=old.read_text()
before="next(r for r in broken['FIELD'] if int(r['slot']) == 3-side)['id'] = '1'"
assert source.count(before)==1
source=source.replace(before,"next(r for r in broken['FIELD'] if int(r['slot']) == 3-side)['id'] = '0' if identity == 1 else '1'")
target.write_text(source)
print('Distinct victim identity fault only; all physical/native gates retained')
