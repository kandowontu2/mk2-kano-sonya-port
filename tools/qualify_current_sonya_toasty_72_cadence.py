"""Same earned route/native RNG/full finite controls gate, new physical rhythm."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_toasty_64_cadence.py').read_text()
assert 'audit_current_sonya_toasty_64_cadence' in source
source=source.replace('audit_current_sonya_toasty_64_cadence','audit_current_sonya_toasty_72_cadence')
exec(compile(source,__file__+'::same_native_earned_gate','exec'))
