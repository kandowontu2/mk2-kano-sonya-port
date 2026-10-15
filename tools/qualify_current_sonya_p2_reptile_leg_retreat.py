"""Earned opening unchanged through Reptile entry; actual damage and ownership."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_reptile_damage_trace.py').read_text().replace('audit_current_sonya_p2_reptile_damage_trace','audit_current_sonya_p2_reptile_leg_retreat')
# Controller changes only upon entering Reptile; compare only preserved opening.
source=source.replace("source=source.replace(\"'INPUT_DIGEST_FINAL'):\",\"'INPUT_DIGEST_FINAL','SONYA_REPTILE_DAMAGE'):\")", "source=source.replace(\"'INPUT_DIGEST_FINAL'):\",\"'INPUT_DIGEST_FINAL','SONYA_REPTILE_DAMAGE'):\").replace('46050','44489')")
exec(compile(source,__file__+'::native_context','exec'))
