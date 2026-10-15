"""Keep every lifecycle row, including the actual paired inter-round teardown.

No invented actors or filtered frame gaps. Admit only the one paired NULL-actor
field immediately before the complete native refill, with matching old/new task
and actor ownership on either side. All original finisher/health/pose gates stay.
"""
import inspect,json,re
from pathlib import Path
import qualify_current_mileena_matrix_v6100 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6103_current_mileena_lifecycle_checked'

def fields(text):
 result=[]
 for line in text.splitlines():
  m=re.match(r'^MK2_CURRENT_MILEENA_(FIELD|NO_ACTOR) ',line)
  if not m:continue
  row=dict(re.findall(r'(\w+)=([^\s]+)',line))
  row={k:int(v,16)if k in prior.HEX else int(v)if re.fullmatch(r'-?\d+',v)else v for k,v in row.items()}
  row['absent']=m[1]=='NO_ACTOR';result.append(row)
 return result

def lifecycle(rows,physical,side,guest):
 refill=prior.health.refill(rows,side,guest)['startFrame'];gone=[r for r in physical if r['absent']]
 need([(r['frame'],r['slot'])for r in gone]==[(refill-1,1),(refill-1,2)],
      'Exactly one retained paired teardown field immediately before the original inter-round refill')
 bykey={(r['frame'],r['slot']):r for r in physical}
 for r in gone:
  before=bykey[(r['frame']-1,r['slot'])];after=bykey[(r['frame']+1,r['slot'])]
  need(r['actor']==0 and not before['absent']and not after['absent']and
       r['main']==before['main']==after['main']and before['actor']==after['actor']and
       before['mode']==5 and after['mode']==7 and after['hp']==4 and
       before['hp']==(0 if r['slot']==side else 161)and r['writes']==0 and r['assistance']=='none',
       'Native post-round teardown and next-round actor/task reinitialization, not arbitrary missing combat')

def physical_gate(rows,physical,fighter,side,guest):
 lifecycle(rows,physical,side,guest)
 source=inspect.getsource(prior.physical_gate)
 replacements=((' for r in physical:\n  need('," for r in physical:\n  if r['absent']:continue\n  need("),
               ("own=[r for r in physical if r['slot']==side]","own=[r for r in physical if r['slot']==side and not r['absent']]"),
               ("any(r['mode']==5 and r['frame']>end for r in physical)","any(not r['absent']and r['mode']==5 and r['frame']>end for r in physical)"))
 for before,after in replacements:
  need(source.count(before)==1,'One complete physical lifecycle adaptation without dropped gap checks')
  source=source.replace(before,after,1)
 scope=dict(prior.physical_gate.__globals__);exec(compile(source,__file__+'::whole_physical_gate','exec'),scope)
 report=scope['physical_gate'](rows,physical,fighter,side,guest);report['retainedNativeTeardownFields']=2
 return report

def rejected(rows,physical,fighter,side,guest):
 source=inspect.getsource(prior.rejected);before='except (AssertionError,RuntimeError):'
 need(source.count(before)==1,'Catch the actual project assertion exception for private-row negative controls')
 source=source.replace(before,'except (AssertionError,RuntimeError,ValueError):',1)
 scope=dict(prior.rejected.__globals__,physical_gate=physical_gate)
 exec(compile(source,__file__+'::whole_negative_controls','exec'),scope)
 result=scope['rejected'](rows,physical,fighter,side,guest)
 for name,key,value in [('teardown_nonzero_actor','actor',0x01032130),('teardown_wrong_field','frame',0)]:
  pp=[dict(r)for r in physical];next(r for r in pp if r['absent'])[key]=value
  try:physical_gate(rows,pp,fighter,side,guest)
  except (ValueError,AssertionError):result.append(name)
  else:raise AssertionError('Unrejected actual lifecycle fault '+name)
 return result

def run():
 source=inspect.getsource(prior.run)
 before='pins={str(Path(__file__).resolve()):sha(__file__)}'
 after="pins={str(Path(__file__).resolve()):sha(__file__),str(Path(prior.__file__).resolve()):sha(prior.__file__)}"
 need(source.count(before)==1,'Preserve failed-source input pin in complete matrix successor')
 source=source.replace(before,after,1)
 scope=dict(prior.run.__globals__,prior=prior,fields=fields,physical_gate=physical_gate,rejected=rejected,__file__=__file__)
 exec(compile(source,__file__+'::whole_current_four_context_matrix','exec'),scope)
 report=scope['run']();report['retainedNativeTeardownFields']=8
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh whole current lifecycle qualification')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2))
