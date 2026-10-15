"""Preserve original full admission/decision/control gate, not universal proof."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_toasty_slow_cadence.py').read_text()
assert 'audit_current_sonya_toasty_slow_cadence' in source
source=source.replace('audit_current_sonya_toasty_slow_cadence','audit_current_sonya_toasty_64_cadence')
source=source.replace('actualSecretLifecycleAccepted=proof','finiteSameRoundControlsPassed=proof')
exec(compile(source,__file__+'::same_native_earned_gate','exec'))
