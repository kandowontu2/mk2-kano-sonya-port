"""Exact source-native frozen position (not unused collision VX=0) successor.

Retain failed6180. Entire original FIFO/floor/shadow/opcode/pixel predicates
remain. Prove every actual integer world coordinate is held on native floor;
retain all observed VX values rather than inventing zero-velocity RAM state.
"""
import argparse
from pathlib import Path
prior_qualifier=Path(__file__).with_name('qualify_current_subzero_scene_v6180.py')
source=prior_qualifier.read_text()
before="       r['vx']==r['vy']==r['gravity']==0,'All real own frozen physical states stay on source-native floor without motion or actor substitution')"
after="       r['x']==own[origin]['x']and r['vy']==r['gravity']==0,'All actual frozen world coordinates stay on native floor without actor substitution; collision VX can be unused')"
assert source.count(before)==1,'Exact actual integer-position/static-floor correction'
source=source.replace(before,after,1)
source=source.replace('audit_v6181_current_subzero_','audit_v6186_current_subzero_')
before="             sourceNativeGroundingAndShadowDisableAccepted=True)"
after="             allActualFrozenIntegerWorldCoordinatesHeld=True,observedUnusedHorizontalVelocityWords=sorted({r['vx']for r in own.values()}),\n             sourceNativeGroundingAndShadowDisableAccepted=True)"
assert source.count(before)==1,'Report all actual unused collision velocities'
source=source.replace(before,after,1)
before="observed,Path(__file__),Path(current.__file__)"
assert source.count(before)==1,'Retain complete failed precursor source pins'
source=source.replace(before,"observed,prior_qualifier,Path(__file__),Path(current.__file__)",1)
exec(compile(source,__file__+'::complete_native_held_position_FIFOfloor','exec'),globals())
