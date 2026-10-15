"""Native winner/damage/throw onset checks, not a presumed policy improvement."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_reptile_hk_throw_onset.py').read_text().replace('audit_current_sonya_p2_reptile_hk_throw_onset','audit_current_sonya_p2_reptile_hk_early_retreat')
exec(compile(source,__file__+'::native_context','exec'))
