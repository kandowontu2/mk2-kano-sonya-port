"""Fresh reduced-observer case; preserve prior executed checker."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_guarded_ball_batch1.py').read_text().replace('audit_current_kano_p2_shao_guarded_ball_batch1','audit_current_kano_p2_shao_guarded_ball_batch2')
exec(compile(source,__file__+'::batch2','exec'))
