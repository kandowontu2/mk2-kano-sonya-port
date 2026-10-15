"""New real input policy after authoritative failed-to-exercise jump result."""
import argparse
from pathlib import Path
import capture_cross_continue_v3 as previous
import cross_continue_ordinary_contract as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
source=previous.source
before='audit_cross_continue_v3_';need(source.count(before)==1,'Fresh ordinary-policy native routes')
source=source.replace(before,'audit_cross_continue_ordinary_',1)
scope=dict(previous.scope,__file__=__file__,contract=contract,gate=contract.gate,LUA=ROOT/'mk2ks_cross_continue_v3.lua',DEPENDENCIES=[*previous.scope['DEPENDENCIES'],*contract.DEPENDENCIES,Path(__file__)])
exec(compile(source,__file__+'::whole_native_cross_continue_fresh_ordinary_controls','exec'),scope)
capture=scope['capture']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
    capture(a.fighter,a.side,'sonya'if a.fighter=='kano'else'kano',True)
