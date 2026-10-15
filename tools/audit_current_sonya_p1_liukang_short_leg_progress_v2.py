"""Preserve the original failed gate; stock morph may re-emit FIGHT within a paid match."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_liukang_short_leg_progress.py').read_text()
source=source.replace("out=root/'audit_current_sonya_p1_liukang_short_leg_progress_checked'","out=root/'audit_current_sonya_p1_liukang_short_leg_progress_v2_checked'")
old=" attempt=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])][-1]"
new=""" candidates=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])]
 latest=candidates[-1]
 attempt=next(r for r in candidates if r['selection']==latest['selection'])"""
assert source.count(old)==1
source=source.replace(old,new)
exec(compile(source,__file__,'exec'))
