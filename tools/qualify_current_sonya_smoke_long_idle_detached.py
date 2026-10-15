"""Exact physical/native prefix and long reset-notifier followthrough."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_smoke_long_idle.py').read_text()
source=source.replace('audit_current_sonya_smoke_long_idle_runtime','audit_current_sonya_smoke_long_idle_detached_runtime').replace('audit_current_sonya_smoke_long_idle_checked','audit_current_sonya_smoke_long_idle_detached_checked')
source=source.replace("t=='SECRET_NATIVE_RESET'","t in ('SECRET_NATIVE_RESET','ACTUAL_RESET_NOTIFY')")
source=source.replace("scope='Current Sonya P1 earned Smoke/return followed by released-input idle; not identical to historical Sonya P2 failing route.'", "scope='Current Sonya P1 earned Smoke/return then released idle with combat taps retired; actual reset callbacks retained. Watchdog elapsed data after tap retirement is not authoritative. Not identical to historical failing P2 route.'")
exec(compile(source,__file__+'::detached','exec'))
