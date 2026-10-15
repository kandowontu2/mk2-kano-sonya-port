"""Whole earned route gate; preserve successful round20504 and all prior inputs."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kitana_close_guard_long.py').read_text()
code=code.replace('kano_kitana_close_guard_long','kano_kitana_close_guard_24000')
code=code.replace("old=chronology.load(sync.ROOT/'audit_current_kano_kitana_close_guard_runtime/run.log')","old=chronology.load(sync.ROOT/'audit_current_kano_kitana_close_guard_long_runtime/run.log')")
code=code.replace("int(r['frame'])<18000","int(r['frame'])<21000")
code=code.replace("result['frame']=='21000'","result['frame']=='24000'")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
