"""Fresh correction of the preserved v4842 parse failure; source-only proof."""
from pathlib import Path

prior = Path(__file__).with_name('qualify_native_subzero_offset_staged_source_v4842.py')
source = prior.read_text()
broken = "('wrong_sonya_offset',text.replace('+18*2,0);','+18*2,1);',1)):"
assert source.count(broken) == 1
try:
    compile(source, str(prior), 'exec')
except SyntaxError as error:
    assert error.lineno == 48 and "never closed" in str(error)
else:
    raise ValueError('Preserved original parse failure no longer reproduced')
source = source.replace(broken, broken[:-1] + '):', 1)
source = source.replace("audit_v4843_native_subzero_offset_staged_source_checked",
                        "audit_v4846_native_subzero_offset_staged_source_checked", 1)
exec(compile(source, str(Path(__file__).resolve()), 'exec'), globals())
