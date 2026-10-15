"""Retained opening and actual jumps for second approved bounded run."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_held_escape.py').read_text()
source=source.replace('audit_current_kano_p2_shao_held_escape','audit_current_kano_p2_shao_held_escape_approved180')
exec(compile(source,__file__+'::second_approved_run','exec'))
