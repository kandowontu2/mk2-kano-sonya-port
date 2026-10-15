"""Same original true-ID/native chronology/owned HK gates for approach response."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_standing.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_standing','audit_current_kano_p2_mileena_approach')
exec(compile(source,__file__+'::same_native_HK_gate','exec'))
