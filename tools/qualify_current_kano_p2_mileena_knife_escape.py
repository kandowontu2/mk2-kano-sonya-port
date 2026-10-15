"""Native chronology and actual owned special/air activation evidence."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_early_airkick.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_early_airkick','audit_current_kano_p2_mileena_knife_escape')
exec(compile(source,__file__+'::native_knife_escape_gate','exec'))
