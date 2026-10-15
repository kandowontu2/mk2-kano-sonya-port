"""Same finite health-interruption gate; preserves -1 source sentinel semantics."""
from pathlib import Path
base=Path(__file__).with_name('qualify_current_cpu_sonya_voice_late_upper.py').read_text()
assert base.count('audit_current_cpu_sonya_voice_late_upper_')==2
code=base.replace('audit_current_cpu_sonya_voice_late_upper_','audit_current_cpu_sonya_voice_earlier_upper_')
needle=" h=hits[0];hf=int(h['frame']);before=owners[hf-1];cb=cry[hf-1]"
assert code.count(needle)==1
code=code.replace(needle,needle+"""
 live={int(x['frame']):x for x in r['LIVE']}
 victim=live[hf];assert victim['human']==victim['cpu']=='18:18'
 assert h['a8']==victim['human_actor'] and h['a13']==victim['human_main']
 assert victim['cpu_actor']==c['actor'] and victim['cpu_main']==c['main']
 assert all(x['mode']=='2' and x['states']=='0,1' and x['roster']=='18,18' for x in r['STATE'] if hf-2<=int(x['frame'])<=hf+10)
""")
needle2=" pos=float(cry[cf]['pos']);assert 0<pos<66523"
assert code.count(needle2)==1
code=code.replace(needle2,""" assert all(f in live and live[f]['human']==live[f]['cpu']=='18:18' and live[f]['human_actor']==victim['human_actor'] and live[f]['human_main']==victim['human_main'] and live[f]['cpu_actor']==c['actor'] and live[f]['cpu_main']==c['main'] and all(int(h)>0 for h in live[f]['health'].split(',')) for f in range(hf-2,cf+9))
"""+needle2)
code=code.replace("['LOSS','SELECT']","['LOSS','SELECT','WIN']")
code=code.replace("['no_cpu_hit','wrong_owner','EOF_substitution','continued_voice']","['no_cpu_hit','wrong_owner','EOF_substitution','continued_voice','wrong_writer','intervening_mode','intervening_id','intervening_WIN']")
needle3="  else:\n   for x in b['CPU_BICYCLE_CHANNEL']:"
assert code.count(needle3)==1
code=code.replace(needle3,"""  elif name=='wrong_writer':
   for x in b['HEALTH']:x['a8']='01000000'
  elif name=='intervening_mode':
   b['STATE'].append(dict(frame=proof['nativeHP']['frame'],mode='3',states='0,1',roster='18,18'))
  elif name=='intervening_id':
   for x in b['LIVE']:
    if x['frame']==proof['nativeHP']['frame']:x['cpu']='1:1'
  elif name=='intervening_WIN':
   b.setdefault('WIN',[]).append(dict(frame=proof['nativeHP']['frame']))
  else:
   for x in b['CPU_BICYCLE_CHANNEL']:""")
# The gate deliberately has no source_num>=0 assertion.  Actual progression,
# marker ownership, native HP writer and early stationary retirement bind it.
exec(compile(code,__file__,'exec'),{'__file__':__file__})
