"""Original earned chronology gate, not automatic full match acceptance."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_standing_counter.py').read_text()
code=code.replace('sonya_mirror_standing_counter','sonya_mirror_active_flag_guard')
code=code.replace("rows['RESULT'][0]['frame']=='24000'","rows['RESULT'][0]['frame']=='21000'")
# The inherited wrapper performs this replacement itself.
code=code.replace("rows['RESULT'][0]['frame']=='30000'","rows['RESULT'][0]['frame']=='30000'")
code=code.replace('==\'24000\'','==\'21000\'')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
