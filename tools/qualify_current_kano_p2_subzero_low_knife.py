"""Same earned/native gate with low-health physical knife observation."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_subzero_standing.py').read_text()
source=source.replace('audit_current_kano_p2_subzero_standing','audit_current_kano_p2_subzero_low_knife')
exec(compile(source,__file__+'::same_earned_gate','exec'))
