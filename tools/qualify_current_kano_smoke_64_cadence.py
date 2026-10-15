"""Same full native Kano gate for64-field physical rhythm."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_smoke_104_cadence.py').read_text()
source=source.replace('audit_current_kano_smoke_104_cadence','audit_current_kano_smoke_64_cadence')
exec(compile(source,__file__+'::same_native_Kano_gate','exec'))
