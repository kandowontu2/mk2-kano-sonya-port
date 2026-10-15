"""Correct current source-derived attack plane; keep6295 failed assumption.

Frozen compiled constant5 gives14-5-1=8, not the older checker plane9.
No gameplay edit, move-mechanics relaxation or repeated native capture.
"""
import inspect,json
from pathlib import Path
import verify_current_kano_cpu_ball_v6294 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha


def main():
 failure=ROOT/'audit_v6295_current_kano_cpu_ball_checked/failure.json'
 need(json.loads(failure.read_text())['error']=="ValueError('Exact native translated high-plane ball descriptor, reaction and24 damage')",
      'Keep actual previous unsupported plane9 assumption')
 compiled=ROOT/prior.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 text=compiled.read_text()
 need('constexpr unsigned mk2_ground_contact_extension = 5;'in text and
      'emit(ball_attack, {57, 14 - mk2_ground_contact_extension - 1, 72, 31, 0x1417, 0x1805, 0, 0, 1});'in text,
      'Whole current compiled constructor derives exact plane8 independently of captured result')
 scope=dict(prior.__dict__,__file__=__file__,OUT=ROOT/'audit_v6297_current_kano_cpu_ball_checked',
            prior_module=prior,failure=failure,compiled=compiled)
 for function in(prior.gate,prior.main):
  source=inspect.getsource(function)
  before='(57,9,72,31,0x1417,0x1805,0,0,1)'if function is prior.gate else'for p in (PARENT,Path(__file__).resolve(),'
  after='(57,14-5-1,72,31,0x1417,0x1805,0,0,1)'if function is prior.gate else'for p in (failure,compiled,Path(prior_module.__file__).resolve(),PARENT,Path(__file__).resolve(),'
  need(source.count(before)==1,'Only source-derived current descriptor and original failure/source pins change')
  source=source.replace(before,after,1)
  exec(compile(source,__file__+'::whole_original_'+function.__name__+'_correct_current_source_plane','exec'),scope)
 scope['main']()


if __name__=='__main__':main()
