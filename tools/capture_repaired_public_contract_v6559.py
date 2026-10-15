"""Preserve unstarted host binding failure; keep semantic-module namespace intact.

The entire original controller/capture/semantic contract remains. Distinguish
collector provenance from its original semantic module; no weaker test gate.
"""
import inspect,json
from pathlib import Path
import capture_repaired_public_specials_v6555 as prior
ROOT,need=prior.ROOT,prior.need
FAILURE=ROOT/'audit_v6556_repaired_public_special_host_failure/failure.json'

def bindings():
 need(json.loads(FAILURE.read_text())['nativeBoots']==0,'Exact unstarted host binding failure preserved')
 source=inspect.getsource(prior.bindings)
 changes={'current=candidate,original=original':'current=candidate,collector=original',
          'Path(original.__file__)':'Path(collector.__file__)',
          'audit_v6556_repaired_public_special_':'audit_v6560_repaired_public_special_',
          'ROOT/\\"PLAY_CURRENT_V6508_CHECKED.cmd\\"':'ROOT/\\"tools/capture_repaired_public_specials_v6555.py\\",ROOT/\\"audit_v6556_repaired_public_special_host_failure/failure.json\\",ROOT/\\"PLAY_CURRENT_V6508_CHECKED.cmd\\"'}
 for a,b in changes.items():need(source.count(a)==1,'Exact distinct collector namespace, preserved full semantic binding and fresh output '+a);source=source.replace(a,b,1)
 scope=dict(prior.__dict__,__file__=__file__)
 exec(compile(source,__file__+'::whole_original_CMD_capture_distinct_collector_name','exec'),scope)
 functions=scope['bindings']()
 need(Path(functions[0].__globals__['original'].__file__).name=='verify_special_repeat_v5115.py',
      'Full original independent semantic model correctly bound before any native dispatch')
 return functions

if __name__=='__main__':
 capture,_=bindings()
 for move,side in [(m,s)for m in ('knife','ring')for s in (1,2)]:capture(move,side)
