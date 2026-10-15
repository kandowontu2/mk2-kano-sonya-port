from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p1_subzero_guard_release_leg.py').read_text()
source=source.replace('audit_current_sonya_p1_subzero_guard_release_leg','audit_current_sonya_p1_liukang_short_leg')
source=source.replace("rows.get('SONYA_SETTLED_LEG_PLAN',[])","rows.get('SONYA_LIUKANG_LEG_PLAN',[])").replace("r['stage']=='11'","r['stage']=='12'")
source=source.replace('ownSubZeroRoundWins','ownLiuKangRoundWins').replace('stage12Reached=12 in stages','stage14Reached=14 in stages')
exec(compile(source,__file__,'exec'))
