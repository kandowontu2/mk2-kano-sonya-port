"""Reject corrupt overlap evidence without modifying captures or game bytes."""
import functools,json,re
from pathlib import Path
import verify_current_cpu_overlap_v1911 as model

ROOT=model.ROOT;OUT=ROOT/'audit_v1912_current_cpu_overlap_counterexamples'

def mutate(log,tag,criteria,key,value):
    lines=log.splitlines();found=[]
    for n,line in enumerate(lines):
        if not line.startswith(tag+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if all(row.get(k)==v for k,v in criteria.items()):found.append(n)
    assert len(found)==1,(tag,criteria,len(found))
    n=found[0]
    if key is None:lines.pop(n)
    else:
        assert re.search(r'\b'+key+'=',lines[n])
        lines[n],count=re.subn(r'\b'+key+r'=[^\s]+',lambda m:key+'='+value,lines[n]);assert count==1
    result='\n'.join(lines)+'\n';assert result!=log,'A counterexample must change evidence'
    return result

def verify():
    path=model.CASE/'run.log';log=path.read_text(encoding='utf-8-sig')
    accepted=json.loads((model.OUT/'report.json').read_text());assert accepted['passed']
    pins=dict(accepted['inputHashes']);pins[str(model.OUT/'report.json')]=model.round_model.sha(model.OUT/'report.json')
    # Reconstruct once, then reuse the same exact read-only source bytes for
    # repeated pure-model tests. No capture or expected word is substituted.
    original_expected=model.round_model.launch.current.expected
    model.round_model.launch.current.expected=functools.lru_cache(maxsize=1)(original_expected)
    model.verify(log)
    O='MK2_CPU_OVERLAP_';P='MK2_CPU_PAIR_';R='MK2_CPU_ROUND_'
    tests=[
      ('missing owned child callback',O+'CHILD_FIELD',{'frame':'3140'},None,None),
      ('detached child parent',O+'CHILD_FIELD',{'frame':'3140'},'shot_owner','010350A0'),
      ('guard tests wrong victim',O+'EVENT',{'frame':'3138','kind':'guard','a8':'0102D6F0'},'a0','01034E90'),
      ('unlogged post-hit health',R+'FIELD',{'frame':'3139','slot':'2'},'hp','115'),
      ('wrong intermediate floor anchor',P+'FIELD',{'frame':'3080','cycle':'2'},'vfloor','83'),
      ('wrong intermediate paired pose',P+'FIELD',{'frame':'3080','cycle':'2'},'vpose','FE82AAA0'),
      ('stale victim lock after cleanup',P+'FLAG',{'frame':'3129','slot':'2','kind':'body'},'after','001A'),
      ('detached original cleanup Main',O+'EVENT',{'frame':'3129','kind':'cleanup'},'a13','01069C80'),
      ('wrong leg native fling request',P+'EVENT',{'frame':'3100','cycle':'2','kind':'fling'},'a0','00040000'),
      ('wrong projectile native chip request',O+'HEALTH',{'frame':'3138','slot':'2'},'a10','00000007'),
      ('non-native projectile health writer',O+'HEALTH',{'frame':'3138','slot':'2'},'pc','FF836710'),
      ('wrong impact group',O+'EVENT',{'frame':'3150','kind':'group'},'a0','FF60C400'),
      ('wrong child fixed-point motion',O+'CHILD_FIELD',{'frame':'3150'},'xraw','03060001'),
      ('child callback persists past retirement',O+'CHILD_FIELD',{'frame':'3166'},'frame','3167'),
      ('missing actual victim cleanup',O+'EVENT',{'frame':'3129','kind':'cleanup'},None,None),
      ('invented incoming victim flag',P+'ENTRY',{'frame':'3399'},'vbody','0000001A'),
      ('stale ring own lock at native handoff',O+'EVENT',{'frame':'3167','kind':'regain'},'flags','0010'),
      ('corrupt emulated original guard code',O+'CODE',{'start':'FF837D40'},'words','0000'),
      ('live proxy instead of Kano',R+'FIELD',{'frame':'3139','slot':'2'},'id','1'),
      ('relabel unexplained original cycle complete',P+'INCOMPLETE',{'frame':'3396'},'cycle','4'),
      ('partial projectile health store',O+'HEALTH',{'frame':'3138','slot':'2'},'mask','00FF'),
      ('wrong native flight velocity',O+'EVENT',{'frame':'3136','kind':'group'},'vx','00090000'),
      ('missing ring original input handoff',O+'EVENT',{'frame':'3167','kind':'regain'},None,None),
      ('wrong Main owner at original cleanup',O+'EVENT',{'frame':'3129','kind':'cleanup'},'main_owner','01034E90'),
    ]
    rejected=[]
    for label,tag,criteria,key,value in tests:
        corrupted=mutate(log,tag,criteria,key,value)
        try:model.verify(corrupted)
        except (AssertionError,KeyError,IndexError,ValueError)as error:
            rejected.append(dict(name=label,error=repr(error)));print('Rejected '+label,flush=True)
        else:raise AssertionError('Accepted corruption: '+label)
    for file,value in pins.items():assert model.round_model.sha(file)==value,'Changed original evidence '+file
    pins[str(Path(__file__).resolve())]=model.round_model.sha(Path(__file__).resolve())
    return dict(passed=True,candidate=model.round_model.launch.NAME,counterexamples=rejected,inputHashes=pins,
        originalCaptureUnchanged=True,gameBytesChanged=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=verify()
    except Exception as error:result=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=result['passed'],rejected=len(result.get('counterexamples',[])),error=result.get('error'))),flush=True)
    raise SystemExit(0 if result['passed']else 1)
