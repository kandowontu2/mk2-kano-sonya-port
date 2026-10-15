"""Distinguish later ordinary HP contact from missed knife uppercut."""
from pathlib import Path
prior=Path(__file__).with_name('qualify_bounded_current_blade_misses.py')
scope={'__file__':str(prior)}
exec(compile(prior.read_text().split('exec(compile(source',1)[0],str(prior),'exec'),scope)
source=scope['source']
source=source.replace("    assert not rows.get('HEALTH',[])","""    recovery=int(rows['RECOVERED'][0]['frame'])
    assert all(int(r['frame'])>recovery and int(r['before'])-int(r['after'])==11 and r['slot']==str(3-side) and r['pc']=='FF836700' for r in rows.get('HEALTH',[]))
    assert all(int(r['frame'])>=int(rows['RESULT'][0]['followup'])+112 for r in rows.get('HEALTH',[]))""")
source=source.replace("all(r['hp']=='161' and r['actor']==r['owner'] for r in fields)","all(r['actor']==r['owner'] and (int(r['frame'])>recovery or r['hp']=='161') for r in fields)")
source=source.replace('audit_bounded_current_blade_misses_checked','audit_bounded_current_blade_miss_followup_checked')
source=source.replace('predecessorCheckerSHA256=sync.sha(prior),','predecessorCheckerSHA256=sync.sha(prior),failedWhiffCheckerSHA256=sync.sha(failed),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=scope['prior'],failed=prior))
