"""Additive host source correction before first native continue attempt."""
import argparse,json
from pathlib import Path
import capture_continue_viewport_v6611 as previous
import cross_continue_contract_v2 as contract
import kano_ball_launch_context_v6642 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
source=(ROOT/'tools/capture_cross_continue.py').read_text()
before='import cross_continue_contract as contract';need(source.count(before)==1,'Use full retained-source contract')
source=source.replace(before,'import cross_continue_contract_v2 as contract')
before="if __name__=='__main__':";source=source[:source.index(before)]
exec(compile(source,__file__+'::whole_first_unstarted_native_capture','exec'),globals())
if __name__=='__main__':
    failure=ROOT/'audit_cross_continue_preflight_source_retrieval_rejection'
    if not failure.exists():
        failure.mkdir();(failure/'failure.json').write_text(json.dumps(dict(passed=False,nativeGameFailure=False,newNativeBoots=0,error="Exact whole original controller/gate adaptation terminal==e['reReady']+180",cause='inspect of dynamically generated function used backing-file lines, not retained whole generated source',inputHashes={str(ROOT/'tools/cross_continue_contract.py'):sha(ROOT/'tools/cross_continue_contract.py'),str(ROOT/'tools/capture_cross_continue.py'):sha(ROOT/'tools/capture_cross_continue.py')}),indent=2)+'\n')
    p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
    capture(a.fighter,a.side,'sonya'if a.fighter=='kano'else'kano',True)
