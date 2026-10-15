"""Exclude new passive action observer from old-prefix row comparison only."""
from pathlib import Path
code = Path(__file__).with_name('qualify_current_kano_kitana_standing_counter.py').read_text()
code = code.replace("code = code.replace(\"len(rows.get", "code = code.replace(\"if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):\", \"if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL','KANO_STANDING_ACTION'):\")\ncode = code.replace(\"len(rows.get", 1)
assert "'KANO_STANDING_ACTION')" in code
exec(compile(code, __file__, 'exec'), {'__file__': __file__})
