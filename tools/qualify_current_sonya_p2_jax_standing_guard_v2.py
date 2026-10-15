"""Correct v1's broad later-stage loop; only Jax-owned paid selections can qualify."""
from pathlib import Path
wrapper=Path(__file__).with_name('qualify_current_sonya_p2_jax_standing_guard.py').read_text()
marker="exec(compile(wrapper,__file__,'exec'))";assert wrapper.count(marker)==1
adapt="""
wrapper=wrapper.replace("code=code.replace('strictSamePaidJaxToKitanaClears=proofs,'", "code=code.replace('strictSamePaidJaxToKitanaClears=proofs,'")
inner="exec(compile(code,__file__,'exec'))"
fix="code=code.replace('audit_current_sonya_p2_jax_standing_guard_checked','audit_current_sonya_p2_jax_standing_guard_v2_checked')\\n"
fix+="code=code.replace('for advance in advances:', \\\"for advance in advances:\\\\n        if not any(t=='FIGHT' and r['stage']=='8' and r['selection']==advance['selection'] for t,r in rows):continue\\\\n        if any(p['selection']==int(advance['selection']) for p in proofs):continue\\\")\\n"
wrapper=wrapper.replace(inner,fix+'\\n'+inner)
"""
# Build the inner adaptation explicitly to avoid any ambiguity in nested quotes.
fix="code=code.replace('audit_current_sonya_p2_jax_standing_guard_checked','audit_current_sonya_p2_jax_standing_guard_v2_checked')\n"
before='for advance in advances:'
after="for advance in advances:\n        if not any(t=='FIGHT' and r['stage']=='8' and r['selection']==advance['selection'] for t,r in rows):continue\n        if any(p['selection']==int(advance['selection']) for p in proofs):continue"
fix+='code=code.replace('+repr(before)+','+repr(after)+')\n'
wrapper=wrapper.replace(marker,"wrapper=wrapper.replace(\"exec(compile(code,__file__,'exec'))\", "+repr(fix)+"+\"\\nexec(compile(code,__file__,'exec'))\")\n"+marker)
exec(compile(wrapper,__file__,'exec'))
