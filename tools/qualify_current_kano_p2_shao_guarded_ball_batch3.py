"""Actual owned entries and preserved opening for final batch case."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_guarded_ball_batch1.py').read_text().replace('audit_current_kano_p2_shao_guarded_ball_batch1','audit_current_kano_p2_shao_guarded_ball_batch3')
exec(compile(source,__file__+'::batch3','exec'))
