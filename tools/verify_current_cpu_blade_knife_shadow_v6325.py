"""Numeric equality for the actual four/eight-digit native body fields.

Keep6324's formatting-only rejection. The additional actual mode7 pose/world
binding and complete original body/shadow fault matrix are not weakened.
"""
import inspect,json
from pathlib import Path
import verify_current_cpu_blade_knife_shadow_v6323 as prior
ROOT,need=prior.ROOT,prior.need
OUT=ROOT/'audit_v6326_current_cpu_blade_knife_body_shadow_checked'


def main():
 failure24=ROOT/'audit_v6324_current_cpu_blade_knife_body_shadow_checked/failure.json'
 need(json.loads(failure24.read_text())['error']=="ValueError('Refill post pose/identity binds actual independent native body publication')",
      'Preserve actual original formatting-only rejection')
 source=inspect.getsource(prior.main)
 changes={
  'r[k]==candidate[k]':'body.num(r,k)==body.num(candidate,k)',
  'for path in(failure,Path(prior_module.__file__),':'for path in(failure24,ROOT/\'tools/verify_current_cpu_blade_knife_shadow_v6323.py\',failure,Path(prior_module.__file__),',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Only numeric native-field format adaptation and preserved failure pin')
  source=source.replace(before,after,1)
 scope=dict(prior.main.__globals__,__file__=__file__,OUT=OUT,failure24=failure24)
 exec(compile(source,__file__+'::whole_previous_mode7_and_original_body_shadow_gates','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
