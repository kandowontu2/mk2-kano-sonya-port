"""Actual route and wins, not knife plan count as success."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_held_escape.py').read_text().replace('audit_current_kano_p2_shao_held_escape','audit_current_kano_p2_shao_close_knife')
namespace=dict(__file__=__file__,print=lambda *args,**kwargs:None)
exec(compile(source,__file__+'::close_knife','exec'),namespace)
rows=namespace['rows']
print(dict(ownedShaoRounds=[r for r in rows['WIN'] if r['stage']=='16' and r['slot']=='2'],results=rows.get('RESULT',[]),fullPortAccepted=False))
