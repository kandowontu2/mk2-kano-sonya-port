"""Compact read-only trajectory inspection of the unresolved current CPU entry."""
import json
import verify_current_cpu_round_trace_v1900 as model

log=(model.CASE/'run.log').read_text(encoding='utf-8-sig')
fields=[r for r in model.paired.rows(log,'FIELD') if r['cycle']==2 and 3099<=r['frame']<=3396]
keys=('action','vaction','vgravity','vhp')
selected=('frame','action','vaction','pose','vpose','x','vxpos','vypos','vfloor','vvx','vvy','vgravity','vflags','vbody','vhp')
previous=None
result=[]
for row in fields:
    current=tuple(row[key] for key in keys)
    if current!=previous or row['frame'] in (3100,3124,3138,3139,3149,3395):
        result.append({key:(f'{row[key]:08X}' if key in ('pose','vpose','vvx','vvy','vgravity') else row[key]) for key in selected})
    previous=current
print(json.dumps(result,indent=2))
