"""Terminal-first whole legacy capture, current private CMD, no raw files."""
import argparse, inspect
from pathlib import Path
import capture_continue_viewport_v6611 as previous
import cross_continue_contract as contract
import kano_ball_launch_context_v6642 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
source=previous.source
changes=(
 ('audit_v6612_continue_viewport_', 'audit_cross_continue_'),
 ("str(ROOT/'PLAY_MK2_KANO_SONYA.cmd')", "str(ROOT/'TEST_KANO_BALL_LAUNCH_V6640.cmd')"),
 ("ROOT/'PLAY_MK2_KANO_SONYA.cmd',", "ROOT/'TEST_KANO_BALL_LAUNCH_V6640.cmd',"),
 ('-str\',\'250\'', '-str\',\'250\''),
)
for before,after in changes:
    need(source.count(before)==1,'Exact original collector/candidate/route adaptation '+before)
    source=source.replace(before,after,1)
scope=dict(previous.scope,__file__=__file__,current=current,contract=contract,
 LUA=ROOT/'mk2ks_cross_continue.lua',DEPENDENCIES=[*contract.DEPENDENCIES,Path(__file__),Path(previous.__file__)],gate=contract.gate)
exec(compile(source,__file__+'::whole_original_continue_RAM_capture_current_CMD','exec'),scope)
capture=scope['capture']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
    capture(a.fighter,a.side,'sonya'if a.fighter=='kano'else'kano',True)
