"""Earned damage is before action; don't count ordinary resumed-match hits."""
from pathlib import Path
original=Path(__file__).with_name('qualify_bounded_cross_finisher_rejoin_p1.py')
source=original.read_text()
source=source.replace("f'audit_bounded_cross_finisher_rejoin_p{side}_checked'","f'audit_bounded_cross_finisher_rejoin_p{side}_damage_window_checked'")
marker="health=[r for r in select('HEALTH') if r['pc']=='FF836700' and int(r['after'])<int(r['before'])<=161]"
assert source.count(marker)==1
source=source.replace(marker,"health=[r for r in select('HEALTH') if int(r['frame'])<int(a['frame']) and r['pc']=='FF836700' and int(r['after'])<int(r['before'])<=161]")
source=source.replace("'survival':d,", "'survival':d,'postActivationHealthObservations':[r for r in select('HEALTH') if int(r['frame'])>=int(a['frame'])],")
context={'__name__':'qualified_damage_window','__file__':str(original)}
exec(compile(source,str(original),'exec'),context)
context['run'](2)
