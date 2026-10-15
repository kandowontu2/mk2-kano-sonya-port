"""Fresh correction of v4852 collector token separator; original retained."""
from pathlib import Path
prior = Path(__file__).with_name('run_native_subzero_offset_regression_v4852.py')
text = prior.read_text()
before = '"sha(candidate/\'mkport_candidate.exe\')==EXE_SHA"),'
after = '"sha(candidate/\'mkport_candidate.exe\')==EXE_SHA "),'
assert text.count(before) == 1
text = text.replace(before, after, 1)
for before, after in (
    ('audit_v4853_native_subzero_offset_regression_source', 'audit_v4857_native_subzero_offset_regression_source'),
    ('audit_v4854_sonya_native_subzero_offset_regression_ram', 'audit_v4858_sonya_native_subzero_offset_regression_ram'),
    ('audit_v4854_{fighter}_native_subzero_offset_regression_ram', 'audit_v4858_{fighter}_native_subzero_offset_regression_ram'),
    ('audit_v4855_sonya_native_subzero_offset_regression_observed', 'audit_v4859_sonya_native_subzero_offset_regression_observed'),
    ('Path(__file__).resolve(), ROOT/LUA, stage.OUT', 'Path(__file__).resolve(), prior, ROOT/LUA, stage.OUT'),
):
    assert text.count(before) == 1
    text = text.replace(before, after, 1)
exec(compile(text, str(Path(__file__).resolve())+'::corrected_source4852', 'exec'), globals())
