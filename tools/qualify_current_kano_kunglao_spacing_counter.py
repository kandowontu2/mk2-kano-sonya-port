"""Same whole earned gate and exact earlier route; no presumed success."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kunglao_early_counter.py').read_text().replace('kano_kunglao_early_counter','kano_kunglao_spacing_counter')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
