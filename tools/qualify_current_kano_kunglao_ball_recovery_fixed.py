"""Full existing earned progression gate, preserve previous checker."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kunglao_guarded_ball.py').read_text().replace('kano_kunglao_guarded_ball','kano_kunglao_ball_recovery_fixed')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
