"""Additive Lua composition correction; retain actual pre-game exit3."""
import argparse
from pathlib import Path
import capture_cross_continue_v2 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
source=previous.source
before='audit_cross_continue_';need(source.count(before)==1,'Fresh native attempt after authoritative pre-game exit3')
source=source.replace(before,'audit_cross_continue_v3_',1)
scope=dict(previous.scope,__file__=__file__,LUA=ROOT/'mk2ks_cross_continue_v2.lua',
 DEPENDENCIES=[*previous.scope['DEPENDENCIES'],Path(previous.__file__),ROOT/'tools/capture_cross_continue.py',ROOT/'tools/cross_continue_contract.py',ROOT/'tools/cross_continue_contract_v2.py',Path(__file__),ROOT/'mk2ks_cross_continue_v2.lua'])
exec(compile(source,__file__+'::same_physical_route_corrected_Lua_composition','exec'),scope)
capture=scope['capture']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
    capture(a.fighter,a.side,'sonya'if a.fighter=='kano'else'kano',True)
