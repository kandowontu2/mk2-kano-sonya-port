"""Censored before111442: compare only actual completed111240 prefix, no full-frontier claim."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_default_kick_deferred_boss_history.py').read_text()
source=source.replace("out=root/'audit_current_sonya_p1_default_kick_deferred_boss_history_checked'","out=root/'audit_current_sonya_p1_default_kick_deferred_partial_history_checked'").replace('111442','111240')
exec(compile(source,__file__,'exec'))
