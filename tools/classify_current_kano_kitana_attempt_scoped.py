"""Health rows lack stage: scope by the proven stage3 arrival chronology."""
from pathlib import Path
code=Path(__file__).with_name('classify_current_kano_kitana_attempt.py').read_text()
old="r.get('stage')=='3' and r.get('pc')=='FF836700'"
assert code.count(old)==1
code=code.replace("damage=[r for r in rows['HEALTH']", "cutoff=int(next(r['frame'] for r in rows['STAGE'] if r['stage']=='3'))\nassert max(int(r['stage']) for r in rows['STAGE'])==3\ndamage=[r for r in rows['HEALTH']")
code=code.replace(old,"int(r['frame'])>=cutoff and r.get('pc')=='FF836700'")
code=code.replace('audit_current_kano_kitana_attempt_classified','audit_current_kano_kitana_attempt_classified_scoped')
exec(compile(code,__file__,'exec'))
