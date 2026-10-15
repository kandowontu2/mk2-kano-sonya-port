"""Original full choke/body/shadow gates plus every native health store in both slots."""
import argparse,inspect,json,struct,traceback,types
from pathlib import Path
import verify_current_cpu_choke_shadow_v5331 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha

def whole_health(log,guest):
 """Replay original tap order against pre-callback, draw-complete and next callback."""
 p=prior.cpu.original
 fields=p.rows(log,'FIELD');stores=p.rows(log,'HEALTH')
 by={r['frame']:r for r in fields};assert len(fields)==len(by)and by,'Unique real pre-execution CPU fields'
 first,last=min(by),max(by)
 assert set(by)==set(range(first,last+1)),'All original live CPU fields contiguous'
 posts={}
 for line in log.splitlines():
  if line.startswith('MK2_HPHASE_POST_FIELD '):
   pairs=prior.re.findall(r'(\w+)=([^\s]+)',line);assert len(pairs)==len(dict(pairs)),'Unique actual draw-complete health fields'
   row=dict(pairs);key=(int(row['frame']),int(row['slot']))
   assert key not in posts,'No duplicate full native post field';posts[key]=row
 assert set(posts)=={(f,s)for f in range(first,last+1)for s in(1,2)},'Both complete draw-time physical slots'
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 at=(0xff836700-48-0xff800000)//8
 assert guest[at:at+6]==original[at:at+6],'Complete actual original health-store instruction words'
 count=0;totals={1:0,2:0}
 for frame in range(first,last+1):
  r=by[frame]
  assert r['writes']==0 and r['assistance']=='none'and r['mode']==2 and (r['state'],r['vstate'])==(0,1),'Every unassisted actual CPU/human callback'
  assert r['owner']==r['actor']and r['vowner']==r['vactor'],'Real actor ownership in entire health history'
  for slot,key in((1,'vhp'),(2,'hp')):
   hp=r[key];assert 0<=hp<=161,'Native pre-execution health bounds'
   for h in [q for q in stores if(q['frame'],q['slot'])==(frame,slot)]:
    assert h['writes']==0 and h['assistance']=='none'and(h['cpu_slot'],h['human_slot'])==(2,1),'Read-only physical health stores'
    assert h['pc']==0xff836700 and h['before']==hp and 0<=h['after']<=hp<=161,'Every ordinary and paired native health store continuous'
    assert h['a8']in(r['actor'],r['vactor'])and h['a13']in(r['main'],r['vmain']),'Only actual executing CPU/human Main, no foreign actor aliases'
    count+=1;totals[slot]+=hp-h['after'];hp=h['after']
   post=posts[frame,slot]
   assert post['writes']=='0'and post['assistance']=='none'and int(post['mode'])==2 and int(post['hp'])==hp,'Every draw-complete health agrees with all native stores, including pre-choke damage'
   prefix='v'if slot==1 else''
   assert (int(post['actor'],16),int(post['main'],16),int(post['owner'],16))==(r[prefix+'actor'],r[prefix+'main'],r[prefix+'actor']),'Actual post health belongs to same physical owner'
   if frame<last:assert by[frame+1][key]==hp,'Next actual pre-execution callback continues complete health ledger'
 assert count==len(stores)>4,'No dropped ordinary or paired health stores'
 return dict(passed=True,first=first,last=last,preFields=len(fields),postActorFields=len(posts),nativeHealthStores=count,
  totalNativeDamageByPhysicalSlot=totals,everyOrdinaryPairedAndPostRecoveryHealthStoreReplayed=True,
  allCPUContextsOrKOOrDCSWaveformsAccepted=False)

def verify_log(log,human,guest):
 result=prior.cpu.verify_log(log,human,guest)
 result['wholeNativeHealthHistory']=whole_health(log,guest)
 return result

def run(human):
 failed=ROOT/'audit_v5332_current_cpu_kano_choke_human_kano_checked/report.json'
 failure=json.loads(failed.read_text())
 need(not failure['passed']and failure['error']=="ValueError('Actual native physical fault accepted: wrong_choke_damage')",
      'Preserve real executed original health-scope counterexample')
 scoped_cpu=types.SimpleNamespace(**dict(vars(prior.cpu),verify_log=verify_log))
 namespace=dict(prior.bindings.__globals__,cpu=scoped_cpu)
 exec(compile(inspect.getsource(prior.bindings),__file__+'::unchanged_source_bound_body_shadow_bindings','exec'),namespace)
 binding=namespace['bindings']
 namespace=dict(prior.run.__globals__,cpu=scoped_cpu,bindings=binding,__file__=__file__)
 exec(compile(inspect.getsource(prior.run),__file__+'::entire_original_phase_body_shadow_real_faults_plus_full_health','exec'),namespace)
 report=namespace['run'](human)
 report.update(entireNativeBothSlotHealthLedgerReplayed=True,preservedExecutedHealthScopeFailure=str(failed),
  originalFailureCause='The actual8-point mutation was in cycle0 ordinary damage before the completed choke. The old finite paired contract deliberately did not validate that earlier damage. New gate replays every actual native health store against both pre/post callbacks; the same unchanged mutation is now rejected.',
  originalFullCPUPairAndBodyShadowGatesUnchanged=True)
 report['inputHashes'][str(Path(prior.__file__).resolve())]=sha(prior.__file__)
 report['inputHashes'][str(failed)]=sha(failed)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--human',choices=('kano','sonya'),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v5334_current_cpu_kano_health_shadow_human_{a.human}_checked';need(not out.exists(),'Fresh immutable health/full-shadow proof')
 try:report=run(a.human)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','actualPhysicalFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
