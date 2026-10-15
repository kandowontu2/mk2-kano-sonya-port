"""Same native whole earned progression gate, finite observation not match claim."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_stance_guard.py').read_text().replace('sonya_mirror_stance_guard','sonya_mirror_standing_counter')
code=code.replace("rows['RESULT'][0]['frame']=='30000'","rows['RESULT'][0]['frame']=='24000'")
code=code.replace("if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):","if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL','MIRROR_STANDING_ACTION','MIRROR_STANDING_DAMAGE'):")
exec(compile(code,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
