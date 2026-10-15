"""Use the source-complete qualified gate for the three unstarted routes."""
import argparse
from pathlib import Path
import capture_cross_continue_v3 as previous
import cross_continue_contract_v3 as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
source=previous.source
before='audit_cross_continue_v3_';need(source.count(before)==1,'Fresh three remaining real routes')
source=source.replace(before,'audit_cross_continue_v4_',1)
scope=dict(previous.scope,__file__=__file__,contract=contract,gate=contract.gate,
 DEPENDENCIES=[*contract.DEPENDENCIES,*previous.scope['DEPENDENCIES'],Path(previous.__file__),Path(__file__),ROOT/'tools/cross_continue_contract_v3.py'])
exec(compile(source,__file__+'::whole_native_three_remaining_cross_continue_routes','exec'),scope)
capture=scope['capture']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
    capture(a.fighter,a.side,'sonya'if a.fighter=='kano'else'kano',True)
