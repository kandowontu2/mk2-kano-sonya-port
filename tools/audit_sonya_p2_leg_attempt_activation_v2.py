"""Successor: HP tap is scoped in Lua, its records omit the stage field."""
from pathlib import Path
source=Path(__file__).with_name('audit_sonya_p2_leg_attempt_activation.py').read_text()
source=source.replace("if row.get('stage')=='3':rows.append(row)","if row.get('stage')=='3' or (row['kind']=='SONYA_KUNGLAO_DAMAGE' and row.get('ids')=='0,18'):rows.append(row)")
exec(compile(source,__file__+'::bounded_log','exec'))
