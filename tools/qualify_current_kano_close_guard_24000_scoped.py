"""Complete frame gate, exact prior productive prefix, no capped clear acceptance."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kitana_close_guard_24000.py').read_text()
code=code.replace("exec(compile(code,__file__,'exec'),", "code=code.replace('kano_kitana_close_guard_24000','kano_close_guard_24000_scoped')\nexec(compile(code,__file__,'exec'),")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
