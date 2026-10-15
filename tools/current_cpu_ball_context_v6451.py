"""Reuse the entire6298 qualified motion gate and all pre-entry physical binds."""
import inspect,re
import verify_current_kano_cpu_ball_v6298 as original
ROOT,need,sha=original.ROOT,original.need,original.sha


def phase_gate():
 source=inspect.getsource(original.main)
 marker=' source=inspect.getsource(prior.main)'
 need(source.count(marker)==1,'Reuse entire source-plane/raw-coordinate qualified ball gate')
 source=source[:source.index(marker)]+" return lambda text,guest:scope['gate'](text,guest,(ROOT/prior.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes())\n"
 scope=dict(original.__dict__)
 exec(compile(source,__file__+'::whole_6298_phase_gate_without_requalification_run','exec'),scope)
 return scope['main']()


def bindings(text):
 result={}
 for line in text.splitlines():
  if not line.startswith('MK2_NAT_CAMPAIGN_BALL_BINDING '):continue
  pairs=re.findall(r'(\w+)=([^\s]+)',line);r=dict(pairs)
  need(len(pairs)==len(r),'Unique complete native binding keys')
  frame,slot=int(r['frame']),int(r['slot']);prefix='v'if slot==1 else''
  need(slot in(1,2)and r['writes']=='0'and r['assistance']=='none'and r['id']==r['roster']=='17',
       'Both actual Kano17 physical actors, never proxy')
  row=result.setdefault(frame,dict(frame=frame))
  for key in('actor','main','owner','id','floor'):
   name=prefix+key;need(name not in row,'Every physical binding exactly once')
   row[name]=int(r[key],16 if key in('actor','main','owner')else 10)
  need(row[prefix+'actor']==row[prefix+'owner'],'Actual Main owns physical native actor')
 need(set(result)==set(range(1813,1920))and all(len(r)==11 for r in result.values()),'Both complete bodies in every pre-entry/roll/recovery binding callback')
 return list(result.values())
