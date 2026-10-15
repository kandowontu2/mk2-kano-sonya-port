"""Actual round-boundary/startup faults, qualified rejection and positive control."""
import copy,json,re,traceback
from pathlib import Path
from unittest.mock import patch
import verify_native_cpu_bicycle_round_boundary_v3128 as model
ROOT=model.ROOT;OUT=ROOT/'audit_v3135_native_cpu_bicycle_round_boundary_units'
def run():
    checked=model.OUT/'report.json';proof=json.loads(checked.read_text());assert proof['passed']
    pins=dict(proof['inputHashes']);pins[str(checked)]=model.capture.assembly.sha(checked)
    folder=ROOT/proof['cases']['new_kano']['case']
    original,guest,case=model.capture.capture(folder,'new','kano','guard_until_close','neutral_hold',{})
    def invoke(log):
        with patch.object(model.capture,'capture',return_value=(log,guest,copy.deepcopy(case))):return model.verify()
    positive=invoke(original)
    assert positive['cases']['new_kano']['phase']==proof['cases']['new_kano']['phase'],'Same mocked capture path positive control'
    def alter(tag,frame,selector,key,value,remove=False):
        lines=original.splitlines();found=[]
        for i,line in enumerate(lines):
            if line.startswith(tag+' ')and f'frame={frame} 'in line and all(token in line for token in selector):found.append(i)
        assert len(found)==1,(tag,frame,selector,len(found))
        at=found[0]
        if remove:lines.pop(at)
        else:
            lines[at],count=re.subn(r'(?<!\w)'+key+r'=[^\s]+',key+'='+value,lines[at]);assert count==1
        result='\n'.join(lines)+'\n';assert result!=original
        return result
    tests=[]
    specs=[
      ('round_reveal_falsely_live','MK2_CPU_ROUND_FIELD',2663,['slot=1 '],'mode','2',False,'Actual previous all-mode callback'),
      ('missing_round_reveal_slot','MK2_CPU_ROUND_FIELD',2663,['slot=2 '],'','',True,'len(before)==2'),
      ('missing_interior_live_callback','MK2_CPU_PAIR_FIELD',2670,[],'','',True,'set(range(start+1,end+2))'),
      ('proxy_entry_identity','MK2_MOBILITY_ENTRY_STATE',2663,['slot=2 '],'id','1',False,'True entry identity'),
      ('detached_entry_owner','MK2_MOBILITY_ENTRY_STATE',2663,['slot=1 '],'owner','01034EA0',False,'True entry identity'),
      ('invented_entry_health','MK2_MOBILITY_ENTRY_STATE',2663,['slot=1 '],'hp','160',False,'snapshot[k]==baseline'),
      ('partial_initial_lock_mask','MK2_MOBILITY_FLAG',2663,['slot=2 ','kind=body '],'mask','00FF',False,'Every actual initial lock store'),
      ('missing_initial_body_lock','MK2_MOBILITY_FLAG',2663,['slot=2 ','kind=body '],'','',True,'len(stores)==3'),
      ('nonzero_pre_entry_stock_clear','MK2_CPU_PAIR_FLAG',2663,['slot=2 ','kind=flags ','pc=FF9B3B40 '],'before','0001',False,'Only preceding stock no-op clear'),
      ('missing_pre_entry_stock_clear','MK2_CPU_PAIR_FLAG',2663,['slot=2 ','kind=flags ','pc=FF9B3B40 '],'','',True,'Entire independently bound initial'),
      ('shifted_fractional_landing','MK2_CPU_PAIR_FIELD',2725,[],'yraw','0051A001',False,"r['yraw']==regain['yraw']"),
    ]
    for name,tag,frame,selector,key,value,remove,expected in specs:
        changed=alter(tag,frame,selector,key,value,remove)
        try:invoke(changed)
        except(AssertionError,ValueError)as error:
            condition=traceback.extract_tb(error.__traceback__)[-1].line or ''
            assert expected in str(error)+' '+condition,(name,str(error),condition)
            tests.append(dict(name=name,rejected=True,errorType=type(error).__name__,error=str(error),rejectedCondition=condition))
        else:raise AssertionError('Accepted altered actual boundary evidence '+name)
    unchanged=model.verify();assert unchanged['cases']['new_kano']['phase']==proof['cases']['new_kano']['phase']
    for file,wanted in pins.items():assert model.capture.assembly.sha(file)==wanted,'Original saved evidence unchanged'
    pins[str(Path(__file__).resolve())]=model.capture.assembly.sha(__file__)
    return dict(passed=True,actualBoundaryCounterexamplesRejected=len(tests),counterexamples=tests,
      sameMockedPathPositiveControlAccepted=True,originalCaptureUnmodified=True,
      gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
    assert not OUT.exists(),'Immutable actual boundary corruption tests'
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('counterexamples','inputHashes','scope')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
