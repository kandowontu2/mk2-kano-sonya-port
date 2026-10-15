"""Whole existing earned progression gate plus prior productive prefix."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kunglao_stance_counter.py').read_text().replace('kano_kunglao_stance_counter','kano_kunglao_early_counter')
code=code.replace("\n    if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):","\n    if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL','KUNGLAO_ACTION_CHANGE','KUNGLAO_DAMAGE_DETAIL'):")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
